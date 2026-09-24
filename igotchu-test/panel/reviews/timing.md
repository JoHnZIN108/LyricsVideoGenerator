# Expert 7: Timing, pacing and sound design (slug: timing)

Reviewer lane: how often the picture changes, how the voiceover lines up with the visuals, pauses, cut rhythm, SFX, the music bed and loudness. Every number below was measured on the files with ffmpeg and numpy. Scratch measurements were run on a copy of `v3/` in the session scratchpad; no repo files were changed.

---

## (a) Research findings

| Topic | Finding | Source |
|---|---|---|
| Shot length / visual change | Average shot length in Hollywood films fell from 8–11 s in the 1930s to about 4.3–4.9 s by 2010. Films also got more motion inside shots. The study measured 160 films frame by frame with a "visual activity index". | Cutting et al., *Quicker, Faster, Darker*, i-Perception 2011: https://journals.sagepub.com/doi/10.1068/i0441aap ; https://pubmed.ncbi.nlm.nih.gov/23145246/ ; Cutting & Candan on shot durations: http://cutting.psych.cornell.edu/pubs/cutting&candanProj15.pdf |
| YouTube retention | Retention editors work to a rule of "some visual change every 3–5 s", with a bigger pattern interrupt around 25–35 s. MrBeast's leaked production guide says the first 60 s must be the most engaging part. In 2024 he publicly walked back hyper-fast cutting: he added breathers and his views went up. The takeaway is steady change, not frantic cutting. | https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8 ; https://www.washingtonpost.com/technology/2024/03/30/video-editing-mrbeast-retention/ |
| Cut rhythm | Walter Murch's Rule of Six ranks emotion (51%), story (23%) and rhythm (10%) above eye-trace. He treats editing as "visual music": the cut lands where the thought lands. | https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch ; https://www.studiobinder.com/blog/walter-murch-rule-of-six/ |
| J-cut / L-cut | In a J-cut the audio of the next shot starts before its picture (audio lead). In an L-cut the audio carries over the new picture. Editors use them to hide cuts and pull the viewer forward. For a code-built explainer: the next scene's first element should land on or just before the first syllable, and the old scene must never go blank before the new one starts. | https://en.wikipedia.org/wiki/J_cut ; https://filmdaft.com/the-l-cut-and-j-cut-how-film-editors-use-audio-to-control-time/ ; https://www.epidemicsound.com/blog/j-cuts-and-l-cuts/ |
| Explainer SFX | Soft whooshes on transitions and small pops when an element "lands" make motion feel intentional. Pro whooshes are layered: a broadband sweep plus low-end texture. | https://medium.com/@amir.otaifa/whoosh-the-importance-of-sound-design-in-animation-video-70393f012718 ; https://soundmorph.com/blogs/news/best-whoosh-sound-effects-for-film-trailers-and-ui-a-designer-s-guide ; https://www.motiontheagency.com/blog/sound-design-for-explainer-videos |
| Music under VO | WCAG 1.4.7 says background sound should be at least 20 dB below foreground speech, except for occasional sounds of 1–2 s. Creator guidance: music 18–24 dB under dialogue, duck amount 15–24 dB, attack 30–80 ms, release 250–700 ms. | https://www.w3.org/WAI/WCAG22/Understanding/low-or-no-background-audio.html ; https://pureaudioinsight.com/blogs/content-production/background-music-volume-how-loud-should-it-be ; https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video |
| YouTube loudness | YouTube turns content louder than about -14 LUFS down to -14. It does **not** turn quieter content up. Stats for Nerds shows "content loudness"; a negative value means the video plays quieter than its peers. | https://productionadvice.co.uk/stats-for-nerds/ ; https://youlean.co/how-to-edit-a-video-to-achieve-good-audio-loudness-on-youtube/ |
| Narration rate | Guo, Kim & Rubin (6.9M edX sessions) found that fast, enthusiastic speakers are *more* engaging; instructors shouldn't slow down on purpose. E-learning voice actors typically work at about 130–150 wpm. Measured YouTube speech runs about 170–180 wpm. Above about 160 wpm, dense content gets harder to follow unless pauses give it room. | https://dl.acm.org/doi/10.1145/2556325.2566239 (PDF: https://www.cs.rochester.edu/hci/pubs/pdfs/edX-MOOC-video-production-and-engagement_LAS-2014.pdf) ; https://kimhandysidesvoiceover.com/2022/08/16/timing-in-elearning-videos/ ; https://prepublish.ai/blog/youtube-script-length-word-count |

