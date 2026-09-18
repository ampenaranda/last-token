---
tags: [mixamo, blender, spline, glb, animation, pipeline]
created: 2026-09-16
updated: 2026-09-16
---

# Mixamo → Blender → Spline Pipeline

How animation clips get from Mixamo into a working Spline character. Built for [[Robot Game — Project Home]]; the method generalises to any Mixamo-rigged model.

## The problem this solves

**Symptom:** idle sits perfectly on the floor, but the moment you press a key the character pops **~19 units into the air**, floats while moving, and drops back on release. A visible snap at both ends of every keypress.

**Cause:** when animation clips are imported into Spline as **separate files**, Spline keeps the *base model's* hips height and plays only the new clip's rotations. Clips authored at a different hip height end up hanging above the floor.

Confirmed by measurement — every source FBX is grounded on its own (lowest foot ≈ 0), but idle rests at hips 0.43 m while walk sits at 0.36–0.42 m. That ~0.05 m gap is ~21 units at this scale, matching the observed float.

**Fix:** deliver **all clips in one GLB**. Each clip then carries its own hips channel and nothing gets substituted. Verified: the float disappeared with no offset hacks.

> There is a second, blunter fix if you're ever stuck with separate files — a `Grounded` state on the Armature (Y −19) applied by a Transition action inside the move/run/jump containers, 120 ms ease-out. Game Controls returns a Transition target to Base State on container exit, so it self-reverts. It worked, but the single-file GLB is the real answer.

## Build recipe

Base = the **textured GLB** (carries the 8K material). Clips = the FBX downloads, transferred onto that rig.

```python
# Blender 4.1, headless
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = 30; sc.render.fps_base = 1.0
bpy.ops.import_scene.gltf(filepath=f"{pack}/robot-mixamo-idle-textured.glb")
assert sc.render.fps == 30                       # see fps trap below

A    = [o for o in bpy.data.objects if o.type=='ARMATURE'][0]
mesh = [o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('b9ef')][0]
for o in list(bpy.data.objects):                 # drop stray Icosphere etc.
    if o not in {A, mesh}: bpy.data.objects.remove(o, do_unlink=True)

idle = A.animation_data.action; idle.name = "idle"; idle.use_fake_user = True
actions = {"idle": idle}

for fname, label in CLIPS:                       # [(source stem, clip name), ...]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=f"{pack}/robot-mixamo-{fname}.fbx",
                             bake_space_transform=True)
    assert sc.render.fps == 30
    new = set(bpy.data.objects) - before
    fa  = [o for o in new if o.type=='ARMATURE'][0]
    act = fa.animation_data.action
    act.name = label; act.use_fake_user = True; actions[label] = act
    for o in new: bpy.data.objects.remove(o, do_unlink=True)   # keep action, drop rig

for a in list(bpy.data.actions):
    if a not in actions.values(): bpy.data.actions.remove(a)

A.animation_data.action = actions["idle"]; sc.frame_set(1)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', use_selection=True,
    export_animations=True, export_animation_mode='ACTIONS',
    export_skins=True, export_image_format='AUTO', export_apply=False)
```

### Rename the base clip afterwards

The glTF exporter names the idle action `Armature|mixamo.com|Layer0`. Patch the GLB's JSON chunk directly — cheap, no re-export:

```python
d = open(p,'rb').read()
magic, ver, total = struct.unpack('<III', d[:12]); ln, ty = struct.unpack('<II', d[12:20])
j = json.loads(d[20:20+ln]); rest = d[20+ln:]
for a in j['animations']:
    if a['name'].startswith('Armature|mixamo'): a['name'] = 'idle'
js = json.dumps(j, separators=(',',':')).encode(); js += b' ' * ((4 - len(js)%4) % 4)
out = (struct.pack('<III', magic, ver, 12+8+len(js)+len(rest))
       + struct.pack('<II', len(js), ty) + js + rest)
open(p,'wb').write(out)
assert struct.unpack('<I', open(p,'rb').read(12)[8:12])[0] == os.path.getsize(p)
```

## Traps

### The fps trap — cost us a silent 25% speed error

`import_scene.fbx` **changes the scene fps** to match the file. Mixamo FBX is 24 fps; the glTF base is 30. Import the FBX after the GLB and the whole scene drops to 24, so the exported idle runs 25% fast.

**Guard with `assert sc.render.fps == 30` after every single import.** It's silent otherwise.

### `export_animation_mode`

Use `'ACTIONS'`. `'NLA_TRACKS'` also works but names every clip `<name>_Armature` and is fiddlier.

### `bake_space_transform=True` is safe here

I initially suspected this of baking a rotation offset into the clips. **It doesn't** — the built GLB measured *byte-identical* to the raw FBX on every metric. Don't go chasing it.

## Measure, don't trust

The single most useful habit in this whole project. Four numbers per clip, computed over every frame:

| Metric | How | Catches |
|---|---|---|
| **Torso tilt** | angle of `Hips.head → Neck.head` from world +Z | zombie/hunched clips, baked rotation errors |
| **Lowest foot** | min world Z over Foot / ToeBase / Toe_End | float above floor, ground penetration |
| **Hips Z range** | min/max of `Hips.head.z` | start/stop pop; whether hip-Y is locked |
| **Root travel** | max distance of hips from frame-0 in XY | **root motion** — fatal for Game Controls |

```python
v = (A.matrix_world @ neck.head) - (A.matrix_world @ hips.head)
tilt = math.degrees(v.angle(Vector((0,0,1))))
```

### What the numbers told us

- **Torso tilt 46.2°** on `walk.fbx` → it was a **zombie walk** all along. Not a pipeline bug. An upright walk measures 3–9°.
- **Root travel 1.83** on `run.fbx` → root motion. The clip moves the character *and* Game Controls moves it → double-counting and foot-slide. Use the in-place variant.
- **Hips Z frozen at 0.444** on `jump-spline.fbx` → the jump would have **no lift**. The pack README recommends this file; the measurement says don't.

Render a frame from the source file when a number looks strange — it settles the argument in one image.

## In-place vs root motion

Game Controls drives the character's position itself, so **clips must be in-place**. A clip with root motion fights the controller.

On Mixamo: **uncheck "In Place"** is wrong here — you *want* In Place enabled for this workflow. Download **with skin**, as FBX, so the rig matches.

## Hip-Y locking (the `-noy` / `-spline` variants)

Locking hips Y to a constant that sits inside idle's range (here 0.433, vs idle's 0.431–0.441) **removes the start/stop pop entirely** — the clips no longer sit at a different height from idle.

Trade-off: no vertical bob while walking. On a robot this reads fine. On an organic character it would look glidey — use the `-inplace` variant instead and accept a small pop.

## Reusable scripts

Kept in the session scratchpad; worth copying somewhere permanent if this recurs:

- `scan2.py` — measure every FBX/GLB in a folder, output the four metrics
- `build6.py` — assemble the multi-clip GLB from a base + list of FBX clips
- Blender CLI: `/Applications/Blender.app/Contents/MacOS/Blender --background --python script.py`

> Write results to a JSON file rather than stdout — Blender's stdout is noisy and `grep`-ing a big JSON blob out of it is fragile.
