igotchu explains AI to complete beginners: a calm voiceover over animated 1920×1080 slides. The look is **Neon Blueprint** — a night-navy drafting table lit by two neon inks. Orange is what you should notice or watch out for; cyan is the answer, and "the AI" itself.

## Voice

- Friendly, confident, a little playful. Talk like a smart friend, not a lecturer: "It just guesses the next word." not "Large language models perform next-token prediction."
- Second person, contractions, short sentences. One idea per slide.
- Sentence case for headlines ("How ChatGPT actually thinks"); UPPERCASE only for `label` / `label-sm` and thumbnails.
- No emoji on screen. No exclamation marks in headlines (captions may keep the narrator's).
- Sign-off is always exactly **"I gotchu."** — on the end card and as the last spoken line.
- Myths get a verdict stamp in one word with a full stop: "NONSENSE.", "NOPE.", "TRUE."

## Colour

- Every frame is `night` under the radial glow (`night-glow` → `night` → `night-950`) and the blueprint grid (`grid` 128px, `grid-fine` 32px). Use `.ig-frame`; never a flat fill.
- Text: `ink` for headlines and body, `ink-muted` for subtitles, `ink-dim` for labels (not on `surface-raised`).
- `orange` = emphasis and warnings: the stressed word, the kicker, misconceptions, the wordmark dot. Max one orange idea per frame.
- `cyan` = answers and the AI: AI chat bubbles, the winning guess, the highlight ring, the current caption word, the payoff word.
- `danger` = false / wrong, and only with a word (the stamp). Never colour alone.
- Solid `orange` or `cyan` fills take `on-orange` / `on-cyan` text, never white.
- Boxes are `surface`; things on boxes are `surface-raised`. `line` is decoration only.

## Type

- Headlines: Archivo Black (`display`) — `headline-xl` 130px for title/statement/end cards, `headline` 112px, `headline-sm` 96px for long sentences, `title` 64px inside frames.
- Everything else: Inter (`sans`) — `body-lg` 56, `body` 48, `body-sm` 40, `caption` 54 (800), `label` 32 (800, +8% tracking, uppercase), `label-sm` 28.
- Phone rule: nothing smaller than 28px on a 1920×1080 frame; full sentences ≥ 36px. About 12 characters per line at 130px, 16 at 96px.
- Both faces load from Google Fonts: `Archivo+Black` and `Inter:wght@500;600;700;800`.

## Layout

- Title-safe box: `safe-y` 96px top/bottom, `safe-x` 128px left/right. All text stays inside it. Blueprint crop marks (`.ig-crops`) sit just outside it.
- Fixed zones, bottom up: progress rail (0–88px) · wordmark bug (left 96, bottom 64; 120 when the rail is on) · caption band (bottom 128px, centred, ≤1400px wide).
- Spacing is an 8px scale: `space-3` 24 between chips, `space-6` 48 card padding, `space-8` 64 between boxes.
- Radii: `radius-sm` 12 chips, `radius-md` 24 cards/bubbles, `radius-lg` 48 phone/slots, `radius-pill` for pills.

## Glow

- A glowing edge = `glow-cyan` / `glow-orange` (2px crisp edge + 24px + 72px halos). Text glows with `glow-text-cyan` / `glow-text-orange`.
- One glowing focus per frame; everything else is flat. Cards float with `lift`.

## Illustration

Flat vector, dark navy grounds, subjects built from simple geometric shapes with 4–7px neon outlines in cyan and orange, soft bloom around the key object, no gradients except the glow, no text. Full rules and prompt templates: see the Illustration prompts section.

## Iconography

No icon font. Draw simple inline SVG in the same language as the art: 4–7px strokes, round caps and joins, `cyan` or `orange` strokes on `surface` fills. No emoji.

## Motion

Things rise, pop, draw and slide — nothing spins or bounces twice. Entrances 0.45–0.8s with `ease-out`; pops use `ease-pop`; the stamp uses `ease-slam`. Stagger words by `stagger-word` (0.08s) and lines by `stagger-line` (0.15s). Every reveal lands on the voiceover word it illustrates. Full rules and per-component timing: DESIGN.md and each component's page.
