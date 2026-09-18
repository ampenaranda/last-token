"""Assemble the textured base + every clip in source/clips into one multi-clip GLB.
Run:  /Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/build-multiclip-glb.py
Edit CLIPS to add/remove animations. Output: build/robot-clips-v<N>.glb (bump VERSION)."""
import bpy, json, math, os, struct
from mathutils import Vector

VERSION = 3
ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE    = f"{ROOT}/source/base/robot-mixamo-idle-textured.glb"
CLIPDIR = f"{ROOT}/source/clips"
OUT     = f"{ROOT}/build/robot-clips-v{VERSION}.glb"
# (file in source/clips, clip name inside the GLB)
CLIPS = [
    ("walk.fbx","walk"), ("run.fbx","run"), ("jump.fbx","jump"), ("wave.fbx","wave"),
    ("walk-zombie.fbx","zombiewalk"), ("cheer.fbx","cheer"), ("dance-samba.fbx","samba"),
    ("dance-hiphop.fbx","hiphop"), ("look-around.fbx","lookaround"), ("thumbs-up.fbx","thumbsup"),
]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = 30; sc.render.fps_base = 1.0
bpy.ops.import_scene.gltf(filepath=BASE)
assert sc.render.fps == 30, "fps changed on GLB import"
A    = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
mesh = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('b9ef')][0]
for o in list(bpy.data.objects):
    if o not in {A, mesh}: bpy.data.objects.remove(o, do_unlink=True)
idle = A.animation_data.action; idle.name = "idle"; idle.use_fake_user = True
actions = {"idle": idle}
for fname, label in CLIPS:
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=f"{CLIPDIR}/{fname}", bake_space_transform=True)
    assert sc.render.fps == 30, f"fps changed importing {fname} — clips would export at the wrong speed"
    new = set(bpy.data.objects) - before
    fa  = [o for o in new if o.type == 'ARMATURE'][0]
    act = fa.animation_data.action; act.name = label; act.use_fake_user = True; actions[label] = act
    for o in new: bpy.data.objects.remove(o, do_unlink=True)
for a in list(bpy.data.actions):
    if a not in actions.values(): bpy.data.actions.remove(a)

# verify every clip on the textured rig
pb   = A.pose.bones
hips = [b for b in pb if b.name.endswith("Hips")][0]
neck = [b for b in pb if b.name.endswith("Neck")][0]
feet = [b for b in pb if any(k in b.name for k in ("ToeBase","Toe_End","Foot"))]
rep = {}
for name, act in actions.items():
    A.animation_data.action = act
    f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
    tilt = 0; low = 1e9; hz = []
    for f in range(f0, f1+1):
        sc.frame_set(f); hw = A.matrix_world @ hips.head
        tilt = max(tilt, math.degrees(((A.matrix_world @ neck.head) - hw).angle(Vector((0,0,1)))))
        for b in feet:
            for p in (b.head, b.tail): low = min(low, (A.matrix_world @ p).z)
        hz.append(hw.z)
    rep[name] = {"sec": round((f1-f0)/30, 2), "tilt": round(tilt, 1), "foot": round(low, 3),
                 "hips": [round(min(hz), 3), round(max(hz), 3)]}

A.animation_data.action = actions["idle"]; sc.frame_set(1)
bpy.ops.object.select_all(action='SELECT')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
    export_animations=True, export_animation_mode='ACTIONS', export_skins=True,
    export_image_format='AUTO', export_apply=False)

# rename the base clip inside the GLB JSON chunk (exporter calls it Armature|mixamo.com|Layer0)
d = open(OUT, 'rb').read()
magic, ver, total = struct.unpack('<III', d[:12]); ln, ty = struct.unpack('<II', d[12:20])
j = json.loads(d[20:20+ln]); rest = d[20+ln:]
for a in j['animations']:
    if a['name'].startswith('Armature|mixamo'): a['name'] = 'idle'
js = json.dumps(j, separators=(',', ':')).encode(); js += b' ' * ((4 - len(js) % 4) % 4)
open(OUT, 'wb').write(struct.pack('<III', magic, ver, 12+8+len(js)+len(rest)) + struct.pack('<II', len(js), ty) + js + rest)
rep["_animations_in_glb"] = [a['name'] for a in j['animations']]
rep["_size_mb"] = round(os.path.getsize(OUT)/1e6, 1)
open(f"{ROOT}/build/robot-clips-v{VERSION}.report.json", "w").write(json.dumps(rep, indent=1))
