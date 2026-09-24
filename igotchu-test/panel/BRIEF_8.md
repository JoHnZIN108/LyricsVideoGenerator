# Expert panel brief: igotchu, Script 3 v2 + video design

## The channel
- **What it is:** "igotchu" (youtube.com/@igotchu-bro) is a faceless voiceover YouTube channel that explains AI to beginners. It signs off with "I gotchu."
- **How the creator works:** they don't edit. Claude writes the script, ElevenLabs does the voice, and the video is built in code: HyperFrames, i.e. HTML + GSAP rendered frame by frame to MP4.
- **The target:** top-1% explainer quality that feels human, not AI-made.

## What you are judging
1. **The script:** `igotchu-test/panel/script3_v2.txt`, "It's autocomplete, but not the kind you think" (about 700 words, about 4:40).
   - This is the NEW script, not yet voiced or built.
   - Personal lines come from the creator's real life. Never invent personal experiences for the narrator; mark them [FILL] instead.
2. **The existing video (v3):** built from the OLD version of this script, `igotchu-test/v3/slides.json`. Its design, animation, timing and sound will be carried into the v2 build, so judge the craft.
   - Full render: `igotchu-test/v3/igotchu-script3-v3-full.mp4` (Neon theme, 220s). Instrument and Patent theme variants sit next to it.
   - 1-fps timestamped contact sheets, 20 seconds per sheet: `igotchu-test/panel/pack/strip-01.jpg` … `strip-12.jpg`. Read these images; they show the whole video.
   - 4-fps motion strips (5s each) for the hook, the phone scene, the morph card and the glass illustration: `igotchu-test/panel/pack/motion-*.jpg`.
   - Theme comparison snapshots: `igotchu-test/v3/snaps_instrument/contact-sheet.jpg` and `igotchu-test/v3/snaps_patent/contact-sheet.jpg`.
   - Build code: `igotchu-test/v3/build_v3.py`, covering scenes, GSAP helpers, eases, SFX cues and the phrase-to-timestamp aligner.
   - Timing: `igotchu-test/v3/timing.json` (slide start/duration).
   - Voiceover: `igotchu-test/panel/pack/voiceover.mp3`. You can't listen, but ffmpeg is installed (silencedetect, ebur128, astats), so measure it.
   - Final mix: `igotchu-test/v3/video/assets/mix.mp3`.
   - SFX recipes: `igotchu-test/v3/sfx/README.md`.
3. **The design system:** `igotchu-test/v3/ds/` (DESIGN.md, tokens.json, bundle.css, illustration-prompts.md).

## Context files
- `igotchu-test/panel/research.md` holds verified facts and sources for this script and the next one. The next script covers failure stories: lawyers, judges, Air Canada, and glue on pizza.
- `.claude/skills/youtube-video/SKILL.md` is the current production playbook, including a 12-rule "De-AI checklist".

## Constraints to respect
- **Tools:** HyperFrames/GSAP (transforms and opacity only; no CSS keyframes); ElevenLabs on a paid plan (voice, images about 185 credits each, SFX, music; video is expensive).
- **The creator is solo, often on a phone, and never edits.** Every recommendation must be something Claude can build in code or prompt.
- **Wording:** the creator approves script wording, so propose exact replacement lines rather than vague advice.

## How to work
1. **RESEARCH FIRST. This is required.** Before judging anything, use WebSearch/WebFetch to become the best possible judge in your area:
   - find what top creators and the best practitioners in your field actually do, with concrete sources, numbers and named examples;
   - aim for at least 5 good sources;
   - some sites (YouTube itself) may be blocked, so use articles, interviews, talks, papers and creator breakdowns.
2. **Then judge the materials against that research.** Look at the actual images and files; don't guess.
3. **Stay in your lane.** Go deep on your assigned expertise; others cover the rest.
4. **Write your full report** to `igotchu-test/panel/reviews/<your-slug>.md` with:
   - (a) research findings with source links;
   - (b) a score out of 10 for your area, with reasons;
   - (c) the TOP 5 changes, ranked by impact. Each must be specific: slide number or timestamp, the exact line or visual, and the exact fix (replacement wording, animation spec, timing value, etc.);
   - (d) what is already working and must be kept;
   - (e) one bold idea.
5. **Your final reply** (under 350 words) is a summary: score, top 5 changes (one line each), the keep list, and the bold idea.
6. **Do not** modify any existing files, commit, or call ElevenLabs/paid tools.
