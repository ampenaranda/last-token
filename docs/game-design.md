---
tags: [spline, game-design, isometric, 80s, robot, plan]
created: 2026-09-17
updated: 2026-09-17
---

# Game Design — LAST TOKEN

*Working title. "After Hours" and "Night Shift" are already taken by earlier projects.*

An isometric 80s neon arcade level. The robot is simply the player's robot. Every station on the level responds to something it already knows how to do: dance, wave, cheer, give a thumbs up, look around.

> The "vintage 1950s mascot" framing from the first draft is **retired from this project** (Ana is keeping it for another one). The robot's chrome still reads well on neon; no story needed.

Part of [[Robot Game — Project Home]]. Mechanics constrained by [[Spline MCP — Field Notes]].


## References — Grok Imagine set (2026-09-17)

Four variations of *"Isometric game level featuring a retro 80s-style robot"*, viewed in the built-in browser (grok.com → Imagine). Saved to `RobotGame/refs/grok-iso-arcade-01..04.jpg`.

What all four agree on — this is the brief:

- **A floating level diorama, not a room.** A dark slab with clear edges, floating in near-black. Multiple tiers joined by short **stairs**. The robot on a raised central platform.
- **Grid / checker floors** (dark purple-grey, magenta or cyan grout), **neon edge tubes** along every ledge, **yellow-black hazard stripes** on the drops.
- **Pits as hazards**: a purple pool in two, a lava pit in one, green slime in one.
- **Big signs as the graphic voice**: ARCADE LEVEL 1 · RETRO POWER · 8-BIT ZONE · SUNSET DRIVE · INSERT COIN · SCORE 198X · LEVEL 01 · EXIT · CAUTION. Marquee-style, on posts or wall panels.
- **80s props**: boombox, cassette tapes, CRT monitors, a purple car, a satellite dish, a neon ring portal, **palm trees** (neon-magenta in one).
- **HUD painted into the image** in #4: `1UP 0123450 · ENERGY ▮▮▮ · TIME 01:23 · LEVEL 1` — this is the website's HUD, for free.
- Palette confirmed: near-black + **purple** + **magenta** + **cyan**, with **yellow** as the hazard/accent — add yellow to the palette table.

#2 (checker tiles, boombox, SCORE 198X, cassette props) is the tone target. #4 is the layout target (central raised octagon, four stations around it, HUD framing).

### What this changes in the plan

| was | now |
|---|---|
| an arcade *interior* with walls | an **open floating slab** — Spline's miniworld/diorama contract, clear square edges, nothing beyond the slab but fog |
| flat floor | **three tiers** with stairs; stations on the outer tier, the plinth on the raised centre |
| stations as furniture | stations as **signposted zones** — each has its marquee sign, which is the Grok-decal job |
| lobby entrance | an **INSERT COIN** strip at the front edge is the entrance |
| no hazards | one **pit** (purple pool) between two tiers — falling in = `resetYPosition` respawn on the plinth. Cheap drama. |
| palette 5 colours | + **yellow** `#ffe14a` for hazard stripes, tokens, score |

The raised centre platform stays as the spawn point / respawn point. No plinth story.

## Palette

| role | hex | use |
|---|---|---|
| midnight | `#12101c` | walls, background, fog |
| grid | `#3a2a6a` | floor lines, dormant tiles |
| magenta | `#ff2fa0` | primary neon, dance tiles |
| cyan | `#2ff0ff` | secondary neon, screens |
| amber | `#ffb347` | jukebox, tokens, warm accents |
| chrome | (robot) | trim on cabinets, the mascot |
| yellow | `#ffe14a` | hazard stripes, tokens, score readouts |

Dark room + emissive neon + two or three point lights. The robot's cream shell is the brightest non-neon thing in the frame, which keeps it the hero from any angle.

## Perspective & scale

**Isometric**: fixed-angle follow camera (azimuth 45°, elevation ~35°), both Game Control camera axes **Locked**, orthographic if Spline's follow camera allows it — otherwise a long-lens perspective (distance ~4000, narrow FOV) reads the same. *Untested — first thing to verify in M1.*

Scale anchor: the robot is **500 units tall**. Treat it as a 1.2 m machine in a human-scaled room.

