# Ep 07 "Anatomy of a good prompt": status

**Current cut:** `anatomy-of-a-good-prompt.mp4`, the motion-broll build with the user's own recorded voice.

## How it's built

- **Voice:** `myvoice/`.
  - `clean.py` takes the raw recording `raw.mp3` and does the cleanup: declick, tightened pauses (0.22–0.48 s) and -16 LUFS. Output: `voice.wav` (ignored) / `anatomy-voice-clean.mp3`, 256.0 s.
  - Transcript: `transcript.txt`, from ElevenLabs Scribe, hand-corrected. One paragraph per section.
  - `align.py` writes `words.json`, `sections.json` and `captions.srt` (also copied to `./captions.srt`).
- **Visuals:** `motion_gen.py` writes 9 motion-broll clips to `motion/clips/`.
  - Every reveal, highlight and typed line is timed from `words.json`.
  - On-screen prompts match the recorded wording.
- **Build:** `build.py` (skill engine) writes to `motion/dist/`. `render.js` renders at 30 fps to `motion/out/`.
- **Assembly:** `motion_assemble.py` trims each clip to exact frame boundaries of its voice section, concatenates, lays the voice on top and masters to -14 LUFS.
- **Look:** warm grey canvas, black and white. Block colours: task graphite, context pink, rules yellow, examples blue. Neon Blueprint is retired.

## Rebuild

```
python3 motion_gen.py
S=../../.claude/skills/motion-broll
python3 $S/engine/build.py motion/dist motion/clips/0[1-9]-[a-z]*.html
NODE_PATH=./motion/node_modules CHROMIUM_PATH=<headless_shell> node $S/engine/render.js motion/dist/NN-name.html motion/out/NN-name.mp4 30
python3 motion_assemble.py
```

## Still to do

- Update the Claude Doc "igotchu Video Scripts" (Script 7) to the recorded wording.
- **Optional:** add light SFX (clicks and whooshes).
- **Superseded:** the older builds (`frames.py`, `build.py`, clone voice in `assets/vo/`) are kept for reference only.
