"""igotchu Script 3 v2.1, build v4: HyperFrames composition on the Neon Blueprint design system,
set in the Type Lab's condensed type ("Neon Instrument" hybrid picked by the 8-expert panel).

What changed from v3 (panel fixes):
- scenes cross over (next scene slides in before its first word, never a blank frame)
- a visible camera push on every scene, phone sway, nothing frozen > ~3 s (checked below)
- one AI illustration only (slide 8); everything else is built in code
- no wordmark or crop marks; a thin progress line plus a chapter name that shows when it changes
- SFX: fixed whoosh, quieter thud, identical sounds spaced >= .3 s, tick on predicted words, phone buzz
- master: two-pass loudnorm to -14 LUFS / -1 dBTP

Inputs: timing.json, slides.json, segments.json (speech segments per slide, relative to slide start), ds/.
Output: video/index.html + video/assets/mix.mp3.
"""
import json
import os
import re
import shutil

THEME = os.environ.get("THEME", "neon")  # neon (hybrid) | instrument | patent
OUT = "video" if THEME == "neon" else f"video_{THEME}"
KEYBG = {"neon": "#18265a", "instrument": "#ffffff", "patent": "#f7faf8"}[THEME]

T = {i + 1: s for i, s in enumerate(json.load(open("timing.json")))}
SL = {s["n"]: s for s in json.load(open("slides.json"))}
SEG = {int(k): v for k, v in json.load(open("segments.json")).items()}
TOTAL = round(T[10]["start"] + T[10]["dur"], 3)
XO = 0.35  # scene crossover


# ---------------------------------------------------------------- timing helpers
def at(n, rel):
    return round(T[n]["start"] + rel, 3)


_ALIGN = {}


def _align(n):
    """Match the script's phrases (split at punctuation) to the slide's speech segments (split at pauses).
    Monotonic DP: each group of 1-3 phrases takes 1-3 segments; cost = squared gap between the group's
    duration and its expected duration at the slide's speaking rate."""
    if n in _ALIGN:
        return _ALIGN[n]
    text = SL[n]["text"]
    cuts = [0] + [m.end() for m in re.finditer(r"[,.?!:;…]+[\"”']?\s+", text)] + [len(text)]
    cuts = sorted(set(cuts))
    ph = [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)]
    segs = SEG[n]
    rate = sum(e - s for s, e in segs) / len(text)
    P, M = len(ph), len(segs)
    INF = float("inf")
    best = {(0, 0): (0.0, None)}
    for i in range(P + 1):
        for j in range(M + 1):
            if (i, j) not in best:
                continue
            c0 = best[(i, j)][0]
            for k in range(1, 4):
                for m in range(1, 4):
                    if i + k > P or j + m > M:
                        continue
                    chars = ph[i + k - 1][1] - ph[i][0]
                    dur = segs[j + m - 1][1] - segs[j][0]
                    c = c0 + (dur - rate * chars) ** 2 + 0.05 * (k + m - 2)
                    if c < best.get((i + k, j + m), (INF,))[0]:
                        best[(i + k, j + m)] = (c, (i, j))
    anchors = []
    node = (P, M)
    while node != (0, 0):
        i0, j0 = best[node][1]
        s0, e0 = segs[j0][0], segs[node[1] - 1][1]
        c_start, c_end = ph[i0][0], ph[node[0] - 1][1]
        for q in range(i0, node[0]):
            anchors.append((ph[q][0], s0 + (e0 - s0) * (ph[q][0] - c_start) / max(1, c_end - c_start)))
        node = (i0, j0)
    _ALIGN[n] = sorted(anchors)
    return _ALIGN[n]


def cue(n, phrase, off=0.0):
    """Absolute time when `phrase` starts in slide n."""
    text = SL[n]["text"]
    i = text.find(phrase)
    if i < 0:
        raise KeyError(f"slide {n}: {phrase!r}")
    anchors = _align(n)
    k = max(q for q in range(len(anchors)) if anchors[q][0] <= i)
    c0, t0 = anchors[k]
    c1, t1 = anchors[k + 1] if k + 1 < len(anchors) else (len(text), SEG[n][-1][1])
    t = t0 + (t1 - t0) * (i - c0) / max(1, c1 - c0)
    return at(n, t + off)


def end_of(n):
    return round(T[n]["start"] + T[n]["dur"], 3)


# ---------------------------------------------------------------- animation helpers (motion system)
A = []
SFX = []
_seen = set()
MOTION = []  # (start, end) of visible changes, for the frozen-frame check


def _tw(sel, frm, to, t, dur, ease):
    v = {**to, "duration": round(dur, 3), "ease": ease}
    if sel in _seen:
        v["immediateRender"] = False
    _seen.add(sel)
    A.append(f"tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(v)},{round(t, 3)});")
    MOTION.append((t, t + dur))


def raw(js, t=None, dur=0.3):
    A.append(js)
    if t is not None:
        MOTION.append((t, t + dur))


def rise(sel, t, y=40, dur=0.55):
    _tw(sel, {"opacity": 0, "y": y}, {"opacity": 1, "y": 0}, t, dur, "igOut")


def settle(sel, t, dur=0.5, sound=False):
    """No-overshoot entrance (panel: replace most bouncy pops)."""
    if sound:
        SFX.append((t, "pop"))
    _tw(sel, {"opacity": 0, "scale": 0.94, "y": 14}, {"opacity": 1, "scale": 1, "y": 0}, t, dur, "igSettle")


def fade(sel, t, dur=0.45):
    _tw(sel, {"opacity": 0}, {"opacity": 1}, t, dur, "none")


def lift_out(sel, t, dur=0.3):
    _tw(sel, {"opacity": 1, "y": 0}, {"opacity": 0, "y": -20}, t, dur, "igIn")


def out(sel, t, dur=0.2):
    _tw(sel, {"opacity": 1}, {"opacity": 0}, t, dur, "none")


def dim(sel, t, to=0.25, dur=0.4):
    raw(f'tl.to({json.dumps(sel)},{{opacity:{to},duration:{dur},ease:"none"}},{round(t, 3)});', t, dur)


def pop(sel, t, dur=0.5, s=0.6, sound=True):
    if sound:
        SFX.append((t, "pop"))
    _tw(sel, {"opacity": 0, "scale": s}, {"opacity": 1, "scale": 1}, t, dur, "igPop")


def land(sel, t):
    SFX.append((t + 0.15, "ding"))
    _tw(sel, {"opacity": 0, "y": -60, "scale": 0.8}, {"opacity": 1, "y": 0, "scale": 1}, t, 0.55, "igPop")


def slide_in(sel, t, dx, dur=0.6):
    _tw(sel, {"opacity": 0, "x": dx}, {"opacity": 1, "x": 0}, t, dur, "igOut")


def grow(sel, t, dur=0.6, sx=0):
    _tw(sel, {"scaleX": sx}, {"scaleX": 1}, t, dur, "igOut")


def draw(sel, t, length, dur=0.8):
    _tw(sel, {"strokeDashoffset": length, "opacity": 1}, {"strokeDashoffset": 0, "opacity": 1}, t, dur, "igOut")


def slam(sel, t):
    SFX.append((t + 0.28, "thud"))
    _tw(sel, {"opacity": 0, "rotation": -16, "scale": 2.4}, {"opacity": 1, "rotation": -8, "scale": 1}, t, 0.32, "igSlam")
    raw(f'tl.to({json.dumps(sel)},{{keyframes:[{{x:-10,y:6,duration:.07}},{{x:8,y:-4,duration:.07}},{{x:-4,y:2,duration:.07}},{{x:0,y:0,duration:.07}}],ease:"none"}},{round(t + 0.32, 3)});', t + 0.32, 0.3)


def ignite(sel, t):
    raw(f'tl.fromTo({json.dumps(sel)},{{opacity:0}},{{keyframes:[{{opacity:1,duration:.11}},{{opacity:.2,duration:.07}},{{opacity:1,duration:.09}},{{opacity:.5,duration:.07}},{{opacity:1,duration:.11}}],ease:"none"}},{round(t, 3)});', t, 0.5)
    _seen.add(sel)


def show(sel, t, disp="inline"):
    raw(f'tl.set({json.dumps(sel)},{{display:"{disp}"}},{round(t, 3)});', t, 0.05)


def hide(sel, t):
    raw(f'tl.set({json.dumps(sel)},{{display:"none"}},{round(t, 3)});', t, 0.05)


def cls(sel, c, t):
    raw(f'tl.set({json.dumps(sel)},{{className:{json.dumps(c)}}},{round(t, 3)});', t, 0.1)


def to(sel, props, t, dur, ease="igIO"):
    p = ",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())
    raw(f'tl.to({json.dumps(sel)},{{{p},duration:{dur},ease:"{ease}"}},{round(t, 3)});', t, dur)


def pulse(sel, t, s=1.08):
    """Emphasis on a stressed word: quick scale up and back."""
    raw(f'tl.fromTo({json.dumps(sel)},{{scale:1}},{{keyframes:[{{scale:{s},duration:.18}},{{scale:1,duration:.32}}],ease:"sine.inOut",immediateRender:false}},{round(t, 3)});', t, 0.5)


def blink(sel, t0, t1):
    n = int((t1 - t0) / 0.5)
    if n > 0:
        raw(f'tl.fromTo({json.dumps(sel)},{{opacity:1}},{{opacity:0,duration:.5,ease:"steps(1)",repeat:{n - 1},yoyo:true,immediateRender:false}},{round(t0, 3)});')


def sway(sel, t0, t1):
    """Subtle handheld drift for physical objects (phone, chat)."""
    d = round(t1 - t0, 2)
    raw(f'tl.fromTo({json.dumps(sel)},{{rotation:-.6}},{{rotation:.6,duration:{d},ease:"sine.inOut",immediateRender:false}},{round(t0, 3)});')


def typeon(prefix, n_chars, t0, cps=18, sound=False):
    for i in range(n_chars):
        t = round(t0 + i / cps, 3)
        show(f"#{prefix}{i}", t)
        if sound and i % 2 == 0:
            SFX.append((t, "click"))
    return t0 + n_chars / cps


def chars(prefix, text, cls_="ch"):
    return "".join(f'<span class="{cls_}" id="{prefix}{i}">{"&nbsp;" if c == " " else c}</span>' for i, c in enumerate(text))


S = []


def scene(n, inner, extra_cls=""):
    s = T[n]
    start = s["start"] if n == 1 else round(s["start"] - XO, 3)
    dur = round(s["dur"] + (0 if n == 1 else XO), 3)
    track = 1 + (n % 2)
    S.append(f'<section id="s{n}" class="clip scene {extra_cls}" data-start="{start}" data-duration="{dur}" data-track-index="{track}">'
             f'<div class="tr"><div class="cam">{inner}</div></div></section>')
    if n > 1:
        SFX.append((start + 0.05, "whoosh"))
        raw(f'tl.fromTo("#s{n} > .tr",{{opacity:0,x:90}},{{opacity:1,x:0,duration:.5,ease:"igOut"}},{start});', start, 0.5)
    if n < 10:
        t_exit = round(T[n + 1]["start"] - XO + 0.05, 3)
        raw(f'tl.to("#s{n} > .tr",{{opacity:0,x:-70,duration:.3,ease:"igIn"}},{t_exit});', t_exit, 0.3)
    # visible camera: content layer push + slight drift for the whole slide
    raw(f'tl.fromTo("#s{n} .cam",{{scale:1,x:0}},{{scale:1.05,x:-24,duration:{round(dur, 2)},ease:"sine.inOut"}},{start});')


def predictor_steps(pid, steps, t0, gaps, show_pct=False, keep_last=False, tick=True):
    """Candidate panel for next-word prediction. steps: [(winner, [(word, pct), ...]), ...]."""
    html = []
    t = t0
    for i, (win, cands) in enumerate(steps):
        rows = "".join(
            f'<div class="pr-row{" win" if w == win else ""}"><span class="w">{w}</span>'
            f'<span class="bar"><i style="width:{p}%"></i></span>'
            + (f'<span class="pct">{p}%</span>' if show_pct else "")
            + "</div>"
            for w, p in cands)
        html.append(f'<div class="pr-panel" id="{pid}-p{i}">{rows}</div>')
        gap = gaps[i] if i < len(gaps) else gaps[-1]
        fade(f"#{pid}-p{i}", t, 0.12)
        raw(f'tl.fromTo("#{pid}-p{i} .bar i",{{scaleX:0}},{{scaleX:1,duration:{round(gap * 0.45, 2)},ease:"igOut",stagger:.05}},{round(t + 0.04, 3)});', t, gap * 0.5)
        cls(f"#{pid}-p{i}", "pr-panel lock", round(t + gap * 0.62, 3))
        show(f"#{pid}-w{i}", round(t + gap * 0.7, 3))
        if tick:
            SFX.append((round(t + gap * 0.62, 3), "tick"))
        _tw(f"#{pid}-w{i}", {"opacity": 0, "y": -24}, {"opacity": 1, "y": 0}, round(t + gap * 0.7, 3), 0.3, "igPop")
        if not (keep_last and i == len(steps) - 1):
            out(f"#{pid}-p{i}", round(t + gap - 0.1, 3), 0.08)
        t += gap
    words = "".join(f'<span class="rw" id="{pid}-w{i}">{w} </span>' for i, (w, _) in enumerate(steps))
    return "".join(html), words, t


