---
name: youtube-video
description: Make a finished faceless, voiceover YouTube video for the igotchu AI-explainer channel from a script. Covers the ElevenLabs voice (one clip per slide), AI concept illustrations, HyperFrames animated slides, and rendering an MP4. Use whenever the user asks to make, build, render, upgrade or redesign a YouTube video, turn a script into a video, or add visuals, voice, captions, music or illustrations to one.
---

# igotchu YouTube video

The channel is a faceless AI explainer for beginners: voiceover, animated slides and concept illustrations. The user doesn't edit. They give a script and approve the result, so the finished video must hold attention on its own.

Reference build: `igotchu-test/` (Script 3). `build.py` generates the HyperFrames composition from `slides.json`, `timing.json` and `cues.json`. Copy its structure for new videos.

## Pipeline

0. **Design system (Claude Design, made by the user).** The user designs the channel's look in Claude Design (claude.ai/design). You don't design it. Your job is to write the prompt when asked and then build faithfully from what comes back: tokens, components, motion notes and image-prompt style (link, ZIP, or DESIGN.md + HTML). Copy its CSS variables and component markup into the HyperFrames composition. Until one exists, use the house style below.
1. **Script.** Scripts live in the "igotchu Video Scripts" Claude Doc. Each has `[SLIDE n: cue]` lines followed by the spoken text. Split them into `slides.json` as `{n, cue, text}`. The cue is only a starting idea. Designing the actual visual is your job.
2. **Voice (ElevenLabs connector).** Generate **one clip per slide** with `creative_generate_speech` so each slide's timing is exact.
   - Put all clips in one flow (`creative_create_flow` first).
   - Set `generations_count: 1`.
   - Use model `eleven_multilingual_v2` unless the user picks another.
   - Default voice: "Marshel - Casual Storytime Narrator" (`cQYsRVGKMkDmd67zTppv`) on `eleven_multilingual_v2`. The user compared it with `eleven_v3` plus acting tags and **preferred multilingual v2**. `eleven_v4` is locked on the free plan. Switch to the user's cloned voice once they have one.
   - The free plan allows **2 generations at a time**, so extra calls fail. Launch 2 at a time, or re-run any that fail.
   - Poll `creative_get_flow_run_status`, then download each `media[].url` with curl. It's a signed Google Storage link that expires in 2 hours, so download right away.
3. **Illustrations (ElevenLabs connector).** Follow the image-prompt style from the Claude Design system, if there is one. See "Concept illustration scene" below. Use `creative_generate_image`, model `gpt-image-2`, `generations_count: 1`. Check the cost first with `estimate_only`: about 185 credits per 16:9 image. Download the `master_url` PNG.
   - AI video clips are expensive: about 7,300 credits for an 8 s Veo 3.1 fast clip, about 1,450 with `ltx-v2-fast`. Use at most one hero clip per video. Illustrations with a push-in are the best value.
   - The **free plan caps images per day**. The 4th image in a day was refused with `free_tier_image_limit_reached`. On the free plan, spend the daily images on the slides that matter most. Paid plans lift the cap.
4. **Timing.** Pad each clip (0.35 s before, 0.55 s after), join them with ffmpeg into `voiceover.mp3` (loudnorm to -16 LUFS), and record each slide's start and length in `timing.json`.
   - In-slide reveal times (`cues.json`) are estimated from where each phrase sits in the text. For exact timing, transcribe with `creative_transcribe_audio` to get word timestamps. Always do this for captions.
5. **Composition (HyperFrames).** Put one `<section class="clip">` per slide in `video/index.html`, with GSAP tweens at absolute times. See "HyperFrames notes".
6. **Check.** Run `npx hyperframes lint .`, then `npx hyperframes snapshot . --at <times> --no-end --describe false`. **Look at the contact sheet** before rendering, and fix anything clipped, overlapping, empty or unreadable.
7. **Render.** Run `npx hyperframes render -q standard -f 30 -w 4 -o out.mp4` in the background. It takes about 3 minutes for a 4-minute video. Send the MP4 with `SendUserFile`, which has a **30 MB limit**. Illustration-heavy renders run about 50 MB, so shrink them first with `ffmpeg -i in.mp4 -c:v libx264 -preset slow -crf 25 -c:a copy -movflags +faststart out.mp4` (about 18 MB with no visible loss). If the render fails with "Failed to run ffmpeg -version", run it again. It was a one-off glitch.

## Required in every video (retention checklist)

Check every item before rendering. These separate a top-performing faceless video from a slideshow.

