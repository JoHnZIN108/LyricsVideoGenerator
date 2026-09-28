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
RENDER_RESULTS

## Not checked
- No human listen yet: the voice is the user's clone (sample G) at 1.08×; pacing was only checked by the timing data.
- Captions (`captions.srt`) were checked for line length and slide boundaries, not watched against the video.
