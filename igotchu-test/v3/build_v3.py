"""igotchu Script 3, v3: HyperFrames composition built on the Neon Blueprint design system.

Inputs (this folder): timing.json (slide start/length), slides.json (narration per slide),
segments.json (speech segments per slide clip, from silence detection), ds/ (design system files).
Output: video/index.html. All motion is GSAP on one paused timeline (no CSS animations: the
renderer seeks frame by frame and cannot drive them).
"""
import json
import re

T = {i + 1: s for i, s in enumerate(json.load(open("timing.json")))}
SL = {s["n"]: s for s in json.load(open("slides.json"))}
SEG = {int(k): v for k, v in json.load(open("segments.json")).items()}
LEAD = 0.35
TOTAL = round(T[10]["start"] + T[10]["dur"], 3)

# ---------------------------------------------------------------- timing helpers
def at(n, rel):
    return round(T[n]["start"] + rel, 3)


_ALIGN = {}


def _align(n):
    """Match the script's phrases (split at punctuation) to the clip's speech segments (split at pauses).
    Monotonic DP: each group of 1-3 phrases takes 1-3 segments; cost = squared gap between the group's
    duration and its expected duration at the slide's speaking rate. Returns (phrase_start_char, time) pairs."""
    if n in _ALIGN:
        return _ALIGN[n]
    text = SL[n]["text"]
    cuts = [0] + [m.end() for m in re.finditer(r"[,.?!:;\u2026]+[\"\u201d']?\s+", text)] + [len(text)]
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
        for q in range(i0, node[0]):  # phrases inside a group: spread by character position
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
    return at(n, LEAD + t + off)


# ---------------------------------------------------------------- animation helpers
A = []
SFX = []  # (time, sound) events, mixed under the voice at the end
_seen = set()


def _tw(sel, frm, to, t, dur, ease):
    v = {**to, "duration": round(dur, 3), "ease": ease}
    if sel in _seen:
        v["immediateRender"] = False
    _seen.add(sel)
    A.append(f"tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(v)},{round(t, 3)});")


def raw(js):
    A.append(js)


def rise(sel, t, y=40, dur=0.55):
    _tw(sel, {"opacity": 0, "y": y}, {"opacity": 1, "y": 0}, t, dur, "igOut")


def fade(sel, t, dur=0.45):
    _tw(sel, {"opacity": 0}, {"opacity": 1}, t, dur, "none")


def out(sel, t, dur=0.2):
    _tw(sel, {"opacity": 1}, {"opacity": 0}, t, dur, "none")


def pop(sel, t, dur=0.5, s=0.6, sound=True):
    if sound:
        SFX.append((t, "pop"))
    _tw(sel, {"opacity": 0, "scale": s}, {"opacity": 1, "scale": 1}, t, dur, "igPop")


def land(sel, t):
    SFX.append((t + 0.15, "ding"))
    _tw(sel, {"opacity": 0, "y": -60, "scale": 0.8}, {"opacity": 1, "y": 0, "scale": 1}, t, 0.55, "igPop")


def slide_in(sel, t, dx):
    _tw(sel, {"opacity": 0, "x": dx}, {"opacity": 1, "x": 0}, t, 0.7, "igIO")


def grow(sel, t, dur=0.6):
    _tw(sel, {"scaleX": 0}, {"scaleX": 1}, t, dur, "igOut")


def draw(sel, t, length, dur=0.8):
    _tw(sel, {"strokeDashoffset": length, "opacity": 1}, {"strokeDashoffset": 0, "opacity": 1}, t, dur, "igOut")


def slam(sel, t):
    SFX.append((t + 0.28, "thud"))
    _tw(sel, {"opacity": 0, "rotation": -16, "scale": 2.4}, {"opacity": 1, "rotation": -8, "scale": 1}, t, 0.32, "igSlam")
    raw(f'tl.to({json.dumps(sel)},{{keyframes:[{{x:-10,y:6,duration:.07}},{{x:8,y:-4,duration:.07}},{{x:-4,y:2,duration:.07}},{{x:0,y:0,duration:.07}}],ease:"none"}},{round(t + 0.32, 3)});')


def ignite(sel, t):
    raw(f'tl.fromTo({json.dumps(sel)},{{opacity:0}},{{keyframes:[{{opacity:1,duration:.11}},{{opacity:.2,duration:.07}},{{opacity:1,duration:.09}},{{opacity:.5,duration:.07}},{{opacity:1,duration:.11}}],ease:"none"}},{round(t, 3)});')
    _seen.add(sel)


def show(sel, t):
    raw(f'tl.set({json.dumps(sel)},{{display:"inline"}},{round(t, 3)});')


def hide(sel, t):
    raw(f'tl.set({json.dumps(sel)},{{display:"none"}},{round(t, 3)});')


def camera(n, amount=0.035, dx=0):
    """Slow push on the scene wrapper for the whole slide: nothing ever sits fully still."""
    raw(f'tl.fromTo("#s{n} .cam",{{scale:1,x:0}},{{scale:{1 + amount},x:{dx},duration:{T[n]["dur"]},ease:"sine.inOut"}},{T[n]["start"]});')


def blink(sel, t0, t1):
    n = int((t1 - t0) / 0.5)
    if n > 0:
        raw(f'tl.fromTo({json.dumps(sel)},{{opacity:1}},{{opacity:0,duration:.5,ease:"steps(1)",repeat:{n - 1},yoyo:true}},{round(t0, 3)});')


S = []


def scene(n, inner, cls=""):
    s = T[n]
    if n > 1:
        SFX.append((s["start"] - 0.2, "whoosh"))
    S.append(f'<section id="s{n}" class="clip scene {cls}" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="1"><div class="cam">{inner}</div></section>')


# ---------------------------------------------------------------- reusable component: predictor panel
def predictor_steps(pid, steps, t0, gaps, show_pct=False, keep_last=False):
    """Candidate panel for next-word prediction. steps: [(winner, [(word, pct), ...]), ...].
    Each step: panel appears with bars growing, winner lights up, word appended to #{pid}-reply."""
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
        fade(f"#{pid}-p{i}", t, 0.15)
        raw(f'tl.fromTo("#{pid}-p{i} .bar i",{{scaleX:0}},{{scaleX:1,duration:{round(gap * 0.45, 2)},ease:"igOut",stagger:.06}},{round(t + 0.05, 3)});')
        raw(f'tl.set("#{pid}-p{i}",{{className:"pr-panel lock"}},{round(t + gap * 0.62, 3)});')
        show(f"#{pid}-w{i}", round(t + gap * 0.7, 3))
        _tw(f"#{pid}-w{i}", {"opacity": 0, "y": -24}, {"opacity": 1, "y": 0}, round(t + gap * 0.7, 3), 0.3, "igPop")
        if not (keep_last and i == len(steps) - 1):
            out(f"#{pid}-p{i}", round(t + gap - 0.12, 3), 0.1)
        t += gap
    words = "".join(f'<span class="rw" id="{pid}-w{i}">{w} </span>' for i, (w, _) in enumerate(steps))
    return "".join(html), words, t


