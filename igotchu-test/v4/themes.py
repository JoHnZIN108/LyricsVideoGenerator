"""Instrument and Patent skins (igotchu Type Lab), carried over from v3 plus v4 scene overrides."""
TYPELAB_FONTS = (
    '@font-face{font-family:"Bricolage Grotesque";font-weight:200 800;font-stretch:75% 100%;src:url(assets/fonts/bricolage-grotesque-latin-wdth-normal.woff2) format("woff2")}'
    + "".join(f'@font-face{{font-family:"DM Sans";font-weight:{w};src:url(assets/fonts/dm-sans-latin-{w}-normal.woff2) format("woff2")}}' for w in (500, 600, 700))
    + "".join(f'@font-face{{font-family:"JetBrains Mono";font-weight:{w};src:url(assets/fonts/jetbrains-mono-latin-{w}-normal.woff2) format("woff2")}}' for w in (500, 700)))

TYPE_CONDENSED = """
:root{--font-display:"Bricolage Grotesque","Arial Narrow",sans-serif;--font-sans:"DM Sans",Arial,sans-serif;--font-mono:"JetBrains Mono",ui-monospace,monospace}
.ig-frame{font-family:var(--font-sans)}
.ig-hxl,.ig-h,.ig-hsm,.ig-title,.ig-wordmark,.ig-signoff,.ig-stamp,.s5-scale,.sentcard .ans,.recipe .ans,.pr-row .w{font-family:var(--font-display);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75}
.ig-hxl{font-size:150px;line-height:.9;letter-spacing:-.02em}.ig-h{font-size:126px;line-height:.9}.ig-hsm{font-size:110px;line-height:.92}
.ig-label,.ig-label-sm,.ig-pill,.ig-kicker,#rail .chapters span,.pr-row .pct,.cw-head,.s3-count{font-family:var(--font-mono);font-weight:700}
.ig-body-lg,.ig-body,.ig-body-sm,.ig-bubble,.ig-guess .word,.fr,.ck{font-family:var(--font-sans)}
"""

