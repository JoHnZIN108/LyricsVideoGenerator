# Retention & packaging review: Script 3 v2 + v3 video

Reviewer: Expert 1, YouTube retention & packaging strategist (slug: `retention`)

## (a) Research findings

1. **The first minute is where most viewers leave, so it has to confirm the click.** The leaked MrBeast production memo calls the first minute "the most important minute of each video". It has two jobs: hold attention, and prove the thumbnail's promise will be met. The memo treats 60M clicks falling to 39M by minute one as a *good* result. ([Simon Willison's summary of the memo](https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/), [Creator Handbook takeaways](https://www.creatorhandbook.net/leaked-document-allegedly-reveals-mrbeasts-secrets-to-youtube-success-the-key-takeaways/), [Dexerto](https://www.dexerto.com/youtube/leaked-mrbeast-pdf-reveals-youtubers-secrets-to-video-success-2900841/))
2. **Paddy Galloway on retention and hook structure.** He works on packaging and retention mapping and says an extra 10% retention can separate a 100k video from a 1M video. The first 30 seconds are commonly broken down as 0–5 s grab, 5–15 s state the promise, 15–30 s stakes and start the journey. ([1of10: hook in the first 30 s](https://1of10.com/blog/how-to-hook-viewers-in-the-first-30-seconds-of-a-youtube-video/), [Galloway strategy notes](https://www.scribd.com/document/873587706/Paddy-Galloway-Strategies), [Medium profile](https://better-question.medium.com/the-godfather-of-youtube-strategy-c9964829b9eb))
3. **Veritasium, "Clickbait is Unreasonably Effective" (2021).** Derek Muller separates "legitbait" (packaging the video actually delivers on) from "clicktraps". Legitbait brought exponentially more views, and the video's own title was A/B-changed from "We Need To Talk About Clickbait". The lesson: an aggressive title is fine *only if the video pays it off*. ([IMDb entry](https://www.imdb.com/title/tt15251060/), [Third Law Reaction write-up](https://www.thirdlawreaction.com/shocking-secret-behind-clickbait/), [HN discussion](https://news.ycombinator.com/item?id=28218165))
4. **Drop-off data.** Aggregated analyses put first-30-second loss at 20–40%, rising to 33%+ with weak intros and 55%+ inside the first minute. Top videos keep 70%+ through 0:30. The most-cited cause: the title's promise isn't confirmed in the first 15–30 s. ([Narration Box](https://narrationbox.com/blog/why-viewers-drop-off-after-30-seconds-youtube), [Humble & Brag benchmarks 2026](https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks), [Teleprompter.com retention guide](https://www.teleprompter.com/blog/youtube-audience-retention), [Creator Playbook](https://www.creator-playbook.com/articles/your-intro-sucks-fix-first-30-seconds), [Retention Rabbit guide](https://www.retentionrabbit.com/blog/ultimate-guide-youtube-audience-retention); Retention Rabbit could not be fetched through the proxy, so it is cited from its search summary)
5. **Confirm the click with a title → thumbnail → hook → payoff chain.** "A title and thumbnail may earn the click, but the intro has to defend the click." ([Overseer: click promise](https://www.overseeros.com/blog/youtube-click-promise), [vidIQ: YouTube intros](https://vidiq.com/blog/post/youtube-intros/))
6. **Johnny Harris front-loads "visual anchors" in the first 30–60 s**, which act as a promise the rest of the video must deliver. Colin & Samir's case studies and their interview with Johnny and Izzy Harris make the same point. ([Medium analysis](https://medium.com/@LMK_writing/how-johnny-harris-mastered-visual-storytelling-on-youtube-343ddf9160ec), [Colin & Samir x Harris](https://craftbyzen.com/curation/stream/link/2025-03-07t181915788z/), [open loops](https://jchristiaancollins.substack.com/p/ignite-curiosity-open-loops-in-copywriting))
7. **Kurzgesagt structure:** opening tension, then the core question, a simple mental model, layered explanation, examples, implications, and a CTA that "links to the next question naturally". ([Kurzgesagt research process](https://medium.com/@Kurzgesagt/how-research-and-factchecking-work-at-kurzgesagt-f5b239188255), [10 Studio on Kurzgesagt](https://10.studio/the-incredible-amount-of-work-behind-kurzgesagts-beautiful-animated-videos/))
8. **The top AI explainer hook.** 3Blue1Brown's *Large Language Models explained briefly* opens on a concrete scene with a missing piece (a movie script with the AI's reply torn off) and makes the viewer the predictor before naming the concept. The Mom-text hook uses the same move, which is a good sign. ([3Blue1Brown lesson](https://www.3blue1brown.com/lessons/mini-llm/))
9. **Endings.** Dexxter Clark's retention tests found that talking *over* the last ~20 s while end-screen elements are up beats a formal goodbye. Signalling "the video is over" before the end screen causes early exits. ([Dexxter Clark](https://www.dexxterclark.com/youtube-videos/how-i-tripled-my-youtube-audience-retention), [Alan Spicer: final 20 seconds](https://alanspicer.com/youtube-end-screen-strategy-final-20-seconds-grow-channel/), [YouTube Help: end screens](https://support.google.com/youtube/answer/6388789?hl=en))

## Measurements I took (not guesses)

- **Voice rate:** v3 = 575 words over 204.8 s of speech, about **2.81 words/s (169 wpm)**.
- **Script v2 length:** 878 spoken words. At the measured rate plus the current 0.9 s per-slide padding, it runs about **5:20, not 4:40**. Projected slide starts:

  | Slide | Start | Slide | Start |
  |---|---|---|---|
  | S1 | 0:00 | S6 | 2:31 |
  | S2 | 0:26 | S7 | 3:19 |
  | S3 | 0:44 | S8 | 3:43 |
  | S4 | 1:22 | S9 | 4:29 |
  | S5 | 2:01 | S10 | 4:54 |

  **The title's question ("so how does it write code?") is first raised at about 2:31.**
- **Dead or static screen in v3** (frame-difference at 2 fps, runs over 4 s):

  | Time | Length | Time | Length |
  |---|---|---|---|
  | 0:23–0:28 | 5 s, near-empty canvas | 2:57–3:03 | 6 s |
  | 0:42.5–0:48 | 5.5 s | 3:08–3:13 | 5 s |
  | 0:57.5–1:02 | 4.5 s | 3:26.5–3:31 | 4.5 s |
  | 1:50–1:54 | 4 s | 3:33.5–end | 7 s |
  | 2:28.5–2:33.5 | 5 s | | |

  The contact sheet also shows the hook frozen from **0:09 to 0:18**: the reply is finished and only the caret blinks.
- **Silence at every slide seam:** 0.9–1.37 s (silencedetect, −35 dB). There are 9 seams, so about 10 s of dead air in 220 s. The seams line up with blank frames at 0:22, 0:38, 2:01, 2:15 and 3:23.
- **Tail:** the voice ends at 212.6 s and the video ends at 220.8 s, leaving **8.2 s of silent end card**.
- **Frame 0 of v3 is a blank gradient.** The headline fades in over about 0.5 s.

## (b) Score: 6/10

**Strengths**
- The Mom-text hook is a genuinely top-tier open: a scene, stakes, the viewer as the predictor, and the emoji twist at 0:26. It is the same move as 3Blue1Brown's LLM explainer.
- "Most people assume it looks it up. It doesn't." is exactly the misconception-first structure.
- It has real re-hooks: the IMO result, "pick your side", and the nonexistent novel.
- The Tidewater Dreams cliffhanger is strong.

**Problems**
- **(1) The title promises code, but the script never shows how it writes code.** It pays off with a math olympiad, Jay's leftovers and a rhyming poem. The code question also arrives at about 2:31, when the research says to confirm the promise within 15–30 s. That is a legitbait-to-clicktrap slide.
- **(2) An open loop is opened and never closed.** "That's a different trick, and we'll get there" (web search) is never paid off. Viewers remember unpaid promises, and the comments will say so.
- **(3) There are three analogies in a row for "guessing from past experience":** the Mom text, the phone, then the barista. The skill's own rule forbids this, and it lands in the 1:20–2:30 zone where explainers sag.
- **(4) The v3 craft leaks retention at every seam:** blank canvases, 1 s silences, a 9 s frozen hook, and an 8 s silent tail. v2 inherits all of it.
- **(5) The ending signposts "Next video:"**, which tells viewers the video is over before the end screen can catch them.

## (c) Top 5 changes, ranked by impact

### 1. Confirm the title inside the first 30 s (S2, about 0:35)

After "…given everything written so far, what probably comes next?", add:

> "And people use this exact same trick to write code that actually runs. Your phone can't even finish a sentence without going in circles. So what's different? Let's take it apart."

- This creates the gap without announcing it (the skill bans "a question that'll bug you").
- It names the title's noun (code) and ties to the thumbnail's "SAME TRICK?".

**Visual:** a 1.2 s insert. The chat box from S1 swaps its text bubble for a 4-line code block that types itself, using the same `predictor_steps` bars (candidates `==` / `=` / `!=`, winner `==`), then hard-cuts back.

**Build:** add `#s2-code` inside the chat window, then `tl.set` the swap at `cue(2,"write code")`, then `out` at +1.4 s. Ding SFX on the winning token.

**Also:** S6's opening "[SLIDE 6: 'So how does autocomplete write working code?']" becomes the **payoff of a planted loop** rather than a cold question.

### 2. Actually pay off "code", and close the web-search loop

**S7, after "…because it helps with the guessing." add:**

> "Code is the same game. To guess the next line of a program, it has to keep track of what every variable is holding, the same way you kept track of Jay. That's how autocomplete ends up writing code that works."

**Visual:** 3 lines of code. `x = 5` pops, then `x = x + 2` pops, then `print(x) → ` with the bars choosing `7`. Same style as the Jay card, with Jay's name in the group chat morphing into the variable `x` (0.4 s crossfade).

**S3, replace the parenthetical** "(Unless you see it searching the web and showing you links. That's a different trick, and we'll get there.)" **with a closed aside:**

> "(If you see it searching the web and showing links, that's an extra step bolted on top. Underneath, it's still this.)"

### 3. Kill the dead air (v3 craft carried into v2)

**Seams**
- Change the per-clip padding in SKILL.md step 4 from **0.35 s before / 0.55 s after** to **0.12 s / 0.28 s**.
- Start every new scene's entrance **0.3 s before the previous clip's last word ends** (a J-cut: the whoosh SFX starts at the same moment).
- Rule: **no frame with less than 1 object on screen for more than 0.5 s.** The 0:22–0:28 gap in v3 is the worst offender: "FINISH THE SENTENCE" sits alone for 5 s in the 0:20–0:30 danger window.

**Frame 0**
- The first frame must be fully drawn, with the lock screen and Mom's notification already lit (no fade-in). It should match the thumbnail's phone so the click is confirmed visually at 0.0 s.

**Hook motion, 0:03–0:20**
- On "Somebody's sick, or you forgot a birthday", 3 ghost thought-bubbles pop in 0.5 s apart: "someone's sick", "forgot a birthday", "I'm in trouble".
- On "guessed what usually comes next", `predictor_steps` bars appear under them (no %). This introduces the video's recurring image at 0:12 instead of 0:38.
- **S2 emoji flip:** the party emoji drops in with the `igSlam` ease. The "sick" bar collapses to 5% while a new "engaged!" candidate bar shoots to the top (0.6 s, `igOut`, thud and ding).
- Nothing on screen stays static for more than 3 s. Add a `camera()` push of 1.00→1.04 across each held beat.

**Tail**
- Cap the hold after "I gotchu" at 5 s (v3 currently holds 8.2 s silent).

### 4. Trim the barista and slide 3 to pull the midpoint forward about 25 s

**S5, replace the whole slide with:**

> "Now scale that up. Picture a barista who's served ten million people. You walk in at 7am in a hoodie and they're already making your oat latte. ChatGPT learned from more writing than a person could read in thousands of lifetimes. Its guesses get so good they stop feeling like guesses."

That is 49 words, down from 80.

**S3, cut** "For a normal answer it goes around that loop a few hundred times." The streaming line already makes the point.

**S4, cut** "The model on your phone is small. Apple's is around 34 million settings." Keep "The ones behind ChatGPT are thousands of times bigger, and that's where it gets weird", reworded as:

> "The one behind ChatGPT is thousands of times bigger, and that's where it gets weird."

Move the 34M figure to the description.

**Result:** about 810 words, about 4:55, with S6 starting around 2:08 instead of 2:31. The added lines from #1 and #2 are already counted.

**S9 re-hook** (it is the lowest-stakes beat, at about 4:00). Replace "One more piece." with:

> "One more piece, and it's why ChatGPT sounds like a polite assistant instead of a comment section."

### 5. End without saying "Next video" (S10, about 4:40 to end)

Replace the last paragraph with:

> "It doesn't exist. Nobody lied on purpose. The guess just sounded right. And that same confident guess has fooled lawyers, judges and a whole airline. That's this one, right here. I gotchu."

**Build**
- The end card (`ig-signoff` + `ig-slot`) and YouTube's real end-screen elements appear **at "And that same confident guess"**, not after the sign-off. The voice keeps talking over them for about 6 s.
- "right here" lands when a pointer draws to the left slot (the Script 4 video).
- Hold 5 s after "I gotchu", then end.

## (d) Keep these

- The **Mom-text cold open** and the emoji flip. It is the best hook the channel has, so do not replace it; the creator has already declined a hook rewrite.
- **"Most people assume it looks your question up. It doesn't."** The misconception is stated, then broken.
- The **IMO "Autocomplete did that."** beat and **"It is autocomplete. It's just not the kind you think."** That second line is the title's thesis, so keep it word for word.
- **"Pick your side in the comments"** (a real debate) and the Tidewater Dreams cliffhanger, which pays off in-video and teases Script 4.
- From v3:
  - the **prediction-bars chat box** as the recurring visual;
  - the **chapter progress bar** at the bottom (it helps viewers feel they are moving through the video);
  - the **WRONG stamp payoff** at 3:20;
  - the glass-and-brain illustration with Ken Burns at 2:02.

## Title & thumbnail verdict

- **Title: "ChatGPT Is Just Autocomplete. So How Does It Write Code?"** This is a good contradiction title (belief plus paradox), with concrete, searchable nouns. **Keep it only if changes #1 and #2 ship.**
  - Without them, it's a clicktrap: code is barely touched.
  - Fallback if the code beats are cut: **"ChatGPT Is Just Autocomplete. So Why Is It This Smart?"**
- **Thumbnail text: "SAME TRICK?"** It complements the title rather than repeating it (correct), but it only works if the image shows the two things being compared.
  - **Left:** a phone keyboard suggestion bar ("I'm going to | be | the"), with the middle key glowing.
  - **Right:** a code editor with a ghost-text completion in cyan.
  - **Between them:** an orange "=" with a "?".
  - Keep "SAME TRICK?" at 2 words, placed top-right, clear of the timestamp.
  - Frame 0 of the video should echo the phone half.
  - Run YouTube's **Test & Compare** against a variant reading **"IT'S JUST GUESSING?"**.

## (e) Bold idea: the "live autocomplete" cold open that becomes the ending

Open frame 0 on the phone keyboard *already running*. The middle-suggestion chain types Mom's reply by itself ("Call me when you get a sec" → "…ok love you see you soon ok love you see you"), looping into nonsense for 2 s. Then Mom's real text lands on top.

Close the video on the same keyboard, with the chain now completing **a line of code that runs**, green check. Then the hard cut to the Tidewater card.

**Why it works**
- It is the thumbnail made literal ("SAME TRICK?").
- The phone-vs-ChatGPT gap becomes a visible bookend.
- It needs zero new assets: it reuses `predictor_steps` and the S4 keyboard rig.
- Viewers who recognise the keyboard at 0:00 have their click confirmed before a word is spoken.

## Author notes (flag for the creator, retention-relevant)

These lines read as personal claims and must be true, or be marked [FILL]:

- "Which is where I got stuck the first time I learned this." (The SKILL.md rules name "when I first learned this" as a banned invented line.)
- "For me it started small… grammar… wrong variable…"
- "Mine gave me: …"

A real, specific scene here (when, what broke) is also the strongest possible S6 re-hook.
