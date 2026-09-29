---
name: youtube-video
description: Make a finished faceless, voiceover YouTube video for the igotchu AI-explainer channel from a script. Covers the Claude Design styles (Neon Blueprint, plus the Type Lab's Instrument and Patent themes), the ElevenLabs voice (one clip per slide), AI concept illustrations, HyperFrames animated scenes, free synthesized sound effects, captions and rendering an MP4. Use whenever the user asks to make, build, render, upgrade or redesign a YouTube video, turn a script into a video, or add visuals, voice, captions, sound, music or illustrations to one.
---

# igotchu YouTube video

The channel is a faceless AI explainer for beginners: voiceover, animated scenes and concept illustrations. The user doesn't edit. They give a script and approve the result, so the finished video must hold attention on its own. The user is often on a phone, so keep them away from file shuffling.

**Newest reference build: `igotchu-test/prompt-video/frames.py` → `video_frames/`** (the user's "Ep 07 Frames" design, https://claude.ai/artifact/DSaXXh4rTgUz92BLBWYUK1: colour card per block, typed prompt with numbered highlights, white AI reply card, blurred block names revealed only when spoken, no screenshots; the user prefers this). Older in the same folder: `build.py` (Script 7 "Anatomy of a good prompt", Ep 07). It follows the student kit (https://github.com/nateherkai/hyperframes-student-kit): one sub-composition file per slide, a persistent world layer, the kit's preflight and beat-sync checks, and real screenshots with a zooming camera and read-along highlights. See "Student-kit build" below.

**Previous reference build: `igotchu-test/v4/`** (Script 3 v2.1, video v4, built after the 8-expert panel). It has the panel fixes: scene crossovers, a visible camera, a frozen-frame check, a two-pass -14 LUFS master and the cloned voice. `igotchu-test/v3/` is the older build and still holds the Instrument and Patent theme CSS.
- v4 files: `make_vo.py` (trim, normalize and pause the clips, write `timing.json`), `make_segments.py`, `build_v4.py`, `make_extras.py`, `youtube-extras.md`.
- The 8 expert reviews and their synthesis are in `igotchu-test/panel/reviews/`.
- `build_v3.py` generates `video/index.html` and the audio mix from `timing.json`, `slides.json`, `segments.json` and `ds/`.
- `make_extras.py` writes `captions.srt`.
- `youtube-extras.md` holds the title, chapters, pinned comment and disclosure.

Copy this structure for every new video. Its helpers are the reusable kit: `cue()` alignment, `rise/pop/land/slam/draw/ignite/camera`, `predictor_steps()`, the phone scene, and the SFX mix.

## READ FIRST: the user's current decisions (house style)

These override anything older further down.
- **Design: "Ep 07 Frames"** (https://claude.ai/artifact/DSaXXh4rTgUz92BLBWYUK1). Build every new video from `videos/ep07-anatomy-of-a-prompt/frames.py`, not the Neon, Instrument or Patent builds.
  - **Colour per block, everywhere:** task graphite/paper, context pink, rules yellow, examples blue.
  - **Two beats per idea:** a full-screen colour card names it, then an evidence frame proves it.
  - **Type:** giant condensed type (Bricolage 75 / DM Sans / JetBrains Mono), and nothing on screen under 26 px.
- **No screenshots on screen.** Show prompts as typed text with numbered tags (1 2 3 4), and sweep each new part with a highlight in its block colour **while the voice reads it**.
- **AI replies:** show the **whole** real reply in the white card (greeting, every paragraph, sign-off), then highlight the quoted line as it's spoken. One sentence on its own confused the user.
- **Never reveal ahead of the voice.** The opening shows the four coloured bars with their **names blurred**, and each name appears only when that block is spoken. Nothing appears before it's said.
- **Every spoken phrase needs something on screen that belongs to it.** Check a 1-fps contact sheet of the render for empty stretches.
- **Voice:**
  - Use the user's clone "Johnson" (`oStMmyqgSXJilnbQGwo3`) on `eleven_v3`, the **whole script as one generation**, split with `split_take.py`, played at **1.08x for every slide**.
  - Never generate per-slide clips; the accent drifts and the user hears it.
  - The user may record their own voice instead: then split their recording the same way.
  - **Don't ask the user to choose between voice takes or options**; they asked for no more options.
- **Script voice:** talk to the viewer ("you"). **Never invent the narrator's personal experiences** (a first-person claim like "I used a card I wrote for my dad" was a mistake). Put wording that belongs in a prompt inside the on-screen prompt, not in the narration as a personal claim.
- **Replies quoted in a video must be real Claude replies** to the exact prompt shown.
- **Credits:** ElevenLabs is on a paid plan but ran low (about 2,800 left at the end of Ep 07). A full one-take script costs about 1 credit per character. Estimate first, and tell the user before spending.

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
   - **Style per video:** for Ep 07 the user answered the style question with the Type Lab link, and **Instrument** (Condensed Grotesque) was used. Confirm the style before each new video, and make only that one unless they ask for all three.
   - Illustration scenes in light themes: show the art on the device **screen** (Instrument) or as a framed **figure plate** (Patent), keeping its original colors. **Never color-invert illustrations**: it changed a person's skin tone. Real patent-style line art needs new images made in that style.
1. **Script.** Scripts live in the "igotchu Video Scripts" Claude Doc. Each has `[SLIDE n: cue]` lines followed by the spoken text. Split them into `slides.json` as `{n, cue, text}`. The cue is only a starting idea: designing the actual scene is your job. **Don't change the user's script wording** unless they say yes (they turned down a hook rewrite). Cutting a whole aside they approve is fine.
2. **Voice (ElevenLabs connector).** Generate **one clip per slide** with `creative_generate_speech` so each slide's timing is exact.
   - Put all clips in one flow (`creative_create_flow` first). Set `generations_count: 1`.
   - **Record the whole script as ONE generation** (eleven_v3 took 3,454 characters in one call), then cut it into slides with `prompt-video/split_take.py`, which uses the phrase aligner and cuts at the pause before each slide. Every slide plays at the same 1.08x. Separate clips per slide drift in accent, and the user heard the voice change at "Block one" every time. Per-slide stretching made it worse.
   - (Superseded) **Voice consistency (Ep 07 lesson):** eleven_v3 takes drift in accent from clip to clip. The user wants every slide to sound like the Ep 07 slide 1 opening. The takes they rejected were flatter and lower (pitch 90th percentile around 200-230 Hz, spread about 7 semitones). Their pick matched the opening (about 320-350 Hz, 8+ semitones). Record 3 takes per slide and keep the liveliest by that profile (`prompt-video/voice_match.py`; the librosa pitch profile is in the build notes). Split long slides into two chunks, because shorter chunks read livelier. **Don't ask the user to pick takes;** they asked for no more options. `make_vo.py` pace-matches every slide to slide 1 (capped at 1.17x).
   - **Voice: the user's own clone "Johnson" (`oStMmyqgSXJilnbQGwo3`) on `eleven_v3`, with no acting tags** (tags sounded overdone).
     - The clone reads slowly (about 146 words a minute), so `make_vo.py` speeds it up to 1.08× with `atempo`, which keeps the pitch. That gives about 158 words a minute; the panel's target is 150–170.
     - Backup voice: Marshel (`cQYsRVGKMkDmd67zTppv`).
     - `eleven_v4` is refused ("not authorized") even on the paid plan, although `estimate_only` says it will work.
   - **Write the voice text the way it's spoken**, and keep captions in written form: "twenty twenty-five" instead of 2025, "thirty-four million" instead of 34M. `slides.json` holds the spoken form so the aligner counts the right characters; `make_extras.py` converts back for captions.
   - **Designed pauses:** split a slide into two clips where the viewer should think (after "Pause the video…", before "It was Jay"). `make_vo.py` inserts exact silence between them (2.2 s and 1.4 s).
   - Concurrency: the free plan allows **2 generations at a time** and the current paid plan allows **3**. Extra calls fail with "Too many concurrent requests" (failed runs were still listed with a price), so send 3 at a time and re-run any that fail. Poll `creative_get_flow_run_status`, then download each `media[].url` right away with curl (signed links expire in 2 h).
   - To cut part of a clip, find the sentence break with `silencedetect` (try `-30dB`, `d=0.08–0.12`; the longest pause near the expected spot is the sentence break). Cut there with `-t` and a short fade.
3. **Illustrations (ElevenLabs connector).** Follow the design system's `illustration-prompts.md` (flat vector, navy, cyan/orange neon, subject in the right 55%, **no text, no faces**). Use `creative_generate_image`, `gpt-image-2`, `generations_count: 1`, about 185 credits each. Download `master_url`.
   - The **free plan caps images per day**. The 4th image was refused with `free_tier_image_limit_reached`.
   - AI video clips cost about 7,300 credits (Veo 3.1 fast, 8 s) or about 1,450 (`ltx-v2-fast`). Reviewers agreed: skip them and animate the illustrations instead.
4. **Timing, all free.** `make_vo.py` does this step.
   - Trim each clip's edge silence with `silencedetect` + `atrim`. **Don't** use the `silenceremove,areverse` chain: it hung forever on one clip.
   - Normalize each clip to -20 LUFS, then pad it (0.15 s before, 0.4 s after).
   - Add a 5.5 s end-card hold, join the slides, and write `timing.json`.
   - `make_segments.py` writes speech segments relative to each slide's start.
   - Word timing: run `silencedetect` per clip to get speech segments (`segments.json`). `cue(n, phrase)` aligns the script's phrases (split at punctuation) to those segments with a small DP. It measured accurately on Script 3.
   - **Don't use `creative_transcribe_audio` for timestamps.** It was estimated at 242 credits, **charged 3,021**, and returned plain text with no word times.
5. **Composition (HyperFrames).** One `<section class="clip scene">` per slide with an inner `.cam` wrapper, and GSAP tweens at absolute times from `cue()`. See "Scene kit" and "HyperFrames notes".
6. **Sound, free.** v4 fixes:
   - **Whoosh:** it needs `bandpass=…:t=h:w=1800`. Without `t=h`, w=1800 is read as Q and the whoosh is silent.
   - **Gains:** thud 0.25 (it was louder than the voice).
   - **New sounds:** `tick` (a predicted word locks in) and `buzz` (phone vibrates).
   - **Spacing:** identical sounds at least 0.3 s apart.
   - **Master:** two-pass `loudnorm` to **-14 LUFS / -1 dBTP** (YouTube's level; the old -16 single pass came out at -17.4).
     - **Limit before you normalize.** A voice mix at about -20 LUFS with -2 dBTP peaks can't reach -14 linearly, so loudnorm silently switches to dynamic mode and undershoots (Ep 07 came out at -15.2). `prompt-video/mix.py` puts `volume=7dB,alimiter=limit=0.6:attack=4:release=60:level=false` ahead of both loudnorm passes and lands at -14.2 LUFS. Always measure the final file with `ebur128=peak=true`.
   - **Still to do:** a music bed about 20 dB under the voice, which the panel recommends.
   Synthesize the SFX with ffmpeg (`v3/sfx/`: pop, click, whoosh, thud, ding; see the build notes). The helpers record events automatically: `pop()` → pop, `land()` → ding, `slam()` → thud, each scene start → whoosh, phone typing and taps → click. The end of `build_v3.py` mixes them under the voice and loudnorms to `<out>/assets/mix.mp3`. A music bed costs about 900 credits with ElevenLabs Music, or use a free YouTube Audio Library track.
6b. **Expert panel (the user asks for this).** Run 8 parallel Opus subagents (`model: "opus"`), each told to **research first** (at least 5 sources on what the best in their field do) and then judge.
   - The lenses: retention/packaging, scriptwriter, learning scientist, fact-checker, motion designer, art director, timing/sound editor, voice director.
   - Give them a shared brief (`panel/BRIEF_8.md`), the script, 1-fps timestamped contact sheets of the current render (`ffmpeg … fps=1,drawtext=…,tile=5x4`), 4-fps motion strips of key moments, the build code and the design-system files.
   - Each writes `panel/reviews/<slug>.md`: score, top 5 fixes with exact lines or specs, a keep list and a bold idea.
   - Combine the reports into `SYNTHESIS.md`, noting agreements and disagreements.
7. **Check.** `npx hyperframes lint .` (0 errors), then `npx hyperframes snapshot . --at <2–3 times per slide> --no-end --describe false -o ../snaps`. **Look at every contact sheet**, and fix overlaps, clipping, early or late reveals, and anything unreadable before rendering.
   - After the render, pull **one frame per second across each slide** (or at least every spoken phrase change), not just 2–3 per slide. The frozen-frame check only catches missing motion: Ep 07 passed it but still had a 2.5 s **empty stage** in slide 7, where the old group left on one phrase and the next arrived two phrases later. Every spoken phrase needs something on stage that belongs to it.
8. **Render** in the background: `npx hyperframes render -q standard -f 30 -w 4 -o out.mp4`, about 3.5 min (about 7 min for a 4-minute student-kit build). `SendUserFile` has a **30 MB limit**, so re-encode with `-c:v libx264 -preset slow -crf 25 -c:a copy -movflags +faststart` first (about 18 MB). If the render fails with "Failed to run ffmpeg -version", run it again. For all three styles: `for th in neon instrument patent; do THEME=$th python3 build_v3.py; done`, then render each output folder (`video/`, `video_instrument/`, `video_patent/`) one after another, about 4 min each.
9. **Extras.** Run `make_extras.py` → `captions.srt` (upload as closed captions). Fill in `youtube-extras.md`: title, thumbnail text, chapters from `timing.json`, a pinned comment for any cut aside, and the AI disclosure.

## Student-kit build (Ep 07, `igotchu-test/prompt-video/`)

The kit is cloned read-only at `/home/user/nateherkai/hyperframes-student-kit`; our notes on it are in `igotchu-test/kit-notes.md`. Our voice, `cue()` timing, SFX and mastering stay; the structure and checks come from the kit.
- **Files:** `build.py` writes `video/index.html` (root "anatomy": `assets/mix.mp3` on track 9, `world` on track 0, scenes on tracks 1/2 with the 0.35 s crossover) and `video/compositions/{world,s01..s10}.html`. Each file is a `<template id="<id>-template">` holding a `data-composition-id` div with `data-anchor="<first spoken phrase>"`, CSS scoped with `[data-composition-id="<id>"]`, and a paused **local-time** timeline at `window.__timelines["<id>"]`, pinned to the slot length with `tl.set({}, {}, SLOT)`.
- **Ids `s01`..`s10`:** the kit's beat-sync script misreads hyphen-digit ids. Put `data-anchor` inside the composition file, not on the mount. Use an anchor that can't match earlier words ("Here's where…" matched an earlier "Here", so the anchor became "where most people start").
- **Checks, in order:** `node <kit>/scripts/preflight.mjs video`, `npx hyperframes lint video` (0/0), `node <kit>/scripts/validate-beat-sync.mjs video` (needs `video/assets/transcript.json` `{words:[{text,start}]}`, which `build.py` writes by interpolating word times; the world layer's NO-ANCHOR is expected), the frozen-stretch report, then snapshots.
- **HyperFrames CLI 0.8.71** (in `igotchu-test/node_modules`, run with `npx --prefix igotchu-test hyperframes …`). The kit pins 0.7.109, which is slower and warns 131 times; keep 0.8.71.
- **World layer** (persistent, full length): header silk, slide tag with LEDs, chapter label, progress line, and the recurring object, here a rack of 4 prompt-block keys. A key is a `.key#kN` wrapper (layout: hero row, side rail, gone) holding an inner `.kb#kbN` body (press and pulse target). **Never press or pulse the element that carries layout transforms**: `fromTo` resets its `y`/`scale` and the rack blew up. `key_state(i, 'spot'|'lit'|'off')` implements the spotlight rule (one key at full strength, lit ones about .6, off .3).
- **Real screenshots, zoomed and highlighted (`class Viewer`):** `ocr_boxes.py` runs Tesseract (`apt-get install -y tesseract-ocr`) on each screenshot and writes word boxes to `ocr/words.json`. `find_words(shot, phrase)` matches letters only, so OCR merges and curly quotes don't matter, and `box()` turns the matched words into a region.
  - `viewer.zoom(region, t, dur, pad, max_s)` eases the `.vcam` (x, y, scale, `igIO`, 1.1 s, soft whoosh) so the region fills the screen, clamped so the image edge never slides into view. `drift()` adds a slow 3.5% push while holding.
  - `viewer.sweep(phrase, t0, t1, color)` draws a highlighter over each word, left to right, timed by letter share between the two voice cues: the read-along highlight the user asked for. Use `mix-blend-mode: screen` on dark screenshots and `multiply` on light ones.
  - **Check that the whole highlighted phrase fits the final zoom.** A hand-picked region cut off "home with" at the right edge; use the OCR box or extend the region to the last word's right edge.
  - SVG marks (ellipses and a connecting line) live inside `.vcam` in image pixels, so they stay on their words while the camera moves.
- **The script's quoted AI answers must match the screenshots word for word.** Take them from the screenshots, update the Claude Doc (with the user's approval), and only then record the voice.

## Writing the script (from the 4-reviewer panel on Script 3)

The panel scored the original Script 3 5/10 on relatability, takeaway, sounding human and structure. Write or revise every script with these rules, then run the de-AI checklist before recording anything.

**Structure**
- **Open on a real, checkable story or a scene, not a claim.** Put a person, stakes and a twist in the first 20 seconds, and deliver the title's promise within the first minute. Never "By the end of this video you'll understand…", and never announce the curiosity gap ("a question that'll bug you"); create it instead.
- **Say the viewer's wrong belief out loud first, then take it apart** ("Most people think it looks your question up. It doesn't."). Veritasium creator Derek Muller's research found this nearly doubles learning.
- **Link beats with "but" or "therefore", never "and then"** (Parker & Stone). Never run 3+ analogies in a row that prove the same point. Re-hook every 30–60 s with a new question the last answer raised.
- **One takeaway spine (3 beats) plus one habit the viewer leaves with.** Cut side ideas that belong in another episode.
- **Pay the twist off inside the video.** A teaser for the next episode comes after the payoff, not instead of it.

**Examples and evidence**
- **Use the viewer's life:** texts from mom, group chats, the barista, your own phone. Avoid the default AI-explainer examples (peanut butter and jelly, capital of France, "a smart friend").
- **Add a 10-second "pause and try it now" moment**, plus a self-check question near the end.
- **Use real, documented incidents** (court rulings, news) with the source shown on screen and linked in the description, so viewers can check them. Verify every fact, date and quote against primary sources; say what's proven versus alleged.
- **Stay accurate:** "next word" is really tokens; ChatGPT can search the web ("unless it shows you links"); don't claim more than the evidence supports.

**Personal truth, only from the user**
- **Never invent the narrator's experiences** ("at work I see…", "when I first learned this…"). Put a `[FILL: …]` where a true story belongs, and ask the user for it. At least one real, specific story per script, told as a scene (when, where, what broke), not as "as a software engineer".
- **One real opinion per script** that someone could disagree with.

### De-AI checklist (run on every script)
1. **Ban list, at most one per script:** Here's the thing / Here's the part / Honestly / Okay, / basically / scary good / actually wild / Let's / Quick [noun] / "If that sounds familiar, it should."
2. **No "not X, (but) Y" contrasts.** State the positive claim.
3. **No lists of three** unless the items are truly specific and uneven. Two or four items is fine. Prefer one weird, specific example.
4. **Cut the last sentence of any slide that only sums it up** ("That is basically the whole trick.").
5. **At least one `[FILL]` real personal detail per script, told as a scene.** "As a software engineer" at most once, and only where it adds something only an engineer would know.
6. **One opinion someone could disagree with.**
7. **At least one joke or aside, and one self-correction** ("well, sort of").
8. **No more than two fragments in a row.** At least one long, loose spoken sentence per slide.
9. **Don't tell viewers what they think or feel.** Ask, or react to a likely comment.
10. **Vary openings, "next video" lead-ins, and where "I gotchu" lands** across the series (it closed 19 of 19 scripts the same way).
11. **Read it aloud at speaking speed.** Rewrite anything you'd stumble on or wouldn't say to a friend.
12. **No absolute promises** ("every time", "always") unless literally true.

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

- **v4 motion system** (see `build_v4.py`):
  - **Scene crossovers:** each section starts 0.35 s early on alternating tracks, and its `.tr` wrapper slides in (`x:90→0`, `igOut`) while the old one exits (`x:-70`, `igIn`). The screen is never blank between slides.
  - **Camera:** `.cam` pushes `scale 1→1.05, x→-24` with `sine.inOut` on every scene; the old 3% push was invisible.
  - **Sway:** `sway()` adds a ±0.6° handheld drift on phones and chats.
  - **Entrances and emphasis:** `settle()` (`igSettle`, no overshoot) replaces most bouncy pops. `pulse()` emphasizes a stressed word.
  - **Frozen-frame check:** the build prints any stretch over 3.2 s with no new motion. Fix every one, with `pulse`/emphasis on the spoken word, before rendering.
- **The `.scene [id]{opacity:0}` trap:** any element with an id that is only animated with scale, x or className (bar fills, markers, strike-through text, highlight rows, AI reply bubbles) stays invisible. Whitelist it in CSS, e.g. `.bar i[id]{opacity:1}`.
- **A `!important` opacity** on a scene class blocks later GSAP fades. Set the starting state with `tl.set(...,0)` instead.
- **Class-name clashes across scenes** (a `.me` tile in slide 5 vs `.gm.me` chat bubbles in slide 7) break layouts silently. Use scene-specific names.
- **Code blocks:** `white-space:pre` on the container turns the HTML's own newlines into blank lines. Put `pre` on each line's div instead.
- **Blinking carets:** `blink()` needs `immediateRender:false`, or the caret shows before its words.
- **Emoji:** use `font-family:"Noto Color Emoji"` plus `@font-face{font-family:"Noto Color Emoji";src:local("Noto Color Emoji")}` (lint requires the declaration).
- **Screenshots of the user's phone:** crop to just the part that matters. The full screenshot showed this chat and the app's model name.

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