THEMES = {
 "instrument": {
  "eases": ("0.2,0.8,0.2,1", "0.3,1.45,0.5,1", "0.7,0,0.84,0", "0.2,0.8,0.2,1"),
  "css": TYPE_CONDENSED + """
:root{--night:#e3e8e4;--night-950:#c3ccc6;--night-glow:#f0f4f1;--surface:#f7faf8;--surface-raised:#ffffff;--line:#c3ccc6;--grid:transparent;--grid-fine:transparent;
 --ink:#131a17;--ink-muted:#4a5751;--ink-dim:#5d6a63;--orange:#d0165c;--orange-soft:rgba(255,61,127,.14);--on-orange:#fff;--cyan:#2343e0;--cyan-soft:rgba(35,67,224,.10);--on-cyan:#fff;
 --danger:#d8261c;--danger-soft:rgba(216,38,28,.1);--glow-cyan:0 0 0 3px #2343e0,0 10px 0 #b9c3bc,0 24px 40px rgba(19,26,23,.14);--glow-orange:0 0 0 3px #ff3d7f,0 10px 0 #b9c3bc,0 24px 40px rgba(19,26,23,.14);
 --glow-text-cyan:none;--glow-text-orange:none;--lift:0 12px 0 #c3ccc6,0 30px 44px rgba(19,26,23,.16)}
.ig-frame{background:#e3e8e4;background-image:radial-gradient(ellipse 70% 60% at 18% 0%,#f0f4f1,transparent 70%),linear-gradient(180deg,transparent 60%,rgba(19,26,23,.05))}
.ig-frame::before{display:none}
#crops{display:none}
.ig-em-o{color:var(--orange)}.ig-em-c{color:var(--cyan)}
/* screws, silkscreen, LEDs */
.screw{position:absolute;width:24px;height:24px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fbfdfc,#b3beb7 70%);box-shadow:inset 0 0 0 2px #a3afa8,0 1px 0 #fff;z-index:30}
.screw::after{content:"";position:absolute;left:5px;right:5px;top:11px;height:2px;background:#8b978f;transform:rotate(-35deg)}
.silk{position:absolute;font-family:var(--font-mono);font-weight:700;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:#4a5751;z-index:30}
.led{display:inline-block;width:20px;height:20px;border-radius:50%;background:#b3bdb6;box-shadow:inset 0 2px 3px rgba(0,0,0,.25);vertical-align:middle;margin-right:12px}
.led.on{background:#ff3d7f;box-shadow:0 0 0 5px rgba(255,61,127,.16),0 0 22px #ff3d7f}
/* keys */
.ig-pill{background:#f7faf8;color:#2343e0;box-shadow:inset 0 -4px 0 rgba(0,0,0,.07),0 8px 0 #c3ccc6,0 18px 30px rgba(19,26,23,.14)}
.ig-pill--o{color:#d0165c}
.ig-kicker{background:#131a17;color:#f7faf8;box-shadow:0 8px 0 #000,0 18px 30px rgba(19,26,23,.2)}
.ig-kicker-dot{background:#ff3d7f;box-shadow:0 0 12px #ff3d7f}
.ig-kicker--cyan{background:#2343e0;color:#fff;box-shadow:0 8px 0 #172e9e,0 18px 30px rgba(19,26,23,.2)}
.ig-kicker--cyan .ig-kicker-dot{background:#ffd21a;box-shadow:0 0 12px #ffd21a}
.ig-blank{background:#0c1310;color:#9db1ff;box-shadow:inset 0 0 0 10px #262f2b,inset 0 0 60px rgba(0,0,0,.7);text-shadow:0 0 18px rgba(157,177,255,.55);font-family:var(--font-mono)}
.blank-caret{background:#9db1ff;box-shadow:0 0 16px rgba(157,177,255,.8)}
.ig-guess{background:#f7faf8;box-shadow:inset 0 -4px 0 rgba(0,0,0,.07),0 10px 0 #c3ccc6,0 24px 36px rgba(19,26,23,.14)}
.ig-guess--win{background:#2343e0;box-shadow:0 10px 0 #172e9e,0 24px 36px rgba(19,26,23,.2)}
.ig-guess--win .word,.ig-guess--win .pct{color:#fff}.ig-guess--win .bar{background:rgba(255,255,255,.25)}.ig-guess--win .bar i{background:#fff;box-shadow:none}
.ig-guess--odd .word,.ig-guess--odd .pct{color:#d0165c}.ig-guess--odd .bar i{background:#ff3d7f}
.ig-chip .t{background:#f7faf8;box-shadow:inset 0 -4px 0 rgba(0,0,0,.07),0 10px 0 #c3ccc6;color:#131a17}
.ig-chip--o .t{background:#ffd21a;color:#131a17;box-shadow:0 10px 0 #b89400}
/* screens: prediction panels read like the device's display */
.pr-panel{background:#0c1310;box-shadow:inset 0 0 0 10px #262f2b,inset 0 0 60px rgba(0,0,0,.7)}
.pr-row{color:#6d7c86}.pr-row .bar{background:#1d2723}.pr-row .bar i{background:#4a5a66}.pr-row .pct{color:#6d7c86}
.pr-panel.lock .pr-row.win{color:#9db1ff;text-shadow:0 0 18px rgba(157,177,255,.55)}
.pr-panel.lock .pr-row.win .bar i{background:#9db1ff;box-shadow:0 0 12px #9db1ff}.pr-panel.lock .pr-row.win .pct{color:#9db1ff}
.chatwin{background:#f7faf8;box-shadow:inset 0 -5px 0 rgba(0,0,0,.07),0 12px 0 #c3ccc6,0 30px 44px rgba(19,26,23,.16);border-radius:36px}
.cw-dot{background:#ff3d7f;box-shadow:0 0 14px #ff3d7f}
.ig-bubble--me{background:#e3e8e4}.ig-bubble--ai{background:rgba(35,67,224,.08);box-shadow:inset 0 0 0 3px #2343e0}
/* phone: graphite device */
.ig-phone{background:#131a17;box-shadow:0 12px 0 #000,0 30px 44px rgba(19,26,23,.25)}
.ig-phone .screen{background:#f7faf8}.ig-phone .notch{background:#131a17}
.p4 .ig-bubble.in{background:#e3e8e4}
.kb,.suggbar{background:#d6ddd8}.k{background:#fff;box-shadow:0 2px 0 #aab4ad}.k.fn{background:#c3ccc6}
.ig-stamp{border-color:#d8261c;outline:none;color:#d8261c;text-shadow:none;background:rgba(247,250,248,.7);box-shadow:inset 0 0 0 5px #f7faf8,inset 0 0 0 10px #d8261c}
.ig-stamp::after{display:none}
.ig-box{background:#f7faf8;box-shadow:inset 0 0 0 3px #ff3d7f,0 12px 0 #c3ccc6,0 30px 44px rgba(19,26,23,.16);border-radius:36px}
.ig-box--c{background:#2343e0;box-shadow:0 12px 0 #172e9e,0 30px 44px rgba(19,26,23,.2)}
.ig-box--c .ig-label,.ig-box--c .ig-body-lg{color:#fff}
.ig-arrow path{stroke:#131a17;filter:none}
.ig-venn .circle.a{background:rgba(255,61,127,.14);box-shadow:inset 0 0 0 4px #ff3d7f}.ig-venn .circle.b{background:rgba(35,67,224,.12);box-shadow:inset 0 0 0 4px #2343e0}
.ig-venn .circle.a{color:#d0165c}
.morph,.recipe{background:#f7faf8;box-shadow:inset 0 -5px 0 rgba(0,0,0,.07),0 12px 0 #c3ccc6,0 30px 44px rgba(19,26,23,.16);border-radius:36px}
.code{background:#0c1310;color:#9db1ff;padding:26px 30px;border-radius:20px;box-shadow:inset 0 0 0 8px #262f2b}
.code .kw{color:#ff7aa8}.code .n{color:#ffd21a}
.egg{background:#fff;box-shadow:inset 0 0 0 4px #131a17}
.burst path{stroke:#ff3d7f}
.ig-signoff{color:#131a17;text-shadow:none}.ig-signoff b{color:#ff3d7f;text-shadow:0 0 22px #ff3d7f}
.ig-slot{border:3px dashed #4a5751;background:rgba(247,250,248,.6)}.ig-slot--round{border-color:#ff3d7f}
.ig-wordmark b{color:#ff3d7f;text-shadow:0 0 14px #ff3d7f}
#rail .track{background:#c3ccc6}#rail .seg{background:#b3bdb6}#pfill{background:#2343e0;box-shadow:none}
#rail .chapters span{color:#66736c}#rail .chapters span.on{color:#2343e0;text-shadow:none}#rail .chapters span.done{color:#131a17}
/* illustration scenes play on the device's screen, in the original neon palette */
.scene.plain{background:transparent}
.scene.plain .cam{inset:110px 96px 150px;border-radius:30px;overflow:hidden;background:#0a1128;box-shadow:inset 0 0 0 12px #262f2b,0 2px 0 #f0f4f1,0 -2px 0 #c3ccc6;
 --ink:#f4f7ff;--ink-muted:#aab6db;--ink-dim:#7d8ab5;--orange:#ff7a1a;--cyan:#22d3ee;--line:#2a3a70;--surface:#111b3d;--surface-raised:#18265a}
.scene.plain .cam > *{transform-origin:50% 50%}
.scene.plain .cam{color:var(--ink)}
#rail .chapters{padding:0 64px}
.s1-left{width:820px}.s1-left .ig-hxl{font-size:124px}
.s6-head{top:120px}.s8-head{top:112px}.s9-note{top:120px}.s9-chat{top:215px}.s9-stamp{top:370px}.scene.plain .s8-head{top:22px}

.scene.plain .art{inset:-110px -96px -150px}
.scene.plain .ig-pill{background:#0a1128;color:#22d3ee;box-shadow:0 0 0 2px #22d3ee,0 0 24px rgba(34,211,238,.55)}
.scene.plain .ig-pill--o{color:#ff7a1a;box-shadow:0 0 0 2px #ff7a1a,0 0 24px rgba(255,122,26,.55)}
.scene.plain .ig-box{background:#111b3d;box-shadow:0 0 0 2px #ff7a1a}.scene.plain .ig-box--c{background:#111b3d;box-shadow:0 0 0 2px #22d3ee}
.scene.plain .ig-box--c .ig-label{color:#22d3ee}.scene.plain .ig-box .ig-label{color:#ff7a1a}.scene.plain .ig-box .ig-body-lg{color:#f4f7ff}
.scene.plain .ig-arrow path{stroke:#22d3ee}
.scene.plain .recipe{background:#111b3d;box-shadow:0 0 0 2px #ff7a1a}.scene.plain .egg{background:#f4f7ff;box-shadow:none}.scene.plain .egg.miss{background:transparent}
.scene.plain .ig-chip .t{background:#18265a;color:#f4f7ff;box-shadow:inset 0 0 0 2px #22d3ee}.scene.plain .ig-chip--o .t{background:rgba(255,122,26,.16);color:#ff7a1a;box-shadow:0 0 0 2px #ff7a1a}
.scene.plain .ig-kicker{background:rgba(255,122,26,.16);color:#ff7a1a;box-shadow:0 0 0 2px #ff7a1a}
.scene.plain .sentcard{background:rgba(10,17,40,.88)}
.scene.plain .ig-em-o{color:#ff7a1a}.scene.plain .ig-em-c{color:#22d3ee}
""",
  "decor": lambda n_slides: (
      '<i class="screw" style="left:36px;top:36px"></i><i class="screw" style="right:36px;top:36px"></i>'
      '<i class="screw" style="left:36px;bottom:36px"></i><i class="screw" style="right:36px;bottom:36px"></i>'
      '<div class="silk" style="left:96px;top:44px">igotchu / Ep 03 — It&#39;s autocomplete, not the kind you think</div>'
      + "".join(f'<div class="silk slidetag" id="tag{n}" style="right:96px;top:40px;display:none"><i class="led on"></i><i class="led"></i><i class="led"></i>Slide {n:02d}</div>' for n in range(1, n_slides + 1))),
 },
 "patent": {
  "eases": ("0.2,0.8,0.2,1", "0.2,0.8,0.2,1", "0.7,0,0.84,0", "0.2,0.8,0.2,1"),
  "css": TYPE_CONDENSED + """
:root{--night:#eef2ee;--night-950:#e2e8e3;--night-glow:#f4f7f4;--surface:#eef2ee;--surface-raised:#f7faf8;--line:#131a17;--grid:transparent;--grid-fine:transparent;
 --ink:#131a17;--ink-muted:#4a5751;--ink-dim:#4a5751;--orange:#c8195a;--orange-soft:rgba(200,25,90,.07);--on-orange:#fff;--cyan:#2343e0;--cyan-soft:rgba(35,67,224,.07);--on-cyan:#fff;
 --danger:#d8261c;--danger-soft:rgba(216,38,28,.08);--glow-cyan:0 0 0 4px #2343e0,0 0 22px rgba(35,67,224,.35);--glow-orange:0 0 0 3px #131a17;
 --glow-text-cyan:0 0 18px rgba(35,67,224,.45);--glow-text-orange:none;--lift:none}
.ig-frame{background:#eef2ee;background-image:none}
.ig-frame::before{display:none}
#crops{display:none}
.pt-border{position:absolute;inset:48px;border:2px solid #131a17;pointer-events:none;z-index:30}
.pt-head{position:absolute;top:62px;left:0;right:0;text-align:center;font-family:var(--font-mono);font-weight:700;font-size:26px;letter-spacing:.08em;text-transform:uppercase;color:#4a5751;z-index:30}
.pt-fig{position:absolute;right:96px;bottom:110px;font-family:var(--font-display);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75;font-size:64px;letter-spacing:.02em;color:#131a17;z-index:30}
.ig-pill{background:#eef2ee;color:#2343e0;box-shadow:0 0 0 3px #2343e0}.ig-pill--o{color:#131a17;box-shadow:0 0 0 3px #131a17}
.ig-kicker{background:transparent;color:#131a17;box-shadow:0 0 0 3px #131a17}.ig-kicker-dot{background:#2343e0;box-shadow:0 0 10px rgba(35,67,224,.6)}
.ig-kicker--cyan{color:#2343e0;box-shadow:0 0 0 3px #2343e0}
.ig-blank{background:transparent;color:#2343e0;box-shadow:none;border-bottom:8px solid #2343e0;border-radius:0}
.blank-caret{background:#2343e0}
.ig-guess{background:transparent;box-shadow:inset 0 0 0 3px #131a17;border-radius:4px}
.ig-guess .bar{background:transparent;box-shadow:inset 0 0 0 2px #131a17;border-radius:0}.ig-guess .bar i{border-radius:0;background:repeating-linear-gradient(45deg,#131a17 0 3px,transparent 3px 9px)}
.ig-guess--win{box-shadow:inset 0 0 0 4px #2343e0,0 0 22px rgba(35,67,224,.3)}.ig-guess--win .bar i{background:#2343e0;box-shadow:none}
.ig-guess--odd .word,.ig-guess--odd .pct{color:#c8195a}
.ig-chip .t{background:transparent;box-shadow:inset 0 0 0 3px #131a17;border-radius:4px;color:#131a17}
.ig-chip--o .t{box-shadow:inset 0 0 0 4px #2343e0;color:#2343e0}
.pr-panel{background:#eef2ee;box-shadow:inset 0 0 0 3px #131a17;border-radius:4px}
.pr-row{color:#4a5751}.pr-row .bar{background:transparent;box-shadow:inset 0 0 0 2px #131a17;border-radius:0}.pr-row .bar i{border-radius:0;background:repeating-linear-gradient(45deg,#131a17 0 3px,transparent 3px 9px)}
.pr-panel.lock .pr-row.win{color:#2343e0;text-shadow:0 0 14px rgba(35,67,224,.35)}.pr-panel.lock .pr-row.win .bar i{background:#2343e0;box-shadow:none}.pr-panel.lock .pr-row.win .pct{color:#2343e0}
.chatwin,.morph,.recipe,.sentcard{background:#eef2ee;box-shadow:inset 0 0 0 3px #131a17;border-radius:6px}
.cw-dot{background:#2343e0;box-shadow:none}.cw-head{border-bottom:2px solid #131a17}
.ig-bubble--me{background:transparent;box-shadow:inset 0 0 0 3px #131a17}.ig-bubble--ai{background:transparent;box-shadow:inset 0 0 0 4px #2343e0,0 0 18px rgba(35,67,224,.25)}
.ig-phone{background:#eef2ee;box-shadow:inset 0 0 0 5px #131a17}.ig-phone .screen{background:#f7faf8;box-shadow:inset 0 0 0 3px #131a17}.ig-phone .notch{background:#131a17}
.ig-phone .avatar{background:transparent;box-shadow:inset 0 0 0 3px #2343e0}
.p4 .ig-bubble.in{background:transparent;box-shadow:inset 0 0 0 3px #131a17}
.kb,.suggbar{background:#e2e8e3}.k{background:#f7faf8;box-shadow:inset 0 0 0 2px #131a17}.k.fn{background:repeating-linear-gradient(45deg,#131a17 0 2px,#f7faf8 2px 8px)}
.compose{box-shadow:inset 0 0 0 3px #131a17}
.ig-stamp{border-color:#d8261c;outline:none;color:#d8261c;text-shadow:none;background:rgba(238,242,238,.7);box-shadow:none}.ig-stamp::after{display:none}
.ig-box{background:transparent;box-shadow:inset 0 0 0 4px #131a17;border-radius:4px}.ig-box--c{box-shadow:inset 0 0 0 5px #2343e0,0 0 26px rgba(35,67,224,.3)}
.ig-box .ig-label{color:#131a17}.ig-box--c .ig-label{color:#2343e0}
.ig-arrow path{stroke:#2343e0;filter:drop-shadow(0 0 8px rgba(35,67,224,.5))}
.ig-venn .circle{mix-blend-mode:normal}.ig-venn .circle.a{background:repeating-linear-gradient(45deg,rgba(19,26,23,.18) 0 2px,transparent 2px 12px);box-shadow:inset 0 0 0 4px #131a17;color:#131a17}
.ig-venn .circle.b{background:rgba(35,67,224,.06);box-shadow:inset 0 0 0 4px #2343e0}
.code{color:#131a17}.code .kw{color:#c8195a}.code .n{color:#2343e0}
.fr{box-shadow:inset 0 0 0 2px #131a17;border-radius:2px}.fr.hi{box-shadow:inset 0 0 0 4px #2343e0}
.box{box-shadow:inset 0 0 0 3px #131a17;border-radius:2px}.box.on{background:#2343e0;box-shadow:none}
.egg{background:#f7faf8;box-shadow:inset 0 0 0 4px #131a17}.egg.miss{border-color:#c8195a;box-shadow:none}
.burst path{stroke:#2343e0}
.ig-signoff{color:#131a17;text-shadow:none}.ig-signoff b{color:#2343e0;text-shadow:0 0 14px rgba(35,67,224,.45)}
.ig-slot{border:3px solid #131a17;background:transparent;border-radius:2px}.ig-slot--round{border-radius:50%;border-color:#2343e0}
.ig-wordmark b{color:#2343e0;text-shadow:0 0 14px rgba(35,67,224,.45)}
#rail .track{background:transparent;border-top:2px solid #131a17}#rail .seg{background:transparent}#pfill{background:#2343e0;box-shadow:0 0 12px rgba(35,67,224,.5);height:8px}
#rail .chapters span{color:#4a5751}#rail .chapters span.on{color:#2343e0;text-shadow:none}#rail .chapters span.done{color:#131a17}
#rail{left:48px;right:48px;bottom:48px}#bug{left:96px;bottom:150px}
/* illustrations: shown as framed figure plates, in their original colours */
.scene.plain{background:transparent}
.scene.plain .cam{inset:118px 110px 190px;overflow:hidden;background:#0a1128;color:var(--ink);box-shadow:0 0 0 3px #131a17,0 0 0 14px #eef2ee,0 0 0 16px #131a17;
 --ink:#f4f7ff;--ink-muted:#aab6db;--ink-dim:#7d8ab5;--orange:#ff7a1a;--cyan:#22d3ee;--line:#2a3a70;--surface:#111b3d;--surface-raised:#18265a}
.scene.plain .art{inset:-118px -110px -190px}
.scene.plain .ig-pill{background:#0a1128;color:#22d3ee;box-shadow:0 0 0 2px #22d3ee}.scene.plain .ig-pill--o{color:#ff7a1a;box-shadow:0 0 0 2px #ff7a1a}
.scene.plain .ig-pointer path{stroke:#22d3ee}.scene.plain .ig-pointer circle{fill:#22d3ee}.scene.plain .ig-pointer--o path{stroke:#ff7a1a}.scene.plain .ig-pointer--o circle{fill:#ff7a1a}
.scene.plain .ig-box{background:#111b3d;box-shadow:0 0 0 2px #ff7a1a}.scene.plain .ig-box--c{background:#111b3d;box-shadow:0 0 0 2px #22d3ee}
.scene.plain .ig-box .ig-label{color:#ff7a1a}.scene.plain .ig-box--c .ig-label{color:#22d3ee}.scene.plain .ig-arrow path{stroke:#22d3ee}
.scene.plain .recipe,.scene.plain .sentcard{background:#111b3d;box-shadow:0 0 0 2px #ff7a1a;border-radius:10px}.scene.plain .egg{background:#f4f7ff;box-shadow:none}.scene.plain .egg.miss{background:transparent;border-color:#ff7a1a}
.scene.plain .ig-chip .t{background:#18265a;color:#f4f7ff;box-shadow:inset 0 0 0 2px #22d3ee}.scene.plain .ig-chip--o .t{color:#ff7a1a;box-shadow:inset 0 0 0 2px #ff7a1a}
.scene.plain .ig-kicker{color:#ff7a1a;box-shadow:0 0 0 2px #ff7a1a}.scene.plain .ig-em-o{color:#ff7a1a}.scene.plain .ig-em-c{color:#22d3ee}
.ringrect{stroke:#ff7a1a}
.s1-left{width:820px}.s1-left .ig-hxl{font-size:124px}
.s6-head{top:120px}.s8-head{top:112px}.s9-note{top:120px}.s9-chat{top:215px}.s9-stamp{top:370px}.scene.plain .s8-head{top:22px}

""",
  "decor": lambda n_slides: (
      '<div class="pt-border"></div>'
      + "".join(f'<div class="pt-head" id="tag{n}" style="display:none">igotchu · Ep 03 · Sheet {n} of {n_slides}</div>' for n in range(1, n_slides + 1))
      + "".join(f'<div class="pt-fig" id="fig{n}" style="display:none">FIG. {n}</div>' for n in range(1, n_slides + 1))),
 },
}


