# HyperFrames Student Kit: notes for igotchu

Source studied: `/home/user/nateherkai/hyperframes-student-kit` (commit ec112ff, package 2.0.0, pins hyperframes 0.7.109 + gsap 3.14.2).
Compared against: `igotchu-test/v4/build_v4.py` and `.claude/skills/youtube-video/SKILL.md`.
Nothing in the kit or in this repo was modified. All experiments ran on copies in the session scratchpad.

---

## (a) What the kit is and its core workflow

It's Nate Herk's agent kit for Claude Code and Codex. It has 15 skills (mirrored in `.claude/skills` and `.agents/skills`), a card library of 406 draft cards in 2 styles, 2 scene templates, Node utilities, and 12 finished example projects. Its main use case is editing **talking-head footage**: transcribe, cut silences, cut mistakes, then add overlays. For a video that is motion graphics only, the relevant path is the **`make-a-video`** skill, supported by the others:

| Stage | Kit artifact | Notes for us |
|---|---|---|
| Interview (Gates 1-4) | `BRIEF.md`, `assets/style-profile.md` | We already know the answers; write the brief ourselves |
| Storyboard (Gate 5) | `STORYBOARD.md`: timing table + per-beat block (visual, motion, eases, exit, audio) | Rule of threes; outro holds 4-6 s; at least one callback |
| World design | `video-storytelling` skill | Persistent world, camera altitudes, spotlight rule, spatial open loops |
| Build (Gate 6) | `index.html` root + one **sub-composition per scene** in `compositions/` via `data-composition-src` | Scoped CSS, IIFE, paused timeline registered on `window.__timelines[id]`, slot pin |
| Check (Gate 7) | `node scripts/preflight.mjs <proj>`, `npx hyperframes lint`, `node scripts/validate-beat-sync.mjs <proj>`, Studio preview | Two human preview gates |
| Draft + verify (Gate 8) | draft render, extract frames at hero moments and transitions, **Read every PNG**, contiguous-frame strips across transitions, `VERIFY.md` | Then a standard render |

Project scaffold: `npm run new-video -- <slug>` copies `examples/starter` (index.html, meta.json, hyperframes.json, DESIGN.md) plus a local `assets/gsap.min.js` into `video-projects/<slug>/`.

Voice in the kit is Kokoro TTS (`npx hyperframes tts`) or recorded footage. It has no ElevenLabs TTS pipeline, no SFX mix (except the `motion-showreel` sfx.mjs, which uses paid ElevenLabs sound generation), and no loudness mastering. **Our voice, SFX and mastering pipeline stays as is.**

## (b) Rules and conventions to adopt, and conflicts with how we build now

### Motion philosophy (`MOTION_PHILOSOPHY.md`)
This is a deconstruction of a 30 s payments ad: black canvas, chrome-gradient type, a perspective grid, and whips every 1.5 s. `CLAUDE.md` itself says to treat the fast pacing as a style reference and to "give educational speech room to breathe". Adopt:
- One idea per beat. At most 5 hues, each with a named meaning. Our orange/cyan meanings already match this.
- The camera never sleeps. Every transition uses motion (whip, blur, recolor), never a hard cut. At least one callback. Hold the outro 4+ s.
- The **tween-comment convention**: every exit tween's comment names the matching entry tween in the next beat. This is cheap and catches broken seams.
- Snap tween end times to multiples of 1/fps (it matters for `expo.in`/`power4.in`).
- No `Math.random`/`Date.now`; no `repeat:-1` (use finite repeats); no `gsap.defaults()`.
- The Law 11 **slot pin**: a sub-composition whose timeline is shorter than its `data-duration` gets hidden, which shows as a black flash. The kit's own sources disagree on the form: MOTION_PHILOSOPHY uses `tl.to({}, {duration:SLOT}, 0)`, while the `hyperframes` skill says "never create empty tweens". The examples and cards use **`tl.set({}, {}, SLOT)`**. Use that.

Ignore: 1-2 s average scenes; chrome gradient on every text; a different font per beat; perspective grid, grain and vignette on every scene. These clash with the Neon Blueprint design system, and the grain component uses a CSS `@keyframes`, which we know doesn't render under frame-seeking.