| thing | metres | units |
|---|---|---|
| arcade cabinet | 1.8 | 750 |
| door | 2.1 | 880 |
| floor tile | 0.5 | 210 |
| room | 8 × 10 | 3360 × 4200 |
| counter height | 1.0 | 420 |

Movement retune for a room this size: `speedTranslate 800`, `runMultiplier 1.5`. At the current `1000 × 2` the robot crosses the whole arcade in two seconds.

## The verbs — what each emote activates

Emotes stay global (they already work anywhere). Each **station** is a Trigger zone on a floor pad; standing in it sets a `station` variable and lights a prompt. The emote's Key Down then carries a **Conditional** (`station == N`) that fires the station's payload. Outside a zone the emote just plays.

| Station | Key | Payload | Variable |
|---|---|---|---|
| **Dance Floor** | 1 / 2 | light tiles run a colour chase, disco ball spins up, speaker cones pulse | `groove` += seconds dancing |
| **Photo Booth** | C / T / H | flash (white plane opacity 1→0), booth sign flickers; **website grabs a canvas frame into a polaroid strip** | `photos` += 1 |
| **Lobby** | H | the two NPC mini-robots wave back | — |
| **Lobby** | L | a hidden token glints and becomes collectible | `tokens` on pickup (Collision) |
| **Jukebox** | T | thumbs up cycles the room's mood palette (magenta → cyan → amber) | `mood` |
| **Prize Counter** | — | walk in with `tokens ≥ 3` → case opens, confetti, the robot's own cheer fires | `won` |
| anywhere | Z | **power-save mode**: neon dims to red, tiles go dormant, NPCs slump — a toggle, not a station | `mode` |

**First build ships three stations: Dance Floor, Photo Booth, Lobby.** Jukebox and Prize Counter are the second pass.

## Think big — motion & light everywhere (Ana, 2026-09-17)

Everything on the slab should move or glow. Built already (✅) or planned:

| element | motion / light | status |
|---|---|---|
| speaker cones | scale pulse, two tempos (430 / 300 ms) | ✅ `animate` loop |
| disco ball | 9 s rotation; later a child Spot sweeping the floor | ✅ spin |
| dance tiles | colour chase when dancing; dormant purple otherwise | tiles built, chase next |
| neon edges | magenta tier 1, cyan tier 2, yellow octagon rim; flicker state on the RETRO POWER sign | ✅ edges + rim |
| palms | trunk sway 2.6 / 3.1 s alternate — fronds still need grouping to the trunk | ✅ partial |
| satellite dish | 24 s slow rotation | ✅ |
| pool | animated noise / wave material layer, purple glow light above | glow ✅, surface anim next |
| INSERT COIN strip | scrolling text or blink | placeholder text ✅ |
| SCORE sign | Text bound to the `tokens` variable (`bindVariable('text', …)`) — live scoreboard for free | planned |
| tokens | spin + bob, Collision pickup | planned |
| photo booth | white flash plane opacity 1 → 0, curtain sway | planned (Grok render generating) |
| CRTs / boombox | screen texture cycling, boombox scale-pulse in time with speakers | planned |
| zombie mode (Z) | every neon → red, tiles dormant, NPCs slump | planned |
| power-up intro | tiers light up one by one when the robot crosses INSERT COIN | planned |
| bloom | page `fx('bloom', 0.7)` — neon reads as neon | ✅ |

## Effects inventory — what's live (2026-09-17, evening)

