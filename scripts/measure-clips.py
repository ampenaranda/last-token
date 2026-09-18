import bpy, json, math, glob, os
from mathutils import Vector
src="/private/tmp/claude-501/-Users-anapenaranda-Desktop-Interactive-Web/7042a23d-2cd9-422b-af9e-e90eba92086c/scratchpad/anims/robot-mixamo-animations"
out={}
for f in sorted(glob.glob(f"{src}/*.fbx")):
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.render.fps=30
    bpy.ops.import_scene.fbx(filepath=f)
    A=[o for o in bpy.data.objects if o.type=='ARMATURE'][0]
    pb=A.pose.bones
    hips=[b for b in pb if b.name.endswith("Hips")][0]
    neck=[b for b in pb if b.name.endswith("Neck")][0]
    feet=[b for b in pb if any(k in b.name for k in ("ToeBase","Toe_End","Foot"))]
    act=A.animation_data.action
    f0,f1=int(act.frame_range[0]),int(act.frame_range[1])
    tilt=0; low=1e9; hz=[]; xy=[]
    for fr in range(f0,f1+1):
        bpy.context.scene.frame_set(fr)
        hw=A.matrix_world@hips.head
        v=(A.matrix_world@neck.head)-hw
        tilt=max(tilt,math.degrees(v.angle(Vector((0,0,1)))))
        for b in feet:
            for p in (b.head,b.tail): low=min(low,(A.matrix_world@p).z)
        hz.append(hw.z); xy.append((hw.x,hw.y))
    travel=max(math.dist(xy[0],p) for p in xy)
    out[os.path.basename(f)]={"frames":f1-f0,"tilt":round(tilt,1),"foot_min":round(low,3),
        "hips_z":[round(min(hz),3),round(max(hz),3)],"root_travel":round(travel,3),
        "arm_rot_x":round(math.degrees(A.rotation_euler.x))}
open("/private/tmp/claude-501/-Users-anapenaranda-Desktop-Interactive-Web/7042a23d-2cd9-422b-af9e-e90eba92086c/scratchpad/scan2.json","w").write(json.dumps(out))