- [ ] **Concept illustration scenes on most slides.** Use at least 1 every 60 seconds, and ideally one for every slide whose cue describes a picture or a metaphor. The user specifically likes this scene. Details below.
- [ ] **Something moves every 2–4 seconds.** Never leave a slide still for more than about 4 s. Use slow push-ins, new labels, highlights and camera moves.
- [ ] **A visual hook in the first 2 seconds.** The first line hits on frame 1: huge type, an impact, or the first image. Never a slow fade from an empty background.
- [ ] **Word-by-word captions** from real word timestamps, shown lower-middle. Highlight the current word in orange.
- [ ] **Sound design:** a soft music bed ducked under the voice, a whoosh on slide changes, and a pop or click when text or chips appear. ElevenLabs can generate these.
- [ ] **Visual variety.** Rotate through illustration scenes, UI mockups (phone, chat, browser), diagrams (chips, flows, Venn diagrams, charts) and big-type moments. Don't use the same layout twice in a row.
- [ ] **UI mockups look real.** Keyboards have letters, apps have status bars and headers, and taps show a ripple. A blank rectangle standing in for a phone looks cheap.
- [ ] **Nothing covers the key text.** Stamps and labels go over less important parts, like the keyboard, not over the sentence the viewer needs to read.
- [ ] **Brand:** the "igotchu." wordmark top-left, a gradient progress bar along the bottom, and a closing "I gotchu." end card.

## Concept illustration scene (the signature scene)

This is a strong visual-metaphor image that fades in with a slow push-in (the "Ken Burns" effect), with labels layered on top as the voice gets to them. Script 3's slide 5, "tiny phone brain vs giant library", is the reference.

**Generating the image**
- Show the idea as one picture instead of saying it: size contrast, before vs after, cause and effect, or an everyday object standing in for an AI concept. Examples: a dropped glass shattering, a robot at "manners school", two roads splitting into "sounds right" and "is right", a whiteboard being erased, weighted dice.
- Use this house-style prompt skeleton: `Flat vector illustration, 16:9, dark navy background. <scene>. Strong <contrast>, clean minimal style, glowing bright orange and cyan accents, no text.`
- Always include **"no text"**. Add labels in HyperFrames so they're sharp and timed to the voice.
- Leave empty space (for example the lower left or the top band) where the labels will go.

**Animating it**
- **Slow reveal and push-in** (the user liked this at 1:35 of the Script 3 test). Fade the image in over about 4 s with `sine.inOut`, and at the same time scale it up about 12% across the whole scene with `ease: "none"`. Use two tweens: `tl.fromTo(img,{scale:1},{scale:1.12,duration:<scene>,ease:"none"},start)` and `tl.fromTo(img,{opacity:0},{opacity:1,duration:4,ease:"sine.inOut",immediateRender:false},start)`.
- Place headlines in the empty space you asked for in the prompt, and add a side gradient (`.shade-left`) behind them.
- Point at details in the image with a glowing ring or a callout when the voice mentions them. Example: on slide 8, the ring goes around the 5-star card at "rate its responses".
- Add a bottom gradient so labels stay readable.
- Pop in labels (tag + short line) on their voice cues. Pop in one big-word moment ("SCALE.") where the voice says it.
- When the voice moves on, dim the image (to about 12% opacity) and put the next idea on top, instead of cutting to an empty slide.

## House style (fallback until a Claude Design system exists)

- Background: navy `#0a1128` with a soft radial glow. Accents: orange `#ff7a1a` for emphasis and warnings, cyan `#22d3ee` for answers and AI. Text: `#f4f6fb` and `#c9d2ea`.
- Fonts: **Archivo Black** for headlines, **Inter** 500–900 for everything else. Both are in `video/assets/fonts`, loaded with `@font-face`.
- 1920×1080 at 30 fps. Headlines 96–132 px, body text at least 40 px. Captions and labels must be readable on a phone.

## HyperFrames notes (learned the hard way)

- **cdn.jsdelivr.net is blocked in this environment.** Install `gsap` and the `@fontsource/*` fonts from npm and copy them into `video/assets/`.
- Rendering needs FFmpeg (`apt-get install -y ffmpeg`) and Chromium. Set `HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell` and `HYPERFRAMES_NO_TELEMETRY=1`.
- A second `fromTo` on the same element needs `immediateRender: false`, or it shows the element early. `build.py`'s `tw()` handles this automatically.
- To type text out or reveal words, hide the pieces with `display:none` and switch them on with `tl.set(el, {display:"inline"}, t)`. Hiding them with opacity still takes up space, so the text won't wrap.
- `.slide [id]{opacity:0}` hides everything animated. Re-show containers that don't animate themselves, like keyboard keys.
- The linter warns "nested_structure_needs_subcomposition" and "track_too_dense". These are advisory, and the render still works.

## Before the user uploads

- Voice made on the **ElevenLabs free plan isn't licensed for monetized use.** Regenerate it on Starter or higher before upload.
- In YouTube Studio, tick **"altered or synthetic content"** (AI voice and images).
- Scripts need the user's real opinions or experiences. YouTube's "inauthentic content" policy targets templated, mass-produced AI videos.