### `video-storytelling` (the most valuable skill for us)
- **One persistent world**, never reset. **Spatial open loops**: plant empty sockets in the hook, show them again at every section boundary, fill one per section, and close on the opening image. This is exactly "Anatomy of a Good Prompt" (4 ghost blocks).
- **Spotlight rule**: exactly one element at full brightness. Context elements sit at about 0.56 opacity and spent ones at about 0.33; labels never go below luma 90 and always inherit their element's state. Finished props retire to 0, not 0.3. Keep one opacity authority per element per window, or the render strobes.
- **One travelling subject** whose state changes (for us, the prompt card).
- About **20 on-screen words per section**. Every shape gets a word or isn't drawn. An anti-pattern visual never overlays the recommendation.
- Keep a global token set (stroke, type and radius scales). Exits are faster than entrances. `back.out` once per section. **No full-bleed cross-fades.**
- **One generator per section**, writing `compositions/<id>.html`. This fits our Python-generator habit.
- **Namespace SVG `defs` ids per section**: duplicate `url(#id)` ids silently paint nothing after assembly.
- Verify the **assembled** render, and read **contiguous frame strips** across every transition (`select='between(n,A,B)',tile=6x7`), not just one frame per beat.

### Sub-compositions (the main structural change)
We build today: one ~1,250-line Python file emits **one big `index.html`** with a single `main` timeline at absolute times.
The kit builds: a root `index.html` with each scene as `<div id="s03" data-composition-id="s03-task" data-composition-src="compositions/s03-task.html" data-start=".." data-duration=".." data-track-index="..">`. Each file has scoped CSS (`[data-composition-id="s03-task"] ...`), an IIFE, a paused timeline in **local time**, and `window.__timelines["s03-task"]`. The framework nests the child timelines, so never `add()` them yourself.
The gain: each slide previews on its own (`?comp=<id>` in Studio), class-name clashes between scenes are gone (a v4 bug), and the timeline and file sizes shrink. It also sidesteps the `.scene [id]{opacity:0}` trap, because each scene owns its CSS.
Our generator can keep `cue()`: emit `cue(n, phrase) - T[n].start` as local times.

### Data-anchor beat sync (`scripts/validate-beat-sync.mjs`)
Each sub-composition file carries `data-anchor="<exact transcript phrase>"`. The script resolves each beat's absolute start from `index.html`, including `id + N` references, and finds the phrase in `assets/transcript.json` (`words:[{text|word,start}]`). It requires the beat to enter between **0.2 s after and 1.8 s before** the word, and `--suggest-fix` prints starts with a 0.5 s lead. It only checks **scene entry**. Timing inside a scene is left to "manual review".
Caveats found:
- **No example project actually uses `data-anchor`.**
- **Bug:** start references like `data-start="sec-01"` fail, because the lazy regex parses `sec` plus offset `-01`. Running it on `golden-ratio-demo` stops with "Unknown beat id referenced: sec". Use ids without hyphen-digits (`s01`) or absolute starts.
- It needs word timestamps, and we have none (see e). **Workaround:** have our generator write `assets/transcript.json` from the DP aligner's phrase anchors (one "word" entry per phrase start). The validator then checks slide entries for free.

### Preflight and verify
- `scripts/preflight.mjs`: root div has id, dimensions and `data-start="0"`; the timeline is registered under the root id and is non-empty; every `data-composition-src` exists; warns when a master holds more than 3 WebGL shader blocks. It's fast, plain Node, and works with any HyperFrames version. Adopt it.
- `hyperframes validate` (WCAG contrast audit) and the skill's `animation-map.mjs` (dead zones over 1 s, collisions, offscreen, pacing flags) complement our frozen-frame check.
- `VERIFY.md` per video: what was checked, with frame paths and limits.