# ================================================================ SCENES
# ---- 1. Hook: prediction chat box
st1 = [("Yes,", [("Yes,", 78), ("No,", 14), ("Well,", 8)]),
       ("technically", [("technically", 55), ("it's", 30), ("actually", 15)]),
       ("it's", [("it's", 70), ("a", 18), ("tomatoes", 12)]),
       ("a", [("a", 88), ("not", 8), ("the", 4)]),
       ("fruit.", [("fruit.", 71), ("berry.", 17), ("vegetable.", 12)])]
p1, w1, t1_end = predictor_steps("h", st1, cue(1, "ChatGPT") + 1.0, [1.7, 1.5, 1.2, 1.0, 1.4])
scene(1, f"""
  <div class="s1-left">
    <h1 class="ig-hxl"><span class="ln" id="s1-l1">ChatGPT doesn't</span><span class="ln" id="s1-l2">know <span class="ig-em-o">anything.</span></span></h1>
    <p class="ig-body-lg ig-muted" id="s1-sub">It's <span class="ig-em-c">guessing.</span> One word at a time.</p>
  </div>
  <div class="chatwin" id="s1-chat">
    <div class="cw-head"><div class="cw-dot"></div><span>Chatbot</span></div>
    <div class="ig-bubble ig-bubble--me cw-q" id="s1-q">Is a tomato a fruit?</div>
    <div class="ig-bubble ig-bubble--ai cw-a" id="s1-a"><span class="reply">{w1}</span><span class="caret" id="s1-caret">|</span></div>
    <div class="pr-dock">{p1}</div>
  </div>
  <div class="qcard" id="s1-q2"><span class="ig-kicker"><span class="ig-kicker-dot"></span>Hold on to this</span>
    <h2 class="ig-hsm">If it's only guessing&hellip;<br/>how can it <span class="ig-em-o">solve problems?</span></h2></div>""")
camera(1, 0.03)
rise("#s1-l1", at(1, 0.15), 50)
rise("#s1-l2", at(1, 0.35), 50)
_tw("#s1-chat", {"opacity": 0, "y": 260}, {"opacity": 1, "y": 0}, at(1, 0.3), 0.8, "igOut")
pop("#s1-q", at(1, 0.9))
pop("#s1-a", cue(1, "ChatGPT") + 0.9)
blink("#s1-caret", cue(1, "ChatGPT") + 0.9, t1_end + 3)
rise("#s1-sub", cue(1, "It's guessing"))
t_q = cue(1, "If it's only guessing")
for s_ in ["#s1-l1", "#s1-l2", "#s1-sub"]:
    out(s_, t_q - 0.4, 0.25)
raw(f'tl.to("#s1-chat",{{x:620,opacity:.25,duration:.6,ease:"igIO"}},{round(t_q - 0.5, 3)});')
rise("#s1-q2", t_q)

# ---- 2. Peanut butter
scene(2, """
  <div class="ig-safe ig-center">
    <div class="ig-label ig-dim" id="s2-lab" style="margin-bottom:48px">Finish the sentence in your head</div>
    <div class="ig-sentence ig-hsm"><span id="s2-sent">Peanut butter and</span>
      <span class="ig-blank" id="s2-blank"><span class="blank-caret" id="s2-caret"></span><span id="s2-ans">jelly</span></span></div>
    <div class="ig-guesses">
      <div class="ig-guess ig-guess--win" id="s2-g1"><span class="word">jelly</span><span class="bar"><i style="--p:78%"></i></span></div>
      <div class="ig-guess ig-guess--odd" id="s2-g2"><span class="word">jam</span><span class="bar"><i style="--p:16%"></i></span></div>
      <div class="ig-guess" id="s2-g3"><span class="word">honey</span><span class="bar"><i style="--p:6%"></i></span></div>
    </div>
    <div class="ig-label ig-em-c s2-note" id="s2-note">Seen together a thousand times</div>
  </div>""")
camera(2, 0.04)
rise("#s2-lab", at(2, 0.3))
rise("#s2-sent", cue(2, "Peanut butter") - 0.3)
pop("#s2-blank", cue(2, "Peanut butter"))
blink("#s2-caret", cue(2, "Peanut butter") + 0.3, cue(2, "You said jelly"))
out("#s2-caret", cue(2, "You said jelly"), 0.05)
land("#s2-ans", cue(2, "You said jelly") + 0.15)
for i, t in enumerate([cue(2, "You said jelly") + 0.3, cue(2, "Or jam"), cue(2, "Or jam") + 0.15]):
    rise(f"#s2-g{i+1}", t)
    grow(f"#s2-g{i+1} .bar i", t + 0.2)
pop("#s2-note", cue(2, "You've just seen") + 0.3)

# ---- 3. Capital of France + the loop
st3 = [("It's", [("It's", 60), ("Paris", 25), ("The", 15)]), ("known", [("known", 50), ("famous", 35), ("home", 15)]),
       ("for", [("for", 90), ("as", 7), ("by", 3)]), ("the", [("the", 70), ("its", 25), ("art", 5)]),
       ("Eiffel", [("Eiffel", 80), ("Louvre", 15), ("food", 5)]), ("Tower,", [("Tower,", 97), ("Tower.", 2), ("tower", 1)]),
       ("art,", [("art,", 50), ("food,", 40), ("wine,", 10)]), ("food", [("food", 60), ("fashion", 30), ("cafes", 10)]),
       ("and", [("and", 85), ("&", 10), ("or", 5)]), ("fashion.", [("fashion.", 55), ("wine.", 30), ("romance.", 15)])]
t3_loop = cue(3, "Then it adds") - 0.2
gaps3 = [0.9, 0.75, 0.6, 0.5, 0.42, 0.36, 0.3, 0.26, 0.24, 0.22]
p3, w3, t3_end = predictor_steps("lp", st3, t3_loop, gaps3, show_pct=False)
scene(3, f"""
  <div class="ig-safe ig-center" id="s3-fill">
    <div class="ig-sentence ig-hsm"><span id="s3-sent">The capital of France is</span>
      <span class="ig-blank" id="s3-blank"><span class="blank-caret" id="s3-caret"></span><span id="s3-ans">Paris</span></span></div>
    <div class="ig-guesses">
      <div class="ig-guess ig-guess--win" id="s3-g1"><span class="word">Paris</span><span class="bar"><i style="--p:94%"></i></span><span class="pct">94%</span></div>
      <div class="ig-guess" id="s3-g2"><span class="word">beautiful</span><span class="bar"><i style="--p:4%"></i></span><span class="pct">4%</span></div>
      <div class="ig-guess" id="s3-g3"><span class="word">Lyon</span><span class="bar"><i style="--p:2%"></i></span><span class="pct">2%</span></div>
    </div>
  </div>
  <div class="s3-loop" id="s3-loop">
    <div class="loopsteps">
      <span class="ig-pill" id="s3-k1">Read so far</span><span class="arr" id="s3-ar1">&rarr;</span>
      <span class="ig-pill" id="s3-k2">Guess next word</span><span class="arr" id="s3-ar2">&rarr;</span>
      <span class="ig-pill" id="s3-k3">Add it</span><span class="arr" id="s3-ar3">&rarr;</span>
      <span class="ig-pill ig-pill--o" id="s3-k4">Repeat</span>
    </div>
    <div class="chatwin wide" id="s3-chat">
      <div class="ig-bubble ig-bubble--me cw-q">What's the capital of France?</div>
      <div class="ig-bubble ig-bubble--ai cw-a"><span class="reply">Paris. {w3}</span></div>
      <div class="pr-dock">{p3}</div>
    </div>
    <div class="s3-count" id="s3-count"><span class="ig-em-o">&times; hundreds</span> &middot; super fast</div>
  </div>""")