| Effect | Object(s) | Trigger | Timing |
|---|---|---|---|
| Floor wave v2 | Tile 0-0 … 7-4 (5×8): +26 units AND cyan↔magenta swap | Start loop | 700 ms ping-pong, (row+col)×90 ms delay |
| Speaker thump | Speaker Tower N/S, Boombox (+3 %) | Start loop | 430 ms ping-pong |
| Disco spots | Disco Spot A/B (real SpotLights, cyan/magenta, ×3.2, 0.38 rad, tilts −55°/−70°) | Start loop | 6 s / 8 s full turns, opposite directions |
| Star light | Warm point light following the robot (Follow event) | always | — |
| Neon palms | A magenta point light inside each crown so the fronds read as lit neon; palms differ in yaw, lean and scale | always | — |
| Footsteps / jump / cheer | `Sfx Servo Walk` loop in the move container, `Sfx Jump` in jump, "Woo-hoo! Yeah!" on **C** | Game Controls / C | — |
| Emote announcer | H "Hey there!", T "Nice! Thumbs up!", L "Hmm… where's the DJ?", 2 "Break it down!", Z "Braaains… beep boop." (OpenAI TTS, `scripts/make-sfx.py`) | H / T / L / 2 / Z | — |
| Dish sweep | Satellite Dish yaw −120 → −80 | Start loop | 7 s ping-pong |
| Dance Light cycle | cyan ↔ magenta ×2.2 | Start loop | 1.8 s ping-pong |
| Arcade attract | Arcade Screen Art (OpenAI pixel-art frame) 3 % flicker | Start loop | 260 ms ping-pong |
| INSERT COIN | Coin Text ↔ #3a2a10 | Start loop | 550 ms ping-pong |
| Marquee swing | 3 stickers ±1.5° | Start loop | 2.6–3.2 s ping-pong |
| **Camera flash** (gated: only on the photo podium) | `Flash Light` white ×16 pops over the booth + `Sfx Flash` + "Say cheese!" | **F** | 260 ms |
| **Dance hit** (gated: only on the tiles) | `Rim Glow` cyan ring fattens to 40 + `Sfx Dance` | **1** (+ samba) | 400 ms |
| Photo podium | `Photo Mat` pulses ±14 on the beat (it is also the sensor) | Start loop | 250 ms ping-pong |
| **Polaroid print** (gated: only on the podium) | A print slides out of the booth's slot, tilts, and settles back into the tray | **F** | 700 ms out, returns after 1.4 s |
| Soundtrack | `Loop Synthwave` (8-s procedural synthwave, infinite) + "Insert coin. Last token!" 1.5 s in | Start (after first input) | — |

Gating pattern (collision pads + bindings) is documented in [[Spline MCP — Field Notes]] Day 6. Everything runs on the 120 BPM grid of the loop.

## M1 status — grey-box (2026-09-17)

**Done through the MCP in one session:** 4200 slab · 2600 tier 2 · octagon centre (top 250) · two flights of stairs · purple pool with yellow rim · 5×5 tiles · two speaker stacks · disco ball + pole · three sign posts with self-lit Bebas lettering · INSERT COIN strip · two neon palms · dish on a mast · 6 lights · fog + AO + bloom. 149 objects.

**Verified:** the isometric follow camera works with Game Controls — a `PerspectiveCamera` at `(3590, 3757, 3590)`, rotation `(-45.5, 35, 0)`, both camera axes Locked, whole slab in frame with the robot centred. Speeds retuned to `800 × 1.5`.

**Dance-floor gate, working design (no nested Conditionals needed):**
1. `station` variable; a Trigger zone on Tier2 over the tiles sets `station = 1`; a Trigger on the centre resets it to 0.
2. Key Down **1** → `SetVariable danceHit = station` (expression `[{id: station}]`).
3. A **Conditional event** on the rim, condition `danceHit == 1`, `in`: Transition rim → `Lit` (250 ms, pingpong ×1) + `SetVariable danceHit = 0` with `delay: 700` to re-arm.

The Conditional *action* is accepted on Key Down, but this bridge can't nest a child action under its if/else branch (every `addAction` signature tried was refused). The Conditional *event* pattern above does the same job and is fully MCP-wireable.

**Grok station renders:** the dance-floor edit (5×5 tiles, disco ball, speaker towers, hazard-striped octagon) matches the grey-box almost one-to-one and is the dressing target; photo booth generating.

## Layout — level diorama (supersedes the room plan below, kept for the station list)

```
            ┌─────────────── SIGN: RETRO POWER ───────────────┐
            │  DANCE FLOOR (tier 2)      JUKEBOX + boombox       │
            │  ▦▦▦▦▦  disco ball         ▐▌  ♪                   │
   stairs → │  ▦▦▦▦▦                                        │ ← stairs
            │        ┌── PLINTH (tier 3, raised octagon) ──┐   │
            │        │   ⌂ spawn / respawn point            │   │
            │        └────────────────────────────────────┘   │
            │  PHOTO BOOTH            ▒▒ PURPLE POOL ▒▒       │
            │  ┌────┐                 (hazard, respawn)       │
            │  │ ▓▓ │                                          │
            │  └────┘   NPC ☺ ☺             PRIZE COUNTER     │
            └──────────── ═ INSERT COIN ═ (front edge) ─────────┘
                     palm · palm            satellite dish
```