### Conflicts and differences summary
| Topic | Kit | Us (keep or change) |
|---|---|---|
| File structure | root + sub-compositions | Change to sub-compositions |
| Timing source | word-level transcript (Scribe/Whisper) | Keep silencedetect + DP `cue()`; export phrase anchors as transcript.json |
| Scene pacing | 1-2 s scenes (ad) | Slides of about 30 s with beats every 2-4 s inside (our retention rule) |
| Exits | hyperframes skill: no exit tweens, the transition is the exit | Our crossover (`.tr` slide in/out) is a transition, so it's compatible |
| Captions | body-level caption clips | Keep the SRT upload (panel decision) |
| Fonts | Google Fonts `@import`, compiler embeds | Keep local `@fontsource` woff2 |
| GSAP | jsdelivr CDN in every card | Local `assets/gsap.min.js` + CustomEase |
| Render workers | storytelling says `--workers 1` (only because a video layer painted black) | We have no video layer, so `-w 4` is fine |
| Grain | CSS `@keyframes` component | Don't use it; do grain with GSAP `backgroundPosition` steps if wanted |

## (c) Card styles and types for a prompt-engineering explainer

Registry (`style-library/registry.json`): 2 styles, 406 cards, all marked `draft`.
- **vox-explainer (106):** tier1 stat 41, overview 21, section 18; tier2 lower-third 13, label 13. Warm paper `#efe9dc`, Fraunces serif, blue marker boxes, stepped "stop-motion" motion.
- **kallaway (300):** 60 each of tier1 section/stat/overview and tier2 lower-third/label. Dark `#0A0E14` with a blue "aurora" bloom, glass cards, Plus Jakarta Sans/Inter/Space Mono, smooth glide.
- **_blueprint:** a skeleton with 2 example cards (t1-stat, t2-list) for building a new style.
- Card contract: a standalone composition with named `data-slot` text, tokens only from `tokens.css`, and self-timed internal reveals (about 1-4 s into a 6-8 s slot). tier1 cards are opaque takeovers; tier2 cards are transparent overlays meant to sit beside a speaker (tier2 is mostly useless for us). `.set({}, {}, N)` pins exist in only 148 of 406 cards.
- To mount a card, wrap it in `<template>` inside `compositions/`, localize gsap and fonts, fill the slots, and re-time its internal reveals to our voice cues.

Best fits (Kallaway, the closest to our dark Neon look), in `style-library/02-kallaway/cards/`:
- The build-up spine: `tier1/t1-overview-layers.html` (a 4-layer stack, perfect for Task, Context, Rules, Example stacking), `tier1/t1-overview-steps.html`, `tier1/t1-overview-numlist.html`.
- The prompt box and typing: `tier1/t1-section-searchbar.html` (text typed into a search/prompt bar), `tier1/t1-section-typed.html`.
- Hook and the "ask me questions first" beat: `tier1/t1-section-question.html`, `tier1/t1-section-chaptercard.html`.
- Answer gets better: `tier1/t1-overview-beforeafter.html`, `tier1/t1-stat-versus.html`, `tier1/t1-stat-score.html`, `tier1/t1-stat-meter.html`, `tier1/t1-overview-tiercompare.html`, `tier1/t1-overview-featurecompare.html`.
- Recap and formula: `tier1/t1-overview-checklist.html`, `tier1/t1-overview-summary.html`, `tier2/t2-lb-formula.html` ("Prompt = Task + Context + Rules + Example"), `tier2/t2-lb-definition.html`, `tier2/t2-lb-keyword.html`.

In Vox (`style-library/01-vox-explainer/cards/tier1/`): `t1-section-correction.html` (a strike-through with a handwritten correction, good for "vague" becoming "specific"), `t1-section-markerbox.html`, `t1-overview-checklist.html`, `t1-overview-compare.html`, `t1-overview-stepper.html`.

### Visual quality, honest take
I viewed these images:
- Showcase frames: `scratchpad/frames/showcase_tile.png`.
- Example projects: `scratchpad/frames/mg_tile.png`.
- 16 cards rendered with localized fonts and gsap through `hyperframes snapshot` at t=5 s: `scratchpad/cards/tile_02-kallaway.png` and `scratchpad/cards/tile_01-vox-explainer.png`.

The scratchpad is `/tmp/claude-0/-home-user-LyricsVideoGenerator/b8ff831e-4fc1-54b6-a439-07cf9366784f/scratchpad/`.