camera(3, 0.035)
rise("#s3-sent", at(3, 0.3))
pop("#s3-blank", at(3, 0.5))
blink("#s3-caret", at(3, 0.8), cue(3, "Paris"))
out("#s3-caret", cue(3, "Paris"), 0.05)
for i in range(3):
    rise(f"#s3-g{i+1}", at(3, 1.2) + i * 0.15)
    grow(f"#s3-g{i+1} .bar i", at(3, 1.4) + i * 0.15)
land("#s3-ans", cue(3, "Paris"))
raw(f'tl.to("#s3-fill",{{opacity:0,y:-60,duration:.35,ease:"power2.in"}},{round(cue(3, "What comes next") - 0.9, 3)});')
_seen.add("#s3-fill")
for i in range(4):
    pop(f"#s3-k{i+1}", cue(3, "What comes next") - 0.5 + i * 0.15)
    if i < 3:
        fade(f"#s3-ar{i+1}", cue(3, "What comes next") - 0.4 + i * 0.15, 0.2)
_tw("#s3-chat", {"opacity": 0, "y": 120}, {"opacity": 1, "y": 0}, t3_loop - 0.5, 0.5, "igOut")
# the loop steps light up in turn, faster and faster, in sync with the word steps
t = t3_loop
for i, g in enumerate(gaps3):
    k = (i % 3) + 1
    raw(f'tl.fromTo("#s3-k{k}",{{boxShadow:"0 0 0 2px #22d3ee, 0 0 60px rgba(34,211,238,.9)",scale:1.08}},{{boxShadow:"0 0 0 2px #22d3ee, 0 0 24px rgba(34,211,238,.55), 0 0 72px rgba(34,211,238,.25)",scale:1,duration:{round(g * 0.9, 2)},ease:"igOut",immediateRender:false}},{round(t, 3)});')
    t += g
pop("#s3-count", cue(3, "Hundreds of times"))

# ---- 4. Phone autocomplete (the v2 scene, restyled to the design system)
typed = "I'm going to"
nwords = "be there in a few minutes and I will be there in a few minutes and".split()
alts = [("the", "get"), ("here", "back"), ("the", "at"), ("few", "bit"), ("couple", "lot"), ("min", "hours"), ("so", "but"),
        ("we", "you"), ("be", "have"), ("home", "back"), ("here", "at"), ("on", "at"), ("the", "few"), ("couple", "lot"),
        ("min", "days"), ("so", "lol")]
chars = "".join(f'<span class="ch" id="s4-c{i}">{"&nbsp;" if c == " " else c}</span>' for i, c in enumerate(typed))
spans = "".join(f'<span class="tw" id="s4-t{i}"> {w}</span>' for i, w in enumerate(nwords))
sets = '<div class="sset" id="s4-set0"><span>I</span><span class="mid">be</span><span>the</span></div>'
for i in range(len(nwords)):
    nxt = nwords[i + 1] if i + 1 < len(nwords) else "be"
    a, b = alts[(i + 1) % len(alts)]
    sets += f'<div class="sset" id="s4-set{i+1}"><span>{a}</span><span class="mid">{nxt}</span><span>{b}</span></div>'