**What I apply below:** a visual change every 2.5–3.5 s and **never more than 4 s** without one. The first 30 s gets the densest change. The voice rate stays at about 160–170 wpm, the voice's natural rate, with pauses set on purpose rather than slowing the delivery. A music bed sits 20 dB under the VO. The master goes to -14 LUFS integrated with a true peak of -1 dBTP.

---

## Measurements (v3)

### Loudness (ebur128)
| File | Integrated | LRA | True peak |
|---|---|---|---|
| `panel/pack/voiceover.mp3` (213.5 s) | -18.4 LUFS | 4.6 LU | -1.7 dBFS |
| `v3/video/assets/mix.mp3` (221.8 s) | **-17.4 LUFS** | 4.4 LU | -4.7 dBFS |
| `v3/igotchu-script3-v3-full.mp4` audio | **-17.5 LUFS** | 4.4 LU | |

The build asks for `loudnorm=I=-16`, but the single-pass dynamic mode lands at -17.4. On YouTube the video will play **3.4–3.5 dB quieter** than normalized channels, because YouTube never raises quiet content. There is also 3 dB of unused true-peak headroom.

### Pauses (silencedetect, -35 dB, ≥0.3 s) on the VO
- 66 pauses, 38.1 s in total, mean 0.58 s, max 1.37 s.
- The pauses are **metronomic**: 43 of 66 are 0.3–0.5 s, and every slide boundary is 0.95–1.37 s (0:21.7, 0:37.3, 1:01.4, 1:21.1, 1:39.6, 2:00.2, 2:32.8, 2:55.3, 3:22.3). There are only 2 deliberate in-slide beats: 0:41.1 (1.37 s, "The capital of France is…") and 2:12.4 (1.0 s).
- **Rushed game beat:** the pause after "Peanut butter and…" is only **0.30 s** (0:28.3 to 0:28.6). The viewer is told to "finish this sentence in your head" and gets no time to do it. The same "…" gave 1.37 s on France, so ElevenLabs is inconsistent with ellipses.
- End: **8.3 s of dead silence** after "I gotchu" (3:33.4–3:41.8).

### Words per minute (slides.json words ÷ timing.json speech)
575 words in 204.8 s of speech = **168 wpm** (156 wpm over the full 220.8 s).

| Slide | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| wpm | 151 | 171 | 138 | **209** | 144 | 178 | 187 | 155 | 167 | **198** |

Slide 4 (phone demo, 1:02–1:22) and slide 10 (the sign-off, 3:23–3:33) are the rushed ones.

### Visual change (4 fps, 160×90, a "change moment" = more than 0.4% of pixels shift by more than 30 levels; checked against the strips)
- 67 change moments, 18.2 per minute, mean interval 3.29 s. The average is fine; the distribution is not.
- **17 stretches of 4 s or more with no meaningful change, totalling about 103 s, or 47% of the runtime.** The camera push alone doesn't count; at 3.5% over a slide it can't be seen.

| Stretch | Length | What's on screen / VO |
|---|---|---|
| **0:08.0–0:18.0** | **10.0 s** | Hook: the chat card is finished and frozen. VO: "By the end of this video you'll understand…" |
| **2:01.75–2:11.0** | **9.25 s** | Glass/brain illustration, static. VO: "To guess the next word really, really well…" |
| **2:35.25–2:43.75** | **8.5 s** | "Taught manners" illustration, static. |
| **0:42.75–0:50.75** | **8.0 s** | "Paris" filled in, nothing moves. VO: "That is basically the whole trick…" |
| 2:57.0–3:03.75 | 6.75 s | "Guessing ≠ Knowing" title card |
| 1:30.25–1:36.5 | 6.25 s | Scale diagram |
| 3:07.75–3:13.75 | 6.0 s | Venn diagram |
| **0:22.75–0:28.5** | 5.75 s | **Almost empty screen** (only the small kicker "FINISH THE SENTENCE…" is visible; content under 0.3% of pixels). VO: "Let's play a game." |
| 2:28.25–2:33.75, 1:49.75–1:54.75, 0:31.25–0:36.25, 3:26.75–3:31.75, 2:47.5–2:52.25, 1:22–1:26.5, 0:57.75–1:02.25, 1:40.75–1:44.75, 1:03–1:07.25 | 4–5.5 s each | |