Slab ≈ 4200 × 4200, tier steps of 120 units, fog to black beyond the edges.

## Room layout (isometric floor plan) — original interior idea

```
 ┌───────────────────────────────────────────┐  north wall: cabinet row (6 cabinets, decal marquees)
 │  [cab][cab][cab][cab][cab][cab]            │
 │                                             │
 │   PRIZE COUNTER          DANCE FLOOR        │  east: dance floor 5×5 tiles, disco ball above,
 │   ┌──────┐               ▦▦▦▦▦             │        two speaker stacks flanking
 │   │ claw │               ▦▦▦▦▦  ♪ ♪         │
 │   └──────┘               ▦▦▦▦▦             │
 │                          ▦▦▦▦▦             │
 │   JUKEBOX                ▦▦▦▦▦             │
 │   ▐▌                                        │
 │                PHOTO BOOTH                  │  south-centre: booth with curtain, flash inside
 │                ┌────┐                       │
 │   LOBBY        │ ▓▓ │                       │  south-west: entrance, two NPC robots
 │   ☺ ☺          └────┘         ═ENTRANCE═    │
 └───────────────────────────────────────────┘
```

The robot starts on the raised centre platform.

## Asset pipeline — decided (2026-09-17, late)

Ana's call: **fidelity from the references**. Grok for stickers and textures, Tripo for hero props, Spline primitives for structure.

| layer | tool | how |
|---|---|---|
| structure (slab, tiers, stairs, tiles, edges, poles, rims) | Spline primitives via MCP | done in M1; stays editable |
| **stickers / textures** — marquees, INSERT COIN, floor graphics, HUD frame, polaroid frame | **Grok Imagine** → `refs/grok/` → cut + key in Python → PNG with alpha → Spline **Decal** / texture layer | 6 stickers cut in `refs/grok/stickers/`; **3 mounted 2026-09-17** — Galaxy Drift → Sign 1 (north), Token Rush → Sign 3 (east), Disco Panic → Sign 2 (west). Recipe: ⌘O → Image tile → paste path → rename, `position` 18 units in front of the panel face, `scale` 1.22–1.28, `shading({category:'phong', emissive:'#8c8c8c'})`; panel resized to 760×380 at y=800, text placeholder hidden |
| **hero props** — speaker towers, photo booth, arcade cabinet, neon palm, boombox, dish, CRT | **Grok single-subject render** (centred, plain black bg, ¾ view, "no text") → **Tripo image-to-3D** → GLB → Spline ⌘O import → scale to 500-unit robot | **7 renders done 2026-09-17** in `refs/grok/props/` — speaker-tower-01, photo-booth-01, arcade-cabinet-01, neon-palm-01, boombox-01, satellite-dish-01, crt-tv-01 (all 1152×1728, dark-grey bg, ¾ view). Tripo step blocked: no Tripo login in either browser and the 1Password relay was unavailable — Ana logs in, then image-to-3D |
| character | already done (Mixamo → Blender → GLB) | — |

Grok renders that exist: 4 level refs, dance-floor station, photo-booth station, 4 marquee sheets — all saved at full resolution in `refs/grok/` (pulled through the built-in browser session; see field notes for the trick).

Tripo rule of thumb from the robot: ~17k verts per prop is fine; import, `applyMaterial` only if the baked texture is bad; place at the grey-box's coordinates and delete the primitive stand-in.

## Asset strategy — build vs generate

**Build in Spline through the MCP (the default).** Everything in an 80s arcade is boxy or emissive, which is exactly what primitives and emissive layers do well — and it stays editable, clones cheaply, and exports light.

