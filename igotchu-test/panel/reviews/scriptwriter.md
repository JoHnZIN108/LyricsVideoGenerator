# Scriptwriter & spoken-word review: Script 3 v2

Reviewer: Expert 2 (scriptwriter). Scope: voice, rhythm, humor, specificity, how it sounds read aloud, TTS deliverability. File judged: `igotchu-test/panel/script3_v2.txt`.

---

## (a) Research findings

Note: Wikipedia, elevenlabs.io, cgpgrey.com and current.org are blocked by the egress proxy, so those pages were read through search-result summaries and mirrors.

1. **Wikipedia, "Signs of AI writing"** ([page](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing); summaries: [Beutler Ink](https://www.beutlerink.com/blog/how-to-spot-ai-writing), [FlowingData](https://flowingdata.com/2025/10/20/signs-of-ai-writing-on-wikipedia/)). The tells that matter for a voiceover:
   - **Negative parallelisms**, including "It's not…, it's…" and specifically **"no …, no …, just …"**.
   - **The rule of three**: "adjective, adjective, adjective" or "phrase, phrase, and phrase". It makes thin analysis sound complete.
   - **Tidy summary sentences** at the end of sections.
   - **Formulaic, punched-up emphasis**.
2. **Russell, Karpinska & Iyyer, ACL 2025**, ["People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text"](https://aclanthology.org/2025.acl-long.267/).
   - Five heavy LLM users, voting together, misclassified **1 of 300** articles, beating most commercial detectors.
   - Their clues were "AI vocabulary", but also **formality, originality and clarity**, meaning text that is too even and too generic.
   - This matters for us: YouTube's AI-explainer audience is exactly this expert group.
3. **Kobak et al., 2024/25**, ["Delving into LLM-assisted writing… through excess vocabulary"](https://arxiv.org/abs/2406.07016).
   - They found 280 "excess style words" (for example *delves*, *showcasing*, *crucial*).
   - **66% of them were verbs and 18% adjectives**, so AI smell comes mostly from intensifier verbs and adjectives, not nouns.
   - Soft intensifiers like "genuinely", "literally" and "really, really" belong to the same family.
4. **Ira Glass on storytelling** ([StoryCenter](https://www.storycenter.org/storycenter-blog/blog/2013/7/1/ira-glass-on-storytelling), [transcript](https://medium.com/@DanlWebster/ira-glass-on-storytelling-1-of-4-rough-transcript-9bb2dc8e27f7)).
   - A story has two building blocks: the **anecdote** (this happened, then this) and the **moment of reflection** ("here's why the hell you're listening").
   - Every anecdote needs its reflection, and vice versa.
   - In this script, the personal beat in Slide 6 has the reflection but no anecdote.
5. **Broadcast "writing for the ear"** ([UF/IFAS WC193](https://edis.ifas.ufl.edu/publication/wc193), [Human Kinetics](https://us.humankinetics.com/blogs/excerpt/tips-for-writing-for-broadcast), [Adonde Media](https://medium.com/@AdondeMedia/the-podcast-script-writing-for-the-ear-95fab0d9c5be)).
   - One idea per sentence, about 8–20 words.
   - The listener gets one pass, so no parentheses and no nested clauses.
   - Read it aloud and rewrite anything you'd stumble on.
   - Use reported speech instead of quotation marks the ear can't see.
6. **Kurzgesagt** ([10 Studio breakdown](https://10.studio/the-incredible-amount-of-work-behind-kurzgesagts-beautiful-animated-videos/), [Kurzgesagt on research](https://medium.com/@Kurzgesagt/how-research-and-factchecking-work-at-kurzgesagt-f5b239188255)).
   - Many rounds of rewording "to find the right balance between simplicity and accuracy".
   - About 100 hours of fact-checking per video.
   - Their voice is plain and concrete, with one absurd image per idea rather than stacked analogies.
7. **CGP Grey** ([profile](https://yespress.io/cgp-grey), ["Growing & Cutting"](https://www.cgpgrey.com/blog/growing-cutting-two-ways-of-writing)). About 10 drafts per script, some redrafted for over a year. The final passes are about **cutting**.
   **Wendover** ([profile](https://yespress.io/wendover-productions)). The script is newsroom-style, and specificity (names, numbers, places) carries the authority.
8. **Deadpan and Casually Explained** ([Deadpan overview](https://en.wikipedia.org/wiki/Deadpan), [StudioBinder](https://www.studiobinder.com/blog/what-is-a-deadpan-definition/)).
   - The joke works when the material has a comic mismatch and **the speaker doesn't underline it**.
   - That suits a TTS voice: flat delivery of an absurd specific line lands better than "right?!" energy.
9. **ElevenLabs TTS best practices** ([docs](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices), [pauses](https://help.elevenlabs.io/hc/en-us/articles/13416374683665-How-can-I-add-pauses)).
   - Write numbers and symbols as words.
   - Use dashes for short pauses and ellipses for hesitation.
   - Use `<break time="1.5s"/>` on v2 models only; v3 ignores SSML, and too many breaks cause artifacts.

**Measured fact for this review.**
- The v3 voiceover read the old script (575 words) in 213.5 s, which is **162 wpm**.
- v2's spoken text is **879 words** (counted from lines 7–69), so at the same voice and pace it runs **about 5:25, not 4:40**.
- Hitting the stated length means cutting about 120 words. The rewrites below are net shorter where it matters.

---

## (b) Score: 7/10 for voice and human feel

**Why it's good.**
- A huge step up from the voiced v1, which had "Here's the thing", "Honestly", "scary good", "Let's play a game", "capital of France" and "By the end of this video".
- The ban list is clean.
- The examples are the viewer's own life: mom's text, the barista, "Jay swears he hates pasta", "Edit: thanks everyone!".
- There's a real pause-and-try moment, the wrong belief is said and then taken apart, and there's a self-correction ("'word' is close enough for us").

**Why not higher.**
1. **The personal beats are unverified.** Slide 6 ("where I got stuck the first time I learned this", "clean up the grammar… broken data structure") and Slide 4 ("Mine gave me…") read as first-person but aren't marked [FILL]. "When I first learned this" is literally the example the skill bans. Slide 6 is also a summary, not a scene.
2. **Structural AI tells remain.**
   - One "no…, no…, just…" in the first sentence.
   - Three lists of three.
   - A parenthetical aside that makes a promise ("we'll get to it") the script never keeps.
3. **No habit, no opinion.** The script ends without the viewer habit or the creator's own opinion (checklist rules 6 and the "one habit" rule). The teaser is a generic three-item list.
4. **It's 25% over length**, and the long lines (57, 55, 43) are where the ear gets lost.

---

## Line-by-line pass

The number is the line in `script3_v2.txt`. **Flag** names the problem; **Rewrite** is the proposed exact wording.

### Slide 1

**L7:** "Your mom texts you: 'Call me when you get a sec.' No emoji, no 'love you', just that."
- **Flag:** this is Wikipedia's textbook "no…, no…, just…" negative parallelism, in sentence one. It also tells us what's missing instead of showing a concrete detail.
- **Rewrite:** "Your mom texts you: 'Call me when you get a sec.' With a period. No emoji."
- The period is the specific, human detail. Everyone knows what a period from mom means.

**L9:** "And your brain has already written the next five minutes of your life. Somebody's sick, or you forgot a birthday. You didn't decide to think any of that. You've seen that exact text before…"
- **Flag:** "You didn't decide to think any of that" tells the viewer what they felt (rule 9), and "that exact text" is a slight overclaim.
- **Rewrite:** "And your brain has already written the next five minutes of your life. Somebody's sick. Or you forgot a birthday. You didn't sit down and reason that out. You've just seen texts like that enough times to know what usually comes next. Hold on to that feeling, because that's pretty much how ChatGPT works."
- Three short sentences in a row are fine here because the next one is long and loose.

### Slide 2

**L13:** "Same text, but now she adds a party emoji. Whole different story, right? Nobody's sick. Somebody's engaged."
- **Flag:** it's good, but there's no joke on the payoff, and this is the cheapest place to buy one.
- **Rewrite:** "Same text, but now there's a party emoji on the end. Whole different story. Nobody's sick. Somebody's engaged. Possibly your mom."
- Deliver the joke flat, no pause before it (deadpan).

**L15:** "That's the exact problem ChatGPT solves all day: given everything written so far, what probably comes next?"
- **Flag:** a colon followed by a question is written grammar, and "solves" is inaccurate, because it answers rather than solves.
- **Rewrite:** "One tiny detail at the very end flipped every guess you were about to make. And that's the one question ChatGPT is answering all day long. Given everything written so far, what probably comes next?"

### Slide 3

**L19:** "There's no answer sheet in there that it checks."
- **Flag:** it trails off on a stranded "that it checks".
- **Rewrite:** "There's no answer key hidden in there."

**L19 (parenthetical):** "(Unless you see it searching the web and showing you links. That's a different trick, and we'll get to it.)"
- **Flag, and it's high priority:**
  - TTS can't voice parentheses, so it will read this at full volume as main text.
  - The script **never gets to it**, which makes it a broken promise.
- **Rewrite:** "Now, if you see it searching the web and showing you links, that's an extra step bolted on top. Different video."

**L21:** "The chunks are called tokens, which are bits of words, but 'word' is close enough for us."
- **Flag:** a nice self-correction, but it's tangled for the ear.
- **Rewrite:** "Those chunks are called tokens. They're usually bits of words, but 'word' is close enough for today. For a normal answer, it goes around that loop a few hundred times, and when the text trickles in on your screen, you're watching it happen live."
- This also drops "literally".

### Slide 4

**L25:** "Pause the video, open any chat, type 'I'm going to' and keep tapping the middle suggestion."
- **Flag:** good, but there's no permission to actually pause.
- **Rewrite:** add "Go on. I'll wait." at the end, followed by a 2 s silence. Use `<break time="2s"/>` on v2, or a hard 2 s gap in the build.

**L27:** "Mine gave me: '…'"
- **Flag, personal claim:** first-person and not marked [FILL]. Keep it only if this is really the creator's phone output.
- **Rewrite:** "[FILL: paste exactly what your phone gave you, and trim it at the funniest point]"
- **TTS:** a run-on with no punctuation gets odd stress from ElevenLabs. Generate this clip on its own with lower stability, or put it on screen and have the voice say only "Mine went: I'm going to go get some lunch now so I'll call when I'm on the road… and it did not stop."

**L27:** "Tell me in the comments what yours said. I genuinely need to know."
- **Flag:** "genuinely" is intensifier filler, and the line is a stock CTA.
- **Rewrite:** "Yours will be different, because it learned from your texts. Put yours in the comments. I want to know what your phone thinks your life is like."

**L29:** "Apple's is around 34 million settings. … and that's where it gets weird."
- **Flag:**
  - "Where it gets weird" promises weirdness, and the next beat (the barista) isn't weird.
  - The digits should be words for TTS.
- **Rewrite:** "The model on your phone is small. Apple's has about thirty-four million settings. The ones behind ChatGPT are thousands of times bigger. Same trick. Way more practice."
- Move "that's where it gets weird" to Slide 8, where it's true.

### Slide 5

**L33:** "You walk in at 7am in a hoodie… because tired people in hoodies at 7am usually order that."
- **Flag:** "7am" and "hoodies" are repeated in one sentence. The digits need to be words, and "Picture a" is a stock explainer opener.
- **Rewrite:** "There's a barista who's served ten million people. You walk in at seven a.m. in a hoodie, and before you open your mouth they're already making an oat latte, because that's what tired people in hoodies order at that hour. Most days they're right. Some days you wanted tea."

**L35:** Keep ("Good enough that it stops feeling like guessing." is the best line in the script).
- **Trim:** cut "That's what scale does." It's a summary sentence (rule 4); the barista already made the point.

### Slide 6

**L39:** "Which is where I got stuck the first time I learned this."
- **Flag, personal claim:** "the first time I learned this" is the skill's own banned example of an invented experience.
- **Rewrite:** "[FILL: were you actually stuck on this? If yes, keep: 'This is where I got stuck.' If not, use: 'Which raises the obvious question.']" (Don't use "Here's the question"; "Here's…" is on the ban list.)

**L41:** "For me it started small. It would clean up the grammar… spot the wrong variable or the broken data structure."
- **Flag, personal claim told as a summary:** it needs to be a scene (Ira Glass's anecdote: when, where, what broke). Nobody says a data structure is "broken"; that's AI vagueness.
- **Rewrite:** "[FILL, one scene, about 35 words: the first time it caught a bug you'd missed. What were you building, what was the bug in plain words, and how long had you been staring at it? Example shape only, do not use: 'I'd spent an hour on a login page that kept logging people out. Pasted it in. It pointed at one line: I'd named the same thing two different ways.']"

**L43:** "…sat the International Math Olympiad, the one for the smartest teenagers on the planet. It wrote full proofs in plain English, under the same time limits, and scored right at the gold-medal line. Plenty of kids still beat it, but come on."
- **Flag:**
  - "Sat" is British; a US ear expects "took".
  - There's a list of three.
  - "Plenty of" is repeated in L57.
- **Rewrite:** "Then it got big. In 2025, AI built on this same predict-the-next-word idea took the International Math Olympiad, the one for the smartest teenagers on the planet. Same time limits, full proofs in plain English, and it landed right on the gold-medal line. A bunch of kids still beat it. But come on. Autocomplete did that."

**L45:** "So is it just autocomplete? At the basic level, yes. It is autocomplete. It's just not the kind you think."
- **Flag:** "It is autocomplete" is redundant, and "At the basic level" is stiff. The final clause is the title callback, so it stays.
- **Rewrite:** "So is it just autocomplete? Technically, yeah. It's just not the kind you're thinking of."

### Slide 7

**L49:** Keep. **TTS:** after "So it was…", add a 1.5 s hold so the viewer answers in their head.

**L51:** "You said Jay. … Nobody wrote detective rules into ChatGPT either. Getting really good at the next word forced it to pick that stuff up, because it helps with the guessing."
- **Flag:**
  - "You said Jay" tells viewers what they thought.
  - "either" has no clear referent.
  - "because it helps with the guessing" is circular.
- **Rewrite:** "It was Jay. It's always Jay. To get there, you had to follow the clues and catch the lie, and nobody ever handed you rules for that. Nobody wrote detective rules into ChatGPT either. It picked that up because you can't guess the end of a mystery without catching the liar."

### Slide 8

**L55:** "And it goes deeper than you'd expect. … it had already picked the word it wanted to land on, 'rabbit', and then built the line to get there."
- **Flag:**
  - The opener is filler.
  - The payoff lacks the real, checkable detail, which is the actual first line from Anthropic's paper.
- **Rewrite:** "And this is where it gets weird. In 2025, researchers at Anthropic looked inside one of these models while it wrote a rhyming poem. The first line was 'He saw a carrot and had to grab it.' Before it wrote a single word of the next line, it had already picked where it wanted to land: 'rabbit.' Then it built the line to get there."
- Verify the carrot line against the Anthropic post before recording.

**L57 (73 words, the longest block):** "Geoffrey Hinton, one of the godfathers of AI, put it this way: 'to predict the next word…' Plenty of researchers think that's way too generous and call it a very fancy parrot. Smart people are still fighting about this one, so pick your side in the comments."
- **Flag:**
  - The quote marks are invisible to the ear, and the TTS voice won't shift for the quote.
  - "Godfathers of AI" is a cliché.
  - "Fancy parrot" is the generic version; research.md already holds a funnier, sourced one (LeCun's housecat).
  - There's no creator opinion (rule 6).
- **Rewrite:** "So yes, it writes one piece at a time. But inside, it can be planning where the sentence is going. Geoffrey Hinton, who won a Nobel Prize for this stuff, told 60 Minutes that to predict the next word, you have to understand the sentence. Yann LeCun, another AI pioneer, says these models don't understand the world as well as a housecat. [FILL: your side, one sentence, e.g. 'I'm closer to ___, because ___.'] Tell me which side you're on."

### Slide 9

**L61:** "Ask 'what's a good dinner tonight?' and it might carry on like a forum post: '…asking for my picky five-year-old. Edit: thanks everyone!'"
- **Flag:** it's good. One tweak makes it funnier and plants Script 4's pizza story.
- **Rewrite:** "Ask it 'what should I make for dinner?' and it might just carry on like a forum post: '…I have chicken, rice and a picky five-year-old. Edit: thanks everyone, we ordered pizza.'"

**L63:** "So the companies train it again, on examples of good answers that real people rated, until it acts like…"
- **Flag:** "Answers that real people rated" is a stacked clause.
- **Rewrite:** "So the companies train it again. People write good answers, rate its answers, and it learns to act like an assistant instead of an internet comment section."

### Slide 10

**L67:** "But in 2025, two real newspapers printed a summer reading list…"
- **Flag:** "two real newspapers" is vague where it should be specific (Wendover's rule), and it drops the best number.
- **Rewrite:** "Which leaves one catch. It's predicting what a good answer sounds like, and most of the time, that's also what's true. But in 2025, the Chicago Sun-Times printed a summer reading list where ten of the fifteen books didn't exist. One was 'Tidewater Dreams', by Isabel Allende. It sounds exactly like a book she'd write. She never wrote it."
- **TTS:** Allende is pronounced "ah-YEN-day". Add it to an ElevenLabs pronunciation dictionary or spell it phonetically in the TTS text.

**L69:** "Next video: why it makes things up with a straight face, and the lawyers, judges and airlines who trusted it anyway. I gotchu."
- **Flag:**
  - A list of three.
  - No viewer habit or self-check (a skill rule).
  - "I gotchu" sits in the same slot as all 19 scripts (rule 10).
- **Rewrite:** "So when it hands you a name, a book title or a quote, that's the part to double-check. That's the part that only has to sound right. I gotchu. Next time: a lawyer who asked ChatGPT, 'Is this case real?' It said yes. It wasn't."

---

## (c) Top 5 changes, ranked by impact

1. **Slide 6, L39–41: replace the invented-sounding personal beat with a real [FILL] scene.**
   - "The first time I learned this" and "clean up the grammar… broken data structure" are first-person, unmarked and summary-style.
   - Use the L39/L41 rewrites above: "Which raises the obvious question." plus a roughly 35-word [FILL] scene covering when, what, and what broke.
   - This is the line that decides whether the channel reads as a person or a pipeline.
2. **Slide 3, L19: kill the parenthetical broken promise.**
   - Use: "Now, if you see it searching the web and showing you links, that's an extra step bolted on top. Different video."
   - TTS can't read parentheses, and the script never "gets to it".
3. **Slide 10, L69: add the viewer habit and a specific teaser; move "I gotchu".**
   - Use: "So when it hands you a name, a book title or a quote, that's the part to double-check. That's the part that only has to sound right. I gotchu. Next time: a lawyer who asked ChatGPT, 'Is this case real?' It said yes. It wasn't."
4. **Cut to length (about 120 words): 879 words at the measured 162 wpm is about 5:25, not 4:40.**
   - Rewrite L57 as above (73 to about 60 words, with better content).
   - Cut "That's what scale does." (L35) and the L45 redundancy.
   - Use the L19 and L43 rewrites.
   - If more is still needed, drop L41's second sentence once the [FILL] scene replaces it.
5. **Remove the remaining structural AI tells.**
   - L7: "No emoji, no 'love you', just that." becomes "With a period. No emoji."
   - L29: "that's where it gets weird" becomes "Same trick. Way more practice." (then reuse "where it gets weird" at L55).
   - L27: "I genuinely need to know." becomes "I want to know what your phone thinks your life is like."
   - L51: "You said Jay." becomes "It was Jay. It's always Jay."
   - L57: "godfathers of AI… fancy parrot" becomes Hinton (Nobel, 60 Minutes) against LeCun's housecat, plus a [FILL] opinion.

### TTS delivery notes (for the builder)
- **Write numbers as words:** "seven a.m.", "thirty-four million", "ten of the fifteen". "2025" is fine as digits.
- **Parentheses and quotes:**
  - No parentheses anywhere.
  - Turn quoted speech into reported speech where the voice can't signal a quote (Hinton).
  - Keep quotes only for the text messages, which appear on screen.
- **The run-on phone quote (L27):** generate it as its own clip. Lower stability, or read a shortened version, and show the full text on screen.
- **Holds:**
  - 2 s after "Go on. I'll wait."
  - 1.5 s after "So it was…"
  - No pause before "Possibly your mom." Deadpan lands on no pause.
- **Pronunciation:** Allende (ah-YEN-day), LeCun (luh-KUN). Put both in a pronunciation dictionary.
- **"Edit: thanks everyone, we ordered pizza."** reads best at a slightly faster rate. Split it into its own clip if the build supports per-clip speed.

---

## (d) What's working and must be kept

- **The mom-text hook, and the emoji flip.** It's a real scene with stakes, and it's the viewer's own life.
- **"Most people assume it looks your question up somewhere. It doesn't."** A textbook misconception-first beat.
- **"'Word' is close enough for us."** The kind of self-correction that sounds human.
- **The pause-and-try phone moment**, and "Yours will be different, because it learned from your texts."
- **The barista, especially "Most days they're right. Some days you wanted tea."** This is deadpan done right.
- **"Good enough that it stops feeling like guessing."**
- **"Autocomplete did that."** Short, earned and conversational.
- **"Jay swears he hates pasta"** and **"Edit: thanks everyone!"** Specific, funny and not generic.
- **"It's predicting what a good answer sounds like, and most of the time that's also what's true."** This is the takeaway spine; don't touch it.
- **The ban list is clean.** None of Here's the thing / Honestly / Let's / basically / scary good appear.

---

## (e) Bold idea: run a de-AI "ear test" before recording

Make the checklist executable. Have Claude write a small linter (`deai_lint.py`) that runs over every script before any ElevenLabs call and prints line-numbered flags for:
- **Banned phrases:** the skill's list, plus the Kobak/Wikipedia verbs and adjectives: genuinely, literally, delve, crucial, testament, showcase.
- **Constructions:** `no X, no Y, just Z` and `not X, (but) Y` regexes, and three-item comma lists.
- **Unspeakables for TTS:** parentheses, digits and symbols.
- **Length and pace:**
  - any sentence over 25 words, or three or more fragments in a row;
  - predicted runtime at the channel's measured 162 wpm against the stated length;
  - any first-person past-tense sentence ("I", "my", "mine" plus a past verb) not inside `[FILL]`, flagged as "personal claim, confirm it's real".

It costs nothing, runs in the creator's no-edit, phone-only workflow, and would have caught 9 of the 12 flags in this review automatically. That frees each human or panel pass for what a linter can't do: jokes, scenes and opinions.
