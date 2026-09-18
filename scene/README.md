# Making the hero go live

The page shows a still until it has a scene to load. There are two ways to give it one.

## Route A, the embed URL (works on this plan)

1. In Spline: **Export** (top right) then **Viewer, Integrated Embed** in the left column.
2. Set **Renderer** to **Both (Auto)** so Safari and older machines still get a picture.
   WebGPU Only shows a "not supported" notice instead of the scene.
3. Press **Update Viewer** and wait for the button to come back. That publishes the build.
4. Copy the URL at the top of the panel. It looks like
   `https://prod.spline.design/XXXXXXXXXXXX/scene.splinecode`.
5. Open `site/index.html`, find `const SCENE_URL = "";` near the bottom, and paste the URL
   between the quotes. That is the only edit.

This publishes the scene to Spline's CDN at an unlisted address. Anyone with the link can
load it. Press **Update Viewer** again after any change to the scene.

## Route B, the self-hosted file (needs an Enterprise plan)

**Export** then **Self-Hosted, Download Assets** gives a zip with no external fetches.
On this account that button opens the Enterprise pricing sheet, so route A is the one to
use for now. If the plan ever changes: take the `.splinecode` out of the zip, rename it to
`scene.splinecode`, drop it in this folder, and the page picks it up on its own with no
edit at all.

## Serving it

A page opened from `file://` cannot fetch, so a local `.splinecode` is only found over http:

    cd ~/Desktop/RobotGame/site
    python3 -m http.server 8765

Then open http://localhost:8765. An embed URL from route A works either way.
