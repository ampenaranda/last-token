# Last Token

An isometric 1980s arcade diorama that runs in the browser, built in Spline and
driven by WebGL. It is a study in animation, controls and interaction: a robot
you can walk around a neon stage, dance on the floor tiles, and photograph in a
working photo booth.

**Live site:** https://ampenaranda.github.io/last-token/

Made by [Ana M. Penaranda](https://ampenaranda.design).

---

## What is in here

| Path | What it holds |
|---|---|
| `index.html` | The whole website. One file: markup, styles, the Spline loader and the button wiring. |
| `img/` | Poster, marquee art, moodboard and process images the page uses. |
| `assets/props/` | The eleven 3D props as optimized GLBs, the files that were imported into Spline. |
| `assets/audio/` | Fourteen sound effects and announcer lines, all synthesized or spoken by TTS. |
| `assets/refs/` | The Grok Imagine renders each prop was reconstructed from, plus the photo booth strip. |
| `scripts/` | The Python that generated the audio and rebuilt the animation clips. |
| `docs/` | The build log. Everything that was learned, including what did not work. |
| `scene/README.md` | How to republish the Spline scene and point the page at it. |

## Running it locally

The page fetches the scene over http, so opening `index.html` from the file
system will not work. Serve the folder:

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765.

## How the page talks to the scene

One runtime instance renders the scene for the whole document, from a
`position: fixed` full-viewport layer behind everything. The hero is text over a
live close-up of the robot on his podium; the editorial block scrolls over it;
the arcade panel after the footer brings the wide diorama back with the controls.

```js
const { Application } = await import(
  "https://cdn.jsdelivr.net/npm/@splinetool/runtime@1.9.28/build/runtime.js"
);
await new Application(document.getElementById("scene")).load(SCENE_URL);
```

**The camera is flown from the page.** The runtime has no camera API — its whole
public surface is `emitEvent`, `setVariable`, `setZoom`, `setSize`, `play`,
`stop`, `findObjectBy*` and friends. So instead of switching between authored
cameras, the scene's camera has its six transform channels bound to scene
variables, and the page writes numbers:

```js
splineApp.setVariable("camPY", 1801.4);   // the camera moves, in degrees and units
```

That buys a curve the page controls rather than a fixed authored transition: the
camera dollies continuously as the arcade panel scrolls in, and the framing is
**computed per viewport**. Both shots sit on one ray through the middle of the
floor, so a narrow frame is handled by pushing the camera further out along that
same ray — it keeps pointing at the same place and simply takes in more. Without
it a phone crops the palms off the corners, because the runtime fills its canvas
rather than letterboxing.

**Rendering is gated on visibility.** The reading block covers the scene
completely in the middle of the page, so the page calls `splineApp.stop()` there
and `play()` on the way out. `play()` resumes the clips where they left off
rather than restarting them, so nothing jumps.

**The drawing buffer is capped.** The runtime calls `setPixelRatio(devicePixelRatio)`
and clamps nothing, so a full-viewport layer at DPR 3 is roughly four times the
pixels of the old card. The scene layer renders into a smaller box and is scaled
back up, holding the effective ratio near 1.5 — measured 4.84 MP down to 3.34 MP
on a DPR-1.8 laptop.

**The controls press keys.** Every emote lives as a KeyDown event on the robot
inside the scene, carrying its sound, announcer line, clip and return to idle. The
buttons dispatch the real key rather than duplicating any of that:

```js
document.dispatchEvent(new KeyboardEvent("keydown", { key: "1", code: "Digit1", ... }));
```

One dispatch on `document` is enough. Clicking **Samba** and pressing **1** are
the same action, down to the audio. The walk pads hold their key down for as long
as the button is held, with pointer capture, so a thumb drives the Game Control
exactly like the keyboard.

| Button | Key | Button | Key |
|---|---|---|---|
| Samba | `1` | Thumbs | `T` |
| Hip Hop | `2` | Look | `L` |
| Cheer | `C` | Zombie | `Z` |
| Wave | `H` | Photo | `F` |

The scene layer is `pointer-events: none`: it is a backdrop, and the deck is the
only control surface. That also keeps the runtime's touch handler from
`preventDefault`-ing multi-touch, which would have killed pinch-zoom site-wide.

## Changing the scene

Edit in the Spline desktop app, then Export, Viewer, Update Viewer. Copy the URL
at the top of that panel and paste it into `SCENE_URL` near the bottom of
`index.html`. Nothing else needs to change. Full steps in
[`scene/README.md`](scene/README.md).

## How it was made

Four pipelines feed one real-time scene.

- **The robot.** Mixamo clips rebuilt in Blender into a single multi-clip GLB.
  Importing clips as separate files made the engine keep the base hips height,
  so every animation floated above the floor. One file fixed it at the source.
  Eleven clips.
- **The props.** A single-subject reference rendered in Grok Imagine, then
  reconstructed with Tripo image-to-3D at v3.1 Ultra: triangles, 40k cap, 8K
  texture bake exported at 2K, lighting removed from the albedo so the scene's
  own neon does the shading. Then a gentle pass with gltf-transform.
- **The sound.** Every effect is synthesized rather than sampled. The shutter is
  a capacitor whine plus a noise burst, the dance stab is a square-wave
  arpeggio, the soundtrack is a 120 BPM loop of kick, snare, hats, square bass
  and saw arp. The announcer is text to speech directed to sound like a cabinet.
- **The gating.** Trigger zones and conditionals would not fire, so the zones
  became collision pads that move. A pulsing podium and the bouncing dance tiles
  re-touch the robot every beat, set a variable, and that variable is bound
  directly to the effect's geometry. No conditionals anywhere.

Everything that loops runs on the same 120 BPM grid, so the scene pulses with
the music rather than near it.

## The build log

[`docs/build-notes.md`](docs/build-notes.md) is the real record: nine days of
working the Spline editor through its automation bridge, including the failures.
The engine limits that cost the most time are all in there.

- [`docs/game-design.md`](docs/game-design.md) — the level, the stations, the palette
- [`docs/animation-clips.md`](docs/animation-clips.md) — every clip, measured
- [`docs/blender-pipeline.md`](docs/blender-pipeline.md) — Mixamo to Blender to Spline

## Credits

Built with 🪙 and many other tokens of love.
