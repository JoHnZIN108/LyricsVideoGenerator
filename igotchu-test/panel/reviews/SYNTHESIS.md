# 8-expert panel synthesis: Script 3 v2 and the v3 video craft

| Expert | Score | Full report |
|---|---|---|
| Retention/packaging | 6 | retention.md |
| Scriptwriter | 7 | scriptwriter.md |
| Learning scientist | 6.5 | learning.md |
| Fact-checker | 7.5 | factcheck.md |
| Motion designer | 6 | motion.md |
| Art director | 5 | artdirector.md |
| Timing/sound editor | 5.5 | timing.md |
| Voice director | 6 | voice.md |

**Average: 6.2.** The script is the strongest part. The build craft (visuals, motion, timing) is where most of the gains are.

## Unanimous or near-unanimous findings

1. **Too long.** The script is about 880 spoken words, which runs about 5:20–5:30, not 4:40 (flagged by 5 of 8). Target about 720–760 words: cut the barista (learning), and tighten slides 3, 4, 6 and 8.
2. **Web search: "we'll get to it" is never paid off** (5 of 8). Replace it with: "If you see it searching the web and showing links, that's an extra step bolted on top. Different video."
3. **Dead air and frozen screens** (retention, motion, art, timing).
   - Every slide change has about 1 s of silence over a blank screen.
   - 43–47% of runtime has no visible change for 2.5–4 s or more.
   - Fixes:
     - the next scene starts before its first word;
     - nothing holds longer than 3 s;
     - a camera push you can actually see;
     - a build check that fails on frozen or empty stretches.
4. **Keep:** the mom-text hook and emoji flip, "It doesn't [look it up]", the prediction bars, the phone scene, the Ken Burns illustration recipe, "Autocomplete did that.", "not the kind you think", Jay/pasta, the Tidewater Dreams ending, the WRONG stamp, and the cue() word sync.
5. **Loudness is about 3.5 dB too quiet** (−17.4 LUFS). Master with a two-pass loudnorm to −14 LUFS / −1 dBTP. This is a free fix.
6. **End card:** use "makes things up" instead of "lies". Shorten the 8 s of silence and talk over the end screen.

## Fact fixes (must do)

- **Air Canada:** it was one airline, not "airlines".
- **Apple 34M:** say "when someone cracked open Apple's keyboard model".
- **IMO:** only DeepMind's result was certified by the IMO; OpenAI self-graded. Suggested line: "Google's scored exactly at the gold line, confirmed by the Olympiad's own graders."
- **"Fancy parrot":** attribute it to linguist Emily Bender.
- **Size comparison:** "likely thousands of times bigger, OpenAI doesn't say exactly."
- **Sydney/Canberra example:** retire it from visuals, because current ChatGPT gets it right.

## Big recommendations by area

- **Retention:** confirm the title's "write code" promise by 0:35, and pay off "code" in the Jay slide.
- **Learning:**
  - Add a one-line recap before the teaser: "It doesn't look things up. It guesses the next word, really, really well."
  - Use the prediction bars as the recurring visual (mom, Jay, rabbit, Tidewater).
  - Keep on-screen text to 2–4 word labels.
- **Art direction:**
  - Use a hybrid "Neon Instrument" theme: Neon's navy and color meanings with Instrument's type (Bricolage condensed, DM Sans, JetBrains Mono).
  - Use one illustration language, mostly code-built SVG. No brains, robots or 3D.
  - Remove the wordmark and corner marks. Keep text at 30 px minimum. Add a layout-overlap check.
- **Motion:**
  - Add a 12-move named vocabulary and two new eases (igIn, igSettle).
  - Use fewer overshoot pops.
  - Add parallax depth layers and a subtle handheld sway on phone/chat.
- **Timing and sound:**
  - Fix the silent whoosh (the bandpass needs `t=h`).
  - Drop the thud gain from .7 to .25.
  - Space SFX at least 0.3 s apart.
  - Add a music bed about 20 dB under the voice, with ducking.
  - Build designed 1.2–1.8 s pauses in code.
- **Voice:**
  - Stay on Marshel + multilingual v2 with tuned settings: stability .42, similarity .75, style .20, speed .96.
  - Use request stitching between clips.
  - Keep a TTS-spelling field so captions stay clean.
  - Add break tags before reveals.
  - eleven_v4 is not publicly released; the account is refused access.

## Disagreements

- **Barista:** learning says cut it. Art director keeps it as the one allowed AI image. Retention says trim it. **Lean: cut** (it helps the length).
- **Voice:** the voice director says stay on v2. The user asked for "more lifelike". **The user decides** from the A–E samples.
- **Title:** retention says keep it only if the code payoff ships; otherwise use "…So Why Is It This Smart?".

## Bold ideas worth doing

1. Cheap:
   - a "Beat the bars" guess-first game (learning);
   - a cursor mascot that types "I gotchu." (art);
   - a "Powers of Ten" zoom-out for the 34M line (motion);
   - a de-AI linter script run before any voice spend (scriptwriter).
2. Big: **performance transfer.** The creator records voice memos, and ElevenLabs speech-to-speech re-voices them as Marshel. This keeps real human timing (voice director).