- **Blank frames at every cut:** every slide opens on an empty background for about 0.5 s (1.25 s at 1:21.9, and about 6 s of near-empty screen at 0:22.3). This happens at the same moment as the 1.0–1.37 s silence, so each of the 9 boundaries is a dead beat for both eye and ear, the opposite of a J-cut.
- **Sync is good where it's cued.** "Paris" lands at 0:42.55, VO onset 0:42.46 (+0.09 s). "jelly" lands at 0:30.85, VO at about 0:30.66 (+0.2 s). The `cue()` aligner works; keep it.

### SFX (events extracted from build_v3.py; 79 events)
- Counts: pop 36, click 28, whoosh 9, ding 4, thud 2. Without the diegetic phone clicks that is 51 accents, or 13.9 per minute.
- **BUG: the whoosh is inaudible.** `whoosh.wav` peaks at **-56 dBFS** (RMS -67), and with gain .35 it sits about 58 dB under the voice. The cause is that `bandpass=f=1400:w=1800` defaults `width_type` to Q, so it is a Q=1800 needle filter. `bandpass=f=1400:t=h:w=1800` gives a -18 dBFS peak (verified). All 9 scene-transition whooshes are currently silent.
- **Thud is too loud:** at gain .7 its RMS is **+1.0 dB above the voice's speech RMS** (peak -3.6 dBFS). It fires at 1:18.1 ("It's nonsense") and 3:20.4 (the stamp). Pop sits at -11.5 dB and ding at -14.4 dB relative to the voice, which is fine.
- **Clusters:** 4 pops inside 0.4 s at 0:50.9–0:51.3, 3 pops inside 0.3 s at 2:15.9–2:16.2, and 3 pops inside 0.3 s at 3:33.1–3:33.4. The 0.09 s same-sound thinning is too short, so these smear into a rattle. There are 12 clicks in 1.2 s at 1:10.0–1:11.2 (phone typing, which is diegetic and OK).
- **Deserts:** 0:01.2–0:22.1 (21 s, the whole hook, only 2 pops even though 5 predictor words lock in), 1:40.1–1:59.1 (19 s, into the "It's actually wild" turn with no riser), and 2:56.2–3:11.6 (15 s).
- **No music bed.**

---

## (b) Score: **5.5 / 10**

What's good: a solid 168 wpm voice, sample-accurate phrase sync, a sensible SFX vocabulary with sane pop/ding levels, and 18 change moments per minute on average. What costs points: nearly half the runtime sits in stretches of 4 s or more with no change, including a 10 s freeze inside the first 20 s. Every slide boundary is a double dead beat (blank screen plus 1–1.4 s of silence). The transition sound is literally silent from a filter bug, the thud is louder than the voice, and the master is 3.5 dB under YouTube's reference. The v2 script is also not the length its header claims (see Change 1).

---

## (c) Top 5 changes, ranked by impact

### 1. Fix the length/pace budget for v2 before voicing
`script3_v2.txt` claims "about 700 words, around 4:40". The narration measures **879 words** (wc on the spoken lines; a regex count gives 885). At this voice's measured 168 wpm that is 5:14 of speech, plus about 9 s of boundaries and a 7 s end hold, so **about 5:30**. Hitting 4:40 with 879 words would need 200+ wpm, which is the pace that already rushed slide 4.
- **Target:** 160–170 wpm clip rate; **700–720 words**; 4:35–4:45 total.
- **Word budget per slide** (current, then target): S1 72→65 · S2 49→45 · S3 102→85 · S4 109→90 · S5 80→65 · S6 **136→100** · S7 65→60 · S8 **127→95** · S9 70→55 · S10 75→50. The exact cuts belong to the scriptwriter; the budget is the timing constraint.
- Or, if the creator wants every line: keep 879 words and title it a 5:30 video. **Do not** speed up ElevenLabs to fit.

