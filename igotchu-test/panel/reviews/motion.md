# Expert 5: Motion design / animation direction (slug: motion)

Reviewer lens: kinetic type, easing, camera, transitions, "moving pictures". Constraint respected throughout: GSAP on one paused timeline, **transform + opacity only, no CSS keyframes** (3D transforms such as `rotationY` with `transformPerspective` count as transforms).

---

## (a) Research findings

| # | Source | What it says | What it means for igotchu |
|---|---|---|---|
| 1 | Disney's 12 principles applied to UI: [IxDF](https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design), [UX Collective](https://uxdesign.cc/disneys-12-principles-of-animation-exemplified-in-ux-design-5cc7e3dc3f75), [Toptal](https://www.toptal.com/designers/ux/motion-design-principles) | The four principles that matter most for motion graphics are **timing, slow in/slow out (easing), follow-through/overlap, and anticipation**. Straight-line moves read as mechanical; arcs and overlap read as alive. | v3 has good easing and weak **overlap**: everything enters one at a time, from below, on the same 40px rise. It has almost no **anticipation** except the phone push-in. |
| 2 | Material 3 motion tokens: [MDC-Android Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md), [M3 easing/duration](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs) | Durations: short 50–200ms, medium 250–400, long 450–600, extra-long 700–1000ms. Emphasized easing is `cubic-bezier(0.2,0,0,1)`, with separate *decelerate* curves for entering and *accelerate* curves for exiting. | v3's 0.55s entrances sit in "long", which suits video. What's missing is an **accelerating exit curve**: every exit is a linear 0.2s opacity fade (`out()`, ease `none`). |
| 3 | Apple springs: [WWDC23 "Animate with springs"](https://developer.apple.com/videos/play/wwdc2023/10158/), [HIG Motion](https://developers.apple.com/design/human-interface-guidelines/foundations/motion), distilled in [emilkowalski/apple-design](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md) | Start at critical damping (no bounce). Add bounce **only when the object carries momentum**; overshoot on something that just faded in "feels wrong". Most transitions run 0.2–0.5s. | `pop()` (back-out, 1.56 overshoot, from scale 0.6) is used on ~40 elements, including cards and pills that have no momentum. Keep overshoot for thrown or dropped objects. |
| 4 | GSAP easing and timelines: [GSAP Eases](https://gsap.com/docs/v3/Eases/), [Timeline docs](https://gsap.com/docs/v3/GSAP/Timeline/), [Annnimate ease guide](https://annnimate.com/learn/easing), [CustomEase](https://annnimate.com/learn/easing/custom-ease) | `.out` for entrances, `.in` for exits, `.inOut` for on-screen moves; expo/power4 for hero reveals (~1.2s); the position parameter (`"-=0.2"`, `"<0.1"`) creates **overlap**. The built-ins expo.out, power4.out, back.out and sine.inOut cover about 90% of cases. | The four CustomEases are well chosen: igOut ≈ expo-out, igPop ≈ back-out, igSlam ≈ expo-in, igIO ≈ cubic-inOut. Add one exit ease (**igIn**) and one no-overshoot settle (**igSettle**). |
| 5 | 3Blue1Brown / manim: [rate functions](https://docs.manim.community/en/stable/reference/manim.utils.rate_functions.html), [animation defaults](https://docs.manim.community/en/stable/reference/manim.animation.animation.Animation.html) | Default `run_time` is 1s and `rate_func=smooth` (zero velocity *and* acceleration at both ends). Objects **transform into** each other (`Transform`, `ReplacementTransform`) rather than cutting; the camera moves to the thing being discussed. | v3 is built from scene cuts plus cross-fades. The 3b1b move is **continuity**: carry an element across the idea change. See "match-cut" in the system below. |
| 6 | Kurzgesagt process: [Skillshare class pt 1](https://www.skillshare.com/en/classes/motion-graphics-with-kurzgesagt-part-1/631970755), [LinkedIn breakdown](https://www.linkedin.com/pulse/how-kurzgesagt-nikko-imperial) | Scenes are layered illustration with **constant secondary motion** (particles, drifting objects, subtle loops) driven by After Effects expressions. 2–3 animators spend 8–10 weeks per video. Nothing is ever perfectly still. | The igotchu equivalent is DOM "life layers" (particles, steam, drifting dust) animated by transform and opacity over the AI art, generated in code at no cost. |
| 7 | Vox / Johnny Harris: [PremiumBeat Vox breakdowns](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/), [Moonb 2.5D guide](https://www.moonb.io/blog/2-5d-animation), [Waxy: 2.5D parallax from photos](https://waxy.org/2019/11/turning-photos-into-2-5d-parallax-animations-with-machine-learning/), [Motion Array: Johnny Harris tips](https://motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/) | Cut-out layers on paper with a **slow multiplane push** and parallax between layers; highlight circles and underlines drawn onto photos on the narration beat; heavy texture. Harris varies Ken Burns with **dynamic camera pushes** and animated transitions. | The loved illustration scenes already use half of this (push plus drawn callouts). The next step is **two or more depth layers moving at different rates** plus a light sweep. |
| 8 | Ken Burns practice: [Kapwing](https://www.kapwing.com/resources/using-the-moving-zoom-effect/), [Cloudinary guide](https://cloudinary.com/guides/image-effects/ken-burns-effect-complete-guide-and-how-to-apply-it), [Kudoflix 2026](https://kudoflix.com/blog/2026/08/04/ken-burns-effect/) | Zoom **5–15%** per shot; 7–10s standard, 10–15s emotional; end the move on a narration beat. | v3's 12% over about 18–25s is textbook, and it is why those scenes read as alive. The `camera()` push on text scenes is **3% over 16–33s ≈ 0.1–0.2%/s**, which is below the threshold of perception (measured below). |
| 9 | Kinetic type: [We Design Motion](https://wedesignmotion.com/blog/design/kinetic-typography-when-and-why-it-works/), [SVGator guide](https://www.svgator.com/blog/kinetic-typography-a-guide-to-text-in-motion/), [Digital Silk 2026](https://www.digitalsilk.com/web-design/web-trends/kinetic-typography/) | Text must rest readable for at least 0.5s after it settles; align word builds to the vocal rhythm; limit simultaneous movers; reserve the big kinetic move for **one moment per section**. | The headline stagger (line 0.2s apart) could be per-word at 0.06–0.08s, timed to the VO. Save kinetic "hero" words for 1 per scene. |

### Measured evidence (my own analysis)
I ran `ffmpeg freezedetect` (n = -45dB, d = 2.5s) on `v3/igotchu-script3-v3-full.mp4`. It found **21 stretches with no visible change, about 94s of the 220s runtime (≈43%)**:

`18.8–22.4 · 22.4–28.5 · 34.6–38.3 · 39.9–50.1 · 59.1–62.4 · 63.0–70.0 · 100.9–104.6 · 109.8–114.7 · 136.2–143.3 · 143.5–146.1 · 148.3–153.9 · 177.0–183.7 · 183.7–186.6 · 187.8–193.7 · 196.9–200.2 · 200.6–203.2 · 204.0–211.7 · 213.1–end`

Every text scene with `camera(n, 0.03)` registers as frozen: the push is mathematically there but invisible. **The Ken Burns illustration scenes (81.9–100.3 and most of 153.8–176.4) register no freezes at all.** The measurement supports what the creator already feels: the illustration scenes feel alive and the rest feel like slides.

---

## (b) Score: **6 / 10** for motion

Reasons it is above average:
- A real motion vocabulary exists (`rise/pop/land/slam/draw/ignite/camera`, four named CustomEases, `cue()` phrase-sync). Sync to speech is excellent; reveals land on the word.
- **The phone scene (62–82s) is genuinely premium.** It has:
  - a physical object with weight (the ±1.5° rig sway);
  - a motivated camera push, `scale 1.2, y -160, 1.0s igIO`, into the area of interest, which is anticipation plus staging;
  - secondary action: key flash, tap ripple and swapping suggestion sets all moving under the primary action (words appearing);
  - accelerating rhythm;
  - a payoff with follow-through: the stamp is thrown at 2.4× scale and −16°, then shakes over 4×0.07s.
- **The illustration scenes (81–100s, 121–136s, 153–176s) work.** A 3s `sine.inOut` "lights up" reveal is anticipation for the eye. A constant 12% push means the frame never stops. Callouts are drawn *from the target outward* on the spoken word (dot, then line, then pill). The picture itself carries richness that flat UI cannot.
- The predictor panel with accelerating gaps (`0.9 → 0.22s`) makes speed visible, which is real motion storytelling.

Reasons it is not higher:
1. **43% of the runtime is visually frozen** (above). The worst offenders:
   - 1:50–1:55: a fully empty navy frame for 4–5s;
   - 0:22–0:28: one small kicker line for 6s;
   - 2:57–3:07: "Guessing ≠ Knowing" held for 10s;
   - 3:24–3:31: the next-video title held for 7s.
2. **Every cut lands on an empty frame.** `scene()` hard-cuts, and the first element only enters at `at(n, 0.3)` or later, so each cut shows 0.3–0.75s of bare background (see 4-fps strips: morph 0.25–0.75s, glass 0.0–0.5s, phone 0.25s). That is the single most "PowerPoint" tell in the video.
3. **Repetition.** Nearly every reveal is the same `rise` (40px from below, 0.55s igOut) or the same `pop` (0.6 to 1 with back-out overshoot, plus a pop SFX). Nothing enters from the side, from depth, or by transforming from something already on screen.
4. **Exits are dead.** `out()` is a 0.2s *linear* opacity fade. Objects never leave with direction or acceleration, so scenes don't "hand off".
5. **Over-busy in two places:**
   - The "It's actually wild" cartoon burst rays (1:59) are clip-art energy that doesn't match the neon-blueprint tone.
   - During the s3 loop, pill glow pulses, bars growing, words dropping and panel swaps all run at once. That breaks your own DESIGN.md rule 3 ("never more than two things moving").
6. **Constraint leaks.** Some tweens animate non-transform properties:
   - `boxShadow` on `#s3-k*`;
   - `backgroundColor` on the phone keys and `#s6-hi`;
   - `width` on `#pfill`.

   They render, but they violate the transform/opacity rule and are the first things to stutter. Easy fixes are in the system section below.

---

## (c) Top 5 changes, ranked by impact

### 1. Kill the empty cut: "pre-rolled" transitions on every scene boundary
**Where:** every slide start in v3 (22.3, 38.3, 62.3, 81.9, 100.3, 121.1, 153.8, 176.4, 203.2) and every slide in v2.

**Fix:** every slide has 0.9s of tail silence (`dur − speech = 0.9` in timing.json), so use it.
- **Outgoing** (last 0.35s of slide n): `tl.to("#sN .cam", {x:-60, opacity:0, duration:0.35, ease:"igIn"}, end-0.35)`, where `igIn = CustomEase "0.5,0,0.75,0"` (easeInQuart).
- **Incoming** (frame 0 of slide n+1): `tl.fromTo("#sN1 .cam", {x:80, opacity:0}, {x:0, opacity:1, duration:0.5, ease:"igOut"}, start)`.
- **Rule:** the first *content* element (the headline, the phone, the art) must be visible by **start + 0.15s**. Change every `at(n, 0.3)`/`at(n, 0.4)` first-entrance to `at(n, 0.0)` with duration 0.5.
- Direction encodes story: new idea = content pushes left (forward in time); returning to an earlier idea (s9 back to the Paris example) = push right.
- **Match-cut** instead of push whenever an object continues. In v2 the **phone persists across slides 1 → 2** (same Mom text, then the emoji arrives) and **slide 3 → 4** (chat to phone). Keep the phone in one continuous DOM element spanning both clips (one section with a data-duration covering both slides) and move it with `camera.focus` instead of cutting. This is the 3b1b "transform, don't cut" principle.

### 2. Make the camera perceptible on every non-illustration scene, with depth parallax
**Where:** `camera()` in build_v3.py (currently `scale 1 → 1.03` over the whole slide, `sine.inOut`).

**Fix:** split each scene into two layers and move them at different rates. That is multiplane parallax, the Vox and Kurzgesagt move.
```js
// .bg = grid + vignette + glow blobs, .cam = content
tl.fromTo("#sN .bg",  {scale:1.00, x:0,  y:0},  {scale:1.08, x:-40, y:-10, duration:D, ease:"none"}, start);
tl.fromTo("#sN .cam", {scale:1.00, x:0,  y:0},  {scale:1.035, x:-12, y:-6, duration:D, ease:"sine.inOut"}, start);
```
- Target speed: **≥0.4%/s scale on the background and ≈0.15–0.2%/s on the foreground**. That stays inside the 5–15% Ken Burns guidance and makes the foreground pop off the grid.
- Add `cam.handheld` to the hero object only (the phone and chat windows). It is three yoyo tweens at incommensurate periods, which reads as a hand holding the phone rather than a float:
  - `x: ±5px, 3.7s`;
  - `y: ±4px, 2.9s`;
  - `rotation: ±0.6°, 5.3s`;
  - all `sine.inOut, repeat:-1, yoyo:true`.
- This alone should remove most of the 94 frozen seconds.

### 3. Replace "hold" with a second beat: nothing sits for more than 3s
**Where, in v3 terms (the same pattern will recur in the v2 build):**
- 1:50–1:55 (empty frame before "That's it?");
- 0:22–0:28 (s2 kicker only);
- 0:40–0:50 (France held);
- 2:57–3:07 (Guessing ≠ Knowing);
- 3:24–3:31 (next video).

**Fix:** a **"stress" move on the word the VO leans on**, plus a scheduled secondary beat. Pick one per hold:
- `mark.underline`: a 6px bar under the key word, `scaleX 0 → 1`, `transformOrigin:"0 50%"`, 0.5s igOut, on the stressed word's `cue()`.
- `mark.highlight`: a cyan block behind the word, `opacity 0 → 0.18` plus `scaleX 0 → 1`, 0.4s igOut. This also replaces the `backgroundColor` tween on `#s6-hi`.
- `cam.focus` onto the winning bar or word: `scale 1 → 1.12`, x/y to centre the target, 0.9s igIO, then hold.
- Never cut to empty. The 1:50 frame should keep the morph card and slide it `x:-80, opacity:.15, 0.5s igIO` while "That's it?" types. The v2 equivalent is the slide-6 "So is it just autocomplete?" beat.
- **Hard rule for the build:** add a lint step to build_v3.py that walks the tween list and **fails the build if any window longer than 3.0s has no tween starting** (ignoring scene-long camera tweens). That automates the "something moves every 2–4s" checklist item that currently isn't enforced.

### 4. Give every illustration scene a "life layer" and a two-plane move (lift the loved scenes further, then use them more)
**Where:** v2 slide 5 (barista), slide 8 (inside the model / "rabbit"), slide 9 (raw model vs assistant), slide 10 (book cover).

**Fix:** keep the loved recipe exactly, and add three things.
- **Keep:** `art scale 1 → 1.12, ease none, full slide` + `opacity 0 → 1, 3s sine.inOut` + callouts `dot pop → line draw 0.5 igOut → pill settle`.
- **Add, depth:** generate the hero object separately on pure black (e.g. the coffee cup, or the glowing "rabbit" word-node), lay it over the scene with static `mix-blend-mode:screen`, and drive it faster than the background. That is 2.5D parallax from two flat images.
  - Hero: `scale 1 → 1.18, x 0 → -30, ease none`.
  - Background: `scale 1 → 1.08`.
  - This costs one extra image (~185 credits) per scene; use it only on 2 scenes per video.
- **Add, life:** 12–20 DOM specks (4–8px, cyan/orange at 0.4–0.7 opacity) on a per-scene container, generated in Python with a seeded RNG. Each one runs `y: 0 → -(80..160)`, `x: ±(10..30)`, `opacity 0 → .6 → 0`, over 5–9s, `ease:"sine.inOut"`, staggered from random start times, `repeat:-1`. On the barista scene, render them as steam: white, 10–18px, rising from the cup, `scale 0.6 → 1.4`.
- **Add, light sweep:** one diagonal gradient div (`linear-gradient(100deg, transparent, rgba(255,255,255,.07), transparent)`, 600px wide) doing `x: -800 → 2400`, 2.2s `sine.inOut`, once, on the scene's key line (e.g. "that's where it gets weird"). This is transform-only and reads as premium sheen.
- Never pulse the glow (keeps DESIGN.md rule 7).

### 5. Rebuild the motion vocabulary: fewer pops, directional exits, per-word hero type
**Where:** `pop()`, `out()`, the headline `rise()` calls, and the s6 "wild" burst.

**Fix:**
- **`pop` becomes `settle` for anything larger than 200px or with no momentum** (pills, cards, chips, end slots): `{opacity:0, scale:0.94, y:18} → {opacity:1, scale:1, y:0}`, 0.5s, `igSettle = CustomEase "0.22,1,0.36,1"` (easeOutQuint, no overshoot).
  - Keep back-out overshoot only for dropped or thrown things: the emoji landing on Mom's text, the answer word landing in the blank, eggs, the stamp.
  - Cap: **one overshoot per 5s**.
- **`out` becomes `exit.lift`:** `{y:0, opacity:1} → {y:-20, opacity:0}`, 0.3s, `igIn`, stagger 0.04s in reverse DOM order. Keep the hard cut for scene ends.
- **Hero headline becomes `type.words`:** split into word spans with `y 60 → 0, opacity 0 → 1, rotation 4 → 0` (tiny arc), 0.6s igOut, **stagger 0.07s**, time-mapped so the last word lands within 0.2s of the VO saying it. Use it only on the one headline per scene; everything else uses plain `rise`.
- **Delete the burst rays** (`#s6-r*`). In v2, the "Autocomplete did that." / "It's just not the kind you think" beat instead gets a `cam.punch`: `.cam scale 1 → 1.06`, 0.12s power2.out, then back to 1.03 over 0.6s igOut, synced to the stressed word. That is energy from the camera, not clip-art.

---

## Proposed motion system: 12 named moves (drop-in helpers for build_v3.py)

Eases (add two to the four existing):

| Name | Curve | Use |
|---|---|---|
| igOut | `0.16,1,0.3,1` (keep) | entrances |
| igPop | `0.34,1.56,0.64,1` (keep) | momentum objects only |
| igSlam | `0.7,0,0.84,0` (keep) | impact arrival |
| igIO | `0.65,0,0.35,1` (keep) | on-screen moves, camera |
| **igIn** | `0.5,0,0.75,0` | exits (accelerate away) |
| **igSettle** | `0.22,1,0.36,1` | cards and pills, no overshoot |

| Move | Spec (from → to, duration, ease, stagger) | Replaces / notes |
|---|---|---|
| `enter.rise` | y 40→0, op 0→1, 0.55s igOut; lines stagger 0.15 | keep as is |
| `enter.settle` | scale .94→1, y 18→0, op 0→1, 0.5s igSettle; items stagger 0.08 | most `pop()` uses |
| `enter.drop` | y -60→0, scale .8→1, op 0→1, 0.55s igPop (+ding) | `land()`, keep for answers and emoji |
| `enter.side` | x ±160→0, op 0→1, 0.7s igIO | `slide_in()`, use for comparisons (cause left, effect right) |
| `type.words` | per word y 60→0, rot 4→0, op 0→1, 0.6s igOut, stagger 0.07 | one hero headline per scene |
| `type.chars` | `show` per char at 0.06–0.11s, caret steps(1) 0.5s blink | keep |
| `exit.lift` | y 0→-20, op 1→0, 0.3s igIn, reverse stagger 0.04 | `out()` |
| `mark.underline` / `mark.highlight` | scaleX 0→1 origin left, 0.5s / 0.4s igOut; highlight op 0→.18 | on stressed word; replaces the bg-color tween |
| `cam.drift` | bg scale 1→1.08 x 0→-40 (none) + cam scale 1→1.035 (sine.inOut), whole slide | `camera()` |
| `cam.focus` | .cam scale 1→1.15–1.25 + x/y to centre target, 0.9–1.0s igIO; return 0.45s igOut | the phone push, generalised |
| `cam.handheld` | x ±5 3.7s, y ±4 2.9s, rot ±0.6° 5.3s, sine.inOut yoyo repeat -1 | hero phone or chat only |
| `cam.punch` | scale +0.06 in 0.12s power2.out, back over 0.6s igOut | max 1 per scene, on stressed word |
| `kenburns` + `art.life` | art scale 1→1.12 none; op 0→1 3s sine.inOut; hero layer 1→1.18; specks loop; one light sweep | loved scenes, now two-plane |
| `callout` | dot settle 0.3 → line draw 0.5 igOut (+0.1) → pill settle 0.35 (+0.5) | keep sequence |
| `slam` | keep exactly; **max 2 per video** | NONSENSE and the fake-book "?" |
| `transition.push` / `.match` | out: .cam x 0→-60 op→0 0.35 igIn; in: x 80→0 op 0→1 0.5 igOut at t=0 / shared element persists | `scene()` default |

**Transform-only fixes to existing code:**
- `#pfill`: `width 0→1920` becomes `scaleX 0→1`, `transformOrigin:"0 50%"`, ease none.
- Phone key flash (`backgroundColor`): add a `.flash` child with orange fill, animated op 1→0 over 0.25s power1.out, plus scale 1.25→1 on the key.
- Loop pill glow (`boxShadow`): add a `.glow` sibling with the big shadow baked in and animate its opacity 1→0.
- `#s6-hi` background tween becomes `mark.highlight`.
- Optional: straight callout leaders drawn with `strokeDashoffset` could become 2px divs scaling from their origin (L-shapes = two divs). That keeps the draw look while staying transform-only.

---

## Scene-by-scene motion notes for the v2 script

- **S1, Mom's text, lock screen:** reuse the phone rig with `cam.handheld`.
  - Notification: `enter.drop` from y -120 at "Your mom texts you".
  - `cam.focus` 1.2× onto the notification on "No emoji".
  - On "your brain has already written the next five minutes", 3 ghost cards ("Somebody's sick?", "Forgot a birthday?") fan out *behind* the phone at slower parallax: x ±220, rotation ±6°, op 0→.7, stagger 0.15, igSettle.
- **S2, party emoji:** same phone, no cut (match).
  - Emoji `enter.drop` with igPop. This is a real momentum case.
  - Ghost cards `exit.lift`, and a new card "Somebody's engaged!" `enter.settle`, then `cam.punch` on "flipped every guess".
- **S3, the loop:** keep `predictor_steps` with accelerating gaps.
  - Add a transform-only odometer for "a few hundred times": a column of digits with `y` stepping, `ease:"steps(n)"` or igIO per step.
  - Drop the pill `boxShadow` pulses so that at most two things move at once.
- **S4, keyboard:** keep everything. It is the benchmark.
  - Add a "PAUSE AND TRY IT" pause-glyph `enter.drop` at centre.
  - On "34 million settings… thousands of times bigger", run the **bold idea** below.
- **S5, barista:** the loved Ken Burns recipe plus a steam life layer and callout pills ("7am", "hoodie", "oat latte") drawn on each spoken word.
  - "Some days you wanted tea" gets a small `enter.side` tea cup nudging the latte out (x 0→-60, igIO).
- **S6, how does autocomplete write code:** make the morph a real morph.
  - The frame div (no text) scales `scaleY 1→1.2`, 0.5s igIO, while contents `exit.lift` then `enter.rise` with 0.1s overlap.
  - Grammar fix: strike line `scaleX`. Code bug: `mark.highlight` on the wrong variable.
  - IMO: a score bar `scaleX 0 → 35/42` over 1.2s igOut stopping exactly on a gold tick line, then `cam.focus` 1.2× on the tick. This is the one earned "hero" moment in the scene.
- **S7, Jay and the leftovers:** a group-chat bubble stack.
  - `mark.underline` on "only one home", then "swears he hates pasta" gets a struck-through `scaleX` line in orange ("catch the lie").
  - The blank then `enter.drop` "Jay".
- **S8, rabbit:** motion *as* the idea.
  - The destination word "rabbit" ignites first at the right end of line 2, then the line types left to right toward it while `.cam` tracks x (0 → -300, igIO over the typing duration).
  - Hinton vs "fancy parrot": `enter.side` from opposite edges, cause left and counter-view right.
- **S9, raw vs assistant:** contrast in easing.
  - Raw model text scrolls with `ease:"none"`, never settling, speeding up (a long column `y 0 → -1400` over 4s, power1.in).
  - "Train it again": the column exits and the assistant reply `enter.settle`s with igOut. Linear rambling next to a decisive settle is the lesson.
- **S10, fake book:** the cover is a 2.5D object.
  - `transformPerspective:1200, rotationY -22 → -8` over the slide with `ease none`, plus `y` drift.
  - Stamp "?" / "DOESN'T EXIST" with `slam` (use #2 of 2).
  - Then `transition.push` into the next-video card and a quick `ignite` sign-off.

---

## (d) Keep list (do not lose these)
1. **The phone scene, all of it.** Rig sway, the 1.0s igIO push to 1.2×, key flashes, tap ripple, swapping suggestion sets, accelerating word rate, stamp with shake.
2. **Ken Burns illustration recipe:** 12% push with `ease none`, 3s `sine.inOut` light-up, callouts drawn from target outward *inside* the scaled wrapper.
3. **`cue()` phrase-sync.** Every reveal lands on its word. This is rarer than it looks.
4. **The accelerating predictor panel** (gaps 0.9 → 0.22s): speed made visible.
5. **The four CustomEases** and the rise/draw/land helpers as the base vocabulary.
6. **`slam` for the payoff**, kept rare (max 2).
7. **The `ignite` neon sign-off.** It's a brand move; keep it the only flicker.
8. **The typed "Autocomplete?" plus backspace gag.** Keep the idea and give it a live background.

## (e) Bold idea: "Powers of Ten" zoom-out, one continuous camera move
On S4 → S5 ("The model on your phone is small… The ones behind ChatGPT are thousands of times bigger, and that's where it gets weird"), do not cut. Instead, pull the camera back in one unbroken shot.
- **The shot:** the phone keyboard shrinks to a dot, which sits on a desk, which sits in a city block of glowing server halls, which is one tile in a grid that fills the frame. Five nested layers, each authored at 10× the scale of its parent.
- **Doable in pure transforms:** nested divs, each child pre-scaled `0.1`; animate a single wrapper's `scale` from `1 → 0.0001`.
- **Constant perceived speed:** perceived zoom speed is logarithmic, so drive it in log space:

  ```js
  tl.to(proxy, {v: 4, duration: 5, ease: "igIO",
    onUpdate: () => gsap.set("#zoom", {scale: Math.pow(10, -proxy.v)})}, t)
  ```

  The camera then glides through each decade at the same pace, with a gentle start and stop, as in the Eameses' *Powers of Ten* and 3b1b's zoom moves.
- **Labels pinned to each decade:** "34 million settings" on the phone, then "×1,000" and "×10,000" pills. Each is `enter.settle`d and counter-scaled so it stays readable.
- **Cost and payoff:** zero ElevenLabs credits (all DOM/SVG shapes). It turns the video's core abstract claim, *scale*, into the single most memorable shot, and it is exactly the kind of "moving picture" a slide deck can't do.
