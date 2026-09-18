# RobotGame clip scripts

Blender 4.1, headless. Docs: Obsidian → WebGL 3D Experiences → Robot Game (Spline)

    /Applications/Blender.app/Contents/MacOS/Blender --background --python <script>

- `measure-clips.py` — measure every FBX/GLB in a folder (tilt, lowest foot, hips range,
  root travel) and write the result to a JSON file next to the script.
- `build-multiclip-glb.py` — assemble a textured base GLB + a list of FBX clips into one
  multi-clip GLB. Edit the CLIPS list and the paths at the top.

Both assert scene fps stays 30 after each import — FBX import silently retimes the scene
to 24 fps, which makes exported clips run 25% fast.