- **The showcase reels** (9:16 talking-head shorts with a warm paper look, 3D-ish stacked cards and word captions) are the best-looking output in the kit. They rely on footage and Kie.ai-generated 3D assets, and their source projects aren't included. `youtube-showreel.mp4`, which the README links to, is missing from the clone.
- **The example projects** (sizzle, linear-promo, lesson-5-1) are clean but plain: big type on dark, sparse diagrams, lots of empty frame. Solid craft, nothing beyond our v4.
- **Kallaway cards:** polished glass-and-glow typography, but generic "SaaS explainer" templates. Their body text is 19-24 px, below our 28 px minimum. I saw real defects at their default copy: in `t1-overview-beforeafter` the 2-line title runs into the cards ("Could Be" is clipped); in `t1-section-searchbar` the text overflows the bar ("Actually" is cut); `t1-overview-layers` sits low with a large empty top. They are "draft" and it shows.
- **Vox cards:** well typeset and distinctive (paper, serif, marker boxes), but there's a placeholder "Vox" circle, lots of empty lower frame, and 20-24 px labels.
- **Compared with our Neon Blueprint v4:** ours is stronger for this channel. It has bespoke, realistic objects (phone, prediction chat box, bars), a coherent design system and larger type. Kallaway is the same visual family, not an upgrade. **Recommendation:** don't adopt a kit style wholesale. Borrow **layouts and motion ideas** (the layer stack, prompt-bar typing, versus/score cards, formula chip, correction strike) and re-skin them in Neon tokens. The kit's real value is **process** (sub-compositions, open loop and spotlight discipline, preflight, anchors, frame-strip QA), not its cards.

## (d) Plan: "Anatomy of a Good Prompt" (about 5 min, 10 slides)

**Skills to follow:**
- Kit `make-a-video` for the gate order. Write the brief ourselves, since we know the answers.
- Kit `video-storytelling` for the world design.
- Kit `hyperframes` + `gsap` for the authoring rules.
- Our `youtube-video` skill for script rules, the ElevenLabs clone voice, SFX, the -14 LUFS master, SRT and extras.
- Skip the footage skills: `edit-video`, `cut-silences`, `cut-mistakes`, `hyperframes-video-beats`.