| asset | recipe |
|---|---|
| floor tiles | Cube 210×8×210, `clone` grid, magenta/cyan emissive states for the chase |
| walls, counter, plinth | Cubes, `cornerRadius: 0`, midnight physical material |
| arcade cabinet | 3 Cubes (base, body, angled hood) + Rectangle screen (emissive cyan) + **Decal** marquee |
| neon signs | Path / Torus tubes, emissive + a matching Point light with short `distance` |
| speakers | Cube box + 2 Cylinder cones; scale state for the pulse |
| disco ball | Sphere, matcap/chrome layer, `animate` rotation loop |
| photo booth | Cube shell + Rectangle curtain + white flash plane |
| tokens | Cylinder 60×12, amber emissive, spin animate, Collision event |
| NPC mini-robots | Sphere head + Cube body + Cylinder arms, ~250 tall, arm-rotation state for the wave |
| jukebox | Cube body + half-Torus dome + Rectangle glass — primitives are enough |

Also worth a look: the Spline library has an `'arcade'` match (`'jukebox'` has none) — inspect before building cabinets by hand.

**Grok → 2D transparent PNG → Spline `Decal` / texture.** This is where Grok earns its place: flat art that primitives can't draw.

- cabinet marquees and side art (6 different games — invent them)
- the **LAST TOKEN** wordmark for the entrance sign and the website title
- floor graphics (star, arrows, "DANCE" lettering)
- the polaroid frame for the website strip

Prompt shape: *"flat vector 80s arcade marquee art, [game name], cyan and magenta on black, chrome bevel lettering, transparent background, no text other than the title"*. Save to `refs/grok/`.

**Tripo — only for a hero prop that's genuinely curvy.** At most two. Candidates: the **claw** in the prize machine, or a rounded **boombox** on the counter. Tripo output arrives textured but baked and heavy (the robot was 17k verts); it can't be recoloured or re-proportioned afterwards. If a prop can be drawn with five primitives, it should be.

## Website layer

Same single-file architecture as [[Night Shift — Two-Bay Heist]] and The Conductor — one HTML file, GitHub Pages.

- **The Spline scene is the hero**, embedded through `@splinetool/runtime` (not an iframe), so the page can read scene variables.
- **HUD**: keycap legend (H C T L 1 2 Z + arrows) that lights on `keydown`; token counter and photo counter bound to `app.getVariable('tokens')` / `('photos')`.
- **Polaroid strip**: on each photo-booth flash the page grabs `canvas.toDataURL()` and pins it into a strip with the Grok frame. Fully client-side.
- **Intro card**: "The arcade closed at 11. Something in the lobby didn't." — press any key.
- **Mood**: the page's own accent colour follows the `mood` variable so the chrome around the canvas shifts with the jukebox.
- Touch: Spline's joysticks handle movement; the HUD keycaps double as tap targets for emotes.
- Audio: synthesised in the page (game-audio skill) — a low hum, tile pings, a flash *thwip*, coin pickup — no assets.

**Every effect diegetic**, as with Night Shift: nothing on the page happens that the arcade itself couldn't explain.

## Build order

| | Milestone | Done when |
|---|---|---|
| M0 | Decisions + references | refs dropped in `RobotGame/refs/`, three first stations confirmed |
| M1 | **Grey-box** | room, walls, plinth, isometric follow camera **verified with Game Controls**, speeds retuned, Dance Floor tiles chasing on 1/2 |
| M2 | Dressing | cabinets, neon, lighting, palette, fog/AO, Grok marquees as decals |
| M3 | Stations | Photo Booth flash + `photos`, Lobby NPCs wave back, token glint + pickup |
| M4 | Website shell | runtime embed, HUD, polaroid strip, intro card; publish to Pages |
| M5 | Second pass | Jukebox mood, Prize Counter finale, Z power-save mode, sound |

M1 is one working session through the MCP and de-risks the only real unknown.

## Risks & open questions

- **Isometric follow camera** — Spline's Game Control follow with an orthographic camera is unverified. Fallback is a long perspective lens; visually near-identical.
- **Conditional actions inside Key Down events** — the Conditional is a documented action type; whether it's allowed on Key Down specifically needs one test. Fallback: separate Trigger-scoped Key Down events per station.
- **Dance emotes as a core verb** — the delayed-idle return (see field notes) fires ~20 s after a dance even if the player walked off. At the dance station specifically, switching 1/2 to **Toggle + Infinite** ("press to dance, press to stop") may be the better feel. Decide in M1.
- **Clap** is still missing (squat file). It would be a natural Photo Booth pose.
- The Spline runtime's variable API from the page (`getVariable`) is the assumed bridge for the HUD; if it's unavailable in the export tier, the HUD falls back to mirroring key presses in the DOM.