# ================================================================ SCENES
# ---- 1. Mom's text on the lock screen; your brain guesses the next five minutes
LOCK = """<div class="lock"><div class="lk-time">7:42</div><div class="lk-date">Tuesday, September 22</div></div>"""
scene(1, f"""
  <div class="rig1" id="s1-rig"><div class="ig-phone p1"><div class="screen lockscreen">
    <div class="notch"></div>{LOCK}
    <div class="notif" id="s1-n"><div class="nf-app"><i class="nf-ico">&#9993;</i><span>MESSAGES</span><span class="nf-now">now</span></div>
      <div class="nf-from">Mom</div><div class="nf-body">Call me when you get a sec<span class="dot" id="s1-dot">.</span><span class="party" id="s1-party">&#127881;</span></div></div>
    <div class="ghosts" id="s1-gh"><div class="gh">Call me.</div><div class="gh">call me when you can</div></div>
  </div></div></div>
  <div class="nope" id="s1-nope"><span class="ig-label ig-em-o">A period. No emoji.</span></div>
  <div class="brain" id="s1-brain">
    <span class="ig-kicker" id="s1-k"><span class="ig-kicker-dot"></span>Your brain, guessing</span>
    <div class="gpanel">
      <div class="grow-r" id="s1-r1"><span class="w">Somebody's sick</span><span class="bar"><i id="s1-b1" style="width:78%"></i></span></div>
      <div class="grow-r" id="s1-r2"><span class="w">Forgot a birthday</span><span class="bar"><i id="s1-b2" style="width:52%"></i></span></div>
      <div class="grow-r" id="s1-r3"><span class="w">Just wants to chat</span><span class="bar"><i id="s1-b3" style="width:18%"></i></span></div>
    </div>
    <div class="eq ig-body-lg" id="s1-eq">That's how <span class="ig-em-c">ChatGPT</span> works.</div>
  </div>""")
raw('tl.set("#s1-rig",{opacity:1},0);')
_tw("#s1-rig", {"scale": 0.96, "y": 30}, {"scale": 1, "y": 0}, 0, 0.9, "igOut")
sway("#s1-rig .ig-phone", 0.2, end_of(1))
t_n = at(1, 0.35)
SFX.append((t_n, "buzz"))
_tw("#s1-n", {"opacity": 0, "y": -90, "scale": 0.96}, {"opacity": 1, "y": 0, "scale": 1}, t_n, 0.55, "igPop")
raw(f'tl.to("#s1-rig",{{keyframes:[{{x:-6,duration:.05}},{{x:6,duration:.05}},{{x:-4,duration:.05}},{{x:0,duration:.05}}],ease:"none"}},{t_n});', t_n, 0.2)
t_ne = cue(1, "No emoji")
raw(f'tl.fromTo("#s1-dot",{{color:"#f4f7ff",scale:1}},{{color:"#ff7a1a",scale:2.2,duration:.35,ease:"igPop"}},{t_ne});', t_ne, 0.35)
settle("#s1-nope", t_ne + 0.1)
pulse("#s1-n", cue(1, "just that"), 1.04)
t_b = cue(1, "And your brain")
lift_out("#s1-nope", t_b - 0.2)
slide_in("#s1-brain", t_b - 0.1, 120)
pop("#s1-k", t_b + 0.1)
for i, ph in enumerate(["Somebody's sick", "or you forgot", "or you forgot"]):
    tt = cue(1, ph) + (0.5 if i == 2 else 0)
    rise(f"#s1-r{i+1}", tt - 0.1, 20, 0.35)
    grow(f"#s1-b{i+1}", tt, 0.7)
t_seen = cue(1, "You've seen")
fade("#s1-gh", t_seen, 0.4)
_tw("#s1-gh .gh", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0}, t_seen, 0.5, "igOut")
pulse("#s1-r1", cue(1, "guessed what"), 1.05)
settle("#s1-eq", cue(1, "That's pretty much"), 0.5, True)

# ---- 2. Party emoji flips every guess; then the promise (it writes working code)
code2 = [("def", "kw"), (" total(prices):", "")]
scene(2, f"""
  <div class="rig1 still" id="s2-rig"><div class="ig-phone p1"><div class="screen lockscreen">
    <div class="notch"></div>{LOCK}
    <div class="notif on"><div class="nf-app"><i class="nf-ico">&#9993;</i><span>MESSAGES</span><span class="nf-now">now</span></div>
      <div class="nf-from">Mom</div><div class="nf-body">Call me when you get a sec<span class="party" id="s2-party">&#127881;</span></div></div>
  </div></div></div>
  <div class="brain on" id="s2-brain">
    <span class="ig-kicker"><span class="ig-kicker-dot"></span>Your brain, guessing</span>
    <div class="gpanel" id="s2-gp">
      <div class="grow-r up" id="s2-r0"><span class="w">Somebody's engaged!</span><span class="bar"><i id="s2-b0" style="width:92%"></i></span></div>
      <div class="grow-r" id="s2-r1"><span class="w"><s id="s2-x1">Somebody's sick</s></span><span class="bar"><i id="s2-b1" style="width:78%"></i></span></div>
      <div class="grow-r" id="s2-r2"><span class="w">Forgot a birthday</span><span class="bar"><i id="s2-b2" style="width:52%"></i></span></div>
    </div>
  </div>
  <div class="q2" id="s2-q"><div class="ig-label ig-dim" id="s2-ql">The whole job</div>
    <h1 class="ig-h"><span id="s2-q1">Given everything so far&hellip;</span><br/><span class="ig-em-c" id="s2-q2">what comes next?</span><span class="caret" id="s2-caret">|</span></h1></div>
  <div class="code2" id="s2-code"><span class="ig-kicker ig-kicker--cyan"><span class="ig-kicker-dot"></span>Same trick</span>
    <div class="editor"><div><i class="kw">def</i> total(prices):</div><div class="ghost" id="s2-gh">&nbsp;&nbsp;&nbsp;&nbsp;<i class="kw">return</i> sum(prices)</div></div></div>""")
t_e = cue(2, "adds a party emoji") + 0.9
pop("#s2-party", t_e, 0.55, 0.2)
raw(f'tl.to("#s2-rig",{{keyframes:[{{y:-14,duration:.12}},{{y:0,duration:.3}}],ease:"sine.inOut"}},{t_e});', t_e, 0.42)
raw('tl.set("#s2-rig,#s2-brain,#s2-gp,#s2-r1,#s2-r2",{opacity:1},0);')
t_ns = cue(2, "Nobody's sick")
raw(f'tl.fromTo("#s2-b1",{{scaleX:1}},{{scaleX:.06,duration:.6,ease:"igIO",immediateRender:false}},{t_ns});', t_ns, 0.6)
cls("#s2-r1", "grow-r dead", t_ns + 0.2)
raw(f'tl.fromTo("#s2-b2",{{scaleX:1}},{{scaleX:.12,duration:.6,ease:"igIO",immediateRender:false}},{t_ns + 0.1});', t_ns, 0.7)
t_en = cue(2, "Somebody's engaged")
_tw("#s2-r0", {"opacity": 0, "y": -40}, {"opacity": 1, "y": 0}, t_en, 0.45, "igPop")
grow("#s2-b0", t_en + 0.1, 0.6)
SFX.append((t_en + 0.4, "ding"))
cls("#s2-r0", "grow-r up win", t_en + 0.5)
pulse("#s2-r0", cue(2, "One emoji flipped"), 1.05)
t_p = cue(2, "That's the problem")
to("#s2-rig", {"x": -900, "opacity": 0}, t_p - 0.3, 0.55, "igIn")
to("#s2-brain", {"x": 700, "opacity": 0}, t_p - 0.3, 0.55, "igIn")
fade("#s2-q", t_p, 0.1)
rise("#s2-ql", t_p + 0.05)
rise("#s2-q1", cue(2, "given everything"), 40)
rise("#s2-q2", cue(2, "what probably"), 40)
blink("#s2-caret", cue(2, "what probably"), end_of(2))
t_c = cue(2, "And somehow")
to("#s2-q", {"y": -170, "scale": 0.8}, t_c - 0.2, 0.5)
rise("#s2-code", t_c, 60)
raw(f'tl.fromTo("#s2-gh",{{opacity:.3}},{{opacity:1,duration:.3,ease:"none",immediateRender:false}},{cue(2, "writes working code")});', cue(2, "writes working code"), 0.3)
SFX.append((cue(2, "writes working code"), "tick"))
pulse("#s2-code .editor", cue(2, "writes working code") + 0.1, 1.04)

# ---- 3. It doesn't look it up; the loop; web search aside; tokens; streaming
st3 = [("How", [("How", 55), ("Maybe", 30), ("Try", 15)]), ("about", [("about", 80), ("'bout", 12), ("abt", 8)]),
       ("Biscuit?", [("Biscuit?", 40), ("Luna?", 35), ("Mochi?", 25)]), ("It's", [("It's", 70), ("Short,", 20), ("Cute,", 10)]),
       ("short", [("short", 60), ("cute", 30), ("classic", 10)]), ("and", [("and", 85), ("but", 10), ("&", 5)]),
       ("cute.", [("cute.", 65), ("sweet.", 30), ("fun.", 5)])]
t3_loop = cue(3, "It predicts the reply") - 0.1
gaps3 = [1.1, 0.95, 0.85, 0.7, 0.6, 0.5, 0.45]
p3, w3, t3_end = predictor_steps("lp", st3, t3_loop, gaps3)
toks = ["How", "&nbsp;about", "&nbsp;Bis", "cuit", "?", "&nbsp;It", "'s", "&nbsp;short"]
tok_html = "".join(f'<span class="tok t{i % 2}" id="s3-t{i}">{w}</span>' for i, w in enumerate(toks))
stream = "Biscuit is a classic, and it suits almost any cat, fluffy or not.".split()
stream_html = "".join(f'<span class="sw" id="s3-sw{i}">{w} </span>' for i, w in enumerate(stream))
scene(3, f"""
  <div class="myth" id="s3-myth">
    <div class="search" id="s3-search"><i>&#128269;</i><span>look up the answer&hellip;</span></div>
    <div class="sheet" id="s3-sheet"><div class="ig-label">Answer key</div><i></i><i></i><i></i><i class="s"></i></div>
    <svg class="xmark" viewBox="0 0 900 600"><path id="s3-x1" d="M120 80 L780 520"/><path id="s3-x2" d="M780 80 L120 520"/></svg>
    <span class="ig-pill ig-pill--o mythpill" id="s3-mp">Myth: it looks it up</span>
  </div>
  <div class="s3-loop" id="s3-loop">
    <div class="loopsteps">
      <span class="ig-pill" id="s3-k1">Read so far</span><span class="arr" id="s3-ar1">&rarr;</span>
      <span class="ig-pill" id="s3-k2">Guess next word</span><span class="arr" id="s3-ar2">&rarr;</span>
      <span class="ig-pill" id="s3-k3">Stick it on the end</span><span class="arr" id="s3-ar3">&#8635;</span>
    </div>
    <div class="chatwin wide" id="s3-chat">
      <div class="ig-bubble ig-bubble--me cw-q">Name for my cat?</div>
      <div class="ig-bubble ig-bubble--ai cw-a" id="s3-ans"><span class="reply">{w3}{stream_html}</span></div>
      <div class="pr-dock" id="s3-dock">{p3}</div>
      <div class="tokens" id="s3-toks"><span class="ig-label-sm ig-dim">Tokens</span>{tok_html}</div>
    </div>
    <div class="s3-count" id="s3-count"><span class="ig-em-o">&times; a few hundred</span> per answer</div>
  </div>
  <div class="web" id="s3-web"><div class="webrow"><i>&#128279;</i> Searching the web&hellip;</div><div class="wl"></div><div class="wl s"></div>
    <span class="ig-pill ig-pill--o" id="s3-wp">Extra step, bolted on</span></div>""")
