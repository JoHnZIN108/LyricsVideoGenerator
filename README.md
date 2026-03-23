# Lyric Video Generator

A browser-based tool for creating lyric videos from your audio files — no installs, no subscriptions, no uploads to a server. Everything runs locally in your browser.

## What It Does

Upload an audio file, type your lyrics, tap-sync them to the music, and download a finished lyric video.

## How to Use

### Step 1 — Upload Audio
Drop or click to select an audio file (MP3, WAV, M4A, OGG).

### Step 2 — Add Lyrics + Song Title
- Enter your song title
- Paste or type your lyrics, **one line per card**
- Each line becomes its own lyric moment in the video

### Step 3 — Tap Sync
- Press **Play** to start the audio
- Tap the **TAP** button (or spacebar) each time the next lyric line should appear
- Tap through all lines, then click **Build Video**

### Step 4 — Player + Download
The player shows a drum-roll lyric display (previous / current / next lines) with a gold waveform visualizer at the bottom.

- **⏺ Record** — starts capturing the video
- **⏹ Stop** — ends the recording and triggers a download of a `.webm` video file
- **↺** — restart from the beginning

## Features

- Smooth vertical drum-roll lyric transitions
- Gold bar waveform visualizer
- Animated sparkle particles
- Song title display
- Exports as `.webm` video (1280×720, landscape)
- Fully offline — no data leaves your device

## Running It

No build step required. Just open `index.html` in a modern browser (Chrome recommended for best `.webm` export support).

```bash
# Option 1: open directly
open index.html

# Option 2: serve locally (avoids any file:// restrictions)
npx serve .
```

## Tech Stack

- Vanilla JavaScript (Web Audio API, MediaRecorder API, Canvas 2D)
- HTML5 + CSS3
- Google Fonts — Bebas Neue

## Browser Support

| Browser | Playback | Recording |
|---------|----------|-----------|
| Chrome  | ✅       | ✅        |
| Edge    | ✅       | ✅        |
| Firefox | ✅       | ⚠️ (VP8 codec, may vary) |
| Safari  | ✅       | ❌ (MediaRecorder limited) |

Chrome is recommended for the best recording experience.
