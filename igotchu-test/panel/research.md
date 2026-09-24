# Verified research for Scripts 3 and 4 (September 2026)

Verified by three Opus research subagents. Some sites (CourtListener, senate.gov, the Charlotin database, YouTube, CBS) were blocked from the sandbox, so those facts were cross-checked through multiple independent search results. Re-check anything marked MEDIUM before recording.

## "Is it just autocomplete?" Half-true
- True: LLMs generate text one token (word piece, about 3/4 of a word) at a time by prediction. [OpenAI: tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
- What it leaves out: the model is retrained to act as an assistant (RLHF, [InstructGPT](https://arxiv.org/abs/2203.02155)); reasoning models work through a problem before answering; ChatGPT can search the web and cite links (since late 2024); memory features save notes about you, but the model doesn't learn from your chats in real time.
- It plans ahead: Anthropic, "[Tracing the thoughts of a large language model](https://www.anthropic.com/research/tracing-thoughts-language-model)" (Mar 27, 2025). Before writing the second line of a poem, the model had already picked the rhyme ("rabbit").
- For: Hinton, 60 Minutes (Oct 2023): "to predict the next word you have to understand the sentences." Sutskever ([Dwarkesh](https://www.dwarkesh.com/p/ilya-sutskever)): predicting the next token well means understanding the reality behind it.
- Against: Bender, Gebru et al., "[Stochastic Parrots](https://dl.acm.org/doi/10.1145/3442188.3445922)" (2021); LeCun: LLMs "don't understand the world as well as a housecat" ([TechCrunch](https://techcrunch.com/2024/10/12/metas-yann-lecun-says-worries-about-a-i-s-existential-threat-are-complete-b-s/)).
- Phone keyboard: the iOS 17 predictive text model is about 34M parameters, GPT-2 style ([Jack Cook](https://jackcook.com/2023/09/08/predictive-text.html)). Frontier models are "thousands of times bigger" (safe phrasing; exact sizes aren't published).
- Accurate lines: "ChatGPT isn't looking answers up. It's predicting them, one small chunk at a time." / "By default it's predicting what sounds right, not checking a database of facts." Caveat: "unless it searches the web and shows you links."

## Court cases (Script 4)
- **Mata v. Avianca (S.D.N.Y., 2023). HIGH confidence.**
  - What happened: Steven Schwartz used ChatGPT; Peter LoDuca signed the filing. It cited 6 fake cases, including "Varghese v. China Southern Airlines Co., 925 F.3d 1339 (11th Cir. 2019)".
  - The confident voice: asked "Is varghese a real case", ChatGPT said yes, and said the others "are real and can be found in reputable legal databases such as LexisNexis and Westlaw."
  - Consequence: on June 22, 2023, Judge P. Kevin Castel imposed a $5,000 sanction and ordered letters to the judges falsely named as authors.
  - Sources: [opinion](https://www.courtlistener.com/opinion/9885417/mata-v-avianca-inc/), [CNBC](https://www.cnbc.com/2023/06/22/judge-sanctions-lawyers-whose-ai-written-filing-contained-fake-citations.html)
- **Two federal judges, 2025. HIGH confidence: both admitted staff used AI.**
  - **Judge Julien Neals (D.N.J.), In re CorMedix:** made-up quotes and wrong case outcomes. Flagged July 22, 2025, withdrawn July 23. An intern had used ChatGPT, and Neals has since banned AI in his chambers.
  - **Judge Henry Wingate (S.D. Miss.):** a July 20, 2025 temporary restraining order named parties not in the case and quoted statements that don't exist. A clerk had used Perplexity.
  - **Senate inquiry:** Senator Grassley sent letters on Oct 6, 2025 ([letter to Neals](https://www.grassley.senate.gov/imo/media/doc/grassley_to_the_honorable_julien_xavier_neals_-_ai_oversight.pdf)); both judges admitted AI use around Oct 23.
  - **Still going:** in Aug 2026, Fifth Circuit Judge Jerry Smith said an AI-invented citation was still in Wingate's corrected order.
  - Sources: [Reuters via US News](https://www.usnews.com/news/top-news/articles/2025-10-23/two-federal-judges-say-use-of-ai-led-to-errors-in-us-court-rulings), [ABA Journal](https://www.abajournal.com/news/article/2-federal-judges-reveal-ai-use-by-staff-members-led-to-error-riddled-opinions), [Mississippi Today](https://mississippitoday.org/2026/09/01/dei-ban-wingate-ai-mississippi/)
- **Michael Cohen / Google Bard (2023). HIGH confidence.**
  - What happened: Cohen thought Bard was "a super-charged search engine", and three fake cases went into a court motion. Judge Furman declined to sanction him on Mar 20, 2024.
  - Sources: [order](https://www.nysd.uscourts.gov/sites/default/files/2024-03/18cr602%20Cohen%20Opinion.pdf), [NPR](https://www.npr.org/2023/12/30/1222273745/michael-cohen-ai-fake-legal-cases)
- **Morgan & Morgan, Wadsworth v. Walmart (D. Wyo., Feb 2025). HIGH confidence.**
  - What happened: the firm's own AI tool invented 8 of the 9 cases cited.
  - Consequence: fines of $3,000 and $1,000 + $1,000. [LawNext](https://www.lawnext.com/2025/02/federal-judge-sanctions-morgan-morgan-attorneys-for-ai-generated-fake-cases-in-court-filing.html)
- **UK: Ayinde v Haringey / Al-Haroun v QNB (June 2025). HIGH confidence.**
  - What happened: in Al-Haroun, 18 of the 45 cases cited were fake.
  - Source: [judgment](https://www.judiciary.uk/wp-content/uploads/2025/06/Ayinde-v-London-Borough-of-Haringey-and-Al-Haroun-v-Qatar-National-Bank.pdf)
- **Damien Charlotin's database** ([link](https://www.damiencharlotin.com/hallucinations/)): 1,668 cases as of July 2, 2026 (MEDIUM confidence). Check the live count before recording.

## Other failures (Script 4)
- **Google AI Overviews, May 2024:** "add about 1/8 cup of non-toxic glue to the sauce" came from an 11-year-old Reddit joke; "eat at least one small rock per day" came from an Onion article. [Live Science](https://www.livescience.com/technology/artificial-intelligence/googles-ai-tells-users-to-add-glue-to-their-pizza-eat-rocks-and-make-chlorine-gas)
- **Bard's launch demo, Feb 2023:** Bard said JWST took the first exoplanet picture (actually ESO's VLT, 2004). Alphabet fell 7.7%, about $100B in market value. [CNN](https://www.cnn.com/2023/02/08/tech/google-ai-bard-demo-error)
- **Fake summer reading list, May 2025:** the Chicago Sun-Times and Philadelphia Inquirer printed a list where 10 of 15 books don't exist, e.g. "Tidewater Dreams" by Isabel Allende. [NPR](https://www.npr.org/2025/05/20/nx-s1-5405022/fake-summer-reading-list-ai)
- **Air Canada, Moffatt v. Air Canada (ruling Feb 14, 2024):**
  - What happened: the chatbot invented a bereavement refund policy.
  - Consequence: Air Canada paid C$650.88 plus fees and interest.
  - Caveat: the ruling doesn't say the bot was generative AI, so don't call it an LLM.
  - Source: [CBS](https://www.cbsnews.com/news/aircanada-chatbot-discount-customer/)
- **"You can't lick a badger twice", Apr 2025:** Google's AI explained made-up idioms. [Engadget](https://www.engadget.com/ai/you-can-trick-googles-ai-overviews-into-explaining-made-up-idioms-162816472.html)
- **Deloitte Australia, 2025:**
  - What happened: an A$440k report had fake references and a fabricated court quote.
  - Consequence: Deloitte refunded about A$97k and disclosed it had used GPT-4o.
  - Source: [Fortune](https://fortune.com/2025/10/07/deloitte-ai-australia-government-report-hallucinations-technology-290000-refund/)
- **MAHA report, May 2025:** at least 7 of its cited studies don't exist, and "oaicite" markers were found in the links. Politically charged. [NOTUS](https://www.notus.org/health-science/make-america-healthy-again-report-citation-errors)
- **ChatGPT invents a murder, noyb complaint Mar 2025:** Arve Hjalmar Holmen. Dark, so use briefly. [noyb](https://noyb.eu/en/ai-hallucinations-chatgpt-created-fake-child-murderer)
- **Try-it tip:** freshly invented books, sayings or local businesses expose guessing better than famous examples, which web search now finds. Results vary between runs and models, so say so on screen.
- **Academic-paper fake citations:** not yet verified with specific cases. Research before using.