kb = ""
for r, row in enumerate(["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]):
    keys = "".join(f'<b class="k" id="s4-k{c}">{c}</b>' for c in row)
    if r == 2:
        keys = '<b class="k fn">&#8679;</b>' + keys + '<b class="k fn">&#9003;</b>'
    kb += f'<div class="krow">{keys}</div>'
kb += '<div class="krow"><b class="k fn w2">123</b><b class="k space" id="s4-kspace">space</b><b class="k fn w2">return</b></div>'
scene(4, f"""
  <div class="rig" id="s4-rig">
    <div class="ig-phone p4" id="s4-phone"><div class="screen">
      <div class="notch"></div>
      <div class="head"><div class="avatar">J</div><div><div class="name">Jay</div><div class="status">online</div></div></div>
      <div class="thread">
        <div class="ig-bubble ig-bubble--me in">yo where are you??</div>
        <div class="ig-bubble ig-bubble--me in">we're all here already</div>
      </div>
      <div class="compose"><span class="ctext">{chars}{spans}</span><span class="caret2">|</span></div>
      <div class="suggbar">{sets}<div class="tap" id="s4-tap"></div></div>
      <div class="kb">{kb}</div>
    </div></div>
    <div class="ig-stamp s4-stamp" id="s4-stamp">NONSENSE.</div>
  </div>
  <div class="s4-label" id="s4-lab"><span class="ig-kicker ig-kicker--cyan"><span class="ig-kicker-dot"></span>Try it</span>
    <p class="ig-body-lg">Type <b class="ig-em-c">"I'm going to"</b><br/>tap the <b class="ig-em-o">middle</b> word.<br/>Again. And again.</p></div>
  <div class="s4-out" id="s4-b"><h2 class="ig-hsm">Your phone is guessing too.</h2><p class="ig-body-lg ig-muted">It's just <span class="ig-em-o">really bad</span> at it.</p></div>""")
_tw("#s4-rig", {"opacity": 0, "y": 260}, {"opacity": 1, "y": 0}, at(4, 0.2), 0.8, "igOut")
raw(f'tl.fromTo("#s4-rig",{{rotation:-1.5}},{{rotation:1.5,duration:{round(T[4]["dur"] - 1, 2)},ease:"sine.inOut",immediateRender:false}},{at(4, 0.2)});')
rise("#s4-lab", cue(4, "Try it") - 0.2)
fade("#s4-set0", at(4, 0.4), 0.2)
tc = cue(4, "Type") + 0.5
for i, c in enumerate(typed):
    t = round(tc + i * 0.11, 3)
    show(f"#s4-c{i}", t)
    SFX.append((t, "click"))
    kid = "#s4-kspace" if c == " " else (f"#s4-k{c.upper()}" if c.isalpha() else None)
    if kid:
        raw(f'tl.fromTo("{kid}",{{backgroundColor:"#ff7a1a",scale:1.25}},{{backgroundColor:"#18265a",scale:1,duration:.25,ease:"power1.out",immediateRender:false}},{t});')
t0 = cue(4, "You'll get something") + 0.8
t_end = cue(4, "It's nonsense") - 0.4
step = (t_end - t0) / len(nwords)
raw(f'tl.to("#s4-rig",{{scale:1.2,y:-160,duration:1.0,ease:"igIO"}},{round(t0 - 1.0, 3)});')
out("#s4-lab", t0 - 0.9, 0.3)
_seen.add("#s4-tap")
for i in range(len(nwords)):
    t = round(t0 + i * step, 3)
    show(f"#s4-t{i}", t)
    SFX.append((t - 0.03, "click"))
    _tw("#s4-tap", {"opacity": 0.9, "scale": 0.3}, {"opacity": 0, "scale": 1.6}, t - 0.05, round(step * 0.9, 3), "power2.out")
    _tw(f"#s4-set{i}", {"opacity": 1}, {"opacity": 0}, t, 0.05, "none")
    _tw(f"#s4-set{i+1}", {"opacity": 0}, {"opacity": 1}, t, 0.05, "none")
tn = cue(4, "It's nonsense")
raw(f'tl.to("#s4-rig",{{scale:1,y:0,duration:.45,ease:"igOut"}},{round(tn - 0.45, 3)});')
slam("#s4-stamp", tn)
raw(f'tl.to("#s4-rig",{{x:-430,duration:.8,ease:"igIO"}},{round(tn + 1.2, 3)});')
rise("#s4-b", tn + 1.7)

# ---- 5. Illustration scene: tiny phone brain vs giant library (token aside cut)
scene(5, """
  <div class="art" id="s5-art"><img src="assets/brain-library.png" alt=""/>
    <svg class="ig-pointer" viewBox="0 0 1920 1080" style="left:0;top:0;width:1920px;height:1080px">
      <circle id="s5-d1" cx="330" cy="700" r="12"/><path id="s5-l1" d="M330 700 V560 H430" style="stroke-dasharray:260"/>
      <circle id="s5-d2" cx="1340" cy="150" r="12" class="c"/><path id="s5-l2" class="c" d="M1340 150 H1080 V230" style="stroke-dasharray:360"/>
    </svg>
    <div class="ig-callout" style="left:440px;top:522px"><span class="ig-pill ig-pill--o" id="s5-p1">Your phone: your texts</span></div>
    <div class="ig-callout" style="left:760px;top:240px"><span class="ig-pill" id="s5-p2">ChatGPT: books, sites, forums, code</span></div>
  </div>
  <div class="s5-scrim"></div>
  <h1 class="s5-scale" id="s5-scale">Scale.</h1>
  <div class="s5-life" id="s5-life"><p class="ig-body-lg">More reading than any human<br/>could do in <span class="ig-em-o">thousands of lifetimes.</span></p></div>""", "plain")
_tw("#s5-art", {"scale": 1.0}, {"scale": 1.12}, at(5, 0.0), T[5]["dur"], "none")
raw(f'tl.fromTo("#s5-art",{{opacity:0}},{{opacity:1,duration:3,ease:"sine.inOut",immediateRender:false}},{at(5, 0.0)});')
_tw("#s5-scale", {"opacity": 0, "scale": 1.6}, {"opacity": 1, "scale": 1}, cue(5, "Scale"), 0.45, "igSlam")
out("#s5-scale", cue(5, "Your phone learned") + 0.6, 0.25)
pop("#s5-d1", cue(5, "Your phone learned"))
draw("#s5-l1", cue(5, "Your phone learned") + 0.1, 260)
pop("#s5-p1", cue(5, "Your phone learned") + 0.6)
pop("#s5-d2", cue(5, "Models like"))
draw("#s5-l2", cue(5, "Models like") + 0.1, 360)
pop("#s5-p2", cue(5, "Models like") + 0.6)
rise("#s5-life", cue(5, "More reading"))

# ---- 6. The question: one card that morphs code -> tax form -> checklist
code = ['<i class="kw">def</i> plan_wedding(guests):', '    venue = find_venue(<i class="n">120</i>)', '    <i class="kw">return</i> budget(venue)']
code_html = "".join(f'<div class="cl" id="s6-cl{i}">{c}</div>' for i, c in enumerate(code))
chk = ["Book the venue", "Send invites", "Taste the cake", "Pick the music"]
chk_html = "".join(f'<div class="ck" id="s6-ck{i}"><span class="box" id="s6-cb{i}"></span>{c}</div>' for i, c in enumerate(chk))
auto = "Autocomplete?"
auto_html = "".join(f'<span class="ch" id="s6-a{i}">{c}</span>' for i, c in enumerate(auto))
scene(6, f"""
  <div class="s6-head" id="s6-head"><div class="ig-label ig-dim">The question that's been bugging you</div>
    <h1 class="ig-hsm">Wait&hellip; then how does it<br/><span class="ig-em-o">solve problems?</span></h1></div>
  <div class="morph" id="s6-card">
    <div class="mc" id="s6-m1"><span class="ig-pill">Write working code</span><div class="code">{code_html}</div></div>
    <div class="mc" id="s6-m2"><span class="ig-pill">Explain a tax form</span>
      <div class="form"><div class="fr"><span>Line 12 &middot; Deductions</span><span class="fv">$13,850</span></div>
      <div class="fr hi" id="s6-hi"><span>Line 15 &middot; Taxable income</span><span class="fv">?</span></div>
      <div class="fr"><span>Line 16 &middot; Tax</span><span class="fv">&mdash;</span></div></div></div>
    <div class="mc" id="s6-m3"><span class="ig-pill">Help plan a wedding</span><div class="chk">{chk_html}</div></div>
  </div>
  <div class="s6-auto" id="s6-auto"><span class="ig-hxl">That's it? </span><span class="ig-hxl ig-em-o">{auto_html}</span><span class="ig-hxl caret3" id="s6-caret">|</span></div>
  <div class="s6-wild" id="s6-wild"><h1 class="ig-hxl">It's actually <span class="ig-em-c" id="s6-w">wild.</span></h1>
    <svg class="burst" viewBox="-300 -300 600 600">{''.join(f'<path id="s6-r{i}" d="M0 -190 V-290" transform="rotate({a})"/>' for i, a in enumerate([-30, 0, 30, 150, 180, 210]))}</svg></div>""")
camera(6, 0.03)
rise("#s6-head", at(6, 0.3))
_tw("#s6-card", {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0}, cue(6, "how can it write") - 0.3, 0.5, "igOut")
fade("#s6-m1", cue(6, "how can it write") - 0.3, 0.2)
for i in range(3):
    rise(f"#s6-cl{i}", cue(6, "how can it write") + 0.1 + i * 0.25, 20, 0.3)
out("#s6-m1", cue(6, "or explain") - 0.1, 0.15)
fade("#s6-m2", cue(6, "or explain"), 0.2)
raw(f'tl.fromTo("#s6-hi",{{backgroundColor:"rgba(34,211,238,0)"}},{{backgroundColor:"rgba(34,211,238,.18)",duration:.4,immediateRender:false}},{round(cue(6, "or explain") + 0.5, 3)});')
out("#s6-m2", cue(6, "or help plan") - 0.1, 0.15)
fade("#s6-m3", cue(6, "or help plan"), 0.2)
for i in range(4):
    rise(f"#s6-ck{i}", cue(6, "or help plan") + 0.05 + i * 0.12, 16, 0.3)
    raw(f'tl.set("#s6-cb{i}",{{className:"box on"}},{round(cue(6, "or help plan") + 0.6 + i * 0.25, 3)});')
t_h = cue(6, "Honestly")
for s_ in ["#s6-card", "#s6-head"]:
    out(s_, t_h - 0.1, 0.25)
t_a = cue(6, "That's it?")
fade("#s6-auto", t_a - 0.1, 0.1)
for i in range(len(auto)):
    show(f"#s6-a{i}", t_a + 0.45 + i * 0.06)
blink("#s6-caret", t_a, cue(6, "no, it's actually wild"))
t_w = cue(6, "no, it's actually wild")
for i in reversed(range(len(auto))):  # backspace
    hide(f"#s6-a{i}", t_w - 0.9 + (len(auto) - 1 - i) * 0.05)
out("#s6-auto", t_w - 0.1, 0.1)
rise("#s6-wild", t_w)
pop("#s6-w", t_w + 0.35, 0.5, 0.3)
for i in range(6):
    draw(f"#s6-r{i}", t_w + 0.45, 100, 0.35)
    out(f"#s6-r{i}", t_w + 1.1, 0.3)

# ---- 7. Illustration: shattering glass, then the recipe card, then what it soaked up
scene(7, """
  <div class="art" id="s7-art"><img src="assets/glass.png" alt=""/>
    <svg class="ig-pointer ig-pointer--o" viewBox="0 0 1920 1080" style="left:0;top:0;width:1920px;height:1080px">
      <circle id="s7-d1" cx="1060" cy="720" r="12"/><path id="s7-l1" d="M1060 720 V860 H900" style="stroke-dasharray:320"/></svg>
    <div class="ig-callout" style="left:560px;top:830px"><span class="ig-pill ig-pill--o" id="s7-p1">Glasses break</span></div>
  </div>
  <div class="ig-scene-scrim"></div>
  <div class="ig-scene-head" id="s7-head" style="width:1000px"><span class="ig-kicker"><span class="ig-kicker-dot"></span>Here's the thing</span>
    <h1 class="ig-hsm">To guess well,<br/>you have to<br/><span class="ig-em-c">understand a lot.</span></h1></div>
  <div class="sentcard" id="s7-sent"><span class="ig-body">"She dropped the glass, and it&hellip;"</span><span class="ans ig-em-c" id="s7-a1">breaks</span></div>
  <div class="recipe" id="s7-rec">
    <div class="ig-label ig-dim">Pancakes</div>
    <div class="rq ig-body-lg">Needs <b>3 eggs</b></div>
    <div class="eggs"><i class="egg" id="s7-e1"></i><i class="egg" id="s7-e2"></i><i class="egg miss" id="s7-e3"></i></div>
    <div class="ig-body">"&hellip;but I only have two, so I&hellip;"</div>
    <div class="ans ig-body-lg ig-em-c" id="s7-a2">buy one more.</div>
    <span class="ig-pill" id="s7-need">Needs reasoning</span>
  </div>
  <div class="s7-soak" id="s7-soak"><div class="ig-label ig-dim" id="s7-sl">What it soaked up</div>
    <div class="ig-chips">
      <span class="ig-chip" id="s7-c1"><span class="t">grammar</span></span><span class="ig-chip" id="s7-c2"><span class="t">facts</span></span>
      <span class="ig-chip" id="s7-c3"><span class="t">logic</span></span><span class="ig-chip ig-chip--o" id="s7-c4"><span class="t">how people explain</span></span></div>
    <p class="ig-body-lg" id="s7-b">Nobody programmed it in. <span class="ig-em-o">It got absorbed.</span></p></div>""", "plain")
t_dim7 = cue(7, "The recipe") - 0.4
_tw("#s7-art", {"scale": 1.0}, {"scale": 1.12}, at(7, 0.0), round(t_dim7 - at(7, 0.0) + 1, 2), "none")
raw(f'tl.fromTo("#s7-art",{{opacity:0}},{{opacity:1,duration:3,ease:"sine.inOut",immediateRender:false}},{at(7, 0.0)});')
raw(f'tl.to("#s7-art",{{opacity:.12,duration:.6,ease:"power1.out"}},{round(t_dim7, 3)});')
rise("#s7-head", at(7, 0.4))
out("#s7-head", t_dim7, 0.3)
rise("#s7-sent", cue(7, "She dropped"))
land("#s7-a1", cue(7, "You need to know"))
pop("#s7-d1", cue(7, "You need to know") + 0.2)
draw("#s7-l1", cue(7, "You need to know") + 0.3, 320)
pop("#s7-p1", cue(7, "You need to know") + 0.8)
for s_ in ["#s7-sent", "#s7-d1", "#s7-l1", "#s7-p1"]:
    out(s_, t_dim7, 0.25)
_tw("#s7-rec", {"opacity": 0, "y": 80}, {"opacity": 1, "y": 0}, cue(7, "The recipe"), 0.55, "igOut")
pop("#s7-e1", cue(7, "The recipe") + 0.4)
pop("#s7-e2", cue(7, "The recipe") + 0.55)
pop("#s7-e3", cue(7, "The recipe") + 0.7)
land("#s7-a2", cue(7, "Now you need") - 0.3)
pop("#s7-need", cue(7, "Now you need") + 0.3)
out("#s7-rec", cue(7, "To predict well") - 0.3, 0.25)
fade("#s7-sl", cue(7, "To predict well"), 0.3)
for i, key in enumerate(["grammar", "facts", "patterns of logic", "how people explain"]):
    pop(f"#s7-c{i+1}", cue(7, key) if key != "grammar" else cue(7, "grammar"))
rise("#s7-b", cue(7, "Nobody programmed"))

# ---- 8. Illustration: manners school, then the comparison
scene(8, """
  <div class="art" id="s8-art"><img src="assets/manners.png" alt=""/>
    <svg class="ig-pointer" viewBox="0 0 1920 1080" style="left:0;top:0;width:1920px;height:1080px">
      <circle id="s8-d1" cx="560" cy="640" r="12"/><path id="s8-l1" d="M560 640 V420 H470" style="stroke-dasharray:320"/>
      <rect id="s8-ring" class="ringrect" x="1030" y="540" width="330" height="200" rx="26"/>
      <path id="s8-l2" d="M1195 540 V470" style="stroke-dasharray:80"/></svg>
    <div class="ig-callout" style="left:150px;top:385px"><span class="ig-pill" id="s8-p1">Examples of great answers</span></div>
    <div class="ig-callout" style="left:960px;top:400px"><span class="ig-pill ig-pill--o" id="s8-p2">Rated by people</span></div>
  </div>
  <div class="s8-top"></div>
  <div class="s8-head" id="s8-head"><span class="ig-kicker"><span class="ig-kicker-dot"></span>Step 2</span><h1 class="ig-h">Taught <span class="ig-em-o">manners.</span></h1></div>
  <div class="ig-safe ig-center s8-cmp" id="s8-cmp"><div class="ig-compare">
    <div class="ig-box" id="s8-b1"><span class="ig-label">Raw text predictor</span><p class="ig-body-lg">Continues random internet text</p></div>
    <div><svg class="ig-arrow" viewBox="0 0 240 120"><path id="s8-arr" d="M20 60 H214 M172 20 L216 60 L172 100" style="stroke-dasharray:340"/></svg>
      <div class="ig-arrow-label ig-label-sm ig-em-c" id="s8-al">trained</div></div>
    <div class="ig-box ig-box--c" id="s8-b2"><span class="ig-label">Helpful assistant</span><p class="ig-body-lg">The one you chat with</p></div>
  </div></div>""", "plain")
t_dim8 = cue(8, "That's the difference") - 0.5
_tw("#s8-art", {"scale": 1.0}, {"scale": 1.1}, at(8, 0.0), round(t_dim8 - at(8, 0.0) + 1, 2), "none")
raw(f'tl.fromTo("#s8-art",{{opacity:0}},{{opacity:1,duration:3,ease:"sine.inOut",immediateRender:false}},{at(8, 0.0)});')
raw(f'tl.to("#s8-art",{{opacity:.1,duration:.6,ease:"power1.out"}},{round(t_dim8, 3)});')
pop("#s8-head .ig-kicker", at(8, 0.3))
rise("#s8-head h1", at(8, 0.5))
pop("#s8-d1", cue(8, "People show"))
draw("#s8-l1", cue(8, "People show") + 0.1, 320)
pop("#s8-p1", cue(8, "People show") + 0.6)
draw("#s8-ring", cue(8, "rate its"), 1100, 0.8)
draw("#s8-l2", cue(8, "rate its") + 0.5, 80, 0.3)
pop("#s8-p2", cue(8, "rate its") + 0.7)
for s_ in ["#s8-d1", "#s8-l1", "#s8-p1", "#s8-ring", "#s8-l2", "#s8-p2"]:
    out(s_, t_dim8, 0.25)
raw(f'tl.to("#s8-head",{{y:-30,scale:.8,duration:.6,ease:"igIO"}},{round(t_dim8, 3)});')
slide_in("#s8-b1", t_dim8 + 0.3, -160)
draw("#s8-arr", t_dim8 + 0.9, 340)
fade("#s8-al", t_dim8 + 1.3, 0.3)
slide_in("#s8-b2", t_dim8 + 1.4, 160)

# ---- 9. Guessing != knowing, the Venn, then the payoff: a wrong answer with the same bars
st9 = [("Sydney.", [("Sydney.", 61), ("Canberra.", 35), ("Melbourne.", 4)])]
p9, w9, _ = predictor_steps("wr", st9, cue(9, "But sometimes") + 1.4, [2.6], show_pct=True, keep_last=True)
scene(9, f"""
  <div class="ig-safe ig-center s9-state" id="s9-state">
    <h1 class="ig-hxl" id="s9-a">Guessing <span class="ig-em-o">&ne;</span> Knowing</h1>
    <p class="ig-body-lg ig-muted" id="s9-sub" style="margin-top:40px">It predicts what <i>sounds</i> right. It doesn't look it up.</p></div>
  <div class="ig-safe ig-center s9-v" id="s9-v"><div class="ig-venn">
    <div class="circle a" id="s9-c1"><span class="ig-label">Sounds right</span></div>
    <div class="circle b" id="s9-c2"><span class="ig-label">Is right</span></div>
    <div class="overlap" id="s9-ov"><span class="ig-label" style="color:var(--ink)">Paris &#10003;</span></div></div></div>
  <div class="chatwin s9-chat" id="s9-chat">
    <div class="ig-bubble ig-bubble--me cw-q" id="s9-q">What's the capital of Australia?</div>
    <div class="ig-bubble ig-bubble--ai cw-a" id="s9-ans"><span class="reply">It's {w9}</span></div>
    <div class="pr-dock">{p9}</div>
  </div>
  <div class="ig-stamp s9-stamp" id="s9-stamp">WRONG.</div>
  <div class="s9-truth" id="s9-truth"><span class="ig-label ig-dim">Actually:</span> <span class="ig-body-lg ig-em-c">Canberra</span></div>
  <div class="s9-note" id="s9-note"><p class="ig-body-lg">Same bars. <span class="ig-em-o">Same confidence.</span></p></div>""")
camera(9, 0.03)
rise("#s9-a", at(9, 0.3), 50)
rise("#s9-sub", cue(9, "Not looking"))
out("#s9-state", cue(9, "Most of the time") - 0.5, 0.25)
_seen.add("#s9-state")
slide_in("#s9-c1", cue(9, "Most of the time"), -160)
slide_in("#s9-c2", cue(9, "Most of the time") + 0.25, 160)
pop("#s9-ov", cue(9, "The capital"))
out("#s9-v", cue(9, "But sometimes") - 0.1, 0.25)
_tw("#s9-chat", {"opacity": 0, "y": 120}, {"opacity": 1, "y": 0}, cue(9, "But sometimes") + 0.1, 0.5, "igOut")
pop("#s9-q", cue(9, "But sometimes") + 0.4)
pop("#s9-ans", cue(9, "But sometimes") + 1.1)
rise("#s9-note", cue(9, "same confident") - 1.4)
slam("#s9-stamp", cue(9, "same confident"))
rise("#s9-truth", cue(9, "same confident") + 0.9)

# ---- 10. Next video teaser + end card with clean zones for YouTube's end-screen elements
scene(10, """
  <div class="ig-safe ig-center" id="s10-next">
    <span class="ig-kicker ig-kicker--cyan" id="s10-k"><span class="ig-kicker-dot"></span>Next video</span>
    <h1 class="ig-hxl" id="s10-t" style="margin-top:48px">Why AI lies with a<br/><span class="ig-em-o">straight face</span></h1>
    <p class="ig-body-lg ig-muted" id="s10-tease" style="margin-top:40px">It once made up a whole court case.</p></div>
  <div class="s10-end" id="s10-end">
    <h1 class="ig-signoff" id="s10-sign">I gotchu<b>.</b></h1>
    <p class="ig-body-lg ig-muted" id="s10-sub" style="margin-top:28px">Watch one of these next</p>
    <div class="ig-slot" id="s10-sl1" style="left:176px;top:500px;width:600px;height:338px"><span class="ig-label-sm" style="color:var(--cyan)">Next video</span></div>
    <div class="ig-slot ig-slot--round" id="s10-sl2" style="left:810px;top:520px;width:300px;height:300px"><span class="ig-label-sm" style="color:var(--orange)">Subscribe</span></div>
    <div class="ig-slot" id="s10-sl3" style="left:1144px;top:500px;width:600px;height:338px"><span class="ig-label-sm" style="color:var(--cyan)">Best for you</span></div>
  </div>""")
pop("#s10-k", at(10, 0.3))
rise("#s10-t", at(10, 0.5), 50)
rise("#s10-tease", cue(10, "Why AI makes") + 0.4)
t_g = cue(10, "I gotchu")
out("#s10-next", t_g - 0.35, 0.25)
_seen.add("#s10-next")
fade("#s10-end", t_g - 0.3, 0.1)
ignite("#s10-sign", t_g - 0.3)
rise("#s10-sub", t_g + 0.8)
for i in range(3):
    pop(f"#s10-sl{i+1}", t_g + 1.05 + i * 0.15)

# ---- progress rail (chapters) across the whole video
chapters = [("The trick", 1, 3), ("Your phone", 4, 5), ("How it's smart", 6, 8), ("Guessing ≠ knowing", 9, 10)]
chap_html = "".join(f'<span id="ch{i}">{name}</span>' for i, (name, _, _) in enumerate(chapters))
for i, (_, a, b) in enumerate(chapters):
    raw(f'tl.set("#ch{i}",{{className:"on"}},{T[a]["start"]});')
    raw(f'tl.set("#ch{i}",{{className:"done"}},{round(T[b]["start"] + T[b]["dur"], 3)});')
raw(f'tl.fromTo("#pfill",{{width:0}},{{width:1920,duration:{TOTAL},ease:"none"}},0);')
raw(f'tl.to("#rail",{{opacity:0,duration:.3}},{round(t_g - 0.4, 3)});')

# ================================================================ STYLES
def tokens_css():
    tk = json.load(open("ds/tokens.json"))
    out_ = [":root{"]
    for fam in ["color", "spacing", "radius", "shadow", "duration", "easing"]:
        for t in tk.get(fam, {}).get("tokens", []):
            v = t["value"]
            if isinstance(v, dict):
                v = list(v.values())[0]
            out_.append(f"--{t['name']}:{v};")
    out_.append('--font-display:"Archivo Black","Arial Black",sans-serif;--font-sans:Inter,"Helvetica Neue",Arial,sans-serif;}')
    return "".join(out_)


def bundle_css():
    css = open("ds/bundle.css").read()
    css = re.sub(r"@import url\([^)]*\);", "", css)
    css = css.split("/* =====================================================================\n   Motion.")[0]  # drop CSS animation classes
    css = css.replace("animation: ig-blink 1s steps(1) infinite, ig-out .01s linear 2.2s both;", "display:none;")
    css = css.replace("animation: ig-dot 1s var(--ig-ease-io) infinite;", "")
    return css


FONTS = "".join(
    f'@font-face{{font-family:Inter;font-weight:{w};src:url(assets/fonts/inter-latin-{w}-normal.woff2) format("woff2")}}'
    for w in (500, 600, 700, 800, 900)) + '@font-face{font-family:"Archivo Black";src:url(assets/fonts/archivo-black-latin-400-normal.woff2) format("woff2")}'

LOCAL = """
#root{position:relative}
.clip{position:absolute;inset:0}
.scene{overflow:hidden}
.cam{position:absolute;inset:0;transform-origin:50% 45%}
.scene.plain{background:var(--night)}
/* everything animated starts hidden; containers that are shown by their children stay visible */
.scene [id]{opacity:0}
.ch,.tw,.rw{display:none}
#s4 .ch,#s4 .tw,#s6 .ch,.scene .rw{opacity:1}
#s4 .k,#s4-phone,#s3-loop,#s1-chat .reply,.pr-dock{opacity:1}
#s6-card,#s7-soak,#s8-cmp,#s8-head,#s9-v,#s3-fill,#s6-hi,#s6 .box{opacity:1}
#s2-caret,#s3-caret{opacity:1}
/* chat window used by the predictor */
.chatwin{position:absolute;right:128px;top:150px;width:760px;padding:40px;border-radius:var(--radius-md);background:var(--surface);
  box-shadow:inset 0 0 0 2px var(--line),var(--lift);display:flex;flex-direction:column;gap:28px}
.chatwin.wide{position:relative;right:auto;top:auto;width:1200px}
.cw-head{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:800;color:var(--ink-muted);padding-bottom:20px;border-bottom:2px solid var(--line)}
.cw-dot{width:18px;height:18px;border-radius:50%;background:var(--cyan);box-shadow:0 0 14px var(--cyan)}
.chatwin .ig-bubble{max-width:none;font-size:40px}
.cw-q{align-self:flex-end}.cw-a{align-self:flex-start;min-height:52px}
.caret{color:var(--cyan);font-weight:400}
.pr-dock{position:relative;height:250px}
.pr-panel{position:absolute;left:0;right:0;top:0;display:flex;flex-direction:column;gap:14px;padding:22px 26px;border-radius:var(--radius-md);
  background:var(--night);box-shadow:inset 0 0 0 2px var(--line)}
.pr-row{display:grid;grid-template-columns:260px 1fr 110px;align-items:center;gap:22px;font-size:36px;font-weight:700;color:var(--ink-muted)}
.pr-row .bar{height:16px;border-radius:8px;background:var(--surface-raised);overflow:hidden}
.pr-row .bar i{display:block;height:100%;border-radius:8px;background:var(--ink-dim);transform-origin:left}
.pr-row .pct{font-size:30px;color:var(--ink-dim);text-align:right}
.pr-panel.lock .pr-row.win{color:var(--cyan);text-shadow:var(--glow-text-cyan)}
.pr-panel.lock .pr-row.win .bar i{background:var(--cyan);box-shadow:0 0 12px var(--cyan)}
.pr-panel.lock .pr-row.win .pct{color:var(--cyan)}
/* slide 1 */
.s1-left{position:absolute;left:128px;top:0;bottom:0;width:900px;display:flex;flex-direction:column;justify-content:center;gap:44px}
.s1-left .ln{display:block}
.qcard{position:absolute;left:128px;right:128px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:44px}
/* fill in the blank */
.blank-caret{position:absolute;left:50%;top:24px;bottom:24px;width:6px;margin-left:-3px;background:var(--cyan);border-radius:3px}
.ig-blank{min-width:360px}
.ig-guess .bar i{transform-origin:left}
.s2-note{margin-top:64px}
/* slide 3 loop */
.s3-loop{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px}
.loopsteps{display:flex;align-items:center;gap:18px}.loopsteps .arr{font-size:44px;color:var(--ink-dim)}
.s3-count{font-size:48px;font-weight:800}
.s3-loop .pr-dock{height:250px}
/* slide 4 phone */
.rig{position:absolute;left:40%;top:50%;width:620px;height:1040px;margin-left:-310px;margin-top:-520px}
.ig-phone.p4{left:0;top:0}
.p4 .thread{flex:1}.p4 .ig-bubble.in{align-self:flex-start;background:var(--surface-raised);border-bottom-left-radius:10px;border-bottom-right-radius:34px;font-size:32px}
.compose{margin:10px 22px;min-height:70px;border-radius:34px;box-shadow:inset 0 0 0 2px var(--line);padding:14px 24px;font-size:31px;font-weight:600;line-height:1.35;color:var(--ink)}
.caret2{color:var(--cyan);font-weight:400}
.suggbar{position:relative;height:70px;background:var(--night)}
.sset{position:absolute;inset:0;display:flex;align-items:center;opacity:0}
.sset span{flex:1;text-align:center;font-size:28px;font-weight:600;color:var(--ink-muted);border-right:2px solid var(--line)}
.sset span:last-child{border-right:none}.sset .mid{color:var(--cyan);font-weight:800}
.tap{position:absolute;left:50%;top:50%;width:130px;height:130px;margin:-65px 0 0 -65px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,122,26,.85) 0%,rgba(255,122,26,.35) 45%,rgba(255,122,26,0) 70%)}
.kb{background:var(--night);padding:12px 8px 30px;display:flex;flex-direction:column;gap:12px}
.krow{display:flex;justify-content:center;gap:7px}
.k{width:48px;height:64px;border-radius:10px;background:var(--surface-raised);color:var(--ink);font-size:27px;font-weight:600;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 0 var(--night-950)}
.k.fn{background:var(--surface);width:64px;font-size:24px}.k.w2{width:112px;font-size:22px}.k.space{width:250px;font-size:22px;color:var(--ink-muted)}
.s4-stamp{left:-20px;top:640px;font-size:96px;z-index:5}
.s4-label{position:absolute;right:128px;top:50%;margin-top:-170px;display:flex;flex-direction:column;align-items:flex-start;gap:30px}
.s4-out{position:absolute;right:128px;top:50%;margin-top:-120px;width:780px;display:flex;flex-direction:column;gap:24px}
/* illustration scenes */
.art{position:absolute;inset:0;transform-origin:50% 50%}
.art img{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover}
.ig-pointer .c,.ig-pointer path.c{stroke:var(--cyan)}
.s5-scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,9,24,.7) 0%,rgba(5,9,24,0) 30%,rgba(5,9,24,0) 70%,rgba(5,9,24,.85) 100%)}
.s5-scale{position:absolute;left:0;right:0;top:360px;text-align:center;font-family:var(--ig-display);font-size:200px;margin:0;color:var(--ink);text-shadow:var(--glow-text-orange)}
.s5-life{position:absolute;left:128px;top:110px}
.s6-head{position:absolute;left:128px;right:128px;top:96px;text-align:center;display:flex;flex-direction:column;gap:20px}
.morph{position:absolute;left:50%;top:470px;width:1100px;height:440px;margin-left:-550px;border-radius:var(--radius-md);background:var(--surface);box-shadow:var(--glow-cyan),var(--lift)}
.mc{position:absolute;inset:0;padding:44px 56px;display:flex;flex-direction:column;gap:30px;align-items:flex-start}
.code{font-family:"DejaVu Sans Mono",monospace;font-size:36px;line-height:1.6;color:var(--ink);white-space:pre}
.code .kw{color:var(--orange);font-style:normal}.code .n{color:var(--cyan);font-style:normal}
.form{width:100%;display:flex;flex-direction:column;gap:14px}
.fr{display:flex;justify-content:space-between;padding:18px 24px;border-radius:12px;box-shadow:inset 0 0 0 2px var(--line);font-size:34px;font-weight:600}
.fr.hi{box-shadow:inset 0 0 0 3px var(--cyan)}.fv{color:var(--cyan);font-weight:800}
.chk{display:flex;flex-direction:column;gap:18px}
.ck{display:flex;align-items:center;gap:24px;font-size:38px;font-weight:600}
.box{width:44px;height:44px;border-radius:10px;box-shadow:inset 0 0 0 3px var(--ink-dim)}
.box.on{background:var(--cyan);box-shadow:0 0 16px var(--cyan)}
.s6-auto{position:absolute;left:0;right:0;top:420px;text-align:center}
.s6-auto .ig-hxl{display:inline}
.caret3{color:var(--cyan)}
.s6-wild{position:absolute;left:0;right:0;top:0;bottom:0;display:flex;align-items:center;justify-content:center}
.s6-wild h1{position:relative;z-index:2}
#s6-w{display:inline-block}
.burst{position:absolute;left:50%;top:50%;width:1200px;height:1200px;margin:-600px 0 0 -600px;overflow:visible}
.burst path{stroke:var(--orange);stroke-width:10;stroke-linecap:round;stroke-dasharray:100}
.sentcard{position:absolute;left:128px;bottom:150px;display:flex;align-items:center;gap:32px;padding:30px 44px;border-radius:var(--radius-md);background:rgba(10,17,40,.88);box-shadow:inset 0 0 0 2px var(--line),var(--lift)}
.sentcard .ans{font-family:var(--ig-display);font-size:64px}
.recipe{position:absolute;left:50%;top:50%;width:1000px;margin:-330px 0 0 -500px;padding:52px 60px;border-radius:var(--radius-md);background:var(--surface);
  box-shadow:var(--glow-orange),var(--lift);display:flex;flex-direction:column;gap:26px;align-items:flex-start}
.eggs{display:flex;gap:30px}
.egg{display:block;width:92px;height:118px;border-radius:50% 50% 46% 46%/60% 60% 40% 40%;background:#f4f7ff;box-shadow:0 0 18px rgba(244,247,255,.35)}
.egg.miss{background:transparent;box-shadow:none;border:5px dashed var(--orange)}
.recipe .ans{font-family:var(--ig-display)}
.s7-soak{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:52px}
.s8-top{position:absolute;left:0;right:0;top:0;height:360px;background:linear-gradient(180deg,rgba(5,9,24,.85),rgba(5,9,24,0))}
.s8-head{position:absolute;left:0;right:0;top:80px;display:flex;flex-direction:column;align-items:center;gap:24px;transform-origin:50% 0}
.s8-cmp{padding-top:170px}
.ringrect{fill:none;stroke:var(--orange);stroke-width:8;stroke-dasharray:1100;filter:drop-shadow(0 0 12px rgba(255,122,26,.9))}
.ig-arrow path{stroke-dasharray:340}
.s9-state{justify-content:center}
.s9-v .ig-venn .circle{mix-blend-mode:normal}
.s9-chat{right:auto;left:50%;top:170px;width:1000px;margin-left:-500px}
.s9-stamp{left:930px;top:330px;font-size:100px;z-index:5}
.s9-truth{position:absolute;left:0;right:0;bottom:170px;text-align:center}
.s9-note{position:absolute;left:0;right:0;top:80px;text-align:center}
.s10-end{position:absolute;inset:0;text-align:center;padding-top:140px}
#s10-sign{opacity:0}
/* rail + bug */
#rail{position:absolute;left:0;right:0;bottom:0;height:88px;z-index:20}
#rail .chapters span.on{color:var(--cyan);text-shadow:var(--glow-text-cyan)}#rail .chapters span.done{color:var(--ink-muted)}
#pfill{position:absolute;left:0;bottom:0;height:12px;background:var(--cyan);box-shadow:0 0 16px rgba(34,211,238,.8)}
#bug{bottom:120px;z-index:20}
#crops{z-index:19}
"""

html = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<script src="assets/gsap.min.js"></script><script src="assets/CustomEase.min.js"></script>
<style>{FONTS}{tokens_css()}{bundle_css()}{LOCAL}</style></head>
<body>
<div id="root" class="ig-frame" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
  <audio id="vo" src="assets/mix.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
  {''.join(S)}
  <div class="ig-crops" id="crops"><i></i><i></i><i></i><i></i></div>
  <div class="ig-wordmark" id="bug">igotchu<b>.</b></div>
  <div class="ig-progress" id="rail"><div class="chapters">{chap_html}</div>
    <div class="track"><div class="seg"></div><div class="seg"></div><div class="seg"></div><div class="seg"></div></div><div id="pfill"></div></div>
</div>
<script>
  gsap.registerPlugin(CustomEase);
  CustomEase.create("igOut","0.16,1,0.3,1");
  CustomEase.create("igPop","0.34,1.56,0.64,1");
  CustomEase.create("igSlam","0.7,0,0.84,0");
  CustomEase.create("igIO","0.65,0,0.35,1");
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
{chr(10).join('  ' + a for a in A)}
  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
</body></html>
"""
open("video/index.html", "w").write(html)
print(f"wrote video/index.html: {TOTAL}s, {len(A)} timeline entries")


# ================================================================ AUDIO MIX: voice + SFX events
import array
import subprocess
import wave

GAIN = {"pop": 0.28, "click": 0.22, "whoosh": 0.35, "thud": 0.7, "ding": 0.3}
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/vo/voiceover.mp3", "-ac", "1", "-ar", "44100", "sfx/_voice.wav"], check=True)
with wave.open("sfx/_voice.wav") as w:
    voice = array.array("h", w.readframes(w.getnframes()))
n_total = int((TOTAL + 1) * 44100)
mix = [0.0] * n_total
for i, v in enumerate(voice):
    mix[i] = float(v)
clips = {}
for name in GAIN:
    with wave.open(f"sfx/{name}.wav") as w:
        clips[name] = array.array("h", w.readframes(w.getnframes()))
last = {}
for t, name in sorted(SFX):
    if t - last.get(name, -9) < 0.09:  # thin out bursts of identical sounds
        continue
    last[name] = t
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
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "sfx/_mix.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2", "-b:a", "192k", "video/assets/mix.mp3"], check=True)
print(f"mixed {len(SFX)} sound events")
