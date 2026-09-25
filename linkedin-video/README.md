# Orchestration explainer (LinkedIn video)

**v2 (current):** `split.html` → `spawn-vs-board.mp4`: 40s, 1920×1080, split screen in the igotchu Instrument style (Bricolage Grotesque condensed, DM Sans, JetBrains Mono). Render with `node render.mjs --page split.html spawn-vs-board.mp4`.

**v1:** 
30s, 1080×1080, silent graphic explainer: in-session spawn vs. cross-harness multi-agent orchestration.

- `scene.html`: the animation (open in a browser to preview it live). All timing lives in `render(t)`.
- `render.mjs`: renders frames with headless Chromium + ffmpeg (libx264) into `orchestration-explainer.mp4`.

```
npm i playwright        # or: ln -s $(npm root -g) node_modules
node render.mjs                 # full MP4
node render.mjs --stills 7,18   # PNG stills
```
Needs `playwright` and an ffmpeg with libx264 (defaults to `imageio-ffmpeg`, or set `FFMPEG=/path/to/ffmpeg`).
