# Expert 4: Fact-check and technical accuracy (slug: factcheck)

Reviewer lens: ML researcher, plus how YouTube comment sections "well actually" AI explainers.
Materials checked: `script3_v2.txt` line by line, `v3/slides.json`, and all 12 contact sheets (`pack/strip-01..12.jpg`) for on-screen claims.

Note on method: several primary sites (cbsnews.com, npr.org, jackcook.com, deepmind.google, techcrunch.com, imo-official.org) are blocked by this sandbox's egress proxy. I checked those through search-engine extracts of the same pages and through secondary reporting that quotes them. anthropic.com was fetched directly.

---

## (a) Research findings

### What gets AI explainers "well actually"-ed in comments
1. **"It's just next-word prediction" with no mention of post-training.** Practitioners now push back hard on this. Pretraining gives you a document-continuer. The assistant you use comes from further training, and much of that is reinforcement learning, which scores whole answers rather than predicting the next word of a document. Sources: [LessWrong, "Next token prediction is a misleading term"](https://www.lesswrong.com/posts/9FWuxzTqvzMa3TqCF/next-token-prediction-is-a-misleading-term); ["Next-token predictor is the wrong mental model" (Sept 2026)](https://gmcgoldr.github.io/2026/09/04/llm-next-token-predictors.html); [arXiv 2408.04666, "LLMs are Not Just Next Token Predictors"](https://arxiv.org/pdf/2408.04666). The script already covers post-training in slide 9, so the risk is only where it credits big achievements (IMO, reasoning) to "autocomplete" alone.
2. **"It doesn't know anything" / "it can't look things up."** Commenters point out two things: facts are stored in the weights, and ChatGPT has search, memory and file tools. The v2 script handles search well; the v3 hook card ("ChatGPT doesn't know anything") does not.
3. **Stale or cherry-picked failure examples.** "ChatGPT says Sydney is the capital of Australia" is exactly the kind of example viewers test live and then post "mine said Canberra." The best explainers use failure cases that are documented, like the Tidewater list, rather than invented ones.
4. **Attributing a result to the wrong system.** "ChatGPT got IMO gold" is wrong on three counts. It was experimental models, Google's result was the only one the IMO certified, and they tied at the gold cutoff.
5. **Anthropomorphic verbs.** Words like "lies", "knows" and "understands" draw pile-ons from both camps. Hedged verbs ("can be planning", "seems to") defuse this, and the v2 script mostly uses them already.
6. **How strong creators handle this:** they attribute claims out loud ("according to…") and pin a corrections comment, which is Cunningham's Law used on purpose ([Wikimedia, Cunningham's Law](https://meta.wikimedia.org/wiki/Cunningham's_Law)). YouTube also has a Studio "Corrections" card for edits after publishing ([overview](https://blog.kdcc.social/yyoutube-corrections-feature/)).
7. **Reference explainers that hold up under scrutiny:** [3Blue1Brown, "LLMs explained briefly"](https://www.3blue1brown.com/lessons/mini-llm/) explains pretraining and then RLHF, samples less-likely words, and uses no absolutes. Karpathy calls a base model an "internet document simulator" ([summary](https://lktuan.github.io/blog/2024-12-12-intro-llm/)). The v2 slide 9 matches this framing well.

### Claim-by-claim verification

| # | Claim (script v2) | Verdict | Source | Safer, still-punchy wording |
|---|---|---|---|---|
| 1 | "The chunks are called tokens, which are bits of words… 'word' is close enough" | **Accurate** | [OpenAI Help: tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them): about 4 characters, or about ¾ of a word, per token | Keep. Optional tweak: "…bits of words, sometimes whole words…" |
| 2 | "For a normal answer it goes around that loop a few hundred times" | **Accurate** | Same source: 100 tokens ≈ 75 words, so a 300-word reply ≈ 400 tokens. Reasoning models also run thousands of hidden "thinking" tokens ([hidden-token audit, arXiv 2508.00912](https://arxiv.org/pdf/2508.00912)) | Keep. |
| 3 | "When the text streams in… you're literally watching it happen" | **Needs light hedge** | Streaming does show tokens as they are generated, but "thinking" models do hidden work first | "When the text streams in on your screen, you're watching that loop happen." |
| 4 | "There's no answer sheet in there that it checks. It predicts…" | **Accurate, but it invites the "facts live in the weights" reply** | 3Blue1Brown; Karpathy | "There's no answer sheet it flips to. Whatever it 'knows' is baked into how it guesses." |
| 5 | "(Unless you see it searching the web… That's a different trick, and we'll get to it.)" | **Broken promise.** Web search never comes back in v2 | script v2 | "That's a different trick, and it gets its own video." |
| 6 | "Apple's is around 34 million settings" | **Needs hedge.** This is reverse-engineered, not published by Apple, and it is the iOS 17 (2023) model | [Jack Cook, Sept 2023](https://jackcook.com/2023/09/08/predictive-text.html): GPT-2-style, about 34M parameters, 15k vocab. Also [Simon Willison](https://simonwillison.net/2024/Jun/3/transformer-powered-predictive-text/) | "When someone cracked open Apple's keyboard model in 2023, it had about 34 million settings." |
| 7 | "The ones behind ChatGPT are thousands of times bigger" | **Needs hedge.** OpenAI doesn't publish sizes. Estimates run GPT-4o ≈ 200B (≈6,000×) but GPT-4o-mini ≈ 8B (only ≈235×) | [Microsoft MEDEC paper, estimates only](https://arxiv.org/pdf/2412.19260) | "The ones behind ChatGPT are likely thousands of times bigger. OpenAI doesn't say exactly." |
| 8 | "Yours will be different, because it learned from your texts" | **Needs hedge.** The base model is trained on general text; it then adapts on-device to your typing | [Apple Support: predictive text](https://support.apple.com/guide/iphone/use-predictive-text-iphd4ea90231/ios) | "Yours will be different, partly because it learns from how you type." |
| 9 | Barista who's served ten million people | **Accurate as an analogy.** It is framed as "Picture…", so it's fine. One nit: no real barista reaches 10M, but the hypothetical framing covers it | n/a | Keep. |
| 10 | "More writing than a person could read in thousands of lifetimes" | **Accurate, even conservative** | [Meta: Llama 3 trained on 15T+ tokens](https://ai.meta.com/blog/meta-llama-3/). 15T tokens ≈ 11T words. Reading nonstop at 250 wpm for 80 years ≈ 10.5B words, so about 1,000 nonstop lifetimes, and tens of thousands at a realistic reading pace | Keep. |
| 11 | "In 2025, AI built on this same predict-the-next-word idea sat the International Math Olympiad…" | **Needs hedge.** These were experimental reasoning models with heavy extra RL training and long thinking time, not ChatGPT, and they didn't "sit" as entrants | [DeepMind](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/): IMO coordinators graded it; Dolinar: "We can confirm… 35 out of a possible 42 points — a gold medal score." OpenAI's run was graded by 3 ex-medalists it hired, not the IMO ([TechCrunch](https://techcrunch.com/2025/07/21/openai-and-google-outdo-the-mathletes-but-not-each-other), [Sequoia recap](https://inferencebysequoia.substack.com/p/the-2025-imo-winners-circle-how-three)) | "In 2025, experimental AIs built on this same next-word engine, plus a lot of extra training to reason, took the actual International Math Olympiad problems…" |
| 12 | "wrote full proofs in plain English, under the same time limits" | **Accurate** | DeepMind: "end-to-end in natural language… within the 4.5-hour competition time limit" | Keep. |
| 13 | "scored right at the gold-medal line" | **Accurate.** 35/42, and the cutoff was 35 | [IntuitionLabs summary](https://intuitionlabs.ai/articles/ai-reasoning-math-olympiad-imo); [CBS](https://www.cbsnews.com/news/humans-beat-ai-technology-google-openai-math-olympiad-machines-catching-up/) | Keep, and add who certified it (see Top 5 #2). |
| 14 | "Plenty of kids still beat it" | **Accurate but vague.** The exact number is stronger | 26 of about 630 contestants scored higher; 5 got perfect 42s ([IntuitionLabs](https://intuitionlabs.ai/articles/ai-reasoning-math-olympiad-imo)) | "Twenty-six kids still beat it, but come on." |
| 15 | "Autocomplete did that." | **Needs hedge.** This is the most "well actually" line in the script (RL, not plain autocomplete) | see #11 | "Souped-up autocomplete did that." |
| 16 | "Nobody wrote detective rules… Getting really good at the next word forced it to pick that stuff up" | **Needs hedge.** "Forced" overclaims, and post-training also shapes reasoning | [LessWrong](https://www.lesswrong.com/posts/9FWuxzTqvzMa3TqCF/next-token-prediction-is-a-misleading-term) | "Getting really good at the next word pushed it to pick up some of that, because it helps with the guessing." |
| 17 | Anthropic "rabbit": planned the rhyme before writing line 2 | **Accurate** | [Anthropic, "Tracing the thoughts of a large language model" (Mar 2025)](https://www.anthropic.com/research/tracing-thoughts-language-model). Model: Claude 3.5 Haiku. Poem: "He saw a carrot and had to grab it, / His hunger was like a starving rabbit." Suppressing "rabbit" gave "habit"; injecting "green" gave a line ending in "green". Caveat from the paper: the method "only captures a fraction of the total computation" | "…researchers at Anthropic looked inside their own model, Claude, while it wrote a rhyming poem… and when they switched 'rabbit' off, it rhymed with 'habit' instead." The switch-off is the proof beat, so use it. |
| 18 | Hinton: "to predict the next word, you have to understand the sentences." | **Accurate (verbatim)** | [CBS 60 Minutes transcript, Oct 2023](https://www.cbsnews.com/news/geoffrey-hinton-ai-dangers-60-minutes-transcript/): "Well, it's true they're just trying to predict the next word. But if you think about it, to predict the next word you have to understand the sentences." | Keep. Optional: "Geoffrey Hinton, who won a Nobel Prize for this stuff…" (Physics 2024). Put "60 Minutes, 2023" on screen. |
| 19 | "Plenty of researchers… call it a very fancy parrot" | **Needs attribution** | [Bender, Gebru, McMillan-Major, Shmitchell, "On the Dangers of Stochastic Parrots," FAccT 2021](https://dl.acm.org/doi/10.1145/3442188.3445922) | "Others, like linguist Emily Bender, call these models 'stochastic parrots'. Basically, very fancy parrots." |
| 20 | "Straight out of training, a model… just keeps writing… like a forum post" | **Accurate, with one hedge.** The forum text is illustrative, and the first stage is pre-training | Karpathy's "internet document simulator"; [InstructGPT](https://arxiv.org/abs/2203.02155) | "Straight out of its first round of training, a model like this doesn't answer you…" Label the forum text on screen "(illustration)". |
| 21 | "train it again, on examples of good answers that real people rated" | **Needs light fix.** This merges two steps: people write example answers (SFT), then people rank the model's answers (RLHF) | [InstructGPT (arXiv 2203.02155)](https://arxiv.org/abs/2203.02155); [3Blue1Brown](https://www.3blue1brown.com/lessons/mini-llm/) | "So the companies train it again, on answers real people wrote, and answers real people rated…" |
| 22 | Tidewater Dreams / Isabel Allende / two real newspapers / 2025 | **Accurate** | [NPR, May 20 2025](https://www.npr.org/2025/05/20/nx-s1-5405022/fake-summer-reading-list-ai); [Philadelphia Inquirer](https://www.inquirer.com/news/king-features-artificial-intelligence-book-list-20250520.html); [Snopes](https://www.snopes.com/fact-check/chicago-sun-times-ai-reading-list/). Chicago Sun-Times plus at least one Inquirer edition, via King Features' "Heat Index" insert; 10 of 15 books were fake; the freelancer admitted using AI. Don't name a specific chatbot, because reports differ | "…two real newspapers printed a summer reading list where ten of fifteen books didn't exist. Like Tidewater Dreams, by Isabel Allende." |
| 23 | "the lawyers, judges and airlines who trusted it anyway" | **Wrong in detail.** It was one airline, and the Air Canada ruling never says the bot was generative AI (per `research.md`) | [CBS on Moffatt v. Air Canada](https://www.cbsnews.com/news/aircanada-chatbot-discount-customer/) | "…and the lawyers and judges who trusted it anyway. Plus one airline chatbot that invented its own refund policy." |

### On-screen claims in v3 frames (visuals that will be reused)

| Time | On screen | Verdict | Fix |
|---|---|---|---|
| 0:00–0:17 | "ChatGPT doesn't know anything." | **Wrong / bait.** This is the #1 comment-war trigger, and v2 deliberately doesn't take a side | Retire it, or change to "ChatGPT doesn't look anything up." |
| 0:03–0:17 | "It's guessing. One word at a time." | Needs hedge | "It's predicting. One chunk at a time." |
| 0:40–0:50 | Paris 94% / beautiful 4% / Lyon 2% | Invented numbers presented as data | Add a small caption: "illustrative odds" |
| 0:58 | "× hundreds · super fast" | Accurate | Keep |
| 1:20 | "Your phone is guessing too. It's just really bad at it." | Fair | Keep, maybe change to "…it's just tiny." |
| 1:28–1:39 | Label "YOUR PHONE: YOUR TEXTS" | **Wrong-ish** (see #8) | "YOUR PHONE: TINY MODEL + YOUR TYPING" |
| 1:30 | "CHATGPT: BOOKS, SITES, FORUMS, CODE" | Accurate | Keep |
| 1:37 | "More reading than any human could do in thousands of lifetimes" | Accurate | Keep |
| 2:02–2:14 | "To guess well, you have to understand a lot." | Contested (the Hinton side, stated as fact) | Put it in quote marks with a "Hinton" credit, or change to "To guess well, you have to pick up a lot." |
| 2:28 | "Nobody programmed it in. It got absorbed." | Fine | Keep |
| 2:34–2:55 | "Taught manners" / "Examples of great answers" / "Rated by people" / "Raw text predictor → Helpful assistant" | Accurate, and matches InstructGPT | Keep (the two labels match fix #21 exactly) |
| 3:04 | "It predicts what *sounds* right. It doesn't look it up." | Accurate for the base loop, but needs the search caveat | "…It doesn't look it up (unless it's searching the web)." |
| 3:14–3:22 | "What's the capital of Australia? → It's Sydney 61% / WRONG." | **Misleading.** Current ChatGPT answers Canberra, so viewers will test it and call it fake | Replace with the Tidewater Dreams book card, which is a documented, real failure, or caption "small/older model, illustration" |
| 3:24–3:31 | "Why AI lies with a straight face" / "It once made up a whole court case." | "Lies" implies intent; the court claim undercounts | "Why AI makes stuff up with a straight face" / "It once invented six court cases. A lawyer filed them." (Mata v. Avianca) |

---

## (b) Score: 7.5 / 10 for factual accuracy

Strengths: the script is well sourced. The Hinton quote is verbatim, the rabbit study is described exactly, the IMO score and time limit are right, "thousands of lifetimes" is conservative, and Tidewater Dreams is real. The web-search caveat and the "at the basic level" framing are smart.

What holds it back:
- One sentence credits IMO gold to plain "autocomplete". It is the biggest target for ML commenters.
- There are two broken or overstated details: the promise to come back to web search, and "airlines".
- A few claims need attribution: Apple's 34M, "thousands of times bigger" and "fancy parrot".
- The reused v3 visuals carry the two most attackable claims in the whole package: "ChatGPT doesn't know anything" and the Sydney example.

---

## (c) Top 5 changes, ranked by impact

1. **Slide 6, the IMO claim, is the biggest "well actually" magnet.** Replace "In 2025, AI built on this same predict-the-next-word idea sat the International Math Olympiad… Plenty of kids still beat it, but come on. Autocomplete did that." with:
   > "In 2025, experimental AIs built on this same next-word engine, plus a lot of extra training to reason, took the actual International Math Olympiad, the one for the smartest teenagers on the planet. They wrote full proofs in plain English, under the same four-and-a-half-hour limits, and Google's scored exactly at the gold-medal line, confirmed by the Olympiad's own graders. Twenty-six kids still beat it, but come on. Souped-up autocomplete did that."

   On screen: "35/42 · gold cutoff 35 · IMO-graded (Google DeepMind)". Add a small "OpenAI: also 35, self-graded" tag.
2. **Kill the two worst reused visuals.** Remove the 0:00 "ChatGPT doesn't know anything" card entirely. Swap the 3:14 "capital of Australia → Sydney" scene for the Tidewater Dreams card, a documented failure that fits slide 10. If the Sydney scene is kept, caption it "illustration".
3. **Slide 3, promise and answer-sheet line.**
   - Replace "That's a different trick, and we'll get to it." with "That's a different trick, and it gets its own video."
   - Replace "There's no answer sheet in there that it checks." with "There's no answer sheet it flips to. Whatever it 'knows' is baked into how it guesses."
   - Replace "you're literally watching it happen" with "you're watching that loop happen."
4. **Slide 4, attribute the phone numbers.**
   - "When someone cracked open Apple's keyboard model in 2023, it had about 34 million settings. The ones behind ChatGPT are likely thousands of times bigger. OpenAI doesn't say exactly. And that's where it gets weird."
   - "Yours will be different, partly because it learns from how you type."
   - Change the v3 label "YOUR PHONE: YOUR TEXTS" to "YOUR PHONE: TINY MODEL + YOUR TYPING".
5. **Slides 8–10, attribution and precision.**
   - "…looked inside their own model, Claude, while it wrote a rhyming poem… And when they switched 'rabbit' off, it rhymed with 'habit' instead."
   - "Others, like linguist Emily Bender, call these models 'stochastic parrots'. Basically, very fancy parrots."
   - "So the companies train it again, on answers real people wrote, and answers real people rated…"
   - Closing line: "…and the lawyers and judges who trusted it anyway. Plus one airline chatbot that invented its own refund policy. I gotchu."
   - v3 card: "Why AI makes stuff up with a straight face." Subline: "It once invented six court cases. A lawyer filed them."

---

## (d) Keep (already accurate and well judged)
- The Hinton quote. It is verbatim; keep the exact wording.
- "At the basic level, yes. It is autocomplete. It's just not the kind you think." True at inference time, and the hedge is honest.
- The web-search caveat in brackets.
- "Thousands of lifetimes" and "a few hundred times". Both check out.
- Slide 9, raw model to assistant. It matches Karpathy and InstructGPT, and the v3 "Examples of great answers / Rated by people" labels are exactly right.
- "It can be planning where the sentence is going." Good hedged verb.
- Tidewater Dreams. It is real, vivid and sourced.
- "Smart people are still fighting about this one." Accurate, and it drives comments without taking a side.
- The description's source list. Keep it and add the Philadelphia Inquirer and the Sequoia/IntuitionLabs IMO link.

## (e) Bold idea: "Receipts" corner tag plus a pinned "Try to break it" comment
Every factual beat gets a tiny animated receipt tag in the lower right, 1.5s, mono 18px, in the existing chip style. Examples:
- "60 Minutes, 2023"
- "Anthropic, Mar 2025"
- "IMO graders, Jul 2025"
- "NPR, May 2025"
- "reverse-engineered, iOS 17"

It is built as one reusable GSAP chip (opacity plus y-transform only). It signals rigor to exactly the viewers most likely to nitpick. It also turns "source?" replies into "oh, they cited it."

Pair it with a pinned comment the creator posts at launch: "Found a mistake? Tell me. Best correction gets pinned and credited in the next video." This is Cunningham's Law on purpose: nitpicks become engagement instead of reputational damage, and it seeds Script 4's credibility.