V4_LIGHT = """
/* v4 scenes on light themes */
.lockscreen{background:#f7faf8 !important}
.lock{color:#131a17}.lk-date{color:#4a5751}
.notif{background:transparent;box-shadow:inset 0 0 0 3px #131a17;color:#131a17;backdrop-filter:none}.nf-app{color:#4a5751}
.gh{background:transparent;box-shadow:inset 0 0 0 2px #c3ccc6;color:#4a5751}
.grow-r .bar{background:transparent;box-shadow:inset 0 0 0 2px #131a17;border-radius:0}.grow-r .bar i{border-radius:0;background:repeating-linear-gradient(45deg,#131a17 0 3px,transparent 3px 9px)}
.grow-r.win .bar i{background:var(--cyan);box-shadow:none}
.gpanel,.web,.gchat,.rc,.qcard,.cmt{background:var(--surface);box-shadow:inset 0 0 0 3px #131a17}
.gm{background:var(--surface-raised);box-shadow:inset 0 0 0 2px #c3ccc6}.gm.me{background:rgba(35,67,224,.10)}
.editor,.code7 .code{background:#0c1310;color:#dfe6ff;box-shadow:inset 0 0 0 10px #262f2b}
.editor .kw,.code7 .code .kw{color:#ff7aa8}.ghost{color:#8b97c0}
.forum{background:var(--surface);box-shadow:inset 0 0 0 3px #131a17}.fb{color:#4a5751}.votes{color:#4a5751}
.track{background:transparent;box-shadow:inset 0 0 0 2px #131a17}
.search{background:var(--surface);box-shadow:inset 0 0 0 3px #131a17}
.tok{color:var(--ink)}
.s3-count,.score,.big,.vsb{color:var(--ink)}
.chap{color:var(--cyan)}#pline{background:#c3ccc6}#pfill{background:var(--cyan);box-shadow:none}
.k{background:#fff;color:#131a17}
.ig-frame::before{display:none}
.rig1{top:120px;scale:.84;transform-origin:50% 0}
.rig{scale:.84}
.scene.plain .s5-a,.scene.plain .s5-b{background:rgba(5,9,24,.82)}
"""
