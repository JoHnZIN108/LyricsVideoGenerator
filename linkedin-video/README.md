# Orchestration explainer (LinkedIn video)

30s, 1080×1080, silent graphic explainer: in-session spawn vs. cross-harness multi-agent orchestration.

- `scene.html`: the animation (open in a browser to preview it live). All timing lives in `render(t)`.
- `render.mjs`: renders frames with headless Chromium + ffmpeg (libx264) into `orchestration-explainer.mp4`.

```
NODE_PATH=$(npm root -g) node render.mjs            # full MP4
NODE_PATH=$(npm root -g) node render.mjs --stills 7,18   # PNG stills
```
Needs `playwright` and an ffmpeg with libx264 (defaults to `imageio-ffmpeg`, or set `FFMPEG=/path/to/ffmpeg`).