## Grok prompts to run

1. `flat vector 80s arcade marquee, "GALAXY DRIFT", cyan and magenta on black, chrome bevel lettering, transparent background`
2. same, `"NEON CIRCUIT"` · 3. `"TOKEN RUSH"` · 4. `"MOONBASE 7"` · 5. `"CHROME KNIGHTS"` · 6. `"DISCO PANIC"`
7. `wordmark "LAST TOKEN", 80s arcade sign, tube-neon style, magenta with cyan outline, transparent background`
8. `instant-camera polaroid frame, blank, slight wear, transparent background, top-down`

### Tripo-prep prompts — single subject, one per render (queued 2026-09-17)

Shared tail for every prompt: *"three-quarter view, whole object fully visible and centered, isolated on a plain flat dark grey background, even soft studio lighting, no text, no people, no floor reflection, no shadow"*. Grok Imagine → **Image** mode → Quality 2.0. One object per image, otherwise Tripo fuses them.

| # | Prop | Prompt head | Replaces in scene |
|---|------|-------------|-------------------|
| 1 | Speaker tower | retro 1980s arcade speaker tower, tall black cabinet, two round woofers + horn tweeter, chrome mesh grille, neon cyan/magenta trim strips, small glowing VU meter, worn stickers | Speaker Box 1/2 + cones (×2) |
| 2 | Photo booth | 1980s arcade photo booth, boxy cabinet with a striped curtain, pink neon "flash" sign strip (no letters), chrome corners, small coin slot, checkered base | photo-booth station (not built yet) |
| 3 | Arcade cabinet | 1980s upright arcade cabinet, black with magenta and cyan side-art stripes, curved marquee, CRT bezel, two joysticks, six buttons, coin door | station prop for ARCADE sign |
| 4 | Neon palm | stylised neon palm tree, dark purple trunk, six hot-pink neon fronds, small flat base | Palm Trunk/Fronds 1 & 2 |
| 5 | Boombox | 1980s boombox, silver and black, two big speakers, cassette deck, chrome handle, red LED VU meters | counter dressing |
| 6 | Satellite dish | small retro satellite dish on a thin mast, white dish, chrome mast, red blinking tip light | Dish + Dish Mast |
| 7 | CRT TV | 1980s wood-grain CRT television, rounded glass screen, dials on the right, rabbit-ear antenna | wall dressing / HUD idea |

Grok tip: `imagine-public.x.ai/imagine-public/images/<id>.jpg` URLs (from `img.currentSrc`) download with plain curl — no auth needed, unlike `assets.grok.com`.

**Tripo Studio settings (decided 2026-09-17, saved in Tripo for next time)** — `studio.tripo3d.ai/workspace/generate`, HD Model tab, AI Model **v3.1 – Best Quality**:

| Setting | Value | Why |
|---|---|---|
| Ultra Mesh Quality | ON | geometry_quality=detailed — it's the fidelity we asked for |
| Topology | **Triangle** | Quad forces an FBX export and only pays off for meshes that deform/get edited; Spline renders triangles anyway |
| Polycount | **40 000** | web budget — the robot is ~34k tris; 7 props at 40k keeps the scene light. Default was 2 000 000 (!) |
| Texture | ON, **2K**, PBR ON | 2K reads fine at isometric prop size; 4K/8K balloons the GLB. 8K is a members-only toggle that auto-enables — switch it off |
| Remove Lighting | **ON** | de-lights the albedo so Spline's neon point lights shade the prop instead of the baked studio light |
| Generate in Parts | **OFF** | tempting for the speaker (separate cones to pulse), but switching it on greys out Texture — parts come untextured (API docs: generate_parts ≠ texture/pbr). Texturing afterwards is a second job with no guarantee it matches the Grok reference. Fake the cone pulse in Spline instead |
| 8K Texture (members) | **ON** for generation | +20 credits; the export dialog has its own Texture Resolution dropdown, so bake at 8K and export at 2K — effectively supersampled |
| AI Complete | OFF | not needed — the Grok renders show the whole object |
| Cost | 65 credits per prop with 8K (45 at 2K) | |