settle("#s3-search", at(3, 0.1))
settle("#s3-sheet", at(3, 0.35))
t_d = cue(3, "It doesn't")
draw("#s3-x1", t_d, 800, 0.35)
draw("#s3-x2", t_d + 0.15, 800, 0.35)
SFX.append((t_d, "thud"))
pop("#s3-mp", t_d + 0.3)
t_ns3 = cue(3, "There's no answer sheet")
raw(f'tl.to("#s3-sheet",{{y:80,rotation:8,opacity:0,duration:.6,ease:"igIn"}},{t_ns3 + 0.3});', t_ns3 + 0.3, 0.6)
lift_out("#s3-myth", t3_loop - 0.5, 0.3)
raw('tl.set("#s3-myth",{opacity:1},0);')
for i in range(3):
    settle(f"#s3-k{i+1}", t3_loop - 0.4 + i * 0.12)
    fade(f"#s3-ar{i+1}", t3_loop - 0.3 + i * 0.12, 0.2)
_tw("#s3-chat", {"opacity": 0, "y": 100}, {"opacity": 1, "y": 0}, t3_loop - 0.5, 0.5, "igOut")
t = t3_loop
for i, g in enumerate(gaps3):
    k = (i % 3) + 1
    raw(f'tl.fromTo("#s3-k{k}",{{boxShadow:"0 0 0 2px #22d3ee, 0 0 60px rgba(34,211,238,.9)",scale:1.08}},{{boxShadow:"0 0 0 2px #22d3ee, 0 0 24px rgba(34,211,238,.55), 0 0 72px rgba(34,211,238,.25)",scale:1,duration:{round(g * 0.9, 2)},ease:"igOut",immediateRender:false}},{round(t, 3)});', t, g)
    t += g
t_web = cue(3, "If you see it searching")
slide_in("#s3-web", t_web, 160)
pop("#s3-wp", cue(3, "that's an extra step"))
t_und = cue(3, "Underneath")
dim("#s3-web", t_und, 0.2)
pulse("#s3-chat", t_und + 0.1, 1.03)
t_tok = cue(3, "The chunks are called tokens")
out("#s3-dock", t_tok - 0.2, 0.2)
lift_out("#s3-web", t_tok - 0.3)
fade("#s3-toks", t_tok, 0.2)
for i in range(len(toks)):
    settle(f"#s3-t{i}", t_tok + 0.2 + i * 0.12)
pulse("#s3-t2", cue(3, "bits of words"), 1.12)
pulse("#s3-t3", cue(3, "bits of words") + 0.15, 1.12)
t_cnt = cue(3, "A normal answer")
pop("#s3-count", t_cnt + 0.2)
for j in range(9):  # the loop spins faster and faster
    k = (j % 3) + 1
    tt = t_cnt + 0.4 + j * max(0.12, 0.35 - j * 0.03)
    raw(f'tl.fromTo("#s3-k{k}",{{boxShadow:"0 0 0 2px #22d3ee, 0 0 60px rgba(34,211,238,.9)",scale:1.08}},{{boxShadow:"0 0 0 2px #22d3ee, 0 0 24px rgba(34,211,238,.55), 0 0 72px rgba(34,211,238,.25)",scale:1,duration:.25,ease:"igOut",immediateRender:false}},{round(tt, 3)});', tt, 0.25)
t_st = cue(3, "When the text streams")
for i in range(len(stream)):
    show(f"#s3-sw{i}", t_st + 0.3 + i * 0.13)
    if i % 3 == 0:
        SFX.append((t_st + 0.3 + i * 0.13, "tick"))

# ---- 4. Phone: pause and try it; my real chain; tell me yours
typed = "I'm going to"
chain = "go get some lunch now so I'll call when I'm on the road I have a couple things I have".split()
alts = [("be", "do"), ("to", "a"), ("the", "some"), ("food", "sleep"), ("and", "for"), ("and", "but"), ("I", "we"), ("be", "just"),
        ("you", "if"), ("I", "you"), ("am", "get"), ("my", "the"), ("way", "phone"), ("so", "and"), ("a", "to"), ("lot", "few"),
        ("of", "more"), ("to", "that"), ("to", "a"), ("to", "left")]
ch4 = chars("s4-c", typed)
spans = "".join(f'<span class="tw" id="s4-t{i}"> {w}</span>' for i, w in enumerate(chain))
sets = '<div class="sset" id="s4-set0"><span>I</span><span class="mid">go</span><span>be</span></div>'
for i in range(len(chain)):
    nxt = chain[i + 1] if i + 1 < len(chain) else "a"
    a, b = alts[i % len(alts)]
    sets += f'<div class="sset" id="s4-set{i+1}"><span>{a}</span><span class="mid">{nxt}</span><span>{b}</span></div>'