**World:** one persistent "prompt workbench". On the left is the **prompt card** (the travelling subject), which grows block by block. On the right is a **Claude answer panel** with a quality meter (the recurring object, like v4's probability bars). The open loop: the hook shows 4 **ghost sockets** labelled TASK / CONTEXT / RULES / EXAMPLE, empty. Each section fills one socket as a live move (about 1.4 s), and the answer re-renders better while the meter rises. The ending pulls back to the full world. Colors: orange = the prompt blocks and emphasis, cyan = Claude's answers. One spotlight at a time.

**Project structure** (in our repo, e.g. `igotchu-test/v5-anatomy/`):
```
BRIEF.md  STORYBOARD.md  DESIGN.md (Neon tokens + meanings)  VERIFY.md
slides.json  timing.json  segments.json  answers.json   # real Claude answers, verbatim
make_vo.py  make_segments.py  make_extras.py            # reused from v4
build.py            # generator: writes video/index.html, video/compositions/*.html, video/assets/transcript.json
video/
  index.html        # root: <audio mix>, ambient-bg (track 0, full length), s01..s10 sub-comps, rail/progress
  compositions/ambient-bg.html  s01-hook.html ... s10-ask-first.html
  assets/ gsap.min.js CustomEase.min.js fonts/*.woff2 mix.mp3 transcript.json
```
Use ids `s01`...`s10`, never `sec-01`. Each composition gets `data-anchor="<first phrase>"`, local times from `cue() - T[n].start`, a `tl.set({}, {}, SLOT)` pin, and scoped CSS. The crossover keeps the 0.35 s overlap on alternating tracks.

**Suggested beats** (the user's script wins): 1 hook, a vague prompt and a bland answer, with the ghost sockets planted · 2 why it fails (the question card) · 3 TASK · 4 CONTEXT · 5 RULES · 6 EXAMPLE (each: the socket fills, the answer improves, the meter rises) · 7 first vs final prompt (versus/before-after) · 8 pull-back recap (layer stack plus the formula chip) · 9 the trick "ask me questions first" (prompt-bar typing, then Claude replies with questions) · 10 checklist recap, a teaser, and the `ig-signoff` end card held at least 5 s.

**Steps**
1. Get the script from the "igotchu Video Scripts" doc and split it into `slides.json`. Run the de-AI checklist; don't reword without a yes.
2. **Capture real Claude answers** for each prompt stage (vague, +Task, +Context, +Rules, +Example, ask-first). The user can run these in claude.ai. Calling the API from here costs money, so ask first. Store them verbatim in `answers.json`, trimmed only with visible "…".
3. Voice: one ElevenLabs clip per slide (the Johnson clone, eleven_v3, 3 concurrent), then `make_vo.py` (1.08× atempo, trim, -20 LUFS, pads) and `make_segments.py`.
4. Write `STORYBOARD.md`: a timing table plus per-beat blocks with the anchor phrase, the visual, the eases, the exit tween and its matching entry, and SFX. Show it to the user.
5. Build `ambient-bg` and **one section end to end first** (s03 TASK). Snapshot it, read contiguous strips, and fix the *system* before building the other nine.
6. Generate the rest. Port the kit layouts in Neon tokens where they help: the layers stack, the searchbar, versus/score, the formula chip, the correction strike.
7. Gates: `node <kit>/scripts/preflight.mjs video`, `npx hyperframes lint`, `node <kit>/scripts/validate-beat-sync.mjs video` (on the phrase-anchor transcript), our frozen-frame check, and `hyperframes snapshot` at 2-3 times per slide. Read every image, plus transition strips.
8. Draft render (`-q draft`). Extract hero and transition frames and read them. Listen at the slide joins.
9. Standard render (`-q standard -f 30 -w 4`), then SFX mix and the two-pass -14 LUFS master. Write `VERIFY.md`, the SRT and `youtube-extras.md`.

## (e) Blockers and environment findings

- **Node:** v22.22.2, which meets the kit's `>=22`. npm is 10.9.7.
- **npm ci / network:** registry.npmjs.org is reachable. `npm ci` from the kit's lockfile, run on a scratch copy, installed 141 packages in 15 s and gave hyperframes 0.7.109. (I didn't run it in the kit, since that would add `node_modules`.) `npm pack @fontsource/*` works for fonts.
- **Network: CDN and fonts:**
  - `cdn.jsdelivr.net` is blocked (403). All 406 cards and most examples load gsap from it, so localize gsap.
  - This session, `fonts.googleapis.com` and `fonts.gstatic.com` returned 200 through the proxy, and the 0.8.71 compiler fetched a font from Google Fonts during a snapshot. Don't rely on that: localize every font with `@fontsource` woff2. Cards' `tokens.css` `@import` lines need stripping.
  - `huggingface.co` is blocked, so there are no Whisper or Kokoro model downloads. **`hyperframes transcribe` and `hyperframes tts` are unusable here**, and no local Whisper is installed.
- **Word timestamps:** these are the one thing the kit assumes and we lack. Options:
  - Keep our free DP aligner.
  - Use ElevenLabs Scribe. It's paid, and last time 242 credits were estimated but 3,021 charged.
  - Ask for word timestamps from a TTS endpoint that returns alignment. The connector doesn't expose one.
- **HyperFrames versions:** I tested the kit example `linear-promo-30s` (gsap localized) under both versions with our headless_shell:
  - 0.8.71: lint 0 errors / 8 warnings (new `studio_missing_editable_id`, so give sub-comp divs an `id`); snapshot OK; sub-compositions render.
  - 0.7.109: lint 0 errors / 131 warnings; snapshot OK; draft render of 30 s took 3 m 42 s.
  - Kit files and scripts are version-agnostic, so **stay on 0.8.71**, our proven renderer.
  - Pass `--describe false` to snapshot, because it calls Gemini when `GEMINI_API_KEY` is set.
- **API keys:** the kit's `.env.example` lists ElevenLabs (Scribe), Kie.ai, OpenAI, Gemini, Groq and ClickUp. None of them is needed for our plan. The voice goes through the ElevenLabs connector as today. Kie.ai-style generated 3D assets (the look in the showcase reels) would cost credits, so ask first.
- **Kit gaps:**
  - `_preview/` holds only `contact-sheet.html`, which iframes the cards and needs jsdelivr. There are no images, and the preview mp4s are gitignored.
  - `youtube-showreel.mp4` is missing.
  - All cards are marked draft.
  - The beat-sync validator has the hyphen-id bug described above.
  - The kit's own docs contradict each other on the slot-pin tween and on exits.
