---
tags: [mixamo, animation, reference, measurements, robot]
created: 2026-09-16
updated: 2026-09-17
---

# Animation Clip Reference

Measured data for every robot animation on disk. Method in [[Mixamo to Blender to Spline Pipeline]]. Files live in `~/Desktop/RobotGame/source/clips/` — see its `MANIFEST.md` for the same table kept next to the files.

All measured in Blender over every frame. Units are metres (model ≈ 1.19 m in Blender ≈ 500 Spline units → **1 m ≈ 420 units**).

## Reading the columns

- **tilt** — max angle of hips→neck from vertical. Upright ≈ 3–9°. 40°+ is a crouch, bow, or hunch.
- **foot** — lowest point any foot bone reaches. ≈ 0 grounded; negative = slight penetration.
- **hips** — vertical range of the hips. A single locked value means no bob.
- **travel** — max root XY distance from frame 0. **net** — last frame vs first. Large travel with net ≈ 0 is sway that returns (loops cleanly); large net snaps on loop.

## What ships in `build/robot-clips-v3.glb` (11 clips)

| clip | source file | sec | tilt | foot | hips | travel | net | bound to |
|---|---|---|---|---|---|---|---|---|
| `idle` | base GLB | 16.6 | 9.1° | 0.001 | 0.431–0.441 | 0.05 | 0 | On Idle |
| `walk` | `walk.fbx` (pack walk-spline) | 1.03 | 3.1° | −0.018 | locked 0.433 | 0.02 | 0 | On Move |
| `run` | `run.fbx` (pack run-spline) | 0.63 | 17.7° | −0.036 | locked 0.433 | 0.02 | 0 | On Run |
| `jump` | `jump.fbx` | 0.83 | 40.1° | −0.015 | 0.243–0.718 | 0.05 | 0 | On Jump |
| `wave` | `wave.fbx` | 3.17 | 4.0° | 0.002 | 0.438–0.444 | 0.03 | 0 | **H** |
| `cheer` | `cheer.fbx` | 2.90 | 28.4° | 0.002 | 0.417–0.432 | 0.03 | 0 | **C** |
| `thumbsup` | `thumbs-up.fbx` | 4.17 | 48.6° | −0.004 | 0.320–0.437 | 0.23 | 0 | **T** (lean-in bow is intentional) |
| `lookaround` | `look-around.fbx` | 1.00 | 18.6° | 0.002 | 0.358–0.416 | 0.03 | 0.03 | **L** |
| `samba` | `dance-samba.fbx` | 19.8 | 34.6° | −0.025 | 0.342–0.477 | 0.34 | 0 | **1** |
| `hiphop` | `dance-hiphop.fbx` | 15.4 | 39.4° | −0.013 | 0.314–0.441 | 0.53 | 0 | **2** |
| `zombiewalk` | `walk-zombie.fbx` | 1.53 | 46.2° | −0.001 | 0.362–0.424 | 0.42 | 0 | **Z** (infinite, a mode) |

Clip order inside the GLB is alphabetical — `cheer, hiphop, idle, jump, lookaround, run, samba, thumbsup, walk, wave, zombiewalk` — and that is the order Spline's dropdowns show. **Every new Animation action defaults to the first one (`cheer`), including On Idle.**

## Alternates kept in `source/clips/`

| file | vs the shipped one | when to use |
|---|---|---|
| `walk-bob.fbx` (pack walk-inplace) | same walk, hips 0.401–0.445 instead of locked | if the hip-locked walk feels too glidey; costs a small start/stop pop |
| `run-bob.fbx` (pack run-inplace) | same run with natural bob | same trade |

## `source/clips/_do-not-use/`

| file | why |
|---|---|
| `run-ROOTMOTION.fbx` | pack `run` — root travels 1.83 m; fights Game Controls (double movement, foot-slide) |
| `jump-FROZEN-HIPS.fbx` | pack `jump-spline` — hips locked at 0.444; the jump never leaves the ground. Pack README recommends it; measurement says no |
| `clap-SQUAT.fbx` | Grok pack `clap` — hips locked at 0.258 (60 % of standing height), renders as a deep squat. Needs a fresh standing "Clapping", In Place, no hip-lock processing |

## Grok's fun pack (2026-09-17) — full measurements

| Mixamo title | file | sec | tilt | foot | hips | travel | net | verdict |
|---|---|---|---|---|---|---|---|---|
| Cheering | cheer | 2.90 | 28.4° | 0.002 | 0.417–0.432 | 0.03 | 0 | ✅ |
| Clapping | clap | 1.17 | 4.6° | 0.002 | **0.258 locked** | 0.0 | 0 | ❌ squat |
| Samba Dancing | dance | 19.8 | 34.6° | −0.025 | 0.342–0.477 | 0.34 | 0 | ✅ sway returns |
| Looking Right | look-around | 1.00 | 18.6° | 0.002 | 0.358–0.416 | 0.03 | 0.03 | ✅ |
| Robot Hip Hop Dance | silly | 15.4 | 39.4° | −0.013 | 0.314–0.441 | 0.53 | 0 | ✅ sway returns |
| Standing Thumbs Up | thumbs-up | 4.17 | 48.6° | −0.004 | 0.320–0.437 | 0.23 | 0 | ✅ (renders as an emphatic lean-in) |

Rendered three frames of each in Blender before trusting the numbers — the sheet is what caught clap as a squat and cleared thumbs-up's 48.6° as deliberate.

## Naming lesson

`robot-mixamo-walk.fbx` was a **zombie walk** and silently became "the walk" for two rebuild cycles. Files in `source/clips/` are now named for what they *are* (`walk-zombie.fbx`, `dance-samba.fbx`), never for the slot they're intended for. The measurement pass catches mislabels — but only if it runs.

## Red herrings ruled out

- Blender glTF vs FBX importers giving different bone rest orientations — built GLB measured identical to the raw FBX. Not a factor.
- `bake_space_transform=True` baking a rotation offset — same. Not a factor.
- Gravity, collider size, or floor collision causing the float — no. Purely per-clip hips height across separate files.
- The hunched walk being a controller/orientation bug — no. It was the source clip.
