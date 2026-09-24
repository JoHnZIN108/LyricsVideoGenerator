# Art direction review: igotchu Script 3 (v3 build → v2 plan)

Reviewer: Expert 6, visual art director / design-system lead (slug `artdirector`)
Scope: composition, typography, colour, hierarchy, illustration style, brand consistency, phone legibility.
Materials read: all 12 `pack/strip-*.jpg`, `motion-morph-4fps.jpg`, `v3/snaps*/` contact sheets plus full-res frames at 5s, 81.14s, 115.82s and 133.1s, `v3/ds/*`, the three illustration PNGs, and the theme CSS in `build_v3.py` (lines 637–960).

---

## (a) Research findings

Note: the egress proxy blocked most article pages (medium.com, aescripts, legibility.info, stensyl, BBC), so several findings below come from search-result summaries of those pages. The sources are still named so the creator can check them.

1. **Kurzgesagt: a small shape vocabulary and a disciplined palette are the brand.** The style is built from rounded geometric shapes, flat fills and vivid but limited colour, and a full in-house team keeps it consistent across hundreds of videos. Their own "How to Kurzgesagt (3/3): Using Color & Contrast" makes contrast the organising tool. Takeaway: consistency comes from a *small, locked vocabulary*, not from a detailed style.
   [Wikipedia: Kurzgesagt](https://en.wikipedia.org/wiki/Kurzgesagt) · [How to Kurzgesagt 3/3](https://www.youtube.com/watch?v=_VrNiya8kLg) · [U-Michigan: "Simple, Bright, Beautiful"](https://artsatmichigan.umich.edu/ink/2019/09/27/simple-bright-beautiful-the-work-of-kurzgesagt)
2. **Vox: "animations explain rather than decorate."** Every visual answers what the narrator just said. The look combines bold geometric headline type, paper/halftone texture and one consistent palette per video, and the motion is synced to the narration.
   [PremiumBeat: 5 breakdowns of the Vox look](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/) · [DEmotion: why your motion graphics never look like Vox](https://trydemotion.com/blog/motion-graphics-like-vox)
3. **Johnny Harris: tangibility.** Maps and collages built in After Effects + GEOlayers get texture overlays, grain and physical-feeling camera moves. The "premium" signal is the sense that a *real object* is being filmed, not a UI.
   [aescripts: How Johnny Harris makes maps](https://aescripts.com/learn/post/how-johnny-harris-makes-maps) · [Motion Array: Johnny Harris style tips](https://motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/)
4. **PolyMatter / Wendover: legibility and labels over spectacle.** They use a unified palette, flat assets and on-screen labels, and the style is recognisable from the thumbnail alone.
   [ad-hoc-news: PolyMatter and the animated explainer](https://www.ad-hoc-news.de/boerse/news/ueberblick/polymatter-and-the-footprint-of-animated-explainers-on-youtube/69642572)
5. **Apple keynote rules.** One idea per slide, about 7 words maximum, a number big enough that it needs no chart, generous empty space (60%+), and an accent colour used *once* per slide.
   [PJ Camillieri, "This is how we make slides at Apple"](https://medium.com/adventures-in-consumer-technology/this-is-how-we-make-slides-at-apple-b8a84352bf6d) · [SlideSpeak keynote-minimal breakdown](https://slidespeak.co/slide-design-prompts/prompts/keynote-minimal)
6. **Phone legibility numbers.**
   - BBC subtitle guideline: line height = 8% of active video height, about 86px at 1080p.
   - General floor for text on 1080p: 40–60px for body, titles at least 1.5× body, captions no smaller than about 44px.
   - Keep text inside the centre 90% × 80%.

   [Clevercast: BBC subtitle guidelines](https://www.clevercast.com/bbc-subtitling-guidelines/) · [vsubtitle: font size and reading speed](https://vsubtitle.com/subtitle-font-size-and-reading-speed-2026/) · [ConvertAudioToText: subtitle readability rules](https://convertaudiototext.com/blog/subtitle-styling-best-practices)
7. **Contrast.** WCAG 2.2 AA asks for 4.5:1 for normal text, 3:1 for large text, and 3:1 for meaningful graphics (SC 1.4.11).
   [W3C: Understanding 1.4.11](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html) · [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/)
8. **AI illustration consistency.** Wiring *one* strong reference image into every generation beats prompt tweaking. Lock the reference file, lock the wording, restate the style with several reinforcing descriptors, and never change core features mid-project.
   [Christy Tucker: consistent style with --sref](https://christytuckerlearning.com/ai-images-with-consistent-style-in-midjourney/) · [Stensyl: reference images for style consistency](https://stensyl.ai/blog/reference-images-ai-style-consistency) · [Mighty Loka: prompt patterns](https://mightyloka.com/blog/2_ai_prompt_patterns/)
9. **"Premium" versus "template."**
   - "Dark background plus glow" became the *default* look of AI and crypto launches. The glow carries no meaning and now reads as generic.
   - Premium comes from system and restraint: few fonts, few colours, minimal effects, and a clear first/second/third read.

   [Jason Tham: the gradient trend vs design efficacy](https://jasontham.com/2026/05/24/the-gradient-trend-vs-design-efficacy/) · [Evoke: what makes a site look expensive](https://madebyevoke.com/blog/what-makes-a-website-look-expensive) · [Webwavers: premium design elements](https://webwavers.de/en/blog/website-design-elemente-premium)

**What this means for igotchu.** The top explainers win on three things: (1) one locked visual vocabulary, (2) every frame answering the narration, and (3) restraint in chrome and effects. Their "premium" never comes from glow.

---

## (b) Score: 5/10 for art direction

**What earns points**
- The design system on paper is excellent: tokens, contrast table, 28px floor, safe zones, one-glow rule, colour semantics (cyan = AI, orange = human/emphasis). That is better documentation than most channels ever write.
- The **code-built** scenes are the strongest frames in the video: the probability bars (0:28–0:50), the loop card (0:51–1:01), the phone keyboard (1:03–1:17) and the Sydney/Canberra bars (3:14–3:22).

**What costs points**
1. **Three illustration styles in one video, none matching the written rules:**
   - `brain-library.png` (1:22–1:39) is a stock-3D perspective render. It adds teal and green bubbles outside the palette and uses the cliché orange/blue brain.
   - `glass.png` (2:02–2:15) is a glowing wireframe tech poster, with a brain again.
   - `manners.png` (2:34–2:51) is a Corporate-Memphis cartoon with a smiling robot mascot, a man's face and yellow stars. It breaks rules 3 and 8 of `illustration-prompts.md` outright.
   - All three are 1280×720 upscaled 1.5× to 1920, so they are visibly soft next to the razor-sharp live type.
2. **Layout collisions: the execution ignores the system's own safe zones.**
   - The wordmark sits on the keyboard's "123" key (1:18–1:21, full-res frame at 81.14s).
   - The NONSENSE stamp bleeds off the left edge (1:18).
   - The camera push crops the phone out of the top of frame (1:13–1:17).
   - The quote card overlaps the wordmark (2:11–2:14, frame at 133.1s).
   - "More reading than any human…" collides with the pill label (1:37–1:39).
   - "Same bars. Same confidence." sits about 40px from the top edge, outside `safe-y` 96 (3:19–3:22).
   - The WRONG stamp covers the user's question bubble (3:20).
   - The chapter labels run *through* the corner crop marks in every frame.
3. **Dead frames:**
   - Near-empty screen with only a kicker or nothing: 0:22–0:27 (5s), 0:38, 1:02, 1:40, 1:50–1:54 (5s), 2:01, 2:15, 2:21–2:22, 2:56, 3:23.
   - About 16s of 220s (7%) where a phone viewer sees a blue gradient.
4. **Chrome clutter reads as "template":**
   - Always-on corner crop marks, a 44px wordmark bug, a four-label chapter rail, the blueprint grid and glow on most headline words all compete with the content.
   - The kicker pill at 2:02 is stretched to about 760px around roughly 400px of text, a flexbox bug.
5. **Rag and hierarchy:**
   - The hook headline breaks as 4 lines for 4 words ("ChatGPT / doesn't / know / anything.").
   - The subtitle orphans "time."
   - "understand a / lot." (2:02) is a broken rag.
   - `build_v3.py` uses 22 distinct font sizes (22px to 200px), and 22–24px appears on the keyboard labels, below the system's own 28px floor.

---

## Theme verdict: Neon ground + Instrument type (a specific hybrid)

| | Neon (main) | Instrument | Patent |
|---|---|---|---|
| Typography | Archivo Black + Inter: the default "YouTube template" pairing | **Bricolage Grotesque 800 @ 75% width + DM Sans + JetBrains Mono: editorial, confident, the most premium thing in the whole set** | Same type as Instrument |
| Ground | Navy, matches all art and the thumbnail | Light grey paper | Light paper + drafting frame |
| Illustrations | Native | Navy art pasted as a dark window inside a light page (138s, 165s): looks like two videos spliced | Same problem, plus a double border |
| Chrome | Crop marks, grid, glow | Screws, slide dots, "IGOTCHU / EP 03" header: *more* chrome | "SHEET 1 OF 10", "FIG. 1" at 64px: charming once, noise by slide 3 |
| Phone at night | Comfortable | 1080p of near-white in a dark room | Same |
| Contrast | ink 17.4:1; `ink-dim` on the glow centre only 3.85:1 | Accent `#d0165c` on paper 4.7:1 (passes) | Chapter label `#66736c` on paper 4.39:1 (fails AA for small text) |

**Recommendation: "Neon Instrument."**
- Keep Neon's `night` ground, its colour semantics and its illustration world.
- Replace its typography with Instrument's fonts.
- Take Patent's *hatched probability bars* as the one borrowed idea.
- Strip the chrome of all three.

Reasons:
- The dark ground protects the brand and the thumbnails, and fits dark-mode phone viewing.
- The Instrument type removes the biggest "template" signal.
- Nothing needs regenerating to switch.

Concrete token changes (edit `tokens.json` → regenerate `tokens.css`):

```
--font-display: "Bricolage Grotesque"; weight 800; font-stretch 75%   (was Archivo Black)
--font-sans:    "DM Sans" 500/600/700                                  (was Inter)
--font-mono:    "JetBrains Mono" 700, labels/kickers/percentages only  (new)
headline-xl 150px / lh 0.95 / ls -0.02em    (condensed face: +20px keeps the same colour weight, fits ~16 chars/line)
headline    120px / lh 0.98
headline-sm 96px  / lh 1.02
title 64 · body-lg 56 · body 48 · body-sm 40 · label 32 mono · label-sm 30 mono (new floor for readable text)
grid:       rgba(34,211,238,0.045)  (was .09)   grid-fine: 0 (remove)
glow-text-*: only on the ONE payoff word per slide; all other accent words flat colour, no text-shadow
ink-dim:    #8b97c0 (was #7d8ab5) → 4.4:1 on night-glow centre, 6.3:1 on night
All headings: text-wrap: balance;  all body: text-wrap: pretty;   (kills "time." and "a / lot." orphans; Chromium supports both)
```

---

## (c) Top 5 changes, ranked by impact

### 1. One illustration language: at most 2 AI images per video, everything else code-built SVG, and a locked style anchor
**Where:** 1:22–1:39 (brain-library), 2:02–2:15 (glass), 2:34–2:51 (manners).

**Fix:**
- Delete all three from the v2 plan.
- In v2, only **Slide 5 (barista)** gets an AI illustration, and optionally one for Slide 8.
- Everything else is inline SVG in the same line language as the UI: 6px round-capped strokes, cyan/orange on `surface` fills. It is cheaper (0 credits), always consistent, and animatable per part with GSAP.

**Style anchor procedure:**
1. Generate one "anchor" image first.
2. Upload it as the reference for *every* later generation (ElevenLabs `creative_upload_flow_reference` → `connect_from`).
3. Store it at `v3/ds/style-anchor.png` and list it in `illustration-prompts.md` as mandatory.

**Generation size:** generate at 1920×1080 or larger (current art is 1280×720, upscaled 1.5×).

**Replacement prompt template** (tighter than the current one: it bans the failure modes seen in the frames):

> Flat vector illustration, 16:9, orthographic straight-on view, NO perspective depth. [SUBJECT]. Built from at most 12 simple geometric shapes. Uniform 6px line weight, round caps, no shading, no gradients, no texture. Deep navy background #0a1128, flat. Fills only #111b3d and #18265a. Outlines only cyan #22d3ee and orange #ff7a1a. ONE soft glow, around [KEY OBJECT] only. Subject occupies the right 55%; left 45% is empty navy. People are faceless flat silhouettes with no facial features. Match the style of the reference image exactly.
>
> **Negative:** brain, robot, mascot, face, eyes, smile, yellow, gold, stars, teal, green, purple, 3D, isometric city, perspective, lens flare, circuit board, hologram, floating screens, text, letters, numbers, logo.

### 2. Put the recommended type system in, and cut the headline ladder to three sizes
**Where:**
- 0:00–0:17: "ChatGPT / doesn't / know / anything." on 4 lines, "time." orphaned.
- 2:02: "understand a / lot."
- 1:26: "Scale." at 200px, grey mid-fade over the busy building.

**Fix:**
- Apply the "Neon Instrument" tokens above.
- Hook headline: 150px condensed, column width 860px. That gives "ChatGPT doesn't / know **anything.**" on 2 lines, with `text-wrap:balance`.
- Only the payoff word gets `glow-text-*`, and never more than one glowing element per frame.
- No free-floating 200px words over illustrations. A statement word sits on the empty left 45%, or on a `night` scrim `linear-gradient(90deg, #0a1128 0 45%, transparent 70%)`.
- Allowed sizes in `build_v3.py`: 150/120/96/64/56/48/40/32/30. Anything smaller is decorative only (keyboard keys may stay at 24px because they are not read).

### 3. No empty frames: every slide shows something within 0.15s of its start
**Where:** 0:22–0:27, 1:50–1:54 (5s each), plus 0:38, 1:02, 1:40, 2:01, 2:15, 2:21, 2:56, 3:23.

**Fix:**
- Rule in the build: `first reveal = slide_start + 0.15s`.
- For a transition, cross-dissolve 0.25s from the previous slide's *last* frame into the new slide's first element, rather than cutting to the bare gradient.
- For slides that open with a question, the headline is on screen at frame 1 and the supporting card rises at the cue word.
- Build-time assertion: sample every 0.5s and fail if fewer than one text element or SVG has `opacity > 0.5` for more than 0.6s.

### 4. Enforce the safe zones with a layout linter, and fix the listed collisions
**Where and fix:**

| Time | Problem | Fix |
|---|---|---|
| 1:13–1:17 | Camera push crops the phone top | Cap `.cam` scale so the phone bbox stays ≥ 96px from the top, or push to 1.06 max, not about 1.25 |
| 1:18–1:21 | Stamp off the left edge; wordmark on the keyboard | Stamp centred on the phone screen at `left: phoneX + 40px`, rotate −6°, width ≤ 560px |
| 2:11 | Quote card over the wordmark | Card bottom = 1080 − 160px |
| 1:37 | Headline over the "CHATGPT: BOOKS…" pill | Remove the pill (the illustration is being cut anyway) |
| 3:19 | "Same bars. Same confidence." at y ≈ 40px | Set at y = 120px, or put it *below* the card at 64px |
| 3:20 | WRONG stamp over the question bubble | Place it over the "It's Sydney." bubble, which is the thing that is wrong |
| 2:02 | Kicker stretched to ~760px | `.ig-kicker{align-self:flex-start;width:fit-content}` |

**Linter:** add a Playwright step before render. For every text element at every slide's settle time, check `getBoundingClientRect()`:
- inside `128 ≤ x ≤ 1792`, `96 ≤ y ≤ 984`;
- no intersection with any other text box, the wordmark or a stamp;
- exit non-zero on failure.

The creator never edits, so the build has to catch these itself.

### 5. Chrome diet: remove what says "template"
**Where:** every frame.

**Fix:**
- **Crop marks** (`.ig-crops`): remove. They collide with the rail labels in every frame and mean nothing to viewers.
- **Wordmark bug:** remove from the frame and use YouTube's channel watermark setting instead. If one must stay, 32px, top-right at (1760, 72), 50% opacity, hidden on slides with phones or illustrations.
- **Chapter rail:** keep only a 6px progress line at the very bottom (`cyan` fill on `line`). Show the chapter *name* as a 30px mono label for 2.5s only when a chapter changes, then fade it out. Four labels on screen for 220s is dashboard chrome.
- **Grid:** 4.5% opacity, major lines only.

---

## (d) Keep these

- **Colour semantics:** cyan = the AI/answer, orange = the human/emphasis, danger = wrong with a word. It is clear and consistent, and it is the channel's real identity.
- **The probability-bar component** (0:28–0:50, 3:14–3:22). It is the channel's signature visual; make it bigger (label 44px, bar 18px tall, percentage 34px mono) and use Patent's hatch fill for non-winning bars.
- **The phone keyboard scene** (1:03–1:17): real, physical, and the viewer can copy it. Keep it, and use the creator's real screenshot `v3/assets/user/phone-autocomplete-real.png` in v2 Slide 4.
- **Big statement cards** ("That's it? Autocomplete|" with the caret at 1:55): pure Apple-keynote. Keep the typing caret.
- **The design-system docs** (`DESIGN.md`, `tokens.json`, contrast table, 28px floor). The system is right; the build has to obey it.
- **Instrument's typography**, per the recommended hybrid.
- **The end card layout** (3:32–3:40).

---

## (e) Bold idea: make the cursor the mascot

Every great explainer channel has one recurring object (Kurzgesagt's bird, Vox's highlighter). igotchu's should be **the cyan text caret**: a 12×120px cyan bar, the literal "what comes next" of the video's thesis.
- It blinks in the corner of the thumbnail.
- It *is* the transition: each slide ends with the caret sliding across the frame at 1400px/s and wiping in the next slide behind it (a GSAP `x` tween plus a `clip-path` or mask).
- It types every headline's payoff word.
- It shows up inside every illustration as the key glowing object.
- In the sign-off, "I gotchu" is typed by it and it blinks twice.

It costs nothing, it is pure code, and after three videos viewers will know an igotchu frame from a 200px crop. That is the thing a template can never have.

---

## Scene-by-scene visual plan for script v2 (10 slides)

Timings are estimates at about 150 wpm (about 4:40 total). Everything is code-built unless marked **AI**. "Payoff glow" means the only glowing element on that slide.

| # | Beat | Layout and elements | Colour roles | Motion cues (spoken word → action) |
|---|---|---|---|---|
| 1 (~30s) | Mom's text | **Lock-screen crop**, not a whole phone. Night-blue wallpaper; time "7:04" at 150px mono-light, centre-top (y 180); notification card 1100×180 at y 420: "Mom" 32px label + "Call me when you get a sec." 56px `ink`. At "next five minutes" three ghost thought cards fan out below (40px `ink-muted`, `surface` fill): "Somebody's sick?", "Forgot a birthday?", "Something happened?" | Notification `ink` on `surface`; thought cards no accent; the payoff line gets the only glow | "texts you" → card drops 60px with 0.45s ease-out; "already written" → cards stagger 0.15s; "how ChatGPT works" → cards blur out, caret blinks at the end of the text |
| 2 (~22s) | Party emoji | Same notification, same position (continuity). A **drawn SVG party popper** (6px strokes, orange/cyan confetti) is appended at the end of the message, because the DS says no platform emoji. Thought cards flip in place: "Somebody's sick?" gets a danger strike, then "Somebody's engaged." in cyan. Lower third, 64px: "Everything so far → **what comes next?**" | Strike `danger` + word; answer cyan | "party emoji" → popper pops (ease-pop) and confetti bursts in 8 SVG pieces; "flipped" → cards rotateX 180° with 0.08s stagger |
| 3 (~44s) | Chunk-by-chunk loop | Hero: v3's chat + probability-bar component **scaled up**: panel 1300px wide, centred. Around it, a thin ring diagram in 4 mono labels: READ → GUESS → ADD → REPEAT, with the active step lit cyan. Counter top-right "× 1" climbing to "× 300" in 64px mono. The web-search aside is a small 32px `ink-muted` tag with a magnifier icon, top-left, visible only during that sentence. "Tokens": the reply splits into chip outlines (`.ig-chip`) for 3s | Winning bar cyan (the only glow); losing bars hatched `ink-dim` (from Patent) | "one small chunk" → first chip; "sticks it on the end" → chip slides into the bubble; "few hundred times" → counter spins from 1 to 300 in 1.2s |
| 4 (~38s) | Your phone | Left 45%: the creator's **real screenshot** `phone-autocomplete-real.png`, height 860px, radius 48, `lift` shadow. Right: PAUSE card, a large ‖ glyph 160px cyan, then "PAUSE AND TRY IT" 32px mono + "Type **I'm going to**, tap the middle word" 56px. Then a keynote number beat: "34,000,000" at 150px, label "settings in Apple's keyboard model" 40px. Then a scale bar: a 6px dot labelled "your phone" next to a bar running off frame right, labelled "ChatGPT: thousands of times bigger" | Pause glyph cyan; the number `ink`; the long bar orange | "Pause the video" → the frame dims 30% for 2s so it really feels like a pause beat; "34 million" → digits roll; "thousands of times bigger" → bar grows 2.5s ease-in-out and the camera follows it right |
| 5 (~30s) | Barista | **AI (the one paid illustration).** Prompt subject: "a faceless flat-silhouette barista behind a simple counter, already pouring a cup, a doorway on the left with a faceless figure in a hoodie stepping in, a wall clock; key object: the cup". Live type on top: "7:00" on the clock (SVG overlay, not in the art); cup label chip "oat latte" (cyan); then "Some days you wanted tea." with an orange teacup outline icon. Then "More writing than thousands of lifetimes": a row of 12 book-spine SVGs that multiply into a wall (x-scale stagger) | Cup = glow; tea = orange | "before you open your mouth" → cup glow on; "wanted tea" → the cyan chip gets a strike, orange tea icon pops; "thousands of lifetimes" → the book wall fills |
| 6 (~48s) | "So how does it write code?" | Opens on a statement card (full-frame, 120px, 2 lines, balanced): "So how does autocomplete write **working code?**" (the caret types "working code"). Then a **three-step staircase** of cards rising left to right, heights 280/420/600px: (1) "Fixed my grammar" [FILL: the creator's real example], (2) "Spotted my wrong variable" with a 3-line code SVG, one token ringed orange, (3) IMO 2025: a horizontal score bar 0–42 with a **gold-line marker at 35** (orange, labelled "gold cutoff") and the AI bar landing exactly on it: "35 / 42". Close with two keynote beats: "It **is** autocomplete." → hard cut → "Just not the kind you think." | Step 3 bar = cyan glow; cutoff line orange | "started small" → card 1; "then it got big" → card 3 slams up; "right at the gold-medal line" → bar stops on the line with a 2px overshoot; "Autocomplete did that" → hold 1.2s |
| 7 (~26s) | Jay puzzle | Group-chat panel, 1300px wide: the message in 3 bubbles (48px). The last bubble ends "So it was ___" with a `.ig-blank`. The viewer gets a 1.5s silence to guess. "Jay" fills the blank in cyan. Then clue rings: cyan underline under "only one home" (evidence), orange ring around "swears he hates pasta" (the lie) | Answer cyan; the lie orange | "finish this one" → blank caret blinks; "You said Jay" → answer lands with ease-pop; "follow the clues" → underline draws 0.8s; "catch the lie" → ring draws |
| 8 (~46s) | Rabbit planning | A "model x-ray" panel: a `surface` card with a thin dashed outline labelled "INSIDE THE MODEL" (30px mono). Line 1 is fully shown: "He saw a carrot and had to grab it," (Anthropic's example). Line 2 is **empty slots**, but the *last* slot already glows cyan with "rabbit" *before* any other word appears. Then the words fill left to right toward it. Then a split-screen verdict: left card, Hinton quote (text only, no photo; attribution "Geoffrey Hinton, 60 Minutes, 2023", 32px); right card, "A very fancy parrot" (Bender et al., 2021). Two vote chips below: "Understands" / "Parrot" | "rabbit" = the glow; both verdict cards neutral (no side taken) | "already picked the word" → "rabbit" ignites alone; "built the line to get there" → words fill at 0.12s stagger; "pick your side" → both chips pop together |
| 9 (~28s) | Raw model to assistant | Two-state card. State A: a generic forum-post UI in the same line language (grey avatar circle, no face; username bar), the question "what's a good dinner tonight?" continuing as rambling text in 40px `ink-muted`: "…asking for my picky five-year-old. Edit: thanks everyone!" State B: the same question, then a clean cyan assistant bubble. Between them, a small label: "Trained again on answers people rated" with 3 small thumbs-up/down SVG ticks (no stars, no faces, no robot) | Assistant bubble cyan glow; the forum post flat | "just keeps writing" → text streams at word speed; "train it again" → the card flips (rotateY, 0.6s ease-in-out) to state B |
| 10 (~30s) | Tidewater Dreams, then outro | A **typographic** book cover, 520×780, centred-left: plain generic paper colour, title "Tidewater Dreams" 64px serif, author line 36px. It must look like a *mock-up*, not an imitation of a real publisher's cover; no publisher logo. At "doesn't exist" a danger stamp "DOESN'T EXIST." at −6° over the cover. Right side: source line 30px mono "Chicago Sun-Times · Philadelphia Inquirer · May 2025". Then the next-video card ("Why it makes things up with a straight face", 120px, orange payoff). Then the end card, with "I gotchu." typed by the caret | Stamp danger + word; next-video payoff orange | "sounds exactly like" → the cover rises; "doesn't exist" → stamp slams (ease-slam); "I gotchu" → caret types it and blinks twice, then the end-screen slots rise |

**Global rules for the v2 build:**
- Maximum one glowing element per frame.
- Nothing readable under 30px.
- Every frame passes the safe-zone and overlap linter.
- No blank frame longer than 0.6s.
- Cross-slide continuity where the script repeats an object: Slide 1 to 2 (same notification), Slide 3 reuses the bars that Slides 7 and 10 echo.
