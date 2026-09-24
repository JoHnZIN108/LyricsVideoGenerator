# Expert 8: Voice director / AI voice producer (slug: voice)

Scope: the ElevenLabs narration. That covers the model and settings, voice choice, delivery, pacing, pauses, emphasis, text written for TTS, and voice loudness. Script wording is included only where TTS will mis-read it.

---

## (a) Research findings

Note: the network proxy blocked direct fetches of elevenlabs.io, help.elevenlabs.io and most third-party sites. The findings below come from search-result extracts of those pages. I have marked each point that needs a live check in the connector.

### Models (as of Sept 2026)
- **Current production TTS models:** `eleven_multilingual_v2`, `eleven_v3`, `eleven_flash_v2_5` and turbo. ElevenLabs presents Multilingual v2 as its most stable long-form model. Flash and Turbo are built for low latency and are half price, but they are less expressive; they are the wrong tool for narration. [Models docs](https://elevenlabs.io/docs/overview/models), [webfuse cheat sheet](https://www.webfuse.com/elevenlabs-cheat-sheet), [BIGVU pricing](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/). v3 and Multilingual v2 both cost $0.10 per 1k characters on the API.
- **Eleven v4:** I found no public general release. ElevenLabs showed a preview at its Warsaw summit ("This model has not been released yet. This is an exclusive showcase."), pitched as speaking "with emotion, intent, and accent", and trackers expect it in H2 2026. [xyz.pl report](https://xyz.pl/poland-unpacked/elevenlabs-wants-ai-to-sound-human-its-next-model-can-whisper-sing-and-sell-1121/), [SkillBoss tracker](https://www.skillboss.co/upcoming-models/elevenlabs-v4). The connector showed `eleven_v4` as locked on the free plan, so it may be in early access for paid tiers. **Treat it as an A/B candidate, not the default, until it wins a blind test.**
- **Eleven v3:** most expressive. It has audio tags and a three-position stability control: Creative (emotional, but prone to hallucination), Natural (closest to the source voice) and Robust (steady, like v2, and less responsive to tags). It does **not** support SSML `<break>` (use `[pause]`, `[short pause]` and `[long pause]` instead), speaker boost, or **request stitching**. [Artlist v3 guide](https://help.artlist.io/hc/en-us/articles/33143492937757-Elevenlabs-Eleven-v3), [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices), [stitching docs](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching).
- **Request stitching** works on v2, not v3. You pass `previous_text`/`next_text`, or up to 3 `previous_request_ids`, and the next clip keeps the prosody of the previous one. It is built for scripts split into several calls, which is exactly our one-clip-per-slide pipeline. `next_request_ids` lets you regenerate a single middle clip without breaking the flow. [ElevenLabs blog](https://elevenlabs.io/blog/request-stitching-for-text-to-speech-api), [docs](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching).

### Voice settings
- **Stability:** lower values give more emotional range but more randomness; higher values sound monotone. For long narration the advice is about 35–45%, and never below 30%. **Similarity:** at most about 75–80%, because higher values reproduce artifacts. **Style exaggeration:** 0 is flat; 30–60 adds expressiveness; above 75 becomes unstable or over-acted. It also slightly reduces stability. **Speaker boost:** a subtle similarity gain; not available on v3. **Speed:** 0.7–1.2. [Voice settings docs](https://elevenlabs.io/docs/api-reference/voices/settings/get), [ZyncAI guide](https://zyncai.com/elevenlabs-voice-control-guide/), [NeuraPulse 2026 settings](https://neuraplus-ai.github.io/blog/best-settings-for-elevenlabs-ai-voice-quality-improvement-2026.html), [aivoicelab emphasis guide](https://aivoicelab.com/blog/how-to-emphasize-in-elevenlabs-tts).

### Pauses, normalization, pronunciation
- On v2 and Flash, `<break time="x.xs" />` is the most consistent way to add a pause, up to 3 s. The model performs it as a natural pause rather than pasted-in silence. **Too many breaks in one generation causes speed-ups and artifacts.** Dashes give short pauses and ellipses give slow, "dramatic" ones. [How can I add pauses](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-add-pauses).
- ElevenLabs recommends **writing numbers and symbols out as words**, because digits are ambiguous. Normalization is on by default (`apply_text_normalization`), but it guesses. [Best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices), [numbers/acronyms help](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/why-are-numbers-dates-symbols-and-acronyms-not-properly-pronounced-or-spoken-in-the-correct-language).
- Pronunciation dictionaries: **alias** rules work on every model, but **phoneme** rules work only on Flash v2 and v3, **not on Multilingual v2**. So on v2 you fix names with alias spellings. [Pronunciation dictionaries](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries).
- Emphasis on v2 comes from capitals, dashes and respelling, and it is unreliable. Sentence structure is the dependable lever. [aivoicelab](https://aivoicelab.com/blog/how-to-emphasize-in-elevenlabs-tts), [blipcut](https://videotranslator.blipcut.com/ai-voice-tips/how-to-emphasize-in-elevenlabs.html).

### Voice design and voice choice
- **Voice Design v3 prompts:** describe age, gender, accent, tone, pacing, emotion and audio quality. The suggested structure is "Native <Language>. <Gender>, <Age>. <Quality>. Persona: <2–5 words>. Emotion: <2–3 adjectives>." Don't write "accent" when you mean intonation, because it triggers dialect shifts. Avoid FX words ("reverb", "phone", "tape"). [Voice Design docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-design), [Voice Design v3 blog](https://elevenlabs.io/blog/voice-design-v3), [prompting guide](https://elevenlabsmagazine.com/elevenlabs-voice-design-guide-2026/).
- **Faceless-channel practice:** pick one voice and keep it on every video, because consistency beats the "best" voice. Top creators do not ship raw narration: they fix pacing, regenerate awkward lines, and layer quiet music under it. [ElevenLabs faceless guide](https://elevenlabs.io/blog/how-to-create-a-faceless-youtube-channel), [fluxnote 2026](https://fluxnote.io/guides/elevenlabs-youtube-voiceover-2026), [thoughtcanopy](https://thoughtcanopy.com/the-secret-weapon-for-faceless-channels-elevenlabs-voiceovers/).
- **Voice type for tech explainers:** the defaults (Adam, the deep authoritative one) are "the AI tech channel voice", which is exactly the tell to avoid. The warmer "knowledgeable peer" voices are recommended for approachable content. [Nerdynav tested review](https://nerdynav.com/elevenlabs-review/), [aivoicereview](https://aivoicereview.com/blog/best-elevenlabs-voices-2026), [cognitivefuture](https://cognitivefuture.ai/best-elevenlabs-voices/).
- **Pace:** YouTube explainers sit at 140–160 WPM. Technical beats land best at 120–140 WPM; story and aside beats can run at 170+. [goteleprompter](https://goteleprompter.com/blog/words-per-minute-speaking-rate-guide/), [Bunny Studio](https://bunnystudio.com/blog/voiceover-words-per-minute-choosing-the-ideal-information-rate/), [breadnbeyond](https://breadnbeyond.com/explainer-video/how-many-words-does-a-60-seconds-explainer-video-needs/).

### Measurements of the current voiceover (`panel/pack/voiceover.mp3`, v3 build, Marshel on multilingual_v2)

| Metric | Value | Read |
|---|---|---|
| Duration | 213.5 s, of which 204.8 s is speech across 10 clips | |
| Overall pace | 575 words in 204.8 s = **168 WPM** | Top of the explainer range |
| Per-slide WPM | 151, 171, 138, **209**, 144, 178, **187**, 155, 167, **198** | Swings are driven by text density, not by intent. The fastest slides (4: phone babble, 7: the dense reasoning slide, 10: the payoff) are where you want the *slowest* delivery |
| Pauses inside slides (-35 dB, ≥80 ms, n=134) | median **0.24 s**, p75 0.37 s, p90 0.50 s | Only **21 pauses over 0.6 s**, and nearly all sit on a paragraph break (`\n\n`) or a slide join. Nothing is placed before a reveal |
| Pitch (autocorrelation F0) | median 99 Hz (p10 85, p90 121), SD 2.5 semitones, p5–p95 range 7.9 st | Lively enough for TTS, but **every slide sits in the same band**: medians 96–105 Hz and SD 2.1–2.6 st on 9 of 10 slides (slide 6 is 3.4). It sounds like the "same energy every slide" |
| Voice-track loudness | −18.4 LUFS, LRA 4.6 LU, true peak −1.7 dBTP | LRA is healthy for speech |
| Raw per-slide clips | −25.8 to **−29.1** LUFS (s07 is 3.3 LU quieter than s10) | Clips are joined before one global loudnorm, so slide 7 stays quieter |
| Final mix / rendered MP4 | **−17.4 / −17.5 LUFS**, peak −4.4 dBFS | `build_v3.py:1040` asks for −16, but single-pass loudnorm undershoots. YouTube normalizes *down* to about −14 and never up, so this plays about 3.5 dB quieter than neighbouring videos |
| A/B files | A (v2) LRA 2.0 LU; B (v3 with tags) LRA 8.3 LU and 74% longer | Confirms the creator's ear: v3 with tags roughly quadrupled the dynamic swing ("overdone") |

**Length warning for v2:** the new script has **885 spoken words**, not about 700 (per slide: 72, 49, 102, 109, 80, 136, 65, 127, 70, 75). At the current 168 WPM that is about 5:16 of speech, or about 5:30 with pads and the end hold, not 4:40. Don't close the gap with voice speed; trim the text instead (that is the script panel's call).

---

## (b) Score: 6/10 (voice and delivery)

- **Good (+):** Marshel is a warm, casual, mid-low voice, not the overused "Adam" narrator. Choosing v2 over tag-driven v3 was the right call. The average pace is in range. Speech LRA of 4.5 LU is natural. Cutting one clip per slide gives exact timing.
- **Weak (−):** No pauses are designed; the pause map just mirrors the paragraph breaks. The delivery is the same on every slide (it is flat from slide to slide, not within a slide). The densest and most important slides run fastest (187–209 WPM). There is no stitching between clips, so every slide "starts over". The final loudness is 3.5 dB under the YouTube reference and clip levels are uneven. The new script has about 15 lines TTS will mis-read or flatten.

---

## (c) Top 5 changes, ranked by impact

### 1. Model, settings and stitching (the whole voice)
- **Model:** `eleven_multilingual_v2`, voice Marshel (`cQYsRVGKMkDmd67zTppv`). Keep it for channel consistency.
- **Settings:** `stability 0.42`, `similarity_boost 0.75`, `style 0.20`, `use_speaker_boost true`, `speed 0.96`. Use speed 0.92 on slides 3 and 8, the dense explain slides.
  - Why: a stability of about 0.4 is the long-form sweet spot. Style 0.2 adds colour without the v3 "acting". Speed 0.96 pulls 168 WPM down to about 160.
- **Request stitching:** pass `previous_text` (the previous slide's full text) and `next_text` (the next slide's first sentence) on every clip. If one clip is regenerated, pass `next_request_ids` for its neighbour.
  - If the connector's `creative_generate_speech` doesn't expose these (check `creative_get_model_schema`), call the REST endpoint once per slide with the paid key. That is still code-only, so nobody edits.
- **Takes:** on the paid plan, use `generations_count: 2` for slides 1, 6, 8 and 10. Pick the take with the wider F0 range (compute it as above) whose WPM is closest to target.
- **v3 and v4 A/B:** run slides 1 and 8 on `eleven_v3` with stability **Natural**, **zero tags** and punctuation only. The "overdone" sound came from the tags, not the model. If the connector now offers `eleven_v4`, run the same two slides on it with no tags.
  - Ship the challenger only if the creator picks it blind.
  - Note that v3 loses `<break>` and stitching.

### 2. TTS-ready spelling of about 15 lines
The full table is below under "Exact lines". These are the highest-risk ones:
- "7am" (twice)
- "In 2025" (×3)
- Isabel **Allende** (v2 is likely to say "a-LEND-ee")
- the scare-quoted "word"
- the parenthetical "(Unless you see it searching…)"
- `type "I'm going to" and keep tapping`, which is ambiguous by ear
- the Hinton quote
- the `"...asking for my picky five-year-old. Edit: thanks everyone!"` forum quote
- "I gotchu", which must match past videos

### 3. Designed pauses: 7 breaks and 1 held silence
On v2, insert `<break time="…" />` at these points. Use at most 2 per clip to avoid the instability the docs warn about.

| Slide | Where | Break |
|---|---|---|
| 1 | after `…just that.` | 0.8 s |
| 2 | after `Whole different story, right?` | 0.6 s |
| 2 | after `Nobody's sick.` | 0.4 s, before `Somebody's engaged.` |
| 4 | after `keep tapping the middle suggestion.` | **no TTS break**. Add **2.5 s of silence in `timing.json`** for the "PAUSE AND TRY IT" card; build it as a pad, not TTS |
| 6 | after `Autocomplete did that.` | 0.8 s |
| 6 | after `At the basic level, yes.` | 0.5 s |
| 7 | after `…So it was…` | 1.2 s, before `You said Jay.` |
| 10 | after `It sounds exactly like a book she'd write.` | 0.9 s, before `It doesn't exist.` |

### 4. Loudness: fix the level players actually hear
- In `build_v3.py`, normalize each `s0N.mp3` clip to −20 LUFS (two-pass loudnorm) **before** joining. That removes the 3.3 LU clip spread.
- Then run **two-pass** loudnorm on the final mix: `I=-14:TP=-1.0:LRA=7`, feeding pass 1's `measured_I/TP/LRA/thresh` into pass 2 with `linear=true`.
- Target −14 LUFS ±0.5. The current −17.5 LUFS plays about 3.5 dB quieter than the channel's competitors.
- Duck the music and SFX 4–6 dB under the voice.

### 5. Pace follows meaning: slow the reveals, allow speed on the asides
- **Target WPM by slide:**
  - 150–158: slides 3, 7 and 8 (the explanations).
  - 165–175: slides 4, 5 and 6 (the stories and asides).
  - About 150 with breaks: slides 1, 2 and 10.
- Before joining, verify with `words ÷ speech-seconds` per clip. If a clip comes out above 180 WPM, regenerate it at speed −0.04.
- In the text, break any sentence over 28 words into two. The model rushes long sentences, which is why the old slides 4 and 7 ran at 187–209 WPM.
- **Over 28 words in the v2 script:**
  - slide 4: the 32-word babble quote (intended, so keep it fast);
  - slide 5: "Picture a barista…" (30);
  - slide 8: "Before it wrote a single word…" (30) and "Geoffrey Hinton…" (38);
  - slide 9: the 30-word "So the companies train it again…".

---

## Per-slide delivery direction (the director's notes)

| Slide | Energy / intent | Speed | Notes |
|---|---|---|---|
| 1 Mom text | Low, intimate, a little ominous: a friend leaning in | 0.94 | Say the quoted text flatter than the narration. Break after "just that." Let "Somebody's sick, or you forgot a birthday." run quick and anxious. "Hold on to that feeling" lands slower |
| 2 Party emoji | Relief, then a grin | 0.98 | "Whole different story, right?" is a real question and needs a rise. "Nobody's sick. Somebody's engaged." is two beats. The last sentence is the thesis, so it should be slow and plain |
| 3 Chunk loop | Myth-bust, confident, unhurried | 0.92 | "It doesn't." is short and falling. Make the web-search aside a quick throwaway at lower level (see the rewrite). "you're literally watching it happen" gets a small smile |
| 4 Phone | Playful, conspiratorial, fastest slide | 1.0 | Read the babble quote deadpan and fast with no internal pauses; the comedy is the run-on. Say "I genuinely need to know." dry. Then drop the energy for "and that's where it gets weird." |
| 5 Barista | Storyteller, warm | 0.96 | "Some days you wanted tea." is a small deflating joke, so give it a beat before. "really, really good" should be two distinct stresses |
| 6 Code / IMO | Personal, then building to awe, then settling | 0.96 → 0.92 at the end | "Then it got big." is the turn. "Plenty of kids still beat it, but come on." should sound incredulous. The ending "It is autocomplete. It's just not the kind you think." is the title line: slowest delivery in the video, with a break before it |
| 7 Jay | Game-host, then detective | 0.95 | Read the quoted clue as a separate "text" voice (split it into its own sentences). 1.2 s break, then "You said Jay." with a knowing smile |
| 8 Rabbit / Hinton | Wonder, then fair-minded debate | 0.92 | "rabbit" gets its own sentence. Hinton's line should be quoted plainly, not dramatized. "Smart people are still fighting about this one" is loose and lighter |
| 9 Raw model | Amused | 0.98 | The forum-post quote is a slightly sing-song parody. Then "So the companies train it again" goes back to plain |
| 10 Tidewater | Serious, quieter, then the sign-off | 0.93 | "It doesn't exist." is flat and low after a 0.9 s break. Keep the "next video" teaser brisk. "I gotchu." is warm and short, never upspeak |

---

## TTS-ready rewrite rules (use for every script)

1. **Write every number as words:** "thirty-four million", "twenty twenty-five", "seven in the morning", "thirty-five out of forty-two". Never use "34M", "7am", "35/42", "%", "$" or "2x".
2. **Acronyms.** Keep "AI" as is. Replace "IMO" with "the Math Olympiad"; if you must use the letters, write "the I-M-O". Never put a normal word in ALL CAPS for emphasis: "IS", "IT", "US" and "AM" get spelled out.
3. **Names and brands.** Put them in an alias pronunciation dictionary. Phoneme rules don't work on v2. Aliases: `Allende → Ah-YEN-day`, and `ChatGPT → Chat G-P-T` only if a test clip mangles it. Lock "I gotchu" to whatever spelling produced the past sign-offs.
4. **No parentheses.** An aside becomes its own short sentence, or a dash clause.
5. **No scare quotes.** TTS can't voice quotation marks. Quoted speech goes after a colon as its own sentence(s), so the model resets its tone.
6. **Pauses, from the measured map:**
   - comma ≈ 0.2 s;
   - period ≈ 0.3–0.5 s;
   - paragraph break ≈ 1.0 s;
   - `<break time="0.4–1.2s" />` before reveals, at most 2 per clip;
   - held silences over 1.5 s go in `timing.json` pads, not in TTS.
   On v3, use `[pause]` instead, since there's no `<break>`.
7. **Ellipses only for "finish this" or trailing off,** and always follow one with a break before the answer.
8. **Emphasis comes from structure:**
   - put the stressed word **last** in a short sentence;
   - follow a long sentence with a 2–5-word one;
   - repeat a word for stress ("really, really").
   Italics and caps don't work.
9. **Real questions end in "?" and stay under about 12 words** so the rise lands. Rhetorical questions that should fall end in a period.
10. **Keep sentences at or under 28 words** unless the run-on is the joke.
11. **End every clip on a full stop.** Never end on "?" or "…", because v2 clip tails pick up breaths and artifacts. Trim tails with silencedetect as you do now.
12. **Keep each clip at or under about 800 characters.** Slide 6 is about 750, which is fine; split anything longer.

---

## Exact lines needing TTS-friendly spelling (proposed replacements)

| # | Slide | Current | Replace with | Why |
|---|---|---|---|---|
| 1 | 1 | `Your mom texts you: "Call me when you get a sec." No emoji, no "love you", just that.` | `Your mom texts you. Call me when you get a sec. No emoji. No love you. Just that.` | Quote marks aren't voiced. Short sentences force the flat "text" read. The mid-sentence quoted "love you" gets read warmly otherwise |
| 2 | 3 | `(Unless you see it searching the web and showing you links. That's a different trick, and we'll get to it.)` | `Well, unless you see it searching the web and showing you links. That's a different trick.` | Parentheses are dropped silently and "Unless" opens a fragment. Also check whether "we'll get to it" is ever paid off in this video; if not, cut it |
| 3 | 3 | `…which are bits of words, but "word" is close enough for us.` | `…which are bits of words. But calling them words is close enough for us.` | Scare quote |
| 4 | 4 | `Pause the video, open any chat, type "I'm going to" and keep tapping the middle suggestion.` | `Pause the video, open any chat, and type the words, I'm going to. Then keep tapping the middle suggestion.` | By ear, "type I'm going to and keep tapping" parses as the narrator's plan |
| 5 | 4 | `Mine gave me: "I'm going to go get some lunch now so I'll call when I'm on the road I have a couple things I have..." and then it just kept going.` | Keep the babble unpunctuated (the joke), but end it: `…I have a couple things I have. And then it just kept going.` | A trailing ellipsis inside a quote makes an odd sustained tail. Also confirm this is the creator's real phone output; if not, it's a [FILL] |
| 6 | 4 | `Apple's is around 34 million settings.` | `Apple's is around thirty-four million settings.` | Digits |
| 7 | 5 | `You walk in at 7am in a hoodie` / `tired people in hoodies at 7am usually order that` | `You walk in at seven in the morning, in a hoodie` / `tired people in hoodies at seven a.m. usually order that` | "7am" can be read as "seven am", "seven A M" or "sevenam" |
| 8 | 6 | `In 2025, AI built on this same predict-the-next-word idea sat the International Math Olympiad` | `In twenty twenty-five, an AI built on this same guess-the-next-word idea sat the International Math Olympiad.` | The year as words. Hyphen chains get slurred on v2, and "guess" matches the video's verb. If anyone adds the score, write "thirty-five out of forty-two", never "35/42", and never "IMO" |
| 9 | 6 | `So is it just autocomplete? At the basic level, yes. It is autocomplete. It's just not the kind you think.` | `So is it just autocomplete? <break time="0.5s" /> At the basic level, yes. It really is autocomplete. It's just not the kind you think.` | The question needs the rise, then a beat. "really" carries the stress v2 can't place on "is" |
| 10 | 7 | `Finish this one. "Someone ate my leftovers. Jay was the only one home, and Jay swears he hates pasta. So it was..."` | `Finish this one. Someone ate my leftovers. Jay was the only one home. And Jay swears he hates pasta. So it was… <break time="1.2s" />` | Split the clue so each fact lands, and leave a real gap for the viewer's answer |
| 11 | 8 | `In 2025, researchers at Anthropic…` | `In twenty twenty-five, researchers at Anthropic…` | Digits |
| 12 | 8 | `…the word it wanted to land on, "rabbit", and then built the line to get there.` | `…the word it wanted to land on. Rabbit. Then it built the line to get there.` | A quoted word inside commas gets swallowed. As its own sentence, it becomes the reveal |
| 13 | 8 | `Geoffrey Hinton, one of the godfathers of AI, put it this way: "to predict the next word, you have to understand the sentences."` | `Geoffrey Hinton, one of the godfathers of AI, put it like this. To predict the next word, you have to understand the sentences.` | Quote marks aren't voiced. The sentence break keeps it from reading as the narrator's own claim. At 38 words it's the longest sentence, so it needs the split |
| 14 | 9 | `Ask "what's a good dinner tonight?" and it might carry on like a forum post: "...asking for my picky five-year-old. Edit: thanks everyone!"` | `Ask it what's a good dinner tonight, and it might just carry on like a forum post. Asking for my picky five-year-old. Edit. Thanks, everyone!` | The embedded "?" puts a rising question mid-sentence. A leading ellipsis and "Edit:" read as noise |
| 15 | 10 | `But in 2025, two real newspapers…` | `But in twenty twenty-five, two real newspapers…` | Digits |
| 16 | 10 | `…a novel called Tidewater Dreams, by Isabel Allende.` | Same text, but add dictionary alias `Allende → Ah-YEN-day` (or write "Isabel Ah-yen-day" in the TTS text only; captions keep "Allende") | v2 has no phoneme support and likely says "a-LEND-ee" |
| 17 | 10 | `It sounds exactly like a book she'd write. It doesn't exist.` | `It sounds exactly like a book she'd write. <break time="0.9s" /> It doesn't exist.` | The reveal needs a beat |
| 18 | all | `ChatGPT` (×6) | Keep it, but test one line first. If it comes out as "chat-gipt", use alias `Chat G-P-T` | The brand name is usually fine on v2 but not guaranteed |
| 19 | 10 | `I gotchu.` | Lock the alias to the spelling that produced the past sign-offs (for example `I got-chu.`) | Brand consistency across the series |

The captions and on-screen text keep the normal spelling. **Only the string sent to TTS is respelled.** Build a `tts_text` field next to `text` in `slides.json` so the captions and the aligner still use the clean text.

---

## (d) Keep, don't touch

- **Marshel on multilingual_v2** as the channel voice. Consistency across videos beats chasing a marginally "better" voice.
- The creator's instinct against **tag-driven v3** (confirmed: LRA 8.3 vs 2.0 LU, and 74% longer).
- **One clip per slide**, the 0.35 s / 0.55 s pads, and cutting with silencedetect.
- About **160–168 WPM overall**, and the natural speech dynamics (LRA about 4.5 LU).
- The conversational register of the new script (contractions, "come on", "I genuinely need to know"). It suits this voice far better than the old "Here's the thing" copy.

## (e) Bold idea: "Performance transfer" (speech-to-speech)

The creator records each slide as a **phone voice memo**. Any room works and flubs are fine; retakes are just "say it again". ElevenLabs **Voice Changer (speech-to-speech)** then re-voices the memo as Marshel, or later as their own clone.

The output keeps the creator's real timing, pauses, emphasis, breaths and laughs; only the timbre changes. This is the one change that removes the "AI cadence" completely, because no model is inventing the prosody.

It fits the no-edit rule:
- Claude receives the memos, runs STS per slide, trims with silencedetect and builds as usual.
- It also makes the [FILL] personal lines sound lived-in, because they are.
- Start with slides 1, 6 and 10 as a pilot, and blind A/B them against TTS.
