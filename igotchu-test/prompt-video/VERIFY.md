# Ep 07 "Anatomy of a good prompt": verification

What was checked before the video went to the user, and what wasn't.

## Automated checks (all on the final build)
| Check | Command | Result |
|---|---|---|
| Kit preflight | `node <kit>/scripts/preflight.mjs video` | pass, 11 targets (root + world + s01..s10) |
| HyperFrames lint (0.8.71) | `npx hyperframes lint video` | 0 errors, 0 warnings |
| Kit beat sync | `node <kit>/scripts/validate-beat-sync.mjs video` | s01..s10 OK (each scene enters 0.17 to 0.93 s before its first word). `world` reports NO-ANCHOR by design: it's the persistent layer, not a beat. |
| Frozen frames | `build.py` report (no new motion for > 3.2 s) | only the end-card hold, 233.8 to 238.4 s |
| Audio | `mix.py` | 152 of 153 SFX events (1 dropped by the same-sound 0.3 s spacing rule); two-pass loudnorm to -14 LUFS / -1 dBTP |

## Screenshot and script match
The script's quoted answers were rewritten from the user's 5 real screenshots (approved; Claude Doc updated before the voice was recorded):
- Slide 2 "Thank you for the love, the patience…" = `screens/01.png` (signed "Johnson", kept at the user's request)
- Slide 4 NHS line = `02.png`
- Slide 5 "Thirty years of bossing doctors around…" = `03.png`
- Slide 6 "Tell Dad the fence…" and "Now you're stuck at home with Dad full time. Toughest shift yet." = `04.png`
- Slide 8 the five questions = `05.png`

Every read-along highlight is placed from Tesseract word boxes (`ocr/words.json`), so it sits on the words in the screenshot, and sweeps word by word between the voice cues for that phrase.

## Visual review
- Snapshots at 2 to 3 times per slide (`snaps2/`, 20 frames) plus spot checks (`snaps3/`, `snaps4/`): every frame was read.
- Fixed from those reviews: the key rack blowing up (press and pulse reset the layout transform), the slide 1 title over the keys, the slide 5 tags over the subtitle, the slide 6 subtitle over "An example beats a description", the slide 3 prompt wrapping, and the slide 6 zoom cutting off "home with" in the highlighted line.
- Known and accepted: the NO QUEENS stamp on slide 5 covers the end of the highlighted rules line after it has been read; the hand-drawn circles around "Dad" touch the neighbouring letters.

## Rendered file
- `igotchu-ep07-anatomy-full.mp4`: 1920x1080, 30 fps, 238.4 s (standard quality, 4 workers, about 6.5 min).
- `igotchu-ep07-anatomy.mp4` (sent to the user): x264 CRF 26 with the re-mastered mix, 20.8 MB, **-14.2 LUFS integrated, -3.9 dBTP** (the first render measured -15.2 LUFS; `mix.py` now limits before loudnorm).
- Transitions: 12-frame strips at 0.1 s across all 9 slide changes (`verify/trans-02.jpg` .. `trans-10.jpg`). Each old scene fades out and the new one slides in, with at most about 0.2 s where only the world layer (key rack, header, progress line) is on screen. That's never a blank frame.
- A 1-fps scan of the whole render found one real problem: slide 7 had an empty stage from 2:27 to 2:30 ("That's the real test of a good prompt"). A "The real test of a good prompt" chip now arrives on that phrase, and the question follows on "Could the answer…". Re-rendered and re-checked at 148.5 s and 151 s.
- Hero frames (`verify/hero.jpg`) are readable after compression.
- Still sparse but on-script: the first 5 s of slide 8 (heading only while "the trick I promised…" plays) and the first 2 s of slide 10.

## Not checked
- No human listen yet: the voice is the user's clone (sample G) at 1.08×; pacing was only checked by the timing data.
- Captions (`captions.srt`) were checked for line length and slide boundaries, not watched against the video.
