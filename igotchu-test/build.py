"""Builds video/index.html (HyperFrames composition) for igotchu Script 3.

Slide start times come from timing.json (voice clip lengths) and in-slide
cue times from cues.json (estimated from where each phrase sits in the text).
"""
import json

T = {i + 1: s for i, s in enumerate(json.load(open("timing.json")))}
C = {int(k): v for k, v in json.load(open("cues.json")).items()}
END_HOLD = 1.5
TOTAL = round(T[10]["start"] + T[10]["dur"] + END_HOLD, 3)
T[10]["dur"] = round(T[10]["dur"] + END_HOLD, 3)


def at(n, key_or_t):
    """Absolute time for slide n + a cue name or a relative offset."""
    rel = C[n][key_or_t] if isinstance(key_or_t, str) else key_or_t
    return round(T[n]["start"] + rel, 3)


anims = []  # GSAP lines


_seen = set()


def tw(sel, frm, to, t, dur=0.6, ease="power3.out"):
    vars_ = {**to, "duration": dur, "ease": ease}
    if sel in _seen:  # later tweens on the same element must not overwrite its start state
        vars_["immediateRender"] = False
    _seen.add(sel)
    anims.append(f'tl.fromTo("{sel}", {json.dumps(frm)}, {json.dumps(vars_)}, {t});')


def pop(sel, t, y=40, dur=0.6):
    tw(sel, {"opacity": 0, "y": y}, {"opacity": 1, "y": 0}, t, dur)


def fade_out(sel, t, dur=0.4):
    tw(sel, {"opacity": 1}, {"opacity": 0}, t, dur, "power1.in")


def slide(n, inner, extra_cls=""):
    s = T[n]
    return (
        f'<section id="s{n}" class="clip slide {extra_cls}" data-start="{s["start"]}" '
        f'data-duration="{s["dur"]}" data-track-index="1">{inner}</section>'
    )


slides = []

# ---------- Slide 1: hook ----------
slides.append(slide(1, """
  <div class="center">
    <h1 class="huge" id="s1-a">ChatGPT doesn't<br/>know <span class="o">anything.</span></h1>
    <p class="sub" id="s1-b">It's <span class="c">guessing.</span> One word at a time.</p>
    <div class="qcard" id="s1-q"><span class="qmark">?</span> If it's only guessing&hellip;<br/>how can it solve problems?</div>
  </div>"""))
pop("#s1-a", at(1, 0.3), 60, 0.8)
pop("#s1-b", at(1, "It's guessing"))
fade_out("#s1-a", at(1, "By the end") + 0.2)
tw("#s1-b", {"y": 0}, {"y": -180}, at(1, "By the end") + 0.2, 0.7)
fade_out("#s1-b", at(1, "If it's only guessing") - 0.5)
pop("#s1-q", at(1, "If it's only guessing"), 60, 0.7)

# ---------- Slide 2: finish the sentence ----------
slides.append(slide(2, """
  <div class="center">
    <div class="tag" id="s2-tag">GAME: FINISH THE SENTENCE</div>
    <h1 class="big" id="s2-a">Peanut butter and <span class="blank"><span class="fill o" id="s2-fill">jelly</span></span></h1>
    <p class="sub" id="s2-b">You didn't look it up. You've just seen it <span class="c">a thousand times.</span></p>
  </div>"""))
