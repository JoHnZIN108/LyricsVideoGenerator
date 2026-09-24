# igotchu: Script 3 test video

Test run of the voiceover-channel workflow on Script 3, "ChatGPT is just guessing the next word".

- **Voice:** ElevenLabs (voice "Marshel - Casual Storytime Narrator", model eleven_multilingual_v2), one clip per slide in `assets/vo/`.
- **Illustration:** slide 5 image made with ElevenLabs image generation (gpt-image-2), `assets/brain-library.png`.
- **Video:** HyperFrames (HTML + GSAP, rendered to MP4). The composition is `video/index.html`.

## Rebuild

```bash
npm install                      # hyperframes, gsap, fonts
python3 build.py                 # regenerates video/index.html from timing.json + cues.json
cd video && npx hyperframes render -q standard -f 30 -o ../igotchu-script3-test.mp4
```

Needs FFmpeg and Chromium. Set `HYPERFRAMES_BROWSER_PATH` if Chromium isn't auto-detected.

- `slides.json`: script text per slide.
- `timing.json`: slide start/length, from the voice clip lengths.
- `cues.json`: estimated in-slide times for each on-screen reveal.

The voiceover was made on the ElevenLabs free plan, so it isn't licensed for monetized use. Regenerate it on a paid plan before uploading.