### 2. Design the pauses in code, in three tiers, and kill the dead beat at every cut
- **Split any clip that has an engineered pause into sub-clips** and insert exact silence with ffmpeg (`apad`/`anullsrc` concat). Don't rely on "…" or `<break>`: the v3 "…" produced 0.30 s in one place and 1.37 s in another.
- Tiers: comma 0.25 s (leave to TTS) · sentence 0.4–0.5 s (TTS) · **beat 1.2–1.8 s, used about 6 times only**. For v2 the beats go here:
  - After "No emoji, no 'love you', just that." → **1.2 s** (the lock screen sits there; the viewer's brain "writes the next five minutes").
  - After "Whole different story, right?" → **0.8 s**, then "Nobody's sick. Somebody's engaged." (the emoji flips on the first word).
  - After "…keep tapping the middle suggestion." → **1.5 s** with a 3-2-1 ring on "PAUSE AND TRY IT".
  - After "…Autocomplete did that." → **1.2 s**.
  - After "So it was..." → **1.5 s**, with a caret blinking 3 times (0.5 s steps), then "You said Jay."
  - After "It doesn't exist." → **1.4 s**, before "Next video:".
- **Slide boundaries:** cut the pad from 0.35 s lead + 0.55 s tail (0.9 s, measured 1.0–1.37 s) to **0.15 + 0.30 = 0.45 s**. The exception is one act break of 1.0 s, before SLIDE 6 ("So how does autocomplete write working code?"). That saves about 5 s.
- **J-cut every scene:** the new scene's first element must be at full opacity by `start + 0.10 s`, i.e. before the first syllable at `start + LEAD`. The old scene holds (L-cut) until the new one covers it, crossfading over 0.25 s. The screen is never empty.

### 3. Hard rule: no stretch over 4 s without a visual change (lint it in build_v3.py)
Add a check after the timeline is built: sort all tween start times, and `assert` that every gap is ≤ 4.0 s (≤ 3.0 s for t < 30 s). Fill each gap with a *meaningful* micro-beat tied to a spoken word via `cue()`: an underline draw, a word highlight, a counter tick, or a 1.03× punch-in. A blanket loop won't do. Worst offenders, carried into v2's equivalent scenes:
- **0:08–0:18 (hook, 10 s):** v2's hook is the Mom lock screen. Plan it at a change every ~2 s: text arrives (with buzz) 0.0 → preview expands 1.8 → "No emoji" strike-through on the empty emoji slot, cued to "No emoji" → "love you" ghost appears and gets crossed out, cued to "no 'love you'" → the screen dims and 3 thought bubbles pop in turn on "Somebody's sick" / "forgot a birthday" / "the next five minutes" → the ChatGPT logo/cursor morph on "how ChatGPT works". That is 7 changes in about 20 s.
- **Static illustrations at 2:01–2:11 and 2:35–2:44 (8.5–9.25 s):** never hold a still image for more than 3 s. Enter it with a scale 1.08→1.0 over 0.8 s, then cut to a 1.35× crop of a detail after 3 s (a "second shot" of the same art), and pull back on the next cued phrase. In v2 this applies to the barista (SLIDE 5) and the rabbit (SLIDE 8) scenes.
- **Held answer cards (0:42–0:50 type, 8 s):** after the reveal, start the next idea's visual on the next sentence. Don't let the answer sit through the explanation.

### 4. Fix the SFX layer: one bug, one gain, spacing, and three missing sounds
- **Whoosh bug** (`v3/sfx/README.md` recipe, and the file): `bandpass=f=1400:w=1800` → **`bandpass=f=1400:t=h:w=1800`**, then gain `whoosh .35 → .30`. That puts it about 20 dB under the voice. Also shorten it: `d=0.35`, `afade=t=in:d=0.22,afade=t=out:st=0.22:d=0.13`. Put the peak on the cut: `SFX.append((s["start"] - 0.22, "whoosh"))`.
- **Thud gain `.7 → .25`** (-9 dB; puts its RMS about 8 dB under the voice). Keep it to 2 uses in v2 at most: the "It doesn't exist" stamp, plus one other.
- **Same-sound spacing `0.09 → 0.30 s`** in the mixer loop, and **cap staggered groups**: a `pop()` inside a stagger of 3 or more sounds only on the first and last item (`sound=(i in (0, n-1))`).
- **Add a "tick"** (a softer click at gain .12, `highpass=f=3000`, d=0.02) to every `predictor_steps` lock (`t + gap*0.62`). This fills the silent 21 s hook and v2's SLIDE 3 chunk loop, rising naturally as the gaps shrink.
- **Add a "riser"**, 1.6 s, free: `ffmpeg -f lavfi -i "anoisesrc=d=1.6:c=pink:a=0.5" -af "highpass=f=400,lowpass=f=6000,volume='min(1,t/1.6)':eval=frame,afade=t=out:st=1.5:d=0.1" -ac 1 riser.wav`, gain .25. Use it **twice only**: ending exactly on "Autocomplete did that." (SLIDE 6) and on "rabbit" lighting up (SLIDE 8).
- **Budget for v2:** 10–14 non-diegetic accents per minute, no accent within 0.3 s of another, and none on a word the voice is stressing (sound on the visual, not on top of the key syllable).
- **Phone buzz for v2's hook:** a 2× 90 ms burst of 150 Hz sine (`aevalsrc='0.5*sin(2*PI*150*t)*(lt(mod(t,0.2),0.09))':d=0.4`), gain .3, on the lock-screen text arrival at 0.0 s. It's the first sound of the video and puts the viewer in the scene.

### 5. Add a music bed, ducked 20 dB under the voice, and master to -14 LUFS
- **Yes to a bed.** Right now the mix is voice plus clicks over digital silence, which reads as "AI-made" (and 8.3 s of pure silence on the end screen). Use an instrumental lo-fi or soft synth-pluck track at 85–95 BPM, with no vocals and sparse mids. A free YouTube Audio Library track works, or ElevenLabs Music (about 900 credits).
- **Levels:** with the VO master at -14 LUFS, the bed sits at **-34 LUFS short-term under speech (-20 dB, WCAG 1.4.7)**. It swells to **-26 LUFS in pauses of 1 s or more and on the end card**. Duck: attack 60 ms, release 450 ms. Implement it deterministically from `segments.json` (a volume envelope built from the speech intervals) or with `sidechaincompress=threshold=0.02:ratio=10:attack=60:release=450:makeup=1`. Fade the bed in over the first 2 s and out over the last 3 s.
- **Master:** replace the single-pass `loudnorm=I=-16:TP=-1.5:LRA=11` with **two-pass `loudnorm=I=-14:TP=-1.0:LRA=7:linear=true`**, feeding in the measured values from pass 1. That turns the video up 3.5 dB relative to today, and YouTube will then play it at the same level as the competition.
- **End hold:** keep 7 s for end-screen elements, but let the bed carry it (it rises to -22 LUFS and resolves), rather than ending on silence.

---

## (d) Keep these
- **The `cue()` phrase-to-timestamp aligner.** Measured sync is +0.1 to +0.2 s visual-after-voice, which is exactly right.
- **The accelerating predictor loop** (`gaps3 = [0.9 … 0.22]`). It's a real rhythmic idea: the visual speeds up as the concept ("again and again") does. Reuse it for v2's SLIDE 3 chunk loop.
- **Phone keyboard clicks synced to each tapped word** (1:10–1:17): diegetic sound done right. Reuse for v2's SLIDE 4.
- **Pop and ding levels** (-11.5 and -14 dB relative to the voice), the `land()` pop-then-ding grammar and the 1.37 s France pause, which shows what a beat should feel like.
- **The voice's natural rate of about 165 wpm.** Don't slow it; control the pauses instead (Guo et al.).
- **The slow camera push**: it's subtle, but it keeps frames from being dead still. It just isn't enough on its own.

---

## (e) Bold idea: a beat-quantized timeline
The whole video is code, so snap the edit to the music the way a human editor cuts on the beat. Pick a 90 BPM bed (beat = 0.667 s). After the voice clips are laid out, the build **quantizes every slide start to the nearest downbeat** by adjusting each boundary pad within 0.30–0.80 s. The whoosh peak and the new scene's first element then land exactly on beat 1. Two more rules:

1. **Music drop-outs as pattern interrupts:** at the 3 biggest reveals ("Somebody's engaged.", "Autocomplete did that.", "It doesn't exist."), the bed cuts to silence **one beat before** the line and comes back on the next downbeat, with the visual reveal on that same downbeat. That is 3 attention resets at about 0:25, 2:25 and 4:20, which matches the 25–35 s interrupt guidance for the first one.
2. **Tempo-matched animation:** tween durations in each scene default to multiples of half a beat (0.333 s), so pops and slides "groove" with the bed.

About 40 lines of Python: read the BPM, compute the grid, nudge `timing.json`, and cut the bed's volume envelope. No editing by the creator, and it's the single biggest step from "generated" toward "edited by a person who cares".