pop("#s2-tag", at(2, 0.3))
pop("#s2-a", at(2, "Peanut butter") - 0.4)
tw("#s2-fill", {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, at(2, "You said jelly"), 0.5, "back.out(2.5)")
pop("#s2-b", at(2, "You didn't look"))

# ---------- Slide 3: capital of France + the loop ----------
loop_words = ["The", "capital", "of", "France", "is", "Paris", "."]
chips = "".join(f'<span class="chip" id="s3-w{i}">{w}</span>' for i, w in enumerate(loop_words))
slides.append(slide(3, f"""
  <div class="center">
    <h1 class="big" id="s3-a">The capital of France is <span class="blank"><span class="fill o" id="s3-fill">Paris</span></span></h1>
    <div id="s3-loop" class="loop">
      <div class="tag">WHAT COMES NEXT?</div>
      <div class="chips">{chips}<span class="chip ghost" id="s3-next">?</span></div>
      <div class="counter" id="s3-count">Repeat &times; hundreds. Super fast.</div>
    </div>
  </div>"""))
pop("#s3-a", at(3, 0.3))
tw("#s3-fill", {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, at(3, "Paris"), 0.5, "back.out(2.5)")
fade_out("#s3-a", at(3, "That is basically") + 1.6)
pop("#s3-loop .tag", at(3, "What comes next") - 0.6)
for i in range(len(loop_words)):
    t = at(3, "That is basically") + 2.4 + i * 0.95
    tw(f"#s3-w{i}", {"opacity": 0, "y": 30, "scale": 0.8}, {"opacity": 1, "y": 0, "scale": 1}, t, 0.35, "back.out(2)")
tw("#s3-next", {"opacity": 0}, {"opacity": 1}, at(3, "That is basically") + 2.2, 0.3)
anims.append(f'tl.to("#s3-next", {{opacity: 0.25, duration: 0.45, yoyo: true, repeat: 15, ease: "sine.inOut"}}, {at(3, "That is basically") + 2.6});')
pop("#s3-count", at(3, "Hundreds of times"))

# ---------- Slide 4: phone autocomplete ----------
typed = "I'm going to"
nonsense = "be there in a few minutes and I will be there in a few minutes and"
nwords = nonsense.split()
alts = [("the", "get"), ("here", "back"), ("the", "at"), ("few", "bit"), ("couple", "lot"), ("min", "hours"),
        ("so", "but"), ("we", "you"), ("be", "have"), ("home", "back"), ("here", "at"), ("on", "at"),
        ("the", "few"), ("couple", "lot"), ("min", "days"), ("so", "lol")]
chars = "".join(f'<span class="ch" id="s4-c{i}">{"&nbsp;" if ch == " " else ch}</span>' for i, ch in enumerate(typed))
spans = "".join(f'<span class="tw" id="s4-t{i}"> {w}</span>' for i, w in enumerate(nwords))
sets = '<div class="sset" id="s4-set0"><span>I</span><span class="mid">be</span><span>the</span></div>'
for i, w in enumerate(nwords):
    nxt = nwords[i + 1] if i + 1 < len(nwords) else "be"
    a, b = alts[(i + 1) % len(alts)]
    sets += f'<div class="sset" id="s4-set{i+1}"><span>{a}</span><span class="mid">{nxt}</span><span>{b}</span></div>'
rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
kb = ""
for r, row in enumerate(rows):
    keys = "".join(f'<b class="k" id="s4-k{ch}">{ch}</b>' for ch in row)
    if r == 2:
        keys = '<b class="k fn">&#8679;</b>' + keys + '<b class="k fn">&#9003;</b>'
    kb += f'<div class="krow">{keys}</div>'
kb += '<div class="krow"><b class="k fn w2">123</b><b class="k space" id="s4-kspace">space</b><b class="k fn w2">return</b></div>'
slides.append(slide(4, f"""
  <div class="rig" id="s4-rig">
    <div class="phone2" id="s4-phone">
      <div class="island"></div>
      <div class="status"><span>9:41</span><span class="sig">&#9679;&#9679;&#9679; &#9646;</span></div>
      <div class="chathead"><div class="avatar">J</div><div><div class="cname">Jay</div><div class="csub">iMessage</div></div></div>
      <div class="thread">
        <div class="msg in">yo where are you??</div>
        <div class="msg in">we're all here already</div>
      </div>
      <div class="compose" id="s4-compose"><span class="ctext">{chars}{spans}</span><span class="caret2" id="s4-caret">|</span></div>
      <div class="suggbar">{sets}<div class="tap" id="s4-tap"></div></div>
      <div class="kb">{kb}</div>
    </div>
    <div class="stamp2" id="s4-stamp">NONSENSE.</div>
  </div>
  <div class="s4-label" id="s4-lab"><div class="tag">TRY IT</div><div class="s4-how">Type <b class="c">"I'm going to"</b><br/>tap the <b class="o">middle</b> word.<br/>Again. And again.</div></div>
  <div class="s4-out" id="s4-b">Your phone is guessing too.<br/>It's just <span class="o">really bad</span> at it.</div>"""))
tw("#s4-rig", {"opacity": 0, "y": 140, "scale": 0.92}, {"opacity": 1, "y": 0, "scale": 1}, at(4, 0.2), 0.9)
anims.append(f'tl.fromTo("#s4-rig", {{rotation: -2}}, {{rotation: 2, duration: {round(T[4]["dur"] - 1, 2)}, ease: "sine.inOut", immediateRender: false}}, {at(4, 0.2)});')
pop("#s4-lab", at(4, "Type") - 0.4)
tw("#s4-set0", {"opacity": 0}, {"opacity": 1}, at(4, 0.4), 0.2, "none")
# type "I'm going to" letter by letter, flashing the matching key
tc = at(4, "Type") + 0.5
_seen.add("#s4-tap")  # stays hidden (CSS) until the first tap
for i, ch in enumerate(typed):
    t = round(tc + i * 0.11, 3)
    anims.append(f'tl.set("#s4-c{i}", {{display: "inline"}}, {t});')
    kid = "#s4-kspace" if ch == " " else (f"#s4-k{ch.upper()}" if ch.isalpha() else None)
    if kid:
        anims.append(f'tl.fromTo("{kid}", {{backgroundColor: "#ff7a1a", scale: 1.25}}, {{backgroundColor: "#3a3f55", scale: 1, duration: 0.25, ease: "power1.out", immediateRender: false}}, {t});')
# zoom the camera in on the phone while the taps happen
t0 = at(4, "You'll get something") + 0.9
t_end = at(4, "It's nonsense") - 0.5
step = (t_end - t0) / len(nwords)
anims.append(f'tl.to("#s4-rig", {{scale: 1.18, y: -150, duration: 1.0, ease: "power2.inOut"}}, {round(t0 - 1.0, 3)});')
for i in range(len(nwords)):
    t = round(t0 + i * step, 3)
    anims.append(f'tl.set("#s4-t{i}", {{display: "inline"}}, {t});')
    tw(f"#s4-tap", {"opacity": 0.9, "scale": 0.3}, {"opacity": 0, "scale": 1.6}, t - 0.05, round(step * 0.9, 3), "power2.out")
    tw(f"#s4-set{i}", {"opacity": 1}, {"opacity": 0}, t, 0.05, "none")
    tw(f"#s4-set{i+1}", {"opacity": 0}, {"opacity": 1}, t, 0.05, "none")
fade_out("#s4-lab", t0 - 0.8)
# stamp slams onto the phone, phone shakes, camera pulls back and slides left
tn = at(4, "It's nonsense")
anims.append(f'tl.to("#s4-rig", {{scale: 1, y: 0, duration: 0.45, ease: "power3.out"}}, {round(tn - 0.45, 3)});')
tw("#s4-stamp", {"opacity": 0, "scale": 3, "rotation": -25}, {"opacity": 1, "scale": 1, "rotation": -12}, tn, 0.3, "power4.in")
anims.append(f'tl.fromTo("#s4-phone", {{x: -14}}, {{x: 14, duration: 0.06, repeat: 5, yoyo: true, ease: "none", immediateRender: false}}, {round(tn + 0.3, 3)});')
anims.append(f'tl.set("#s4-phone", {{x: 0}}, {round(tn + 0.7, 3)});')
anims.append(f'tl.to("#s4-rig", {{x: -420, duration: 0.8, ease: "power3.inOut"}}, {round(tn + 1.2, 3)});')
pop("#s4-b", tn + 1.7)

# ---------- Slide 5: phone brain vs library (AI illustration) ----------
slides.append(slide(5, """
  <img class="bgimg" id="s5-img" src="assets/brain-library.png" alt=""/>
  <div class="shade"></div>
  <div class="lab left-lab" id="s5-l"><div class="tag">YOUR PHONE</div>learned from <b>your texts</b></div>
  <div class="lab right-lab" id="s5-r"><div class="tag c-tag">CHATGPT</div>learned from <b>books, websites,<br/>articles, forums, code</b></div>
  <div class="scale" id="s5-scale">SCALE.</div>
  <div class="lifetimes" id="s5-life">More reading than any human<br/>could do in <span class="o">thousands of lifetimes.</span></div>
  <div class="tokens" id="s5-tok">
    <div class="tag">SMALL CORRECTION: IT'S <span class="o">TOKENS</span></div>
    <div class="tokrow"><span class="tk">un</span><span class="tk">believ</span><span class="tk">able</span><span class="plus">+</span><span class="tk whole">guess</span></div>
    <p class="sub small">Sometimes a whole word, sometimes half a word.</p>
  </div>"""))
tw("#s5-img", {"scale": 1.0, "opacity": 0}, {"scale": 1.12, "opacity": 1}, at(5, 0.1), 19, "none")
tw("#s5-img", {"opacity": 1}, {"opacity": 0.12}, at(5, "And one small"), 0.8, "power1.out")
tw("#s5-scale", {"opacity": 0, "scale": 1.6}, {"opacity": 1, "scale": 1}, at(5, "Scale"), 0.5, "power4.out")
fade_out("#s5-scale", at(5, "Your phone learned") + 0.8)
pop("#s5-l", at(5, "Your phone learned"))
pop("#s5-r", at(5, "Models like"))
pop("#s5-life", at(5, "More reading"))
for s in ["#s5-l", "#s5-r", "#s5-life"]:
    fade_out(s, at(5, "And one small") - 0.2)
pop("#s5-tok .tag", at(5, "And one small") + 0.4)
for i, t in enumerate([at(5, "tokens") - 1.0, at(5, "tokens") - 0.6, at(5, "tokens") - 0.2]):
    anims.append(f'tl.fromTo("#s5-tok .tk:nth-child({i+1})", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.35, ease:"back.out(2)"}}, {round(t,3)});')
tw("#s5-tok .plus", {"opacity": 0}, {"opacity": 1}, at(5, "Sometimes a whole") - 0.3, 0.3)
tw("#s5-tok .whole", {"opacity": 0, "x": -30}, {"opacity": 1, "x": 0}, at(5, "Sometimes a whole"), 0.35, "back.out(2)")
pop("#s5-tok .sub", at(5, "Sometimes a whole") + 0.8)

# ---------- Slide 6: the question ----------
slides.append(slide(6, """
  <div class="center">
    <h1 class="big" id="s6-a">Wait&hellip; then how does it<br/><span class="o">solve problems?</span></h1>
    <div class="cards" id="s6-cards">
      <div class="card" id="s6-c1"><span class="ic">&lt;/&gt;</span>Write working code</div>
      <div class="card" id="s6-c2"><span class="ic">$</span>Explain a tax form</div>
      <div class="card" id="s6-c3"><span class="ic">&#9829;</span>Plan a wedding</div>
    </div>
    <div class="auto" id="s6-auto">That's it? <span class="strike">Autocomplete?</span></div>
    <div class="wild" id="s6-wild">No. It's actually <span class="o">wild.</span></div>
  </div>"""))
pop("#s6-a", at(6, 0.3), 60, 0.8)
pop("#s6-c1", at(6, "how can it write"))
pop("#s6-c2", at(6, "or explain"))
pop("#s6-c3", at(6, "or help plan"))
fade_out("#s6-cards", at(6, "That's it?") - 0.6)
pop("#s6-auto", at(6, "That's it?") - 0.2)
T6W = at(6, "no, it's actually wild") - 0.4
anims.append(f'tl.fromTo("#s6-auto .strike", {{"--strike": "0%"}}, {{"--strike": "100%", duration: 0.5, ease: "power2.out"}}, {T6W});')
pop("#s6-wild", at(6, "no, it's actually wild"))

# ---------- Slide 7: to guess well you have to understand (concept scene: shattering glass) ----------
slides.append(slide(7, """
  <img class="bgimg" id="s7-img" src="assets/glass.png" alt=""/>
  <div class="shade-left"></div>
  <div class="center">
    <h1 class="big s7-title" id="s7-a">To guess well,<br/>you have to<br/><span class="c">understand a lot.</span></h1>
    <div class="sent s7-first" id="s7-s1"><span>"She dropped the glass, and it&hellip;"</span><span class="ans o" id="s7-a1">breaks</span><span class="need" id="s7-n1">needs: facts</span></div>
    <div class="sent" id="s7-s2"><span>"Need 3 eggs, have 2, so I&hellip;"</span> <span class="ans o" id="s7-a2">buy more</span><span class="need" id="s7-n2">needs: reasoning</span></div>
    <div class="absorb" id="s7-abs">
      <span class="pill" id="s7-p1">grammar</span><span class="pill" id="s7-p2">facts</span><span class="pill" id="s7-p3">logic</span><span class="pill" id="s7-p4">how people explain</span>
    </div>
    <p class="sub" id="s7-b">Nobody programmed these in. <span class="o">They got absorbed.</span></p>
  </div>"""))
t_dim7 = at(7, "The recipe") - 0.5
tw("#s7-img", {"scale": 1.0}, {"scale": 1.12}, at(7, 0.0), round(t_dim7 - at(7, 0.0), 2), "none")
anims.append(f'tl.fromTo("#s7-img", {{opacity: 0}}, {{opacity: 1, duration: 4, ease: "sine.inOut", immediateRender: false}}, {at(7, 0.0)});')
tw("#s7-img", {"opacity": 1}, {"opacity": 0.12}, t_dim7, 0.8, "power1.out")
pop("#s7-a", at(7, 0.4), 60, 0.8)
fade_out("#s7-a", t_dim7)
pop("#s7-s1", at(7, "She dropped"))
pop("#s7-a1", at(7, "You need to know"), 20, 0.4)
pop("#s7-n1", at(7, "You need to know") + 0.5, 10, 0.4)
anims.append(f'tl.to("#s7-s1", {{x: 100, y: -470, duration: 0.7, ease: "power3.inOut"}}, {round(t_dim7, 3)});')
pop("#s7-s2", at(7, "The recipe"))
pop("#s7-a2", at(7, "Now you need") - 0.4, 20, 0.4)
pop("#s7-n2", at(7, "Now you need") + 0.3, 10, 0.4)
for s_ in ["#s7-s1", "#s7-s2"]:
    fade_out(s_, at(7, "To predict well") - 0.2)
for i in range(4):
    tw(f"#s7-p{i+1}", {"opacity": 0, "scale": 0.5}, {"opacity": 1, "scale": 1}, at(7, "To predict well") + 1.2 + i * 1.0, 0.45, "back.out(2)")
pop("#s7-b", at(7, "Nobody programmed"))

# ---------- Slide 8: taught manners (concept scene: robot at manners school) ----------
slides.append(slide(8, """
  <img class="bgimg" id="s8-img" src="assets/manners.png" alt=""/>
  <div class="s8-head" id="s8-head"><div class="tag" id="s8-tag">STEP 2</div><h1 class="big" id="s8-a">Taught <span class="o">manners.</span></h1></div>
  <div class="callout" id="s8-ex">examples of<br/><b>great answers</b></div>
  <div class="ring" id="s8-ring"></div>
  <div class="callout c2" id="s8-rt">rated by<br/><b class="o">people</b></div>
  <div class="center s8-diag" id="s8-diag">
    <div class="flow">
      <div class="box raw" id="s8-raw"><div class="bt">Raw text predictor</div>&hellip;continues random internet text</div>
      <div class="arrow" id="s8-arr"><div class="stars" id="s8-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><div class="line"></div><div class="lbl">examples + ratings</div></div>
      <div class="box good" id="s8-good"><div class="bt">Helpful assistant</div>the one you chat with</div>
    </div>
  </div>"""))
t_dim8 = at(8, "That's the difference") - 0.6
tw("#s8-img", {"scale": 1.0}, {"scale": 1.12}, at(8, 0.0), round(t_dim8 - at(8, 0.0), 2), "none")
anims.append(f'tl.fromTo("#s8-img", {{opacity: 0}}, {{opacity: 1, duration: 4, ease: "sine.inOut", immediateRender: false}}, {at(8, 0.0)});')
tw("#s8-img", {"opacity": 1}, {"opacity": 0.12}, t_dim8, 0.8, "power1.out")
pop("#s8-tag", at(8, 0.3))
pop("#s8-a", at(8, 0.5), 50, 0.7)
pop("#s8-ex", at(8, "People show"))
tw("#s8-ring", {"opacity": 0, "scale": 0.6}, {"opacity": 1, "scale": 1}, at(8, "rate its"), 0.5, "back.out(2)")
pop("#s8-rt", at(8, "rate its") + 0.3)
for s_ in ["#s8-ex", "#s8-ring", "#s8-rt"]:
    fade_out(s_, t_dim8)
anims.append(f'tl.to("#s8-head", {{y: -40, scale: 0.85, duration: 0.6, ease: "power2.inOut"}}, {round(t_dim8, 3)});')
pop("#s8-raw", t_dim8 + 0.3)
tw("#s8-arr .line", {"scaleX": 0}, {"scaleX": 1}, t_dim8 + 0.7, 0.6, "power2.inOut")
pop("#s8-arr .lbl", t_dim8 + 1.0, 10, 0.4)
tw("#s8-stars", {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, t_dim8 + 1.0, 0.5, "back.out(3)")
pop("#s8-good", t_dim8 + 1.6)
T8D = t_dim8 + 3.2
anims.append(f'tl.fromTo("#s8-good", {{boxShadow: "0 0 0px rgba(34,211,238,0)"}}, {{boxShadow: "0 0 60px rgba(34,211,238,0.55)", duration: 0.8, immediateRender: false}}, {T8D});')

# ---------- Slide 9: guessing != knowing ----------
slides.append(slide(9, """
  <div class="center">
    <h1 class="huge" id="s9-a">Guessing <span class="o">&ne;</span> Knowing</h1>
    <p class="sub" id="s9-b">Predicting what <i>sounds</i> right. Not looking it up.</p>
    <div class="venn" id="s9-venn">
      <div class="circ c1" id="s9-c1"><span>Sounds<br/>right</span></div>
      <div class="circ c2" id="s9-c2"><span>Is<br/>right</span></div>
      <div class="overlap" id="s9-ov">Paris &#10003;</div>
    </div>
    <div class="warn" id="s9-warn">&#9888; Wrong answers come in the <span class="o">same confident voice.</span></div>
  </div>"""))
pop("#s9-a", at(9, 0.3), 60, 0.8)
pop("#s9-b", at(9, "Not looking"))
anims.append(f'tl.to("#s9-a", {{scale: 0.62, y: -250, duration: 0.7, ease: "power3.inOut"}}, {at(9, "Most of the time") - 0.8});')
fade_out("#s9-b", at(9, "Most of the time") - 0.8)
tw("#s9-c1", {"opacity": 0, "x": -260}, {"opacity": 1, "x": -110}, at(9, "Most of the time"), 0.8)
tw("#s9-c2", {"opacity": 0, "x": 260}, {"opacity": 1, "x": 110}, at(9, "Most of the time"), 0.8)
pop("#s9-ov", at(9, "The capital"), 10, 0.4)
anims.append(f'tl.to("#s9-c2", {{x: 330, duration: 0.9, ease: "power2.inOut"}}, {at(9, "But sometimes")});')
anims.append(f'tl.to("#s9-c1", {{x: -330, duration: 0.9, ease: "power2.inOut"}}, {at(9, "But sometimes")});')
fade_out("#s9-ov", at(9, "But sometimes"), 0.3)
pop("#s9-warn", at(9, "same confident") - 1.2)

# ---------- Slide 10: next + sign-off ----------
slides.append(slide(10, """
  <div class="center">
    <div class="tag" id="s10-tag">NEXT VIDEO</div>
    <h1 class="big" id="s10-a">Why AI lies with a<br/><span class="o">straight face</span></h1>
    <div class="endcard" id="s10-end">I gotchu<span class="o">.</span></div>
  </div>"""))
pop("#s10-tag", at(10, 0.3))
pop("#s10-a", at(10, 0.6), 60, 0.8)
fade_out("#s10-tag", at(10, "I gotchu") - 0.5)
fade_out("#s10-a", at(10, "I gotchu") - 0.5)
tw("#s10-end", {"opacity": 0, "scale": 0.7}, {"opacity": 1, "scale": 1}, at(10, "I gotchu") - 0.2, 0.6, "back.out(2)")

# progress bar across the whole video
anims.append(f'tl.fromTo("#progress", {{scaleX: 0}}, {{scaleX: 1, duration: {TOTAL}, ease: "none"}}, 0);')

CSS = """
@font-face{font-family:Inter;font-weight:500;src:url(assets/fonts/inter-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:Inter;font-weight:700;src:url(assets/fonts/inter-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:Inter;font-weight:800;src:url(assets/fonts/inter-latin-800-normal.woff2) format("woff2")}
@font-face{font-family:Inter;font-weight:900;src:url(assets/fonts/inter-latin-900-normal.woff2) format("woff2")}
@font-face{font-family:"Archivo Black";src:url(assets/fonts/archivo-black-latin-400-normal.woff2) format("woff2")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#0a1128}
#root{width:1920px;height:1080px;position:relative;overflow:hidden;font-family:Inter,sans-serif;color:#f4f6fb;
  background:radial-gradient(1200px 700px at 75% 20%,#16235a 0%,#0a1128 60%,#070c1d 100%)}
.clip{position:absolute;inset:0}
.slide{display:flex;align-items:center;justify-content:center}
.center{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:44px;width:1920px;height:1080px;position:relative}
.top{position:absolute;top:120px;left:0;right:0}
.o{color:#ff7a1a}.c{color:#22d3ee}
.huge{font-family:"Archivo Black",Inter,sans-serif;font-size:132px;line-height:1.05;letter-spacing:-0.02em}
.big{font-family:"Archivo Black",Inter,sans-serif;font-size:96px;line-height:1.1;letter-spacing:-0.01em}
.sub{font-size:52px;font-weight:700;color:#c9d2ea;line-height:1.3}
.sub.small{font-size:40px}.sub.left{text-align:left}
.tag{display:inline-block;font-weight:800;font-size:30px;letter-spacing:0.18em;color:#ff7a1a;border:3px solid #ff7a1a;padding:10px 22px;border-radius:12px}
.c-tag{color:#22d3ee;border-color:#22d3ee}
.blank{display:inline-block;min-width:330px;border-bottom:10px solid #22d3ee;text-align:center;margin-left:14px}
.fill{display:inline-block}
.qcard{position:absolute;font-size:64px;font-weight:800;line-height:1.3;background:#111b40;border:3px solid #2a3a7a;border-radius:28px;padding:50px 80px;top:50%;left:50%;margin-left:-640px;margin-top:-150px;width:1280px}
.qmark{color:#ff7a1a;font-family:"Archivo Black";font-size:90px;margin-right:18px;vertical-align:middle}
.loop{display:flex;flex-direction:column;align-items:center;gap:40px;position:absolute;top:50%;left:0;right:0;margin-top:-150px}
.chips{display:flex;gap:18px;flex-wrap:wrap;justify-content:center}
.chip{font-size:64px;font-weight:800;background:#16235a;border:3px solid #22d3ee;border-radius:18px;padding:14px 30px}
.chip.ghost{border-style:dashed;border-color:#ff7a1a;color:#ff7a1a}
.counter{font-size:44px;font-weight:700;color:#c9d2ea}
.rig{position:absolute;left:50%;top:50%;width:560px;height:1000px;margin-left:-280px;margin-top:-500px}
.phone2{position:absolute;inset:0;border-radius:78px;background:#05070f;border:14px solid #1b2033;
  box-shadow:0 0 0 3px #3b4466,0 40px 120px rgba(0,0,0,.6),0 0 90px rgba(34,211,238,.18);overflow:hidden;display:flex;flex-direction:column}
.island{position:absolute;top:14px;left:50%;margin-left:-70px;width:140px;height:38px;border-radius:22px;background:#000;z-index:3}
.status{display:flex;justify-content:space-between;padding:18px 40px 0;font-size:22px;font-weight:700;color:#fff;height:58px}
.sig{letter-spacing:2px;font-size:16px}
.chathead{display:flex;align-items:center;gap:16px;padding:14px 26px 16px;border-bottom:1px solid #1d2233}
.avatar{width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#ff7a1a,#ff3b8b);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:28px}
.cname{font-size:26px;font-weight:800}.csub{font-size:18px;color:#8b93ad}
.thread{flex:1;display:flex;flex-direction:column;gap:12px;padding:22px 22px 0}
.msg{max-width:78%;font-size:26px;font-weight:500;padding:14px 20px;border-radius:26px;line-height:1.3}
.msg.in{background:#262a37;color:#eef1f8;border-bottom-left-radius:8px}
.compose{margin:10px 16px;min-height:66px;border:2px solid #2f3547;border-radius:30px;padding:12px 20px;font-size:29px;font-weight:600;line-height:1.35;color:#fff}
.ch,.tw{display:none}
#s4 .ch,#s4 .tw{opacity:1}.caret2{color:#22d3ee;font-weight:400}
.suggbar{position:relative;height:66px;background:#1a1d28;margin:0}
.sset{position:absolute;inset:0;display:flex;align-items:center;opacity:0}
.sset span{flex:1;text-align:center;font-size:26px;font-weight:600;color:#cfd5e6;border-right:1px solid #2c3142}
.sset span:last-child{border-right:none}
.sset .mid{color:#fff;font-weight:800}
.tap{position:absolute;left:50%;top:50%;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;background:radial-gradient(circle,rgba(255,122,26,.85) 0%,rgba(255,122,26,.35) 45%,rgba(255,122,26,0) 70%);opacity:0}
.kb{background:#1a1d28;padding:10px 8px 34px;display:flex;flex-direction:column;gap:12px}
.krow{display:flex;justify-content:center;gap:7px}
.k{width:46px;height:62px;border-radius:9px;background:#3a3f55;color:#fff;font-size:26px;font-weight:600;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 0 #0b0d14}
.k.fn{background:#2a2e3e;width:62px;font-size:24px}.k.w2{width:110px;font-size:21px}
.k.space{width:250px;font-size:21px;color:#cfd5e6}
.stamp2{position:absolute;left:50%;top:66%;width:720px;margin-left:-360px;text-align:center;font-family:"Archivo Black";font-size:104px;color:#ff3b3b;border:10px solid #ff3b3b;border-radius:18px;padding:4px 0;background:rgba(10,17,40,.55);opacity:0;z-index:5;text-shadow:0 0 30px rgba(255,59,59,.5)}
.s4-label{position:absolute;right:130px;top:50%;margin-top:-150px;display:flex;flex-direction:column;gap:26px;align-items:flex-start}
.s4-how{font-size:50px;font-weight:800;line-height:1.3}
.s4-out{position:absolute;right:120px;top:50%;margin-top:-90px;width:760px;font-family:"Archivo Black";font-size:64px;line-height:1.2}
.bgimg{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,12,29,0) 45%,rgba(7,12,29,.85) 100%)}
.lab{position:absolute;bottom:90px;font-size:44px;font-weight:600;line-height:1.35;display:flex;flex-direction:column;gap:14px;align-items:flex-start}
.left-lab{left:90px}.right-lab{right:90px;text-align:right;align-items:flex-end}
.scale{position:absolute;top:120px;left:0;right:0;text-align:center;font-family:"Archivo Black";font-size:170px;color:#fff;text-shadow:0 0 40px rgba(255,122,26,.7)}
.lifetimes{position:absolute;top:110px;left:90px;font-size:52px;font-weight:800;line-height:1.3;text-shadow:0 4px 30px #000}
.tokens{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:50px}
.tokrow{display:flex;gap:14px;align-items:center}
.tk{font-size:96px;font-weight:900;background:#16235a;border:4px solid #ff7a1a;border-radius:20px;padding:10px 34px}
.tk.whole{border-color:#22d3ee}.plus{font-size:80px;font-weight:900;color:#7d8bb8;margin:0 20px}
.cards{display:flex;gap:36px}
.card{font-size:44px;font-weight:800;background:#111b40;border:3px solid #2a3a7a;border-radius:24px;padding:36px 44px;display:flex;flex-direction:column;gap:18px;align-items:center;width:440px}
.ic{font-family:"Archivo Black";font-size:70px;color:#22d3ee}
.auto{position:absolute;top:50%;margin-top:30px;font-size:80px;font-weight:900;left:0;right:0}
.strike{position:relative;--strike:0%}
.strike::after{content:"";position:absolute;left:0;top:52%;height:12px;width:var(--strike);background:#ff7a1a;border-radius:6px}
.wild{position:absolute;top:50%;margin-top:190px;left:0;right:0;font-size:80px;font-weight:900}
.sent{font-size:54px;font-weight:700;background:#111b40;border:3px solid #2a3a7a;border-radius:24px;padding:30px 44px;display:flex;align-items:center;gap:26px;position:absolute;left:50%;width:1500px;margin-left:-750px}
#s7-s2{top:50%;margin-top:110px}
.ans{font-weight:900}.need{margin-left:auto;font-size:32px;font-weight:800;color:#22d3ee;letter-spacing:.06em;text-transform:uppercase}
.absorb{display:flex;gap:26px;position:absolute;top:50%;margin-top:-40px}
.pill{font-size:52px;font-weight:800;background:#16235a;border:3px solid #22d3ee;border-radius:60px;padding:18px 40px}
#s7-b{position:absolute;top:50%;margin-top:130px}
.flow{display:flex;align-items:center;gap:40px}
.box{width:520px;border-radius:28px;padding:40px;font-size:36px;font-weight:600;color:#c9d2ea;line-height:1.35;text-align:left}
.bt{font-size:46px;font-weight:900;color:#fff;margin-bottom:12px}
.raw{background:#161a2b;border:3px dashed #56607f}.good{background:#0f2440;border:4px solid #22d3ee}
.arrow{width:360px;display:flex;flex-direction:column;align-items:center;gap:16px}
.arrow .line{width:100%;height:10px;background:#ff7a1a;border-radius:6px;transform-origin:left center;position:relative}
.arrow .line::after{content:"";position:absolute;right:-6px;top:-14px;border-left:30px solid #ff7a1a;border-top:19px solid transparent;border-bottom:19px solid transparent}
.stars{font-size:50px;color:#ffc53d;letter-spacing:6px}.lbl{font-size:30px;font-weight:700;color:#c9d2ea}
.shade-left{position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,12,29,.8) 0%,rgba(7,12,29,.35) 45%,rgba(7,12,29,0) 65%)}
.s7-title{position:absolute;left:110px;top:150px;text-align:left;font-size:92px}
.sent.s7-first{left:110px;margin-left:0;width:auto;top:auto;bottom:130px;flex-wrap:nowrap}
.s8-head{position:absolute;top:60px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:20px}
.callout{position:absolute;font-size:40px;font-weight:700;line-height:1.25;background:rgba(10,17,40,.82);border:3px solid #22d3ee;border-radius:20px;padding:18px 26px;left:230px;top:330px}
.callout.c2{left:auto;right:120px;top:360px;border-color:#ff7a1a}
.ring{position:absolute;left:1015px;top:520px;width:380px;height:230px;border:8px solid #ff7a1a;border-radius:30px;box-shadow:0 0 50px rgba(255,122,26,.6)}
.s8-diag{padding-top:120px}
.venn{position:absolute;top:50%;left:50%;width:0;height:0}
.circ{position:absolute;width:520px;height:520px;border-radius:50%;left:-260px;top:-190px;display:flex;align-items:center;font-size:48px;font-weight:900;line-height:1.15}
.c1{background:rgba(255,122,26,.28);border:5px solid #ff7a1a;justify-content:flex-start;padding-left:70px}
.c2{background:rgba(34,211,238,.25);border:5px solid #22d3ee;justify-content:flex-end;padding-right:90px;text-align:right}
.overlap{position:absolute;left:-120px;top:50px;width:240px;text-align:center;font-size:44px;font-weight:900}
.warn{position:absolute;top:50%;margin-top:370px;font-size:48px;font-weight:800;left:0;right:0}
.endcard{position:absolute;font-family:"Archivo Black";font-size:190px;top:50%;margin-top:-120px;left:0;right:0}
#brand{position:absolute;top:44px;left:60px;font-family:"Archivo Black";font-size:34px;color:#fff;opacity:.85;z-index:10}
#brand span{color:#ff7a1a}
#progress{position:absolute;left:0;bottom:0;height:10px;width:1920px;background:linear-gradient(90deg,#ff7a1a,#22d3ee);transform-origin:left center;z-index:10}
/* everything animated starts hidden */
.slide [id]{opacity:0}
#s5-scale,#s5-l,#s5-r,#s5-life{opacity:0}
.tokens .tag,.tokens .tk,.tokens .plus,.tokens .sub,.loop .tag{opacity:0}
#s8-arr .lbl{opacity:0}
#s6-cards,#s8-arr,#s8-diag,#s8-head,#s9-venn,#s3-loop,#s5-tok,#s7-abs,#s4-phone,#s4-compose,#s4-caret,#s4 .k{opacity:1}
"""

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1920, height=1080"/>
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
  <audio id="vo" src="assets/vo/voiceover.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
  <div id="brand">igotchu<span>.</span></div>
  {''.join(slides)}
  <div id="progress"></div>
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join('  ' + a for a in anims)}
  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
</body>
</html>
"""
open("video/index.html", "w").write(html)
print("wrote video/index.html, total", TOTAL, "s,", len(anims), "tweens")
