# DESIGN.md — summary

Direction **Neon Blueprint** · frames 1920×1080 (thumbnail 1280×720) · plain HTML + CSS · fonts from Google Fonts.

## Files

- `tokens.css` (generated from `tokens.json`) — every token as a CSS variable.
- `components/bundle.css` — the frame, type classes, all components and the motion classes. Load it after `tokens.css`.
- `components/<Name>/preview.html` — a live 1920×1080 example of each component. Copy its markup.

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components/bundle.css">
<div class="ig-frame"> … </div>
```

## Tokens

| Group | Tokens |
| --- | --- |
| Background | `night` #0a1128 · `night-950` #050918 · `night-glow` #1a2c68 · `grid` / `grid-fine` (cyan at 9% / 4%) |
| Surfaces | `surface` #111b3d · `surface-raised` #18265a · `line` #2a3a70 |
| Text | `ink` #f4f7ff · `ink-muted` #aab6db · `ink-dim` #7d8ab5 |
| Accents | `orange` #ff7a1a (+ `orange-soft`, `on-orange`) · `cyan` #22d3ee (+ `cyan-soft`, `on-cyan`) |
| Danger | `danger` #ff5c7a (+ `danger-soft`) |
| Type | `headline-xl` 130 · `headline` 112 · `headline-sm` 96 · `title` 64 · `thumb` 150 · `wordmark` 44 (Archivo Black) — `body-lg` 56 · `body` 48 · `body-sm` 40 · `caption` 54 · `label` 32 · `label-sm` 28 (Inter) |
| Spacing | `space-1` 8 · `space-2` 16 · `space-3` 24 · `space-4` 32 · `space-6` 48 · `space-8` 64 · `space-12` 96 · `safe-x` 128 · `safe-y` 96 |
| Radius | `radius-sm` 12 · `radius-md` 24 · `radius-lg` 48 · `radius-pill` 999 |
| Glow | `glow-cyan` · `glow-orange` · `glow-danger` · `glow-text-cyan` · `glow-text-orange` · `lift` |
| Motion | `dur-fast` 0.2s · `dur-base` 0.45s · `dur-slow` 0.8s · `stagger-word` 0.08s · `stagger-line` 0.15s · `ease-out` · `ease-pop` · `ease-slam` · `ease-in-out` |

Contrast on `night`: ink 17.4, ink-muted 9.3, ink-dim 5.5, orange 7.2, cyan 10.3, danger 6.3 (all ≥ 4.5:1).

## Components

| Component | Class | What it's for |
| --- | --- | --- |
| Title card | `.ig-titlecard` | Episode opener |
| Big statement | `.ig-statement` | One idea, huge |
| Fill in the blank | `.ig-sentence` `.ig-blank` `.ig-guesses` | Next-word prediction |
| Word chips | `.ig-chips` `.ig-chip` | Tokens |
| Callout | `.ig-pointer` `.ig-pill` | Naming a part |
| Highlight ring | `.ig-ringed` `.ig-ring` | Circling one word |
| Stamp | `.ig-stamp` | Myth verdicts |
| Comparison | `.ig-compare` `.ig-box` `.ig-arrow` | In → out, A vs B |
| Venn | `.ig-venn` | Overlap = result |
| Caption bar | `.ig-caption` | Word-by-word captions |
| Chat mockup | `.ig-phone` `.ig-bubble` | Real chatbot examples |
| Wordmark | `.ig-wordmark` | Lower-left bug, lockup |
| Progress bar | `.ig-progress` | Chapters |
| End card | `.ig-signoff` `.ig-slot` | "I gotchu." + end screen |
| Thumbnail | `.ig-frame--thumb` `.ig-thumb-text` | 1280×720 |
| Illustration scene | `.ig-scene-*` | Full-bleed concept art |

## Motion rules

1. **Sync to speech.** Every reveal lands on the word it illustrates. Timings in the component pages are defaults for a silent preview.
2. **Enter, don't perform.** Entrances only: `a-rise` (40px up + blur, 0.55s ease-out), `a-pop` (0.6→1, 0.5s ease-pop), `a-draw` (stroke draw, 0.8s ease-out), `a-left`/`a-right` (160px slide, 0.7s ease-in-out), `a-grow` (scale-x from left), `a-land`, `a-slam`, `a-ignite`. Set the delay with `--d`.
3. **Stagger** words/chips 0.08s, lines/cards 0.15s. Never more than two things moving at once.
4. **Hold** at least 1.5s after the last element lands before cutting.
5. **Exit** with a hard cut on a beat, or a 0.2s fade. No exit animations per element.
6. **Draw lines from the target outward** (callouts), **cause before effect** (comparison), **answer last** (fill in the blank).
7. **Glow never pulses.** Only the typing dots and the blank's caret loop.
8. Captions swap instantly per word; they never slide.

## Screen zones (bottom up)

Progress rail 0–88px · wordmark bug left 96 / bottom 64 (120 with the rail) · caption band bottom 128, centred, ≤ 1400px · title-safe 128 × 96.

## Illustrations

Flat vector, navy ground, cyan/orange neon outlines, one glowing key object, subject in the right 55%, left 45% empty, **no text in the image**. Prompt template in "Illustration prompts".