First result (speaker tower, 2K, 36 823 tris, GLB 4.2 MB with basecolor + roughness/metal + normal): shape and stripes/VU meter/horn faithful, woofer cones a bit muddy → re-ran at 8K. Export: GLB, name it in the dialog, lands in `~/Downloads/` → move to `build/props/`.

**Tripo results (2026-09-17)** — all v3.1 Ultra, 8K bake → 2K GLB export, triangles, polycount cap 40k, in `build/props/`:

| GLB | MB | tris | Verdict |
|---|---|---|---|
| speaker-tower.glb (v2, 8K bake) | 3.3 | 34 625 | excellent — cones, grille, VU meter, stickers all read; `speaker-tower-v1-2k.glb` kept as the 2K-bake comparison (muddier cones) |
| photo-booth.glb | 3.2 | 32 399 | excellent — curtain stripes, neon top bar, checker base |
| crt-tv.glb | 3.4 | 33 548 | excellent — wood grain, dials, antennas survived |
| boombox.glb | 4.2 | 36 949 | excellent |
| satellite-dish.glb | 2.5 | 39 280 | excellent, thin struts intact |
| neon-palm.glb | 2.2 | 38 690 | good — fronds became solid tubes, trunk lost its glitter texture (smooth purple); fine at game scale, or keep the primitive palms |
| arcade-cabinet.glb | 2.0 | 34 748 | OK — side-art stripes came out muted/dark vs the reference; consider a re-run with `texture_alignment: original_image` in mind (Studio default) or a brighter reference render |

Studio export dialog: File Name → Format GLB → Texture Resolution (512/1k/2k/4k/8k Current) → lands in `~/Downloads/<name>.glb`. Each GLB = 1 mesh, 3 images (basecolor, rm = roughness/metal, normal).

**Performance pass (2026-09-17, `analyze_scene` before → after):** materials 69 → 30 (17 shared assets: Tile A/B, Neon Outer/Inner, Pool Rim, Stair, Sign Pole, Sign Panel), lights 10 → 7 with a single shadow caster, polygons 364k (fine, threshold 5M), textures 29 (21 are the 7 props × basecolor/rm/normal; duplicates share). Still flagged: 4 unused images + 8 unused materials — only the Performance panel's **Remove Unused Assets** can drop those. Stand-in primitives deleted; speaker towers carry a 430 ms ping-pong `Thump` scale state from Start.

Post-Tripo checklist: export GLB → `RobotGame/build/props/<name>.glb` → ⌘O 3D Model tile → scale to robot (500 units tall) → place at the grey-box coordinates → delete the primitive stand-in → keep the primitive's Transition/State events by re-adding them on the new object (events don't transfer).


---

## Website, second design pass (2026-09-17)

Ana's note on the first version was "still not quite my taste". No direction given, so the pass
went after craft rather than a new concept. What changed:

- **The page-wide neon wash and scanlines are gone.** They were doing the work that the scene
  and the shader panel should do. Flat near-black now, with a 3.5% grain layer as the only
  full-page treatment. The glow belongs to the content.
- **A monospace joins the type system** (JetBrains Mono) for section numbers, labels, captions,
  stats and the colophon. Bebas stays for display but at fewer sizes and solid colour instead of
  a gradient fill. The gradient headline was the most generic thing on the page.
- **Sections are numbered and ruled** (01 / Controls, 02 / Artwork, and so on) with the number in
  a left column on wide screens. Reads like a spec sheet rather than a landing page.
- **Components flattened**: hairline borders, one radius scale, grid-gap seams instead of
  card shadows, keycaps as small outlined mono chips instead of chunky 3D keys.
- **New**: sticky top bar with section links, a scroll progress hairline, a voice-line ticker
  under the hero, and reveal-on-scroll with a safety net so nothing can stay invisible.
- CDN moved from unpkg to jsDelivr so the page also renders inside a Claude artifact preview.

Stats corrected to 187 objects and 9 props. Local copy is `site/index.html`; a preview is
published as a private artifact for reviewing on a phone.
