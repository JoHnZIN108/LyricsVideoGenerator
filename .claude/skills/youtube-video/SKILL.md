---
name: youtube-video
description: Make a finished faceless, voiceover YouTube video for the igotchu AI-explainer channel from a script. Covers the Claude Design styles (Neon Blueprint, plus the Type Lab's Instrument and Patent themes), the ElevenLabs voice (one clip per slide), AI concept illustrations, HyperFrames animated scenes, free synthesized sound effects, captions and rendering an MP4. Use whenever the user asks to make, build, render, upgrade or redesign a YouTube video, turn a script into a video, or add visuals, voice, captions, sound, music or illustrations to one.
---

# igotchu YouTube video

The channel is a faceless AI explainer for beginners: voiceover, animated scenes and concept illustrations. The user doesn't edit. They give a script and approve the result, so the finished video must hold attention on its own. The user is often on a phone, so keep them away from file shuffling.

**Reference build: `igotchu-test/v3/`** (Script 3, v3).
- `build_v3.py` generates `video/index.html` and the audio mix from `timing.json`, `slides.json`, `segments.json` and `ds/`.
- `make_extras.py` writes `captions.srt`.
- `youtube-extras.md` holds the title, chapters, pinned comment and disclosure.

Copy this structure for every new video. Its helpers are the reusable kit: `cue()` alignment, `rise/pop/land/slam/draw/ignite/camera`, `predictor_steps()`, the phone scene, and the SFX mix.

## Pipeline

0. **Design system: Claude Design, made by the user.** The user designs the look in Claude Design (claude.ai/design → **Design System**). You don't design it. When asked, write the prompt; then build faithfully from what comes back.
   - Current system: **igotchu, "Neon Blueprint"**, https://claude.ai/artifact/FzwY3yEcM9KiqUGXW5uiEq.
   - To read it: `Artifact` `list` with `scope:"files"`, then `read` with `paths` for `project/tokens.json`, `project/components/bundle.css`, `project/DESIGN.md`, `project/README.md`, `project/guidelines/illustration-prompts.md` and each `components/<Name>/preview.html`. Copies are in `v3/ds/`.
   - Generate `tokens.css` from `tokens.json` (`tokens_css()`).
   - Use `bundle.css` with its `@import` removed (regex `@import url\([^)]*\);`: the URL itself contains `;`) and everything from the "Motion." section on cut. **CSS keyframe animations never render under frame-seeking.** Also strip the blank caret and typing-dot `animation:` lines.
   - Re-create its eases in GSAP with CustomEase (`gsap/dist/CustomEase.min.js`): `igOut` 0.16,1,0.3,1 · `igPop` 0.34,1.56,0.64,1 · `igSlam` 0.7,0,0.84,0 · `igIO` 0.65,0,0.35,1.
   - Components to use: `ig-frame` (grid and glow), `ig-crops`, `ig-wordmark`, `ig-progress` (chapter rail), `ig-kicker`, `ig-hxl/h/hsm`, `ig-sentence` + `ig-blank` + `ig-guesses` (fill in the blank), `ig-chips`, `ig-pill` + `ig-pointer` (callouts), `ig-stamp`, `ig-compare` + `ig-box` + `ig-arrow`, `ig-venn`, `ig-phone` + `ig-bubble`, `ig-signoff` + `ig-slot` (end card), `ig-scene-scrim` / `ig-scene-head` (illustration scenes).
   - Follow its rules: orange means emphasis and warnings; cyan means answers and "the AI". Keep one glowing focus per frame, nothing smaller than 28 px, and text inside the title-safe box (96 px top/bottom, 128 px sides).
   - **Alternative styles: igotchu Type Lab** (https://claude.ai/artifact/5rVQ8uuKWCxB5kxw2UkphQ): **Instrument** (light hardware panel: screws, silkscreen, keys, LEDs, dark screens) and **Patent** (patent drawing sheet: ink border, "Sheet n of 10", FIG. n, line art, blue for the AI). The Lab offers 7 font pairings; the default is Condensed Grotesque (Bricolage Grotesque at wdth 75, DM Sans, JetBrains Mono, from `@fontsource`).
   - Same scenes, different skin: `THEME=instrument python3 build_v3.py` (or `patent`) writes `video_<theme>/`. Themes are CSS overrides of the DS tokens and components (`THEMES` in `build_v3.py`) plus per-slide decorations. The default (`neon`) writes `video/`.
   - Theme parts to keep in sync: its eases (Instrument snaps with overshoot `0.3,1.45,0.5,1`; Patent is precise, `0.2,0.8,0.2,1` with no overshoot), `KEYBG` (the color phone keys return to after a flash), and the `common` layout nudges. The condensed font is wider at the same size, and the theme headers sit at the top, so headings drop to about 120 px and slide 1's headline shrinks.
   - **The user hasn't chosen a style yet** (Neon vs Instrument vs Patent). Ask before building the next video, and make only that one unless they ask for all three.
   - Illustration scenes in light themes: show the art on the device **screen** (Instrument) or as a framed **figure plate** (Patent), keeping its original colors. **Never color-invert illustrations**: it changed a person's skin tone. Real patent-style line art needs new images made in that style.
1. **Script.** Scripts live in the "igotchu Video Scripts" Claude Doc. Each has `[SLIDE n: cue]` lines followed by the spoken text. Split them into `slides.json` as `{n, cue, text}`. The cue is only a starting idea: designing the actual scene is your job. **Don't change the user's script wording** unless they say yes (they turned down a hook rewrite). Cutting a whole aside they approve is fine.
2. **Voice (ElevenLabs connector).** Generate **one clip per slide** with `creative_generate_speech` so each slide's timing is exact.
   - Put all clips in one flow (`creative_create_flow` first). Set `generations_count: 1`.
   - Voice: "Marshel - Casual Storytime Narrator" (`cQYsRVGKMkDmd67zTppv`) on `eleven_multilingual_v2`. The user preferred it over `eleven_v3` with acting tags. `eleven_v4` is locked on the free plan. Switch to the user's cloned voice once they have one.
   - The free plan allows **2 generations at a time**; extra calls fail, so re-run any that fail. Poll `creative_get_flow_run_status`, then download each `media[].url` right away with curl (signed links expire in 2 h).
   - To cut part of a clip, find the sentence break with `silencedetect` (try `-30dB`, `d=0.08–0.12`; the longest pause near the expected spot is the sentence break). Cut there with `-t` and a short fade.
3. **Illustrations (ElevenLabs connector).** Follow the design system's `illustration-prompts.md` (flat vector, navy, cyan/orange neon, subject in the right 55%, **no text, no faces**). Use `creative_generate_image`, `gpt-image-2`, `generations_count: 1`, about 185 credits each. Download `master_url`.
   - The **free plan caps images per day**. The 4th image was refused with `free_tier_image_limit_reached`.
   - AI video clips cost about 7,300 credits (Veo 3.1 fast, 8 s) or about 1,450 (`ltx-v2-fast`). Reviewers agreed: skip them and animate the illustrations instead.
4. **Timing, all free.** Pad each clip (0.35 s before, 0.55 s after), join with ffmpeg (loudnorm -16 LUFS), and write `timing.json`. Add about 7 s of hold after the last line for YouTube's end screen.
   - Word timing: run `silencedetect` per clip to get speech segments (`segments.json`). `cue(n, phrase)` aligns the script's phrases (split at punctuation) to those segments with a small DP. It measured accurately on Script 3.
   - **Don't use `creative_transcribe_audio` for timestamps.** It was estimated at 242 credits, **charged 3,021**, and returned plain text with no word times.
5. **Composition (HyperFrames).** One `<section class="clip scene">` per slide with an inner `.cam` wrapper, and GSAP tweens at absolute times from `cue()`. See "Scene kit" and "HyperFrames notes".
6. **Sound, free.** Synthesize the SFX with ffmpeg (`v3/sfx/`: pop, click, whoosh, thud, ding; see the build notes). The helpers record events automatically: `pop()` → pop, `land()` → ding, `slam()` → thud, each scene start → whoosh, phone typing and taps → click. The end of `build_v3.py` mixes them under the voice and loudnorms to `<out>/assets/mix.mp3`. A music bed costs about 900 credits with ElevenLabs Music, or use a free YouTube Audio Library track.
6b. **Optional review.** Before a big redesign, the user likes getting the plan reviewed by 3 parallel Opus subagents with different lenses: retention strategist, motion designer in this stack, and beginner viewer plus producer/budget. Give each one the narration file and contact sheets, combine the results into one plan, and point out any disagreements.
7. **Check.** `npx hyperframes lint .` (0 errors), then `npx hyperframes snapshot . --at <2–3 times per slide> --no-end --describe false -o ../snaps`. **Look at every contact sheet**, and fix overlaps, clipping, early or late reveals, and anything unreadable before rendering.
8. **Render** in the background: `npx hyperframes render -q standard -f 30 -w 4 -o out.mp4`, about 3.5 min. `SendUserFile` has a **30 MB limit**, so re-encode with `-c:v libx264 -preset slow -crf 25 -c:a copy -movflags +faststart` first (about 18 MB). If the render fails with "Failed to run ffmpeg -version", run it again. For all three styles: `for th in neon instrument patent; do THEME=$th python3 build_v3.py; done`, then render each output folder (`video/`, `video_instrument/`, `video_patent/`) one after another, about 4 min each.
9. **Extras.** Run `make_extras.py` → `captions.srt` (upload as closed captions). Fill in `youtube-extras.md`: title, thumbnail text, chapters from `timing.json`, a pinned comment for any cut aside, and the AI disclosure.

## Scene kit (what worked in v3)

- **Prediction chat box** (`predictor_steps`), the video's recurring image. A chat window builds the AI reply word by word. Before each word, a panel shows 3 candidates with growing bars, and the winner lights up cyan. Hook: bars **without numbers** (beginners can't read % yet). Show % only after the concept is explained. Payoff: a **wrong answer wins with the same bars and confidence** (keep the panel with `keep_last=True`), then a WRONG stamp and the real answer.
- **Fill in the blank** (DS): a blinking caret in the blank, the answer lands with a ding, guess cards rise, bars grow.
- **Loop**: the step pills (Read → Guess → Add → Repeat) light up in turn, faster and faster, synced to the predictor.
- **Realistic phone**: status bar, chat, typed text, a real keyboard with key flashes, suggestions that change each tap, a tap ripple, a camera zoom, and a stamp slammed on the keyboard. The user praised this as the production-quality benchmark: every scene should feel this real.
- **Morphing card**: one card that crossfades between mini UIs (code, form, checklist) instead of three static cards.
- **Typed then backspaced** text ("Autocomplete?"), then a burst on the payoff word. Keep burst rays off the text.
- **Comparison** (DS) for before/after, and **Venn** (DS) for "most of the time these overlap".
- **End card** (DS `ig-signoff` + `ig-slot`), held at least 5 s with empty slots where YouTube's real end-screen elements go. A next-video teaser comes before it. **Never a fake cursor clicking subscribe.**

## Retention checklist (from the three-reviewer pass)

- [ ] A concept-illustration scene about every 60 s. The user's favorite; see below.
- [ ] Something moves every 2–4 s: a `camera()` push on every scene plus timed reveals.
- [ ] Every text slide has an **object** in it (chat box, card, phone, diagram). Text only is the weakest look.
- [ ] One recurring visual idea per video that pays off at the end (Script 3: probability bars).
- [ ] Sound: whoosh between scenes, pops and dings on reveals, thud on stamps.
- [ ] Captions as an **SRT upload**, not burned in over text-heavy slides.
- [ ] Nothing covers key text; the stamps land on less important parts.
- [ ] No mascot in the corners (it clutters, and AI images drift). No fake ChatGPT or YouTube UI: use the design system's own chat look.
- [ ] Not the same skeleton every video: vary scene types across the 21 scripts ("inauthentic content" policy).

## Concept illustration scene (the signature scene)

A visual-metaphor image fades in slowly while pushing in (Ken Burns), and labels draw onto it on voice cues. The user loved this at 1:35 of the first test.
- Prompt: the design system's template. Put the subject in the right 55% and leave empty space where the headline goes.
- Motion: `tl.fromTo(art,{scale:1},{scale:1.12,duration:<scene>,ease:"none"})` plus a separate opacity 0→1 over 3–4 s with `sine.inOut` (`immediateRender:false`). Put pointers and pills **inside** the scaled `.art` wrapper so they stay on their targets.
- Callouts: the DS `ig-pointer` (dot pops, line draws from the target, then the pill pops). Place pills away from faces and key objects.
- When the voice moves on, dim the art to about 0.1 and build the next idea on top.

## HyperFrames notes (learned the hard way)

- **cdn.jsdelivr.net and Google Fonts are blocked here.** Copy `gsap`, `CustomEase` and `@fontsource/{inter,archivo-black}` woff2 files into `video/assets/`.
- Rendering needs FFmpeg (`apt-get install -y ffmpeg`) and Chromium: `HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`, `HYPERFRAMES_NO_TELEMETRY=1`.
- Animate transforms and opacity only; `left`/`top` tweens are a lint **error**. No CSS `@keyframes`, no `Math.random`.
- A second `fromTo` on the same element needs `immediateRender:false` (`_tw()` handles it). Use `tl.set(el,{className:…})` for state swaps.
- Text color is inherited as a computed value: redefining `--ink` on a wrapper doesn't recolor text inside it. Also set `color:var(--ink)` on that wrapper (the Instrument screen scenes needed this).
- `.scene [id]{opacity:0}` hides everything animated. Any container that isn't tweened itself must be listed as visible, or its children never appear.
- Reveal text with `display:none` → `tl.set(el,{display:"inline"})` so it wraps naturally.
- Blinking carets: a `fromTo` with `ease:"steps(1)"`, `repeat`, `yoyo`.
- Advisory lint warnings (nested_structure, track_too_dense, composition_file_too_large) are fine.

## Budget (ElevenLabs)

- Free plan: 10k credits/month. One video's voice is about 3.5k credits, so the free plan covers 1–2 videos a month. Starter ($6): 30k credits, commercial rights, cloning, and likely no daily image cap.
- Always use `estimate_only` first, but **estimates can be badly wrong** (transcription: 242 estimated, 3,021 charged). Try a new kind of generation on a tiny input first, and **ask before spending** when credits are low (about 2,300–2,900 left after Script 3).

## Before the user uploads

- Voice made on the **ElevenLabs free plan isn't licensed for monetized use**: regenerate it on Starter or higher (per-slide clips make that easy).
- In YouTube Studio, tick **"altered or synthetic content"**.
- Scripts need the user's real opinions and experiences ("inauthentic content" policy).