kb = ""
for r, row in enumerate(["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]):
    keys = "".join(f'<b class="k" id="s4-k{c}">{c.lower()}</b>' for c in row)
    if r == 2:
        keys = '<b class="k fn">&#8679;</b>' + keys + '<b class="k fn">&#9003;</b>'
    kb += f'<div class="krow">{keys}</div>'
kb += '<div class="krow"><b class="k fn w2">123</b><b class="k space" id="s4-kspace">space</b><b class="k fn w2">return</b></div>'
scene(4, f"""
  <div class="rig" id="s4-rig">
    <div class="ig-phone p4" id="s4-phone"><div class="screen">
      <div class="notch"></div>
      <div class="head"><div class="avatar">S</div><div><div class="name">Sam</div><div class="status">online</div></div></div>
      <div class="thread"><div class="ig-bubble ig-bubble--me in">what time you coming?</div></div>
      <div class="compose"><span class="ctext">{ch4}{spans}</span><span class="caret2">|</span></div>
      <div class="suggbar">{sets}<div class="tap" id="s4-tap"></div></div>
      <div class="kb">{kb}</div>
    </div></div>
  </div>
  <div class="s4-label" id="s4-lab"><span class="ig-kicker ig-kicker--cyan"><span class="ig-kicker-dot"></span>Pause and try it</span>
    <p class="ig-body-lg">Type <b class="ig-em-c">"I'm going to"</b><br/>tap the <b class="ig-em-o">middle</b> word.<br/>Again. And again.</p>
    <svg class="ring4" viewBox="0 0 140 140"><circle cx="70" cy="70" r="60" class="rb"/><circle cx="70" cy="70" r="60" class="rf" id="s4-ring"/></svg></div>
  <div class="real" id="s4-real"><span class="ig-kicker"><span class="ig-kicker-dot"></span>Mine, for real</span>
    <div class="shot"><img src="assets/phone-real.png" alt=""/></div></div>
  <div class="cmt" id="s4-cmt"><span class="bub">&#128172;</span><span class="ig-body">What did <b class="ig-em-c">yours</b> say?</span></div>""")
_tw("#s4-rig", {"opacity": 0, "y": 200}, {"opacity": 1, "y": 0}, at(4, 0.0), 0.7, "igOut")
sway("#s4-phone", at(4, 0.1), end_of(4))
rise("#s4-lab", cue(4, "Pause the video") - 0.1)
fade("#s4-set0", at(4, 0.3), 0.2)
tc = cue(4, "type") + 0.4
for i, c in enumerate(typed):
    t = round(tc + i * 0.1, 3)
    show(f"#s4-c{i}", t)
    SFX.append((t, "click"))
    kid = "#s4-kspace" if c == " " else (f"#s4-k{c.upper()}" if c.isalpha() else None)
    if kid:
        raw(f'tl.fromTo("{kid}",{{backgroundColor:"#ff7a1a",scale:1.25}},{{backgroundColor:"{KEYBG}",scale:1,duration:.25,ease:"power1.out",immediateRender:false}},{t});', t, 0.25)
t_mid = cue(4, "keep tapping")
_seen.add("#s4-tap")
_tw("#s4-tap", {"opacity": 0.9, "scale": 0.3}, {"opacity": 0, "scale": 1.6}, t_mid + 0.3, 0.5, "power2.out")
# the designed pause: ring counts down while you try it
t_pause = cue(4, "keep tapping") + 2.0
t_mine = cue(4, "Mine gave me")
raw(f'tl.fromTo("#s4-ring",{{strokeDashoffset:0,opacity:1}},{{strokeDashoffset:377,opacity:1,duration:{round(t_mine - t_pause, 2)},ease:"none"}},{t_pause});', t_pause, t_mine - t_pause)
pulse("#s4-lab .ig-kicker", t_pause + 0.4, 1.08)
pulse("#s4-lab .ig-kicker", t_pause + 1.4, 1.08)
out("#s4-lab", t_mine - 0.2, 0.25)
t0 = t_mine + 0.9
t_end = cue(4, "and it just kept going") - 0.2
step = (t_end - t0) / len(chain)
to("#s4-rig", {"scale": 1.18, "y": -150}, t0 - 0.9, 0.9)
for i in range(len(chain)):
    t = round(t0 + i * step, 3)
    show(f"#s4-t{i}", t)
    SFX.append((t - 0.03, "click"))
    _tw("#s4-tap", {"opacity": 0.9, "scale": 0.3}, {"opacity": 0, "scale": 1.6}, t - 0.05, round(step * 0.9, 3), "power2.out")
    _tw(f"#s4-set{i}", {"opacity": 1}, {"opacity": 0}, t, 0.05, "none")
    _tw(f"#s4-set{i+1}", {"opacity": 0}, {"opacity": 1}, t, 0.05, "none")
t_kg = cue(4, "and it just kept going")
to("#s4-rig", {"scale": 1, "y": 0, "x": -330}, t_kg, 0.6)
slide_in("#s4-real", t_kg + 0.2, 160)
settle("#s4-cmt", cue(4, "Tell me in the comments"), 0.5, True)
pulse("#s4-cmt", cue(4, "what yours said"), 1.06)

# ---- 5. Powers of ten: phone model -> giant model; lifetimes of reading; guesses get good
scene(5, """
  <div class="world" id="s5-world"><div class="grid dimg"></div><div class="grid lit" id="s5-lit"></div><div class="mytile" id="s5-me"></div><div class="mylab" id="s5-ml"><span class="ig-pill ig-pill--o">&larr; your phone's model</span></div></div>
  <div class="s5-a" id="s5-a"><span class="ig-kicker"><span class="ig-kicker-dot"></span>Your phone's keyboard model</span>
    <div class="big"><span class="ig-em-o">~34 million</span> settings</div><div class="ig-label-sm ig-dim">Reverse-engineered, 2023</div></div>
  <div class="s5-b" id="s5-b"><span class="ig-kicker ig-kicker--cyan"><span class="ig-kicker-dot"></span>The models behind ChatGPT</span>
    <div class="big">Likely <span class="ig-em-c">thousands of times</span> bigger</div><div class="ig-label-sm ig-dim">Exact size isn't published</div></div>
  <div class="s5-c" id="s5-c"><div class="books">""" + "".join(f'<i class="bk" id="s5-bk{i}"></i>' for i in range(12)) + """</div>
    <p class="ig-body-lg">More reading than <span class="ig-em-o">thousands of lifetimes</span></p></div>
  <div class="s5-d" id="s5-d"><div class="sent ig-hsm">Happy birth<span class="ig-em-c" id="s5-day">day</span></div>
    <div class="pr-panel lock stat" id="s5-pp"><div class="pr-row win"><span class="w">day</span><span class="bar"><i id="s5-pb1" style="width:99%"></i></span><span class="pct">99%</span></div>
      <div class="pr-row"><span class="w">days</span><span class="bar"><i id="s5-pb2" style="width:1%"></i></span><span class="pct">1%</span></div></div>
    <div class="ig-body-lg ig-muted" id="s5-feel">Good enough it stops <span class="ig-em-o">feeling</span> like guessing.</div></div>""", "plain")
raw('tl.set("#s5-world",{opacity:1,scale:28,transformOrigin:"1005px 555px"},0);')
fade("#s5-me", at(5, 0.0), 0.3)
rise("#s5-a", cue(5, "When someone cracked") + 0.2)
pulse("#s5-a .big", cue(5, "thirty-four million"), 1.06)
t_z = cue(5, "The ones behind ChatGPT")
lift_out("#s5-a", t_z - 0.3)
SFX.append((t_z, "whoosh"))
raw(f'tl.to("#s5-world",{{scale:1,duration:2.6,ease:"igIO"}},{t_z});', t_z, 2.6)
raw(f'tl.fromTo("#s5-lit",{{opacity:0}},{{opacity:.55,duration:2,ease:"none"}},{t_z + 0.6});', t_z + 0.6, 2)
settle("#s5-ml", t_z + 2.4, 0.45, True)
lift_out("#s5-ml", cue(5, "they learned from") - 0.3)
rise("#s5-b", t_z + 1.6)
t_l = cue(5, "they learned from")
lift_out("#s5-b", t_l - 0.1)
dim("#s5-world", t_l, 0.18, 0.5)
fade("#s5-c", t_l, 0.1)
for i in range(12):
    _tw(f"#s5-bk{i}", {"opacity": 0, "y": -50}, {"opacity": 1, "y": 0}, t_l + 0.15 + i * 0.09, 0.35, "igOut")
rise("#s5-c p", cue(5, "thousands of lifetimes"))
t_g = cue(5, "So the guesses")
lift_out("#s5-c", t_g - 0.3)
fade("#s5-d", t_g, 0.1)
rise("#s5-d .sent", t_g + 0.05)
settle("#s5-pp", t_g + 0.3)
grow("#s5-pb1", t_g + 0.5, 0.8)
grow("#s5-pb2", t_g + 0.5, 0.8)
SFX.append((t_g + 1.1, "tick"))
t_ge = cue(5, "Good enough")
out("#s5-pp", t_ge + 0.2, 0.4)
rise("#s5-feel", t_ge + 0.3)
raw('tl.set("#s5-day",{opacity:1},0);')
pulse("#s5-d .sent", t_ge + 1.2, 1.05)

# ---- 6. Real work: grammar -> code -> Math Olympiad; "just autocomplete?" "At the basic level, yes."
just = "Just autocomplete?"
scene(6, f"""
  <div class="s6-head" id="s6-head"><h1 class="ig-h">If it's only <span class="ig-em-o">guessing</span>&hellip;<br/>how does it do <span class="ig-em-c">real work?</span></h1></div>
  <div class="morph" id="s6-card">
    <div class="mc" id="s6-m1"><span class="ig-pill">Fix my grammar</span>
      <div class="msg"><span class="wr" id="s6-w1"><s>their</s><b>they're</b></span> gonna be late, <span class="wr" id="s6-w2"><s>dont</s><b>don't</b></span> wait</div></div>
    <div class="mc" id="s6-m2"><span class="ig-pill">Find the bug</span>
      <div class="code"><div>prices = [4, 9, 12<b class="fix" id="s6-br">]</b><i class="miss" id="s6-mb">&#9646;</i></div><div>total = 0</div><div><i class="kw">for</i> p <i class="kw">in</i> prices:</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;<span class="wr" id="s6-v"><s>totl</s><b>total</b></span> += p</div></div></div>
  </div>
  <div class="imo" id="s6-imo">
    <svg class="medal" viewBox="0 0 300 420" id="s6-medal"><path d="M90 0 L150 150 L210 0" class="rib"/><circle cx="150" cy="270" r="118" class="gold"/><circle cx="150" cy="270" r="86" class="gold2"/><path d="M150 214 l18 38 42 5 -31 29 8 42 -37 -21 -37 21 8 -42 -31 -29 42 -5z" class="star"/></svg>
    <div class="imo-r"><span class="ig-kicker"><span class="ig-kicker-dot"></span>International Math Olympiad &middot; 2025</span>
      <div class="scoreline"><div class="track"><i class="gold-line"></i><span class="gl">gold line</span><b class="mk" id="s6-mk"></b></div><div class="score"><span class="ig-em-c">35</span> / 42</div></div>
      <div class="chips6"><span class="ig-pill" id="s6-c1">Same next-word engine + training to reason</span><span class="ig-pill" id="s6-c2">Same time limits as the kids</span>
        <span class="ig-pill" id="s6-c3">Full proofs, plain English</span><span class="ig-pill ig-pill--o" id="s6-c4">&#10003; Confirmed by the Olympiad's graders</span>
        <span class="ig-label-sm ig-dim" id="s6-c5">26 students still scored higher</span></div></div>
  </div>
  <div class="did" id="s6-did"><h1 class="ig-hxl"><span class="ig-em-c">Autocomplete</span> did that.</h1></div>
  <div class="just" id="s6-just"><div class="jq"><span class="ig-h">{chars("s6-j", just)}</span><span class="ig-h caret3" id="s6-caret">|</span></div>
    <div class="yes" id="s6-yes"><span class="ig-body-lg">At the basic level?</span> <span class="ig-h ig-em-c">Yes.</span></div>
    <div class="kind" id="s6-kind"><span class="ig-h">Just not the <span class="ig-em-o">kind you think.</span></span></div></div>""")
rise("#s6-head", at(6, 0.1), 40)
pulse("#s6-head .ig-em-o", cue(6, "If it's only guessing") + 0.5, 1.1)
pulse("#s6-head .ig-em-c", cue(6, "how does it do real work") + 0.8, 1.1)
t_sm = cue(6, "For me it started small")
to("#s6-head", {"y": -250, "scale": 0.62}, t_sm - 0.2, 0.6)
_tw("#s6-card", {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0}, t_sm, 0.5, "igOut")
raw('tl.set("#s6-card",{opacity:1},0);')
fade("#s6-m1", t_sm, 0.2)
t_gr = cue(6, "clean up the grammar")
for i, w in enumerate(["#s6-w1", "#s6-w2"]):
    cls(w, "wr bad", t_gr + i * 0.3)
    cls(w, "wr bad fixed", t_gr + 1.0 + i * 0.3)
    SFX.append((t_gr + 1.0 + i * 0.3, "tick"))
t_code = cue(6, "Then I started pasting")
out("#s6-m1", t_code - 0.1, 0.15)
fade("#s6-m2", t_code, 0.2)
t_var = cue(6, "spot the wrong variable")
cls("#s6-v", "wr bad", t_var + 0.1)
cls("#s6-v", "wr bad fixed", t_var + 1.0)
SFX.append((t_var + 1.0, "tick"))
t_ds = cue(6, "the broken data structure")
pop("#s6-mb", t_ds + 0.1, 0.3, 0.5, False)
out("#s6-mb", t_ds + 0.9, 0.1)
land("#s6-br", t_ds + 0.9)
t_big = cue(6, "Then it got big")
to("#s6-card", {"y": -80, "opacity": 0}, t_big - 0.2, 0.4, "igIn")
out("#s6-head", t_big - 0.2, 0.3)
fade("#s6-imo", t_big, 0.1)
raw('tl.set("#s6-imo",{opacity:1},0);')
_tw("#s6-medal", {"opacity": 0, "scale": 0.6, "rotation": -20}, {"opacity": 1, "scale": 1, "rotation": 0}, t_big + 0.1, 0.8, "igOut")
rise("#s6-imo .ig-kicker", cue(6, "In twenty twenty-five"))
settle("#s6-c1", cue(6, "plus a lot of extra"))
raw(f'tl.fromTo("#s6-medal",{{rotation:0}},{{keyframes:[{{rotation:-8,duration:.4}},{{rotation:4,duration:.4}},{{rotation:0,duration:.4}}],ease:"sine.inOut",immediateRender:false}},{cue(6, "In twenty twenty-five") + 2.2});', cue(6, "In twenty twenty-five") + 2.2, 1.2)
pulse("#s6-medal", cue(6, "Google's wrote") - 1.4, 1.06)
pulse("#s6-imo .score", cue(6, "Google's wrote"), 1.08)
rise("#s6-imo .scoreline", cue(6, "sat the International"))
settle("#s6-c2", cue(6, "under the same time"))
settle("#s6-c3", cue(6, "wrote full proofs"))
t_gl = cue(6, "scored right at")
_tw("#s6-mk", {"x": -620}, {"x": 0}, t_gl, 1.2, "igOut")
SFX.append((t_gl + 1.1, "ding"))
settle("#s6-c4", cue(6, "confirmed by"), 0.5, True)
settle("#s6-c5", cue(6, "Plenty of kids"))
t_did = cue(6, "Autocomplete did that")
dim("#s6-imo", t_did - 0.3, 0.12, 0.4)
_tw("#s6-did", {"opacity": 0, "scale": 1.3}, {"opacity": 1, "scale": 1}, t_did, 0.45, "igSettle")
SFX.append((t_did + 0.1, "thud"))
t_j = cue(6, "So is it just autocomplete")
lift_out("#s6-did", t_j - 0.3)
out("#s6-imo", t_j - 0.3, 0.3)
raw('tl.set("#s6-just",{opacity:1},0);')
raw('tl.set("#s6-caret",{opacity:0},0);')
fade("#s6-caret", t_j - 0.2, 0.1)
typeon("s6-j", len(just), t_j + 0.1, 16)
blink("#s6-caret", t_j + 1.3, end_of(6))
rise("#s6-yes", cue(6, "At the basic level"))
pulse("#s6-yes .ig-h", cue(6, "yes") + 0.1, 1.15)
rise("#s6-kind", cue(6, "It's just not the kind"))

# ---- 7. Jay: beat the bars; clues; code is the same game
scene(7, """
  <div class="gchat" id="s7-chat"><div class="gc-head"><span class="gc-ico">&#127968;</span><span>Roommates</span></div>
    <div class="gm" id="s7-m1"><b>Alex</b>Someone ate my leftovers &#128548;</div>
    <div class="gm" id="s7-m2"><b>Alex</b><span id="s7-h1">Jay was the only one home</span></div>
    <div class="gm" id="s7-m3"><b>Alex</b>and <span id="s7-h2">Jay swears he hates pasta</span></div>
    <div class="gm me" id="s7-m4">So it was<span class="dots">&hellip;</span> <span class="ans ig-em-c" id="s7-ans">Jay.</span></div></div>
  <div class="guess7" id="s7-g"><span class="ig-kicker ig-kicker--cyan" id="s7-gk"><span class="ig-kicker-dot"></span>Your guess?</span>
    <div class="pr-panel" id="s7-pp"><div class="pr-row win"><span class="w">Jay</span><span class="bar"><i id="s7-b1" style="width:91%"></i></span></div>
      <div class="pr-row"><span class="w">the cat</span><span class="bar"><i id="s7-b2" style="width:6%"></i></span></div>
      <div class="pr-row"><span class="w">a ghost</span><span class="bar"><i id="s7-b3" style="width:3%"></i></span></div></div>
    <svg class="ring7" viewBox="0 0 140 140"><circle cx="70" cy="70" r="60" class="rb"/><circle cx="70" cy="70" r="60" class="rf" id="s7-ring"/></svg></div>
  <div class="clue" id="s7-cl1"><span class="ig-pill">Clue: only one home</span></div>
  <div class="clue" id="s7-cl2"><span class="ig-pill ig-pill--o">Lie: "hates pasta"</span></div>
  <div class="rules" id="s7-rules"><div class="ig-label">Detective rules</div><i></i><i></i><i></i><svg viewBox="0 0 400 240"><path id="s7-rx" d="M20 220 L380 20"/></svg></div>
  <div class="code7" id="s7-code"><span class="ig-kicker"><span class="ig-kicker-dot"></span>Code is the same game</span>
    <div class="code"><div id="s7-l1">home&nbsp;&nbsp;&nbsp;= ["Jay"]<span class="val" id="s7-v1">1 person</span></div>
      <div id="s7-l2">claims&nbsp;= "hates pasta"<span class="val o" id="s7-v2">suspicious</span></div>
      <div id="s7-l3">eaten&nbsp;&nbsp;= "pasta"<span class="val" id="s7-v3">leftovers</span></div>
      <div class="hl" id="s7-l4">culprit = home[0]<span class="val" id="s7-v4">"Jay"</span></div></div></div>""")
_tw("#s7-chat", {"opacity": 0, "x": -120}, {"opacity": 1, "x": 0}, at(7, 0.0), 0.5, "igOut")
sway("#s7-chat", at(7, 0.2), end_of(7))
for i, ph in enumerate(["Someone ate", "Jay was the only", "and Jay swears", "So it was"]):
    settle(f"#s7-m{i+1}", cue(7, ph) - 0.05, 0.4, True)
t_sw = cue(7, "So it was")
slide_in("#s7-g", t_sw - 0.2, 140)
raw('tl.set("#s7-pp",{opacity:1},0);')
raw('tl.set("#s7-ring",{opacity:1,strokeDashoffset:0},0);')
t_jay = cue(7, "It was Jay")
raw(f'tl.fromTo("#s7-ring",{{strokeDashoffset:0,opacity:1}},{{strokeDashoffset:377,opacity:1,duration:{round(t_jay - t_sw - 0.9, 2)},ease:"none"}},{t_sw + 0.9});', t_sw + 0.9, t_jay - t_sw - 0.9)
pulse("#s7-gk", t_sw + 1.6, 1.1)
for i in range(3):
    grow(f"#s7-b{i+1}", t_jay - 0.1 + i * 0.05, 0.6)
cls("#s7-pp", "pr-panel lock", t_jay + 0.3)
out("#s7-ring", t_jay, 0.2)
land("#s7-ans", t_jay + 0.2)
pulse("#s7-ans", cue(7, "It's always Jay"), 1.2)
t_cl = cue(7, "follow the clues")
cls("#s7-h1", "hl-c", t_cl)
settle("#s7-cl1", t_cl + 0.1, 0.45, True)
t_lie = cue(7, "catch the lie")
cls("#s7-h2", "hl-o", t_lie)
settle("#s7-cl2", t_lie + 0.1, 0.45, True)
t_nr = cue(7, "Nobody wrote detective rules")
out("#s7-g", t_nr - 0.2, 0.3)
settle("#s7-rules", t_nr)
draw("#s7-rx", t_nr + 0.8, 420, 0.35)
SFX.append((t_nr + 0.8, "thud"))
pulse("#s7-chat", cue(7, "Getting really good"), 1.03)
t_cg = cue(7, "Code is the same game")
for s_ in ["#s7-rules", "#s7-cl1", "#s7-cl2"]:
    lift_out(s_, t_cg - 0.3)
to("#s7-chat", {"x": -40, "scale": 0.86, "opacity": 0.35}, t_cg - 0.3, 0.5)
slide_in("#s7-code", t_cg, 140)
for i in range(4):
    rise(f"#s7-l{i+1}", t_cg + 0.3 + i * 0.25, 20, 0.35)
t_var7 = cue(7, "keep track of what every")
for i in range(4):
    settle(f"#s7-v{i+1}", t_var7 + 0.2 + i * 0.35, 0.35, True)
cls("#s7-l4", "hl on", cue(7, "the way you kept track"))

# ---- 8. Illustration: it picks "rabbit" before writing the line; Hinton vs Bender; pick a side
line2 = "His hunger was like a starving "
scene(8, f"""
  <div class="art" id="s8-art"><img src="assets/plan.png" alt=""/>
    <div class="glowdot" id="s8-glow"></div>
    <svg class="ig-pointer" viewBox="0 0 1920 1080" style="left:0;top:0;width:1920px;height:1080px">
      <circle id="s8-d1" cx="1590" cy="250" r="12" class="c"/><path id="s8-l1" class="c" d="M1590 250 V420 H1450" style="stroke-dasharray:320"/></svg>
    <div class="ig-callout" style="left:1080px;top:392px"><span class="ig-pill" id="s8-p1">Picked first: rabbit</span></div>
  </div>
  <div class="ig-scene-scrim" id="s8-scrim"></div>
  <div class="ig-scene-head" id="s8-head" style="width:820px"><span class="ig-kicker"><span class="ig-kicker-dot"></span>Anthropic &middot; 2025</span>
    <h1 class="ig-hsm">Looking <span class="ig-em-c">inside</span> the model</h1></div>
  <div class="poem" id="s8-poem"><div class="pl" id="s8-pl1">He saw a carrot and had to grab it,</div>
    <div class="pl">{chars("s8-c", line2)}<b class="rab ig-em-c" id="s8-rab">rabbit</b></div></div>
  <div class="both" id="s8-both"><span class="ig-pill">One word at a time &#10003;</span><span class="ig-pill ig-pill--o">Planning ahead &#10003;</span></div>
  <div class="versus" id="s8-vs">
    <div class="qcard c" id="s8-q1"><div class="ig-label">Geoffrey Hinton</div><p class="ig-body">"To predict the next word, you have to understand the sentences."</p><div class="ig-label-sm ig-dim">60 Minutes, 2023</div></div>
    <div class="vsb" id="s8-vsb">VS</div>
    <div class="qcard o" id="s8-q2"><div class="ig-label">Emily Bender, linguist</div><p class="ig-body">Closer to a very fancy parrot: <span class="ig-em-o">"stochastic parrots"</span></p><div class="ig-label-sm ig-dim">Bender et al., 2021</div></div>
  </div>
  <div class="side" id="s8-side"><span class="bub">&#128172;</span><span class="ig-body-lg">Pick your side <span class="ig-em-c">in the comments</span></span></div>""", "plain")
t_dim8 = cue(8, "Geoffrey Hinton") - 0.4
_tw("#s8-art", {"scale": 1.0}, {"scale": 1.14}, at(8, 0.0), round(t_dim8 - at(8, 0.0) + 1, 2), "none")
raw(f'tl.fromTo("#s8-art",{{opacity:0}},{{opacity:1,duration:3,ease:"sine.inOut",immediateRender:false}},{at(8, 0.0)});', at(8, 0.0), 3)
raw('tl.set("#s8-scrim",{opacity:1},0);')
rise("#s8-head", at(8, 0.3))
t_poem = cue(8, "while it wrote a rhyming poem")
rise("#s8-poem", t_poem, 40)
raw('tl.set("#s8-pl1",{opacity:1},0);')
t_pick = cue(8, "it had already picked")
_tw("#s8-glow", {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1}, t_pick, 0.7, "igOut")
SFX.append((t_pick, "ding"))
pop("#s8-d1", t_pick + 0.5, sound=False)
draw("#s8-l1", t_pick + 0.6, 320)
settle("#s8-p1", t_pick + 1.0, 0.45, True)
t_rab = cue(8, "rabbit")
pulse("#s8-glow", t_rab, 1.3)
t_built = cue(8, "and built the line")
te = typeon("s8-c", len(line2), t_built + 0.1, 16)
land("#s8-rab", te + 0.05)
t_one = cue(8, "So it writes one piece")
lift_out("#s8-head", t_one - 0.2)
settle("#s8-both", t_one + 0.2)
pulse("#s8-both .ig-pill--o", cue(8, "it can be planning ahead"), 1.08)
raw(f'tl.to("#s8-art",{{opacity:.08,duration:.6,ease:"power1.out"}},{round(t_dim8, 3)});', t_dim8, 0.6)
for s_ in ["#s8-poem", "#s8-both", "#s8-d1", "#s8-l1", "#s8-p1", "#s8-glow"]:
    out(s_, t_dim8, 0.3)
raw('tl.set("#s8-vs",{opacity:1},0);')
slide_in("#s8-q1", cue(8, "Geoffrey Hinton"), -140)
pulse("#s8-q1 .ig-label", cue(8, "Geoffrey Hinton") + 2.6, 1.1)
pulse("#s8-q1 p", cue(8, "to predict the next word") + 2.3, 1.04)
pulse("#s8-q2 .ig-label", cue(8, "Others, like the linguist") + 2.4, 1.1)
pulse("#s8-q1", cue(8, "to predict the next word"), 1.03)
slide_in("#s8-q2", cue(8, "Others, like the linguist"), 140)
pulse("#s8-q2", cue(8, "very fancy parrot"), 1.03)
pop("#s8-vsb", cue(8, "Smart people are still fighting"), 0.5, 0.3)
settle("#s8-side", cue(8, "pick your side"), 0.5, True)

# ---- 9. Raw model rambles like a forum post; trained again on rated answers; assistant
ramble = "...asking for my picky five-year-old. Edit: thanks everyone!".split()
ramble_html = "".join(f'<span class="sw" id="s9-r{i}">{w} </span>' for i, w in enumerate(ramble))
pre = "i've tried pasta and tacos but she won't eat anything green lol".split()
pre_html = "".join(f'<span class="sw" id="s9-p{i}">{w} </span>' for i, w in enumerate(pre))
scene(9, f"""
  <div class="col9 l" id="s9-raw"><span class="ig-kicker"><span class="ig-kicker-dot"></span>Straight out of training</span>
    <div class="forum" id="s9-forum"><div class="votes">&#9650;<b>12</b>&#9660;</div><div class="fp">
      <div class="fu">u/dinnerq &middot; 3h</div><div class="ft">what's a good dinner tonight?</div>
      <div class="fb">{pre_html}{ramble_html}</div></div></div></div>
  <div class="mid9" id="s9-mid"><svg class="ig-arrow" viewBox="0 0 240 120"><path id="s9-arr" d="M20 60 H214 M172 20 L216 60 L172 100" style="stroke-dasharray:340"/></svg>
    <div class="ig-label-sm ig-em-c" id="s9-al">trained again</div>
    <div class="rated" id="s9-rated"><div class="rc" id="s9-rc0"><i></i><i class="s"></i><b>&#9733;&#9733;&#9733;&#9733;&#9733;</b></div>
      <div class="rc" id="s9-rc1"><i></i><i class="s"></i><b>&#9733;&#9733;&#9733;&#9733;&#9734;</b></div>
      <div class="rc" id="s9-rc2"><i></i><i class="s"></i><b>&#128077;</b></div>
      <div class="ig-label-sm ig-dim" id="s9-rl">written &amp; rated by people</div></div></div>
  <div class="col9 r" id="s9-asst"><span class="ig-kicker ig-kicker--cyan"><span class="ig-kicker-dot"></span>Assistant</span>
    <div class="chatwin c9"><div class="ig-bubble ig-bubble--me cw-q">what's a good dinner tonight?</div>
      <div class="ig-bubble ig-bubble--ai cw-a">Try a 20-minute stir-fry: chicken, rice, and whatever veg you've got.</div></div></div>""")
rise("#s9-raw", at(9, 0.1), 50)
pulse("#s9-raw .ig-kicker", cue(9, "Straight out"), 1.1)
pulse("#s9-forum .ft", cue(9, "Ask") + 0.3, 1.06)
raw(f'tl.set("#s9-forum .votes b",{{innerHTML:"47"}},{cue(9, "Ask") + 2.6});', cue(9, "Ask") + 2.6, 0.1)
pulse("#s9-forum .votes", cue(9, "Ask") + 2.6, 1.2)
raw('tl.set("#s9-forum",{opacity:1},0);')
t_kw = cue(9, "It just keeps writing")
for i in range(len(pre)):
    show(f"#s9-p{i}", t_kw + 0.1 + i * 0.3)
t_q9 = cue(9, "...asking for my")
for i in range(len(ramble)):
    show(f"#s9-r{i}", t_q9 + i * 0.3)
pulse("#s9-forum", cue(9, "Edit: thanks") + 0.3, 1.03)
t_tr = cue(9, "So the companies train")
dim("#s9-raw", t_tr, 0.45)
raw('tl.set("#s9-mid",{opacity:1},0);')
draw("#s9-arr", t_tr + 0.1, 340, 0.6)
fade("#s9-al", t_tr + 0.4, 0.3)
raw('tl.set("#s9-rated",{opacity:1},0);')
t_rt = cue(9, "on good answers")
for i in range(3):
    settle(f"#s9-rc{i}", t_rt + i * 0.2, 0.4, True)
fade("#s9-rl", cue(9, "wrote and rated"), 0.3)
t_as = cue(9, "until it acts like an assistant")
slide_in("#s9-asst", t_as, 160)
t_cs = cue(9, "instead of a comment section")
raw(f'tl.to("#s9-raw",{{opacity:.18,filter:"grayscale(1)",duration:.5}},{t_cs});', t_cs, 0.5)
pulse("#s9-asst .chatwin", t_cs + 0.3, 1.03)

# ---- 10. The catch (Tidewater Dreams), recap, next video, end card
scene(10, """
  <div class="ig-safe ig-center s10v" id="s10-v"><div class="ig-venn">
    <div class="circle a" id="s10-c1"><span class="ig-label">Sounds right</span></div>
    <div class="circle b" id="s10-c2"><span class="ig-label">Is right</span></div>
    <div class="overlap" id="s10-ov"><span class="ig-label-sm" style="color:var(--ink)">most of the time</span></div></div></div>
  <div class="paper" id="s10-paper"><div class="pp-mast">Summer Reading List</div><div class="pp-sub">2025 &middot; 15 books for the beach</div>
    <div class="pp-row"><i></i><i class="s"></i></div><div class="pp-row hi" id="s10-hi"><span>Tidewater Dreams</span> &mdash; Isabel Allende</div><div class="pp-row"><i></i><i class="s"></i></div><div class="pp-row"><i class="s"></i><i></i></div></div>
  <div class="book" id="s10-book"><div class="bk-waves"></div><div class="bk-t">Tidewater<br/>Dreams</div><div class="bk-a">ISABEL ALLENDE</div></div>
  <span class="ig-pill chk" id="s10-sr">Sounds right &#10003;</span>
  <div class="ig-stamp s10-stamp" id="s10-stamp">DOESN'T EXIST</div>
  <div class="recap" id="s10-recap"><div class="ig-label ig-dim" id="s10-rl">The whole video in one line</div>
    <h1 class="ig-h" id="s10-r1">It doesn't <span class="ig-em-o">look things up.</span></h1>
    <h1 class="ig-h" id="s10-r2">It guesses the next word, <span class="ig-em-c">really, really well.</span></h1></div>
  <div class="ig-safe ig-center" id="s10-next">
    <span class="ig-kicker ig-kicker--cyan" id="s10-k"><span class="ig-kicker-dot"></span>Next video</span>
    <h1 class="ig-h" id="s10-t" style="margin-top:44px">Why it makes things up<br/>with a <span class="ig-em-o">straight face</span></h1>
    <p class="ig-body-lg ig-muted" id="s10-tease" style="margin-top:36px">It once invented six court cases. A lawyer filed them.</p></div>
  <div class="s10-end" id="s10-end">
    <h1 class="ig-signoff" id="s10-sign">I gotchu<b>.</b></h1>
    <div class="ig-slot" id="s10-sl1" style="left:176px;top:470px;width:600px;height:338px"><span class="ig-label-sm" style="color:var(--cyan)">Next video</span></div>
    <div class="ig-slot ig-slot--round" id="s10-sl2" style="left:810px;top:490px;width:300px;height:300px"><span class="ig-label-sm" style="color:var(--orange)">Subscribe</span></div>
    <div class="ig-slot" id="s10-sl3" style="left:1144px;top:470px;width:600px;height:338px"><span class="ig-label-sm" style="color:var(--cyan)">Best for you</span></div>
  </div>""")
raw('tl.set("#s10-v",{opacity:1},0);')
slide_in("#s10-c1", at(10, 0.0), -160)
slide_in("#s10-c2", at(10, 0.2), 160)
pop("#s10-ov", cue(10, "most of the time"))
pulse("#s10-c1", cue(10, "It's predicting what"), 1.04)
pulse("#s10-c2", cue(10, "It's predicting what") + 2.2, 1.04)
t_nw = cue(10, "But in twenty twenty-five")
out("#s10-v", t_nw - 0.2, 0.3)
_tw("#s10-paper", {"opacity": 0, "y": 80, "rotation": -4}, {"opacity": 1, "y": 0, "rotation": -2}, t_nw, 0.6, "igOut")
t_td = cue(10, "a novel called Tidewater")
cls("#s10-hi", "pp-row hi on", t_td + 0.2)
for i_, sel_ in enumerate(["#s10-paper .pp-mast", "#s10-paper .pp-sub"]):
    pulse(sel_, t_nw + 1.6 + i_ * 1.4, 1.04)
SFX.append((t_td + 0.2, "tick"))
_tw("#s10-book", {"opacity": 0, "x": 200, "rotation": 8}, {"opacity": 1, "x": 0, "rotation": 3}, cue(10, "by Isabel Allende"), 0.6, "igOut")
settle("#s10-sr", cue(10, "It sounds exactly"), 0.45, True)
slam("#s10-stamp", cue(10, "It doesn't exist"))
t_rc = cue(10, "So here's the whole video")
for s_ in ["#s10-paper", "#s10-book", "#s10-sr", "#s10-stamp"]:
    lift_out(s_, t_rc - 0.3)
raw('tl.set("#s10-recap",{opacity:1},0);')
rise("#s10-rl", t_rc)
rise("#s10-r1", cue(10, "It doesn't look things up"), 40)
rise("#s10-r2", cue(10, "It guesses the next word"), 40)
pulse("#s10-r2 .ig-em-c", cue(10, "really, really well") + 0.3, 1.06)
t_nx = cue(10, "Next video")
lift_out("#s10-recap", t_nx - 0.3)
raw('tl.set("#s10-next",{opacity:1},0);')
pop("#s10-k", t_nx)
rise("#s10-t", t_nx + 0.2, 50)
rise("#s10-tease", cue(10, "and the lawyers"))
pulse("#s10-t .ig-em-o", cue(10, "and the lawyers") + 2.4, 1.08)
t_gt = cue(10, "I gotchu")
lift_out("#s10-next", t_gt - 0.35)
fade("#s10-end", t_gt - 0.3, 0.1)
ignite("#s10-sign", t_gt - 0.3)
for i in range(3):
    settle(f"#s10-sl{i+1}", t_gt + 0.9 + i * 0.15)

# ---- progress line + chapter name (shows for 2.5 s when the chapter changes)
chapters = [("The trick", 1), ("Your phone", 4), ("Real work", 6), ("Inside the model", 8), ("The catch", 10)]
chap_html = "".join(f'<span class="chap" id="ch{i}">{name}</span>' for i, (name, _) in enumerate(chapters))
for i, (_, n) in enumerate(chapters):
    t0c = T[n]["start"] + (0.6 if n > 1 else 1.0)
    _tw(f"#ch{i}", {"opacity": 0, "x": -20}, {"opacity": 1, "x": 0}, t0c, 0.4, "igOut")
    raw(f'tl.to("#ch{i}",{{opacity:0,duration:.4}},{round(t0c + 2.5, 3)});')
raw(f'tl.fromTo("#pfill",{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:"none"}},0);')
raw(f'tl.to("#rail",{{opacity:0,duration:.3}},{round(t_gt - 0.4, 3)});')


# ================================================================ FROZEN-FRAME CHECK
def frozen_report(limit=3.2):
    spans = sorted((max(0, a), b) for a, b in MOTION)
    gaps, cur = [], 0.0
    for a, b in spans:
        if a - cur > limit:
            gaps.append((round(cur, 2), round(a, 2)))
        cur = max(cur, b)
    if TOTAL - 6 - cur > limit:
        gaps.append((round(cur, 2), round(TOTAL - 6, 2)))
    return gaps


# ================================================================ STYLES
def tokens_css():
    tk = json.load(open("ds/tokens.json"))
    out_ = [":root{"]
    for fam in ["color", "spacing", "radius", "shadow", "duration", "easing"]:
        for t_ in tk.get(fam, {}).get("tokens", []):
            v = t_["value"]
            if isinstance(v, dict):
                v = list(v.values())[0]
            out_.append(f"--{t_['name']}:{v};")
    out_.append("}")
    return "".join(out_)


def bundle_css():
    css = open("ds/bundle.css").read()
    css = re.sub(r"@import url\([^)]*\);", "", css)
    css = css.split("/* =====================================================================\n   Motion.")[0]
    css = css.replace("animation: ig-blink 1s steps(1) infinite, ig-out .01s linear 2.2s both;", "display:none;")
    css = css.replace("animation: ig-dot 1s var(--ig-ease-io) infinite;", "")
    return css


FONTS = (
    "".join(f'@font-face{{font-family:Inter;font-weight:{w};src:url(assets/fonts/inter-latin-{w}-normal.woff2) format("woff2")}}' for w in (500, 600, 700, 800))
    + '@font-face{font-family:"Bricolage Grotesque";font-weight:200 800;font-stretch:75% 100%;src:url(assets/fonts/bricolage-grotesque-latin-wdth-normal.woff2) format("woff2")}'
    + "".join(f'@font-face{{font-family:"DM Sans";font-weight:{w};src:url(assets/fonts/dm-sans-latin-{w}-normal.woff2) format("woff2")}}' for w in (500, 600, 700))
    + '@font-face{font-family:"Noto Color Emoji";src:local("Noto Color Emoji")}'
    + "".join(f'@font-face{{font-family:"JetBrains Mono";font-weight:{w};src:url(assets/fonts/jetbrains-mono-latin-{w}-normal.woff2) format("woff2")}}' for w in (500, 700)))

LOCAL = """
:root{--font-display:"Bricolage Grotesque","Arial Narrow",sans-serif;--font-sans:"DM Sans",Inter,Arial,sans-serif;--font-mono:"JetBrains Mono",ui-monospace,monospace;--ink-dim:#8b97c0;--ig-display:var(--font-display)}
.ig-frame{font-family:var(--font-sans)}
.ig-frame::before{opacity:.45}
.ig-hxl,.ig-h,.ig-hsm,.ig-signoff,.ig-stamp,.big,.sent,.score,.rab,.vsb{font-family:var(--font-display);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75}
.ig-hxl{font-size:150px;line-height:.92;letter-spacing:-.02em}.ig-h{font-size:120px;line-height:.95;letter-spacing:-.01em}.ig-hsm{font-size:96px;line-height:.95}
.ig-h,.ig-hxl{text-wrap:balance}
.ig-label,.ig-label-sm,.ig-pill,.ig-kicker,.chap,.pr-row .pct,.cw-head,.s3-count,.code,.editor,.tok{font-family:var(--font-mono);font-weight:700}
.ig-body-lg,.ig-body,.ig-bubble,.w{font-family:var(--font-sans)}
#root{position:relative}
.clip{position:absolute;inset:0}
.scene{overflow:hidden}
.tr{position:absolute;inset:0}
.cam{position:absolute;inset:0;transform-origin:50% 45%}
.scene.plain{background:var(--night)}
.scene [id]{opacity:0}
.ch,.rw,.sw,.tw{display:none}
.scene .ch,.scene .rw,.scene .sw,.scene .tw,#s4 .k,#s4-phone,.pr-dock,.reply,#s6-m1 [id],#s6-m2 [id],#s7-h1,#s7-h2,#s5-day{opacity:1}
.bar i[id],#s2-x1,.mk,#s10-hi,#s3-ans{opacity:1}
.caret,.caret2,.caret3{color:var(--cyan);font-weight:400}
/* prediction panel */
.chatwin{position:absolute;right:128px;top:150px;width:760px;padding:40px;border-radius:var(--radius-md);background:var(--surface);
  box-shadow:inset 0 0 0 2px var(--line),var(--lift);display:flex;flex-direction:column;gap:28px}
.chatwin.wide{position:relative;right:auto;top:auto;width:1240px}
.chatwin .ig-bubble{max-width:none;font-size:42px}
.cw-q{align-self:flex-end}.cw-a{align-self:flex-start;min-height:56px}
.pr-dock{position:relative;height:230px}
.pr-panel{position:absolute;left:0;right:0;top:0;display:flex;flex-direction:column;gap:14px;padding:22px 26px;border-radius:var(--radius-md);
  background:var(--night);box-shadow:inset 0 0 0 2px var(--line)}
.pr-row{display:grid;grid-template-columns:280px 1fr 110px;align-items:center;gap:22px;font-size:38px;font-weight:700;color:var(--ink-muted)}
.pr-row .bar{height:18px;border-radius:9px;background:var(--surface-raised);overflow:hidden}
.pr-row .bar i{display:block;height:100%;border-radius:9px;background:var(--ink-dim);transform-origin:left}
.pr-row .pct{font-size:30px;color:var(--ink-dim);text-align:right}
.pr-panel.lock .pr-row.win{color:var(--cyan);text-shadow:var(--glow-text-cyan)}
.pr-panel.lock .pr-row.win .bar i{background:var(--cyan);box-shadow:0 0 12px var(--cyan)}
.pr-panel.lock .pr-row.win .pct{color:var(--cyan)}
/* 1-2 lock screen */
.rig1{position:absolute;left:180px;top:40px;width:560px;height:1000px}
.rig1.still,#s2-rig{opacity:1}
.ig-phone.p1{position:absolute;left:0;top:0;width:560px;height:1000px}
.lockscreen{background:radial-gradient(ellipse 90% 60% at 50% 20%,#1d2d6b,#0b1433 70%) !important}
.lock{text-align:center;padding-top:120px;color:#f4f7ff}
.lk-time{font-family:var(--font-display);font-weight:600;font-stretch:90%;font-size:150px;line-height:1}
.lk-date{font-size:30px;font-weight:600;color:#c3cdf0;margin-top:10px}
.notif{position:absolute;left:22px;right:22px;top:420px;padding:22px 26px;border-radius:30px;background:rgba(244,247,255,.14);backdrop-filter:blur(10px);box-shadow:inset 0 0 0 2px rgba(255,255,255,.12);color:#f4f7ff}
.notif.on{opacity:1 !important}
.nf-app{display:flex;align-items:center;gap:12px;font-size:22px;font-weight:700;letter-spacing:.06em;color:#c3cdf0}.nf-ico{font-style:normal;width:36px;height:36px;border-radius:9px;background:#34c759;color:#fff;display:grid;place-items:center;font-size:20px}
.nf-now{margin-left:auto;letter-spacing:0;font-weight:600}
.nf-from{font-size:34px;font-weight:800;margin-top:10px}.nf-body{font-size:34px;font-weight:500;margin-top:4px}
.dot{display:inline-block;opacity:1 !important;font-weight:800}
.party{display:inline-block;margin-left:8px;font-family:"Noto Color Emoji";font-size:40px}
.ghosts{position:absolute;left:40px;right:40px;top:640px;display:flex;flex-direction:column;gap:14px}
.gh{padding:16px 22px;border-radius:24px;background:rgba(244,247,255,.07);color:#8b97c0;font-size:28px;font-weight:600}
.nope{position:absolute;left:220px;top:300px}
.brain{position:absolute;left:880px;top:220px;width:900px;display:flex;flex-direction:column;align-items:flex-start;gap:34px}
.gpanel{width:100%;display:flex;flex-direction:column;gap:22px;padding:34px 36px;border-radius:var(--radius-md);background:var(--surface);box-shadow:inset 0 0 0 2px var(--line),var(--lift)}
.grow-r{display:grid;grid-template-columns:420px 1fr;align-items:center;gap:26px;font-size:44px;font-weight:700;color:var(--ink)}
.grow-r .bar{height:22px;border-radius:11px;background:var(--surface-raised);overflow:hidden}
.grow-r .bar i{display:block;height:100%;border-radius:11px;background:var(--ink-dim);transform-origin:left}
.grow-r.dead{color:var(--ink-dim)}.grow-r.dead s{text-decoration-color:var(--orange);text-decoration-thickness:5px}
.grow-r s{text-decoration:none}.grow-r.dead s{text-decoration:line-through;text-decoration-color:var(--orange);text-decoration-thickness:5px}
.grow-r.win{color:var(--cyan);text-shadow:var(--glow-text-cyan)}.grow-r.win .bar i{background:var(--cyan);box-shadow:0 0 14px var(--cyan)}
.eq{margin-top:10px}
.q2{position:absolute;left:128px;right:128px;top:210px;text-align:center;display:flex;flex-direction:column;gap:30px;align-items:center}
.code2{position:absolute;left:50%;top:600px;width:1000px;margin-left:-500px;display:flex;flex-direction:column;gap:22px;align-items:flex-start}
.editor{width:100%;box-sizing:border-box;padding:34px 40px;border-radius:var(--radius-md);background:#070d22;box-shadow:inset 0 0 0 2px var(--line);font-size:46px;line-height:1.6;color:var(--ink)}
.editor .kw,.code .kw{color:var(--orange);font-style:normal}
.ghost{color:var(--ink-dim);opacity:.3}
/* 3 */
.myth{position:absolute;left:50%;top:170px;width:900px;height:600px;margin-left:-450px}
.search{position:absolute;left:0;right:0;top:0;display:flex;align-items:center;gap:22px;padding:26px 36px;border-radius:60px;background:var(--surface);box-shadow:inset 0 0 0 2px var(--line);font-size:44px;font-weight:600;color:var(--ink-muted)}
.search i{font-style:normal;font-family:"Noto Color Emoji";font-size:40px}
.sheet{position:absolute;left:170px;right:170px;top:170px;height:360px;padding:36px 44px;border-radius:24px;background:#f1efe6;color:#1b2340;box-shadow:var(--lift);display:flex;flex-direction:column;gap:26px}
.sheet i{display:block;height:20px;border-radius:10px;background:#c9c5b4}.sheet i.s{width:60%}
.sheet .ig-label{color:#1b2340}
.xmark{position:absolute;inset:0;width:900px;height:600px;overflow:visible}
.xmark path{fill:none;stroke:var(--danger);stroke-width:18;stroke-linecap:round;stroke-dasharray:800;filter:drop-shadow(0 0 14px rgba(255,92,122,.8))}
.mythpill{position:absolute;left:50%;bottom:-40px;transform:translateX(-50%)}
.s3-loop{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;padding-bottom:40px}
#s3-loop{opacity:1}
.loopsteps{display:flex;align-items:center;gap:18px}.loopsteps .arr{font-size:48px;color:var(--ink-dim)}
.s3-count{font-size:44px}
.tokens{display:flex;align-items:center;gap:0;flex-wrap:wrap;position:absolute;left:40px;right:40px;bottom:40px}
.tokens .ig-label-sm{margin-right:24px}
.tok{font-size:42px;padding:10px 6px;border-bottom:8px solid var(--cyan)}.tok.t1{border-bottom-color:var(--orange)}
.web{position:absolute;right:120px;bottom:200px;width:560px;z-index:5;padding:30px 34px;border-radius:var(--radius-md);background:var(--surface);box-shadow:inset 0 0 0 2px var(--line),var(--lift);display:flex;flex-direction:column;gap:18px;align-items:flex-start}
.webrow{font-size:34px;font-weight:700;color:var(--ink-muted)}.webrow i{font-style:normal;font-family:"Noto Color Emoji"}
.wl{height:16px;width:100%;border-radius:8px;background:var(--surface-raised)}.wl.s{width:70%}
/* 4 phone */
.rig{position:absolute;left:38%;top:50%;width:620px;height:1040px;margin-left:-310px;margin-top:-520px}
.ig-phone.p4{left:0;top:0}
.p4 .thread{flex:1}.p4 .ig-bubble.in{align-self:flex-start;background:var(--surface-raised);border-bottom-left-radius:10px;border-bottom-right-radius:34px;font-size:32px}
.compose{margin:10px 22px;min-height:70px;border-radius:34px;box-shadow:inset 0 0 0 2px var(--line);padding:14px 24px;font-size:31px;font-weight:600;line-height:1.35;color:var(--ink)}
.suggbar{position:relative;height:70px;background:var(--night)}
.sset{position:absolute;inset:0;display:flex;align-items:center;opacity:0}
.sset span{flex:1;text-align:center;font-size:28px;font-weight:600;color:var(--ink-muted);border-right:2px solid var(--line)}
.sset span:last-child{border-right:none}.sset .mid{color:var(--cyan);font-weight:800}
.tap{position:absolute;left:50%;top:50%;width:130px;height:130px;margin:-65px 0 0 -65px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,122,26,.85) 0%,rgba(255,122,26,.35) 45%,rgba(255,122,26,0) 70%)}
.kb{background:var(--night);padding:12px 8px 30px;display:flex;flex-direction:column;gap:12px}
.krow{display:flex;justify-content:center;gap:7px}
.k{width:48px;height:64px;border-radius:10px;background:#18265a;color:var(--ink);font-size:28px;font-weight:600;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 0 var(--night-950)}
.k.fn{background:var(--surface);width:64px;font-size:24px}.k.w2{width:112px;font-size:22px}.k.space{width:250px;font-size:22px;color:var(--ink-muted)}
.s4-label{position:absolute;right:150px;top:50%;margin-top:-240px;width:640px;display:flex;flex-direction:column;align-items:flex-start;gap:30px}
.ring4,.ring7{width:140px;height:140px;transform:rotate(-90deg)}
.ring4 circle,.ring7 circle{fill:none;stroke-width:10}.rb{stroke:var(--surface-raised)}.rf{stroke:var(--cyan);stroke-dasharray:377;filter:drop-shadow(0 0 8px var(--cyan))}
.real{position:absolute;right:110px;top:200px;width:860px;display:flex;flex-direction:column;gap:24px;align-items:flex-start}
.shot{width:860px;border-radius:26px;overflow:hidden;box-shadow:0 0 0 3px var(--line),var(--lift)}.shot img{display:block;width:100%}
.cmt{position:absolute;right:110px;top:600px;display:flex;align-items:center;gap:22px;padding:24px 34px;border-radius:var(--radius-md);background:var(--surface);box-shadow:var(--glow-cyan)}
.bub{font-family:"Noto Color Emoji";font-size:52px}
/* 5 powers of ten */
.world{position:absolute;left:0;top:0;width:1920px;height:1080px}
.grid{position:absolute;inset:0}
.grid.dimg{background-image:linear-gradient(90deg,#050918 3px,transparent 3px),linear-gradient(#050918 3px,transparent 3px);background-size:30px 30px;background-color:#18265a}
.grid.lit{background-image:linear-gradient(90deg,#050918 3px,transparent 3px),linear-gradient(#050918 3px,transparent 3px);background-size:30px 30px;background-color:#22d3ee;
  -webkit-mask-image:radial-gradient(circle at 52% 51%,#000 0,#000 30%,rgba(0,0,0,.35) 60%,rgba(0,0,0,.15) 100%)}
.mytile{position:absolute;left:993px;top:543px;width:27px;height:27px;background:#ff7a1a;box-shadow:0 0 1px #ff7a1a}
.mylab{position:absolute;left:1040px;top:524px}
.s5-a,.s5-b{position:absolute;left:128px;top:120px;width:1100px;display:flex;flex-direction:column;gap:20px;align-items:flex-start;padding:36px 44px;border-radius:var(--radius-md);background:rgba(5,9,24,.82)}
.big{font-size:110px;line-height:.95}
.s5-c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:50px}
#s5-c{opacity:1}
.books{display:flex;gap:14px;align-items:flex-end}
.bk{display:block;width:62px;height:240px;border-radius:8px;background:#18265a;box-shadow:inset 0 0 0 4px #22d3ee,0 0 22px rgba(34,211,238,.35)}
.bk:nth-child(3n){height:200px;box-shadow:inset 0 0 0 4px #ff7a1a}.bk:nth-child(4n){height:270px}
.s5-d{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px}
.s5-d .pr-panel.stat{position:relative;width:900px}
/* 6 */
.s6-head{position:absolute;left:128px;right:128px;top:330px;text-align:center;transform-origin:50% 0}
.morph{position:absolute;left:50%;top:420px;width:1200px;height:470px;margin-left:-600px;border-radius:var(--radius-md);background:var(--surface);box-shadow:var(--glow-cyan),var(--lift)}
.mc{position:absolute;inset:0;padding:48px 60px;display:flex;flex-direction:column;gap:36px;align-items:flex-start}
.msg{font-size:62px;font-weight:600;line-height:1.35}
.wr{position:relative;display:inline-block}
.wr s{text-decoration:none}.wr b{display:none;color:var(--cyan);font-weight:800;text-shadow:var(--glow-text-cyan)}
.wr.bad s{text-decoration:underline wavy var(--orange);text-decoration-thickness:4px;text-underline-offset:12px}
.wr.bad.fixed s{display:none}.wr.bad.fixed b{display:inline}
.code{font-size:44px;line-height:1.55;color:var(--ink);white-space:normal}.code>div{white-space:pre}
.fix{color:var(--cyan);font-weight:800;text-shadow:var(--glow-text-cyan)}.miss{font-style:normal;color:var(--orange)}
.imo{position:absolute;left:128px;right:128px;top:130px;bottom:150px;display:flex;align-items:center;gap:80px}
.medal{width:300px;height:420px;flex:none}
.medal .rib{fill:none;stroke:#ff7a1a;stroke-width:34}.medal .gold{fill:#e7b53c;filter:drop-shadow(0 0 30px rgba(231,181,60,.6))}.medal .gold2{fill:none;stroke:#fff3c8;stroke-width:6;opacity:.6}.medal .star{fill:#fff3c8}
.imo-r{flex:1;display:flex;flex-direction:column;gap:36px;align-items:flex-start}
.scoreline{display:flex;align-items:center;gap:40px;width:100%}
.track{position:relative;flex:1;height:26px;border-radius:13px;background:var(--surface-raised)}
.gold-line{position:absolute;left:83%;top:-24px;bottom:-24px;width:6px;background:#e7b53c;box-shadow:0 0 14px #e7b53c}
.gl{position:absolute;left:83%;top:-66px;transform:translateX(-50%);font-family:var(--font-mono);font-size:26px;color:#e7b53c;text-transform:uppercase}
.mk{position:absolute;left:83%;top:50%;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:var(--cyan);box-shadow:0 0 20px var(--cyan)}
.score{font-size:110px;line-height:1}
.chips6{display:flex;flex-wrap:wrap;gap:20px 20px;align-items:center}
.did{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.just{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:48px}
.jq .ch{display:none}
/* 7 */
.gchat{position:absolute;left:128px;top:130px;width:820px;padding:34px 36px;border-radius:var(--radius-md);background:var(--surface);box-shadow:inset 0 0 0 2px var(--line),var(--lift);display:flex;flex-direction:column;gap:22px;transform-origin:0 50%}
.gc-head{display:flex;align-items:center;gap:16px;font-size:34px;font-weight:800;color:var(--ink-muted);padding-bottom:18px;border-bottom:2px solid var(--line)}.gc-ico{font-family:"Noto Color Emoji"}
.gm{align-self:flex-start;max-width:680px;padding:20px 28px;border-radius:30px;border-bottom-left-radius:10px;background:var(--surface-raised);font-size:40px;font-weight:600;line-height:1.3}
.gm b{display:block;font-size:24px;color:var(--orange);letter-spacing:.04em}
.gm.me{align-self:flex-end;background:rgba(34,211,238,.14);border-bottom-left-radius:30px;border-bottom-right-radius:10px}
.gm .ans{display:inline-block;color:var(--cyan);font-weight:800}
.hl-c{background:rgba(34,211,238,.22);box-shadow:0 0 0 4px rgba(34,211,238,.22);border-radius:6px}.hl-o{background:rgba(255,122,26,.22);box-shadow:0 0 0 4px rgba(255,122,26,.22);border-radius:6px}
.guess7{position:absolute;right:128px;top:260px;width:780px;display:flex;flex-direction:column;gap:30px;align-items:flex-start}
.guess7 .pr-panel{position:relative;width:100%;box-sizing:border-box}
.ring7{position:absolute;right:0;top:-30px}
.clue{position:absolute}#s7-cl1{right:360px;top:330px}#s7-cl2{right:260px;top:450px}
.rules{position:absolute;right:220px;top:600px;width:440px;height:260px;padding:30px 36px;box-sizing:border-box;border-radius:22px;background:#f1efe6;color:#1b2340;display:flex;flex-direction:column;gap:22px}
.rules .ig-label{color:#1b2340}.rules i{display:block;height:16px;border-radius:8px;background:#c9c5b4}
.rules svg{position:absolute;inset:10px;width:420px;height:240px;overflow:visible}.rules path{fill:none;stroke:var(--danger);stroke-width:14;stroke-linecap:round;stroke-dasharray:420}
.code7{position:absolute;right:128px;top:200px;width:960px;display:flex;flex-direction:column;gap:24px;align-items:flex-start}
.code7 .code{width:100%;box-sizing:border-box;padding:36px 40px;border-radius:var(--radius-md);background:#070d22;box-shadow:inset 0 0 0 2px var(--line);font-size:40px}
.code7 .code > div{position:relative;border-radius:10px;padding:2px 10px}
.val{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-size:26px;padding:4px 16px;border-radius:30px;color:var(--cyan);box-shadow:0 0 0 2px var(--cyan)}
.val.o{color:var(--orange);box-shadow:0 0 0 2px var(--orange)}
.hl.on{background:rgba(34,211,238,.16);box-shadow:0 0 0 3px var(--cyan)}
/* 8 */
.art{position:absolute;inset:0;transform-origin:50% 50%}
.art img{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover}
.glowdot{position:absolute;left:1500px;top:40px;width:330px;height:330px;border-radius:50%;background:radial-gradient(circle,rgba(34,211,238,.55),rgba(34,211,238,0) 70%)}
.ig-pointer .c,.ig-pointer path.c{stroke:var(--cyan)}.ig-pointer circle.c{fill:var(--cyan)}
.poem{position:absolute;left:128px;bottom:170px;width:1100px;padding:34px 44px;border-radius:var(--radius-md);background:rgba(10,17,40,.9);box-shadow:inset 0 0 0 2px var(--line);display:flex;flex-direction:column;gap:14px;font-size:50px;font-weight:600}
.rab{font-size:60px}
.both{position:absolute;left:128px;top:350px;display:flex;flex-direction:column;gap:22px;align-items:flex-start}
.versus{position:absolute;left:128px;right:128px;top:170px;display:grid;grid-template-columns:1fr 160px 1fr;align-items:center}
.qcard{padding:44px 48px;border-radius:var(--radius-md);background:var(--surface);display:flex;flex-direction:column;gap:26px;min-height:420px;box-sizing:border-box}
.qcard.c{box-shadow:var(--glow-cyan),var(--lift)}.qcard.c .ig-label{color:var(--cyan)}.qcard.o{box-shadow:var(--glow-orange),var(--lift)}.qcard.o .ig-label{color:var(--orange)}
.vsb{font-size:90px;text-align:center;color:var(--ink)}
.side{position:absolute;left:0;right:0;bottom:170px;display:flex;justify-content:center;align-items:center;gap:22px}
/* 9 */
.col9{position:absolute;top:170px;width:620px;display:flex;flex-direction:column;gap:26px;align-items:flex-start}
.col9.l{left:128px}.col9.r{right:128px}
.forum{display:flex;gap:26px;width:100%;box-sizing:border-box;padding:30px 34px;border-radius:18px;background:#10182f;box-shadow:inset 0 0 0 2px var(--line)}
.votes{display:flex;flex-direction:column;align-items:center;gap:6px;color:var(--ink-dim);font-size:30px}.votes b{color:var(--ink)}
.fp{flex:1;display:flex;flex-direction:column;gap:16px}
.fu{font-family:var(--font-mono);font-size:24px;color:var(--ink-dim)}.ft{font-size:44px;font-weight:800}.fb{font-size:36px;font-weight:500;line-height:1.4;color:var(--ink-muted)}
.mid9{position:absolute;left:50%;top:260px;width:320px;margin-left:-160px;display:flex;flex-direction:column;align-items:center;gap:14px}
.rated{display:flex;flex-direction:column;gap:14px;align-items:center;margin-top:30px}
.rc{width:280px;padding:16px 18px;border-radius:16px;background:var(--surface);box-shadow:inset 0 0 0 2px var(--line);display:flex;flex-direction:column;gap:10px}
.rc i{display:block;height:12px;border-radius:6px;background:var(--surface-raised)}.rc i.s{width:60%}.rc b{font-size:26px;color:#e7b53c;font-family:"Noto Color Emoji",var(--font-sans)}
.chatwin.c9{position:relative;right:auto;top:auto;width:620px;box-sizing:border-box}
.c9 .ig-bubble{font-size:38px}
/* 10 */
.s10v .ig-venn .circle{mix-blend-mode:normal}
.paper{position:absolute;left:170px;top:150px;width:760px;padding:44px 50px;background:#f1efe6;color:#1b2340;box-shadow:var(--lift);display:flex;flex-direction:column;gap:22px;font-family:Georgia,"DejaVu Serif",serif}
.pp-mast{font-size:64px;font-weight:700;border-bottom:4px double #1b2340;padding-bottom:12px}.pp-sub{font-size:28px;font-style:italic;color:#5b6070}
.pp-row{display:flex;gap:16px;align-items:center;font-size:36px}.pp-row i{display:block;height:16px;flex:1;border-radius:8px;background:#c9c5b4}.pp-row i.s{flex:.5}
.pp-row.hi{padding:6px 10px;border-radius:8px}.pp-row.hi.on{background:rgba(255,122,26,.3);box-shadow:0 0 0 4px #ff7a1a}
.book{position:absolute;right:230px;top:130px;width:520px;height:760px;border-radius:10px 22px 22px 10px;overflow:hidden;background:linear-gradient(180deg,#0f4c5c,#1b7a8a 60%,#e8d9b0);box-shadow:inset 14px 0 0 rgba(0,0,0,.25),var(--lift)}
.bk-waves{position:absolute;left:0;right:0;bottom:170px;height:160px;background:repeating-radial-gradient(circle at 50% 160%,rgba(255,255,255,.25) 0 6px,transparent 6px 26px)}
.bk-t{position:absolute;left:50px;right:40px;top:90px;font-family:Georgia,"DejaVu Serif",serif;font-size:84px;line-height:1;color:#fff8e6;font-style:italic}
.bk-a{position:absolute;left:50px;bottom:70px;font-family:Georgia,"DejaVu Serif",serif;font-size:34px;letter-spacing:.2em;color:#1b2340}
.chk{position:absolute;right:320px;top:910px}
.s10-stamp{left:1150px;top:430px;font-size:84px;z-index:5}
.recap{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:36px;text-align:center;padding:0 128px}
.s10-end{position:absolute;inset:0;text-align:center;padding-top:150px}
#s10-sign{opacity:0}
/* chrome: thin progress line + chapter name */
#rail{position:absolute;left:0;right:0;bottom:0;height:60px;z-index:20;opacity:1}
#pline{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(42,58,112,.6)}
#pfill{position:absolute;left:0;bottom:0;width:1920px;height:6px;background:var(--cyan);box-shadow:0 0 12px rgba(34,211,238,.8);transform-origin:left}
.chap{position:absolute;left:128px;bottom:28px;font-size:26px;letter-spacing:.1em;text-transform:uppercase;color:var(--cyan);opacity:0}
"""

THEME_CSS, DECOR = "", ""
EASES = ("0.16,1,0.3,1", "0.34,1.56,0.64,1", "0.7,0,0.84,0", "0.65,0,0.35,1")
if THEME != "neon":
    import themes
    th = themes.THEMES[THEME]
    THEME_CSS, DECOR, EASES = th["css"] + themes.V4_LIGHT, th["decor"](10), th["eases"]
    for n in range(1, 11):
        for pre in ("tag", "fig"):
            if f'id="{pre}{n}"' in DECOR:
                A.append(f'tl.set("#{pre}{n}",{{display:"block"}},{T[n]["start"]});')
                A.append(f'tl.set("#{pre}{n}",{{display:"none"}},{round(T[n]["start"] + T[n]["dur"], 3)});')
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree("video", OUT, ignore=shutil.ignore_patterns("index.html", ".hyperframes"))

html = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<script src="assets/gsap.min.js"></script><script src="assets/CustomEase.min.js"></script>
<style>{FONTS}{tokens_css()}{bundle_css()}{LOCAL}{THEME_CSS}</style></head>
<body>
<div id="root" class="ig-frame" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
  <audio id="vo" src="assets/mix.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
  {''.join(S)}
  {DECOR}
  <div id="rail">{chap_html}<div id="pline"></div><div id="pfill"></div></div>
</div>
<script>
  gsap.registerPlugin(CustomEase);
  CustomEase.create("igOut","{EASES[0]}");
  CustomEase.create("igPop","{EASES[1]}");
  CustomEase.create("igSlam","{EASES[2]}");
  CustomEase.create("igIO","{EASES[3]}");
  CustomEase.create("igIn","0.5,0,0.75,0");
  CustomEase.create("igSettle","0.22,1,0.36,1");
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
{chr(10).join('  ' + a for a in A)}
  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
</body></html>
"""
open(f"{OUT}/index.html", "w").write(html)
print(f"wrote {OUT}/index.html: {TOTAL}s, {len(A)} timeline entries")
gaps = frozen_report()
print("frozen stretches > 3.2 s:", gaps if gaps else "none")


# ================================================================ AUDIO MIX: voice + SFX events, mastered to -14 LUFS
import array
import subprocess
import sys
import wave

if THEME != "neon":  # same voice and sound for every skin: reuse the neon mix
    print("reused video/assets/mix.mp3")
    sys.exit(0)

GAIN = {"pop": 0.2, "click": 0.18, "whoosh": 0.45, "thud": 0.25, "ding": 0.26, "buzz": 0.35, "tick": 0.22}
SPACING = {"click": 0.07}
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/vo/voiceover.wav", "-ac", "1", "-ar", "44100", "sfx/_voice.wav"], check=True)
with wave.open("sfx/_voice.wav") as w:
    voice = array.array("h", w.readframes(w.getnframes()))
n_total = int((TOTAL + 1) * 44100)
mix = [0.0] * n_total
for i, v in enumerate(voice[:n_total]):
    mix[i] = float(v)
clips = {}
for name in GAIN:
    with wave.open(f"sfx/{name}.wav") as w:
        clips[name] = array.array("h", w.readframes(w.getnframes()))
last = {}
used = 0
for t, name in sorted(SFX):
    if t - last.get(name, -9) < SPACING.get(name, 0.3):  # identical sounds at least .3 s apart
        continue
    last[name] = t
    used += 1
    start = int(t * 44100)
    g = GAIN[name]
    for k, v in enumerate(clips[name]):
        if 0 <= start + k < n_total:
            mix[start + k] += v * g
peak = max(abs(x) for x in mix) or 1
scale = min(1.0, 32000 / peak)
out_ = array.array("h", (int(x * scale) for x in mix))
with wave.open("sfx/_mix.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(out_.tobytes())
# two-pass loudnorm: measure, then apply linear normalization to -14 LUFS / -1 dBTP
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", "sfx/_mix.wav", "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "sfx/_mix.wav", "-af", af, "-ar", "48000", "-ac", "2", "-b:a", "192k", "video/assets/mix.mp3"], check=True)
print(f"mixed {used} of {len(SFX)} sound events")
