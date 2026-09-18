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

The scene is published from Spline and loaded with the Spline runtime rather
than the `<spline-viewer>` element, so the page holds an application object and
the canvas can be sized and driven directly.

```js
const { Application } = await import(
  "https://cdn.jsdelivr.net/npm/@splinetool/runtime@1.9.28/build/runtime.js"
);
await new Application(document.getElementById("scene")).load(SCENE_URL);
```

Every emote already lives inside the scene as a KeyDown event on the robot, and
each one carries the whole performance: a sound effect, an announcer line, the
animation clip, and the timed return to idle. So the buttons do not re-implement
any of that. They press the key.

```js
document.dispatchEvent(new KeyboardEvent("keydown", { key: "1", code: "Digit1", ... }));
```

One dispatch on `document` is enough — the runtime's listener sits above it and
catches the event as it bubbles. Clicking **Samba** and pressing **1** are
therefore the same action, down to the audio, and there is only one copy of the
behaviour to maintain. The earlier approach, invisible hook objects fired with
`emitEvent("mouseDown", ...)`, played the clip but left the sound behind.

| Button | Key | Button | Key |
|---|---|---|---|
| Samba | `1` | Thumbs | `T` |
| Hip Hop | `2` | Look | `L` |
| Cheer | `C` | Zombie | `Z` |
| Wave | `H` | Photo | `F` |

The buttons stay disabled until the scene finishes loading, and the hint line
above them says why. Each button wears its key as a small cap in the corner.

Arrow keys walk the robot and Space makes him jump. Those are Spline's own Game
Control; the deck shows them as a key legend. Mouse orbit is switched off in
the scene (`playControls('none')`), so the view stays put.

**Sound.** The runtime plays through WebAudio. The page wraps `AudioContext`
before the runtime loads, keeps every context it opens, and the Sound button
suspends or resumes them all at once. The choice is remembered per browser in
`localStorage`; if storage is unavailable the page simply starts with sound on.

**Layout.** The hero is a two-column grid: title on the left, the scene card
(7:5) on the right with the deck beneath it. The card's width is capped from
the viewport height (`max-width: calc((100svh - 330px) * 1.4)`) so the whole
hero, deck included, fits on the first screen of a laptop. Under 1000px it
stacks.

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

[`docs/build-notes.md`](docs/build-notes.md) is the real record: eight days of
working the Spline editor through its automation bridge, including the failures.
The engine limits that cost the most time are all in there.

- [`docs/game-design.md`](docs/game-design.md) — the level, the stations, the palette
- [`docs/animation-clips.md`](docs/animation-clips.md) — every clip, measured
- [`docs/blender-pipeline.md`](docs/blender-pipeline.md) — Mixamo to Blender to Spline

## Credits

Built with 🪙 and many other tokens of love.
