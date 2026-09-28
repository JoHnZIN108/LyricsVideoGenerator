"""igotchu Script 7, "Anatomy of a good prompt": HyperFrames build in the student-kit structure.

Kit conventions followed (nateherkai/hyperframes-student-kit, make-a-video + video-storytelling):
- root video/index.html + one sub-composition per slide in video/compositions/sNN.html (ids s01..s10,
  scoped CSS, IIFE, paused local-time timeline registered on window.__timelines, slot pin)
- one persistent world (video/compositions/world.html, full length): the Instrument panel, header strip,
  and the four block keys (Task, Context, Rules, Example) that light up as the video fills them in
- spotlight rule: one key at full strength, lit keys at .6, unlit sockets at .3
- data-anchor per slide + video/assets/transcript.json (phrase starts from our free aligner) for the
  kit's validate-beat-sync.mjs

Built here because the kit lacks them: Instrument (Type Lab) components, a screenshot viewer with a
camera that eases onto the quoted lines, and word-by-word highlighting synced to the voice (OCR boxes).
Look: igotchu Type Lab "Instrument" style, Condensed Grotesque type (Bricolage 75 / DM Sans / JetBrains Mono).
"""
import json
import os
import re
import shutil

T = {i + 1: s for i, s in enumerate(json.load(open("timing.json")))}
SL = {s["n"]: s for s in json.load(open("slides.json"))}
SEG = {int(k): v for k, v in json.load(open("segments.json")).items()}
OCR = json.load(open("ocr/words.json"))
TOTAL = round(T[10]["start"] + T[10]["dur"], 3)
XO = 0.35  # scene crossover
IMG = {"01": (1232, 958), "02": (1495, 812), "03": (1568, 607), "04": (1547, 784), "05": (1330, 758)}
DARK = {"01", "02", "03", "04"}  # screenshots in dark mode (highlight blends differently)


# ---------------------------------------------------------------- timing (free aligner, as in v4)
def at(n, rel):
    return round(T[n]["start"] + rel, 3)


_ALIGN = {}


def _align(n):
    if n in _ALIGN:
        return _ALIGN[n]
    text = SL[n]["text"]
    cuts = sorted(set([0] + [m.end() for m in re.finditer(r"[,.?!:;…]+[\"”']?\s+", text)] + [len(text)]))
    ph = [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)]
    segs = SEG[n]
    rate = sum(e - s for s, e in segs) / len(text)
    P, M = len(ph), len(segs)
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
                    if c < best.get((i + k, j + m), (float("inf"),))[0]:
                        best[(i + k, j + m)] = (c, (i, j))
    anchors, node = [], (P, M)
    while node != (0, 0):
        i0, j0 = best[node][1]
        s0, e0 = segs[j0][0], segs[node[1] - 1][1]
        c_start, c_end = ph[i0][0], ph[node[0] - 1][1]
        for q in range(i0, node[0]):
            anchors.append((ph[q][0], s0 + (e0 - s0) * (ph[q][0] - c_start) / max(1, c_end - c_start)))
        node = (i0, j0)
    _ALIGN[n] = sorted(anchors)
    return _ALIGN[n]


def time_at_char(n, i):
    text = SL[n]["text"]
    anchors = _align(n)
    k = max(q for q in range(len(anchors)) if anchors[q][0] <= i)
    c0, t0 = anchors[k]
    c1, t1 = anchors[k + 1] if k + 1 < len(anchors) else (len(text), SEG[n][-1][1])
    return at(n, t0 + (t1 - t0) * (i - c0) / max(1, c1 - c0))


def cue(n, phrase, off=0.0, nth=0):
    """Absolute time when `phrase` starts in slide n (interpolated inside a phrase)."""
    text = SL[n]["text"]
    i = -1
    for _ in range(nth + 1):
        i = text.find(phrase, i + 1)
    if i < 0:
        raise KeyError(f"slide {n}: {phrase!r}")
    return round(time_at_char(n, i) + off, 3)
    anchors = _align(n)
    k = max(q for q in range(len(anchors)) if anchors[q][0] <= i)
    c0, t0 = anchors[k]
    c1, t1 = anchors[k + 1] if k + 1 < len(anchors) else (len(text), SEG[n][-1][1])
    return at(n, t0 + (t1 - t0) * (i - c0) / max(1, c1 - c0) + off)


def end_of(n):
    return round(T[n]["start"] + T[n]["dur"], 3)


# ---------------------------------------------------------------- per-composition timeline builder
SFX = []
MOTION = []


class Comp:
    def __init__(self, cid, start, dur):
        self.cid, self.start, self.dur = cid, round(start, 3), round(dur, 3)
        self.A, self._seen = [], set()

    def L(self, t):
        return round(t - self.start, 3)

    def tw(self, sel, frm, to, t, dur, ease="igOut"):
        v = {**to, "duration": round(dur, 3), "ease": ease}
        if sel in self._seen:
            v["immediateRender"] = False
        self._seen.add(sel)
        self.A.append(f"tl.fromTo({json.dumps(sel)},{json.dumps(frm)},{json.dumps(v)},{self.L(t)});")
        MOTION.append((t, t + dur))

    def to(self, sel, props, t, dur, ease="igIO"):
        v = {**props, "duration": round(dur, 3), "ease": ease}
        self.A.append(f"tl.to({json.dumps(sel)},{json.dumps(v)},{self.L(t)});")
        MOTION.append((t, t + dur))

    def set(self, sel, props, t):
        self.A.append(f"tl.set({json.dumps(sel)},{json.dumps(props)},{self.L(t)});")
        MOTION.append((t, t + 0.05))

    def raw(self, js, t=None, dur=0.3):
        self.A.append(js)
        if t is not None:
            MOTION.append((t, t + dur))

    # named moves (v4 motion system)
    def rise(self, sel, t, y=40, dur=0.55):
        self.tw(sel, {"opacity": 0, "y": y}, {"opacity": 1, "y": 0}, t, dur, "igOut")

    def settle(self, sel, t, dur=0.5, sound=None):
        if sound:
            SFX.append((t, sound))
        self.tw(sel, {"opacity": 0, "scale": 0.94, "y": 14}, {"opacity": 1, "scale": 1, "y": 0}, t, dur, "igSettle")

    def snap(self, sel, t, sound="pop"):
        if sound:
            SFX.append((t, sound))
        self.tw(sel, {"opacity": 0, "y": 34, "scale": 0.96}, {"opacity": 1, "y": 0, "scale": 1}, t, 0.45, "igSnap")

    def fade(self, sel, t, dur=0.4):
        self.tw(sel, {"opacity": 0}, {"opacity": 1}, t, dur, "none")

    def out(self, sel, t, dur=0.3):
        self.tw(sel, {"opacity": 1, "y": 0}, {"opacity": 0, "y": -18}, t, dur, "igIn")

    def pulse(self, sel, t, s=1.06):
        self.A.append(f'tl.fromTo({json.dumps(sel)},{{scale:1}},{{keyframes:[{{scale:{s},duration:.18}},{{scale:1,duration:.32}}],ease:"sine.inOut",immediateRender:false}},{self.L(t)});')
        MOTION.append((t, t + 0.5))

    def press(self, sel, t):
        """Key press: pushes down like a real key."""
        SFX.append((t, "click"))
        self.A.append(f'tl.fromTo({json.dumps(sel)},{{y:0}},{{keyframes:[{{y:10,duration:.09}},{{y:0,duration:.22}}],ease:"sine.out",immediateRender:false}},{self.L(t)});')
        MOTION.append((t, t + 0.31))

    def slam(self, sel, t):
        SFX.append((t + 0.26, "thud"))
        self.tw(sel, {"opacity": 0, "rotation": -12, "scale": 1.8}, {"opacity": 1, "rotation": -7, "scale": 1}, t, 0.28, "igSlam")
        self.A.append(f'tl.to({json.dumps(sel)},{{keyframes:[{{x:-8,y:5,duration:.07}},{{x:6,y:-3,duration:.07}},{{x:0,y:0,duration:.07}}],ease:"none"}},{self.L(t + 0.28)});')

    def show(self, sel, t, disp="inline"):
        self.A.append(f'tl.set({json.dumps(sel)},{{display:"{disp}"}},{self.L(t)});')

    def blink(self, sel, t0, t1):
        n = int((t1 - t0) / 0.5)
        if n > 0:
            self.A.append(f'tl.fromTo({json.dumps(sel)},{{opacity:1}},{{opacity:0,duration:.5,ease:"steps(1)",repeat:{n - 1},yoyo:true,immediateRender:false}},{self.L(t0)});')

    def typeon(self, prefix, n_chars, t0, cps=22, sound=True):
        for i in range(n_chars):
            t = t0 + i / cps
            self.show(f"#{prefix}{i}", t)
            if sound and i % 2 == 0:
                SFX.append((t, "click"))
        MOTION.append((t0, t0 + n_chars / cps))
        return t0 + n_chars / cps


def chars(prefix, text):
    return "".join(f'<span class="ch" id="{prefix}{i}">{"&nbsp;" if c == " " else c}</span>' for i, c in enumerate(text))


# ---------------------------------------------------------------- screenshot viewer + word highlighter
VW, VH = 1440, 690  # viewer size (px) for single-screenshot slides


def letters(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("|", "i"))


def find_words(shot, phrase):
    """Indices of the OCR words that spell `phrase` (robust to OCR merges like 'anurse')."""
    W = OCR[shot]
    cat, own = "", []
    for idx, w in enumerate(W):
        l = letters(w["t"])
        cat += l
        own += [idx] * len(l)
    p = letters(phrase)
    i = cat.find(p)
    if i < 0:
        raise KeyError(f"{shot}: {phrase!r} not found in OCR")
    return sorted(set(own[i:i + len(p)]))


def box(shot, idxs, pad=10):
    W = OCR[shot]
    x0 = min(W[i]["x"] for i in idxs) - pad
    y0 = min(W[i]["y"] for i in idxs) - pad
    x1 = max(W[i]["x"] + W[i]["w"] for i in idxs) + pad
    y1 = max(W[i]["y"] + W[i]["h"] for i in idxs) + pad
    return x0, y0, x1, y1


class Viewer:
    """A device screen showing a real screenshot. The camera (.vcam) eases onto regions; highlights sit in
    image coordinates so they stay glued to the words while zooming."""

    def __init__(self, comp, vid, shot, w=VW, h=VH):
        self.c, self.vid, self.shot, self.w, self.h = comp, vid, shot, w, h
        self.iw, self.ih = IMG[shot]
        self.marks = []
        self.fit = min(w / self.iw, h / self.ih)

    def view_of(self, region=None, pad=60, max_s=2.3):
        if region is None:
            s = self.fit
            cx, cy = self.iw / 2, self.ih / 2
        else:
            x0, y0, x1, y1 = region
            s = min(self.w / (x1 - x0 + 2 * pad), self.h / (y1 - y0 + 2 * pad), max_s)
            s = max(s, self.fit)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        x = self.w / 2 - cx * s
        y = self.h / 2 - cy * s
        # keep the image edge from sliding into view when possible
        if self.iw * s >= self.w:
            x = min(0, max(self.w - self.iw * s, x))
        if self.ih * s >= self.h:
            y = min(0, max(self.h - self.ih * s, y))
        return {"x": round(x, 1), "y": round(y, 1), "scale": round(s, 4)}

    def start(self, region=None, t=None):
        self.c.set(f"#{self.vid} .vcam", self.view_of(region), t if t is not None else self.c.start)

    def zoom(self, region, t, dur=1.2, pad=60, max_s=2.3):
        SFX.append((t, "whoosh_s"))
        self.c.to(f"#{self.vid} .vcam", self.view_of(region, pad, max_s), t, dur, "igIO")

    def drift(self, t, dur):
        """Slow push while holding on a region: the frame never sits dead still."""
        self.c.A.append(f'tl.fromTo("#{self.vid} .vdrift",{{scale:1}},{{scale:1.035,duration:{round(dur, 2)},ease:"sine.inOut",immediateRender:false}},{self.c.L(t)});')

    def sweep(self, phrase, t0, t1, color):
        """Highlighter sweeps across each word of `phrase` between t0 and t1, in reading order."""
        idxs = find_words(self.shot, phrase)
        W = OCR[self.shot]
        lens = [max(1, len(letters(W[i]["t"]))) for i in idxs]
        tot = sum(lens)
        t = t0
        first = len(self.marks)
        for i, ln in zip(idxs, lens):
            d = (t1 - t0) * ln / tot
            w = W[i]
            mid = f"{self.vid}-m{len(self.marks)}"
            self.marks.append(f'<i class="hl {color}" id="{mid}" style="left:{w["x"] - 5}px;top:{w["y"] - 7}px;width:{w["w"] + 12}px;height:{w["h"] + 14}px"></i>')
            self.c.tw(f"#{mid}", {"scaleX": 0, "opacity": 1}, {"scaleX": 1, "opacity": 1}, t, max(0.08, d * 0.9), "none")
            t += d
        SFX.append((t0, "tick"))
        return list(range(first, len(self.marks)))

    def mark_ids(self, ids):
        return ",".join(f"#{self.vid}-m{i}" for i in ids)

    def html(self, cls=""):
        mode = "dark" if self.shot in DARK else "light"
        return (f'<div class="viewer {mode} {cls}" id="{self.vid}" style="width:{self.w}px;height:{self.h}px">'
                f'<div class="vdrift"><div class="vcam" style="width:{self.iw}px;height:{self.ih}px">'
                f'<img src="assets/screens/{self.shot}.png" alt=""/>{"".join(self.marks)}</div></div></div>')


# ================================================================ WORLD (persistent, full length)
world = Comp("world", 0, TOTAL)
KEYS = [("01", "The task", "g"), ("02", "The context", "b"), ("03", "The rules", "y"), ("04", "What good looks like", "p")]
HERO = [(128 + i * (370 + 61.33), 420) for i in range(4)]
RAIL_S = 0.45
RAIL = [(96, 150 + i * 190) for i in range(4)]


def key_state(i, state, t, dur=0.35):
    """Spotlight rule: 'spot' 1.0, 'lit' .6, 'off' .3 (socket not filled yet)."""
    op = {"spot": 1, "lit": 0.62, "off": 0.3}[state]
    world.to(f"#k{i}", {"opacity": op}, t, dur, "none")
    world.set(f"#k{i}-led", {"className": "in-led on" + ({"b": " b", "y": " y"}.get(KEYS[i - 1][2], "")) if state != "off" else "in-led"}, t)


def layout(kind, t, dur=0.9):
    for i in range(4):
        hx, hy = HERO[i]
        if kind == "hero":
            world.to(f"#k{i+1}", {"x": 0, "y": 0, "scale": 1}, t + i * 0.04, dur, "igIO")
        elif kind == "rail":
            rx, ry = RAIL[i]
            world.to(f"#k{i+1}", {"x": rx - hx, "y": ry - hy, "scale": RAIL_S}, t + i * 0.04, dur, "igIO")
        elif kind == "gone":
            world.to(f"#k{i+1}", {"y": 700, "opacity": 0}, t + i * 0.05, 0.6, "igIn")


keys_html = "".join(
    f'<div class="key" id="k{i+1}" style="left:{HERO[i][0]:.1f}px;top:{HERO[i][1]}px"><div class="in-key in-key--{c} kb" id="kb{i+1}">'
    f'<span class="num">{n}<i class="in-led" id="k{i+1}-led"></i></span><span class="lab">{lab}</span></div></div>'
    for i, (n, lab, c) in enumerate(KEYS))
tags = "".join(f'<div class="in-silk tag" id="tag{n}"><i class="in-led on"></i><i class="in-led"></i><i class="in-led"></i><span>Slide {n:02d}</span></div>' for n in range(1, 11))
world_html = f"""
<i class="in-screw" style="left:36px;top:36px"></i><i class="in-screw" style="right:36px;top:36px"></i>
<i class="in-screw" style="left:36px;bottom:36px"></i><i class="in-screw" style="right:36px;bottom:36px"></i>
<div class="in-silk" style="left:96px;top:44px">igotchu / Ep 07 &mdash; Anatomy of a prompt</div>
{tags}
<div class="rack">{keys_html}</div>
<div class="chap" id="chap"></div>
<div id="pline"></div><div id="pfill"></div>"""
for n in range(1, 11):
    world.set(f"#tag{n}", {"display": "flex"}, T[n]["start"])
    world.set(f"#tag{n}", {"display": "none"}, end_of(n))
world.A.append(f'tl.fromTo("#pfill",{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:"none"}},0);')

# key choreography, slide by slide (the open loop: 4 empty sockets, filled one per section)
for i in range(1, 5):
    world.set(f"#k{i}", {"opacity": 0.3}, 0)
t4 = cue(1, "four small parts")
for i in range(4):
    world.pulse(f"#kb{i+1}", t4 + 0.25 + i * 0.18, 1.05)
    world.to(f"#k{i+1}", {"opacity": 1}, t4 + 0.25 + i * 0.18, 0.2, "none")
    SFX.append((t4 + 0.25 + i * 0.18, "click"))
t_one = cue(1, "Most people only use one")
for i in range(2, 5):
    key_state(i, "off", t_one + 0.3)
key_state(1, "spot", t_one + 0.3)
world.press("#kb1", t_one + 0.3)
for i in range(4):
    world.pulse(f"#kb{i+1}", cue(1, "one block at a time") + i * 0.22, 1.05)
layout("rail", at(2, 0.1))
world.pulse("#kb1", cue(2, "you only gave it one block"), 1.08)
# 3: task
world.press("#kb1", cue(3, "Block one"))
for i in range(2, 5):
    world.pulse(f"#kb{i}", cue(3, "the other three") + 0.3 + (i - 2) * 0.2, 1.08)
# 4-6: each new block presses in and takes the spotlight
for n, k in ((4, 2), (5, 3), (6, 4)):
    tb = cue(n, "Block")
    for j in range(1, k):
        key_state(j, "lit", tb)
    key_state(k, "spot", tb + 0.1)
    world.press(f"#kb{k}", tb + 0.1)
    SFX.append((tb + 0.25, "ding"))
# 7: all four lit; "missing a block. Usually context"
t_all = at(7, 0.3)
for i in range(1, 5):
    key_state(i, "spot", t_all + i * 0.12)
    world.press(f"#kb{i}", t_all + i * 0.12)
t_uc = cue(7, "Usually context")
world.pulse("#kb2", t_uc, 1.12)
world.pulse("#kb2", t_uc + 0.6, 1.12)
# 8: back to empty sockets, then "All four blocks, filled in" lights them in a run
for i in range(1, 5):
    key_state(i, "off", at(8, 0.2))
t_ff = cue(8, "All four blocks")
for i in range(1, 5):
    key_state(i, "spot", t_ff + 0.1 + i * 0.14, 0.15)
    world.press(f"#kb{i}", t_ff + 0.1 + i * 0.14)
# 9: recap, keys come back to the hero row and press one per phrase
layout("hero", at(9, 0.0))
for i in range(1, 5):
    key_state(i, "off", at(9, 0.0))
for i, ph in enumerate(["The task", "The context", "The rules", "And an example"]):
    tk = cue(9, ph)
    key_state(i + 1, "spot", tk)
    world.press(f"#kb{i+1}", tk)
t_dn = cue(9, "You don't need all four")
for i in range(2, 5):
    key_state(i, "off", t_dn + 0.2)
t_gb = cue(9, "give it the blocks")
for i in range(2, 5):
    key_state(i, "spot", t_gb + (i - 2) * 0.12, 0.15)
    world.press(f"#kb{i}", t_gb + (i - 2) * 0.12)
# 10: keys leave for the end card
layout("gone", at(10, 0.0))

# chapter name, shown for 2.5 s when it changes
CHAPS = [(1, "The four blocks"), (3, "Block 1 · Task"), (4, "Block 2 · Context"), (5, "Block 3 · Rules"),
         (6, "Block 4 · Example"), (7, "Before vs after"), (8, "The cheat code"), (9, "Recap")]

# ================================================================ SCENES
SCENES = {}


def scene(n):
    s = T[n]["start"] - (XO if n > 1 else 0)
    d = T[n]["dur"] + (XO if n > 1 else 0)
    c = Comp(f"s{n:02d}", s, d)
    SCENES[n] = c
    if n > 1:
        SFX.append((s + 0.05, "whoosh"))
        c.tw(".sc", {"opacity": 0, "x": 90}, {"opacity": 1, "x": 0}, s, 0.5, "igOut")
    if n < 10:
        c.to(".sc", {"opacity": 0, "x": -70}, T[n + 1]["start"] - XO + 0.05, 0.3, "igIn")
    c.A.append(f'tl.fromTo(".sc-cam",{{scale:1}},{{scale:1.03,duration:{round(d, 2)},ease:"sine.inOut"}},0);')
    return c


HTML = {}

# ---- 1. Title + the four empty sockets (keys live in the world layer)
c = scene(1)
HTML[1] = f"""
<h1 class="in-h hd1" id="s1-h">Anatomy of<br/>a prompt<span class="in-dot"></span></h1>
<p class="in-body sub1" id="s1-sub">Useless answer <b class="arr">&rarr;</b> brilliant answer</p>
<div class="in-silk note1" id="s1-n1">4 blocks &middot; most people use <b style="color:var(--pink)">1</b></div>
<div class="in-screen scr1" id="s1-scr">&gt;&nbsp;<span class="in-cursor" id="s1-cur"></span></div>
<div class="better1" id="s1-better"><span class="in-silk" style="position:static">Answer quality</span><div class="bar1"><i id="s1-bf"></i></div></div>
<div class="in-key in-key--p cheat1" id="s1-cheat"><span class="num">??<i class="in-led on"></i></span><span class="lab">+ a cheat code</span></div>"""
c.set("#s1-h", {"opacity": 1}, 0)
c.tw("#s1-h", {"opacity": 0, "y": 30, "filter": "blur(12px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, 0.05, 0.8, "igOut")
c.rise("#s1-sub", cue(1, "useless AI answer") + 0.4)
c.pulse("#s1-sub .arr", cue(1, "and a brilliant one"), 1.3)
c.snap("#s1-n1", cue(1, "Most people only use one") + 0.4)
c.out("#s1-sub", cue(1, "We're going to build") - 0.2)
c.snap("#s1-scr", cue(1, "We're going to build"), "click")
c.blink("#s1-cur", cue(1, "We're going to build"), cue(1, "And at the end"))
t_ob = cue(1, "one block at a time")
c.snap("#s1-better", cue(1, "watch the answer get better"))
c.tw("#s1-bf", {"scaleX": 0.08}, {"scaleX": 1}, cue(1, "get better with every block"), 1.6, "igOut")
c.out("#s1-better", cue(1, "And at the end") - 0.1)
c.snap("#s1-cheat", cue(1, "a trick that basically"))
c.pulse("#s1-cheat", cue(1, "writes the prompt for you"), 1.06)

# ---- 2. The bad prompt and the petrol-station answer (screenshot 1)
c = scene(2)
v2 = Viewer(c, "v2", "01", 1440, 700)
p2 = "Write a birthday message for my mum."
HTML_p2 = chars("s2-c", p2)
c.snap("#s2-scr", cue(2, "Here's where most people start"), "click")
tp = c.typeon("s2-c", len(p2), cue(2, '"Write a birthday'), 26)
c.blink("#s2-cur", cue(2, "Here's where"), cue(2, "And you get back"))
t_back = cue(2, "And you get back")
c.settle("#v2", t_back - 0.5, 0.6, "pop")
v2.start(None, t_back - 0.5)
t_q = cue(2, '"Thank you for')
reg = box("01", find_words("01", "Thank you for the love, the patience, and all the times you believed in me before I believed in myself."), 16)
v2.zoom(reg, t_q - 0.9, 1.1, 40, 1.35)
ids = v2.sweep("Thank you for the love, the patience, and all the times you believed in me before I believed in myself.", t_q, cue(2, "It's fine") - 0.25, "c")
v2.drift(t_q + 0.2, 6)
t_fine = cue(2, "It's fine")
v2.zoom(None, t_fine + 0.2, 1.2)
c.slam("#s2-stamp", cue(2, "petrol station") - 0.1)
c.snap("#s2-any", cue(2, "It could be for anyone's mum"))
c.pulse("#s2-any", cue(2, "only gave it one block"), 1.06)
HTML[2] = f"""
<div class="in-screen scr2" id="s2-scr">&gt;&nbsp;{HTML_p2}<span class="in-cursor" id="s2-cur"></span></div>
<div class="vwrap" style="left:384px;top:300px">{v2.html()}</div>
<div class="in-stamp stamp2" id="s2-stamp">GENERIC.</div>
<div class="in-silk any" id="s2-any">Could be anyone&rsquo;s mum &middot; <b style="color:var(--graphite)">1 of 4</b> blocks</div>"""

# ---- 3. Block 1: the task
c = scene(3)
p3 = "Write a birthday message"
HTML[3] = f"""
<div class="bh" id="s3-bh"><span class="num-b">Block 01</span><h2 class="in-h bt">The task</h2><p class="in-body bs">What you want it to do.</p></div>
<div class="in-screen scr3" id="s3-scr"><span class="ln3">&gt;&nbsp;<span class="task-hl" id="s3-t">{p3}</span><span class="rest">&nbsp;for my mum.</span></span></div>
<div class="chip3" id="s3-ev"><i class="in-led on"></i>Everybody gets this block</div>
<div class="ghosts3" id="s3-gh"><div class="gk b">02</div><div class="gk y">03</div><div class="gk p">04</div><div class="in-silk ghl">the other three make the magic</div></div>"""
c.rise("#s3-bh", at(3, 0.1))
c.snap("#s3-scr", cue(3, "What you want it to do"), "click")
c.tw("#s3-t", {"backgroundSize": "0% 100%"}, {"backgroundSize": "100% 100%"}, cue(3, '"Write a birthday message" is'), 0.9, "igOut")
SFX.append((cue(3, '"Write a birthday message" is'), "tick"))
c.snap("#s3-ev", cue(3, "Everybody gets this block"))
c.settle("#s3-gh", cue(3, "It's the other three"), 0.5)
for i, gk in enumerate(["b", "y", "p"]):
    c.pulse(f"#s3-gh .gk.{gk}", cue(3, "make the magic") + i * 0.18, 1.15)


# ---- helper for the block slides 4-6: headline + viewer + two sweeps
def block_head(n, num, title, sub, color):
    return (f'<div class="bh" id="s{n}-bh"><span class="num-b {color}">Block {num}</span><h2 class="in-h bt">{title}</h2>'
            f'<p class="in-body bs">{sub}</p></div>')


# ---- 4. Block 2: the context (screenshot 2)
c = scene(4)
v4 = Viewer(c, "v4", "02", 1440, 640)
c.rise("#s4-bh", at(4, 0.1))
t_st = cue(4, "The stuff that's in your head")
c.settle("#v4", t_st, 0.6, "pop")
v4.start(None, t_st)
t_q1 = cue(4, '"My mum\'s turning sixty')
q1 = "She's turning sixty. She just retired after thirty years as a nurse. She's funny, a bit sarcastic, and she'd cringe at anything too soppy."
v4.zoom(box("02", find_words("02", "Write a birthday message for my mum. " + q1), 16), t_q1 - 0.9, 1.1, 30, 1.25)
v4.sweep(q1, t_q1, cue(4, "Now look at the answer") - 0.2, "b")
t_na = cue(4, "Now look at the answer")
t_q2 = cue(4, '"The NHS')
q2 = "The NHS will have to find someone else to give that look to patients who say \"it's probably nothing.\""
v4.zoom(box("02", find_words("02", q2), 16), t_na, 1.2, 40, 1.5)
v4.sweep(q2, t_q2, cue(4, "Suddenly it's about her") - 0.2, "b")
v4.drift(t_q2, 5)
t_sa = cue(4, "Suddenly it's about her")
v4.zoom(None, t_sa, 1.2)
for i, ph in enumerate(["The nursing", "the retirement", "the sense of humor"]):
    c.snap(f"#s4-t{i}", cue(4, ph))
c.pulse("#s4-bh .bt", cue(4, "You just let it into your head"), 1.05)
HTML[4] = block_head(4, "02", "The context", "What&rsquo;s in your head that the AI can&rsquo;t see.", "b") + f"""
<div class="vwrap" style="left:384px;top:330px">{v4.html()}</div>
<div class="tags4"><span class="tg b" id="s4-t0">nursing</span><span class="tg b" id="s4-t1">retirement</span><span class="tg b" id="s4-t2">humor</span></div>"""

# ---- 5. Block 3: the rules (screenshot 3)
c = scene(5)
v5 = Viewer(c, "v5", "03", 1440, 560)
c.rise("#s5-bh", at(5, 0.1))
c.snap("#s5-r0", cue(5, "Length"))
c.snap("#s5-r1", cue(5, "tone"))
c.snap("#s5-r2", cue(5, "what to avoid"))
t_k = cue(5, '"Keep it under')
c.settle("#v5", t_k - 0.9, 0.6, "pop")
v5.start(None, t_k - 0.9)
q3 = "Keep it under fifty words. It's going in a card, so no emojis. Don't say 'queen'."
v5.zoom(box("03", find_words("03", q3), 16), t_k - 0.3, 1.0, 40, 1.6)
v5.sweep(q3, t_k, cue(5, "You'd be surprised") - 0.2, "y")
c.snap("#s5-cut", cue(5, "The rules stop the stuff"))
c.pulse("#s5-cut", cue(5, "delete anyway"), 1.06)
t_qn = cue(5, "call your mum a queen")
c.slam("#s5-queen", t_qn)
t_cr = cue(5, "Now it's short and card-ready")
c.out("#s5-queen", t_cr - 0.2)
q4 = "Thirty years of bossing doctors around, and now you're free to boss us full-time."
v5.zoom(box("03", find_words("03", q4), 16), t_cr, 1.1, 40, 1.6)
v5.sweep(q4, cue(5, '"Thirty years'), end_of(5) - 0.5, "y")
v5.drift(cue(5, '"Thirty years'), 4.5)
c.out("#s5-cut", cue(5, "Now it's short") - 0.2)
c.snap("#s5-ok", cue(5, "card-ready") + 0.3)
HTML[5] = block_head(5, "03", "The rules", "", "y") + f"""
<div class="rules5"><span class="tg y" id="s5-r0">length</span><span class="tg y" id="s5-r1">tone</span><span class="tg y" id="s5-r2">what to avoid</span></div>
<div class="vwrap" style="left:384px;top:400px">{v5.html()}</div>
<div class="in-stamp stamp5" id="s5-queen">NO QUEENS.</div>
<div class="chip3 cut5" id="s5-cut"><i class="in-led on y"></i>Stops the stuff you&rsquo;d delete anyway</div>
<div class="chip3 ok5" id="s5-ok"><i class="in-led on y"></i>43 words &middot; no emojis &middot; zero queens</div>"""

# ---- 6. Block 4: what good looks like (screenshot 4)
c = scene(6)
v6 = Viewer(c, "v6", "04", 1440, 640)
c.rise("#s6-bh", at(6, 0.1))
c.snap("#s6-nb", cue(6, "almost nobody uses"))
c.pulse("#s6-bh .bt", cue(6, "the most powerful"), 1.05)
t_pi = cue(6, "Paste in a few texts")
c.out("#s6-nb", t_pi - 0.5)
c.settle("#v6", t_pi - 0.4, 0.6, "pop")
v6.start(None, t_pi - 0.4)
v6.zoom(box("04", find_words("04", "Here are a few texts I've sent her, so you can match how I write: \"Mum I finally used the slow cooker. Nobody got food poisoning, you'd be proud\" \"Did you actually watch the whole series in one night?? Who even are you\" \"Tell Dad the fence he 'fixed' has fallen over again\""), 16), t_pi, 1.1, 30, 1.5)
q5 = "Tell Dad the fence he 'fixed' has fallen over again"
dad1 = v6.sweep(q5, cue(6, '"Tell Dad'), cue(6, "Look what came back") - 0.2, "p")
t_lw = cue(6, "Look what came back")
q6 = "now you're stuck at home with Dad full time. Toughest shift yet."
v6.zoom(box("04", find_words("04", q6), 16), t_lw, 1.1, 40, 1.5)
dad2 = v6.sweep(q6, cue(6, '"Now you\'re stuck'), cue(6, "It picked up Dad") - 0.2, "p")
t_pu = cue(6, "It picked up Dad")
v6.zoom((60, 190, 1440, 545), t_pu, 1.1, 20, 1.2)
# ring both "Dad"s and draw the link between them
W4 = OCR["04"]
d_a = [i for i in find_words("04", q5) if letters(W4[i]["t"]) == "dad"][0]
d_b = [i for i in find_words("04", q6) if letters(W4[i]["t"]) == "dad"][0]
ax, ay = W4[d_a]["x"] + W4[d_a]["w"] / 2, W4[d_a]["y"] + W4[d_a]["h"] / 2
bx, by = W4[d_b]["x"] + W4[d_b]["w"] / 2, W4[d_b]["y"] + W4[d_b]["h"] / 2
v6.marks.append(f'<svg class="link" viewBox="0 0 {IMG["04"][0]} {IMG["04"][1]}" style="width:{IMG["04"][0]}px;height:{IMG["04"][1]}px">'
                f'<ellipse id="v6-r1" cx="{ax}" cy="{ay}" rx="46" ry="26" style="stroke-dasharray:240"/>'
                f'<ellipse id="v6-r2" cx="{bx}" cy="{by}" rx="46" ry="26" style="stroke-dasharray:240"/>'
                f'<path id="v6-ln" d="M{ax - 30} {ay + 24} C {ax - 260} {ay + 70}, {bx - 260} {by - 60}, {bx - 44} {by - 6}" style="stroke-dasharray:700"/></svg>')
c.tw("#v6-r1", {"strokeDashoffset": 240, "opacity": 1}, {"strokeDashoffset": 0, "opacity": 1}, t_pu + 1.0, 0.5, "igOut")
c.tw("#v6-ln", {"strokeDashoffset": 700, "opacity": 1}, {"strokeDashoffset": 0, "opacity": 1}, t_pu + 1.4, 0.8, "igOut")
c.tw("#v6-r2", {"strokeDashoffset": 240, "opacity": 1}, {"strokeDashoffset": 0, "opacity": 1}, t_pu + 2.1, 0.5, "igOut")
SFX.append((t_pu + 2.2, "ding"))
c.snap("#s6-never", cue(6, "I never asked it"))
t_eb = cue(6, "An example beats")
c.out(".vwrap6", t_eb - 0.2, 0.3)
c.out("#s6-never", t_eb - 0.2, 0.3)
c.out("#s6-bh .bs", t_eb - 0.1, 0.25)
c.rise("#s6-eb", t_eb + 0.1)
c.snap("#s6-vague", cue(6, 'Telling it "be casual"'))
c.snap("#s6-bp", cue(6, "Showing it how you actually talk"))
c.press("#s6-bp", cue(6, "that's a blueprint"))
c.pulse("#s6-bp", cue(6, "that's a blueprint") + 0.1, 1.05)
HTML[6] = block_head(6, "04", "What good looks like", "Show it an example.", "p") + f"""
<div class="vwrap vwrap6" style="left:384px;top:330px">{v6.html()}</div>
<div class="chip3 nb6" id="s6-nb"><i class="in-led on"></i>Almost nobody uses this one</div>
<p class="in-body eb6" id="s6-eb">An example beats a description. Every time.</p>
<div class="chip3 never6" id="s6-never"><i class="in-led on"></i>Dad came from the example. I never asked.</div>
<div class="vs6">
  <div class="in-key vague" id="s6-vague"><span class="num">DESCRIBE<i class="in-led"></i></span><span class="lab">&ldquo;be casual&rdquo;</span><span class="cap">vague</span></div>
  <div class="in-key in-key--p bp" id="s6-bp"><span class="num">SHOW<i class="in-led on"></i></span><span class="lab">&ldquo;Tell Dad the fence he fixed has fallen over again&rdquo;</span><span class="cap">a blueprint</span></div>
</div>"""

# ---- 7. Before vs after, the real test, lazy prompts
c = scene(7)
va = Viewer(c, "v7a", "01", 690, 470)
vb = Viewer(c, "v7b", "04", 690, 470)
reg_a = box("01", find_words("01", "Happy Birthday, Mum! Thank you for the love, the patience, and all the times you believed in me before I believed in myself. So much of who I am comes from you: your kindness, your strength, and the way you always make home feel like home."), 14)
reg_b = box("04", find_words("04", "Happy 60th Mum! Thirty years of keeping strangers alive, and now you're stuck at home with Dad full time. Toughest shift yet. Retirement looks good on you, though. Love you (yes, I'm allowed to say it once a year, stop rolling your eyes)."), 14)
va.start(reg_a, c.start)
vb.start(reg_b, c.start)
c.rise("#s7-cmp", at(7, 0.2))
c.slam("#s7-st", cue(7, "could be for anyone") + 0.2)
c.tw("#v7b", {"boxShadow": "0 0 0 0 rgba(255,61,127,0)"}, {"boxShadow": "0 0 0 10px rgba(255,61,127,.9)"}, cue(7, "could only be for your mum"), 0.5, "igOut")
c.snap("#s7-only", cue(7, "could only be for your mum") + 0.2)
t_rt = cue(7, "That's the real test")
c.out("#s7-cmp", t_rt - 0.2, 0.35)
c.out("#s7-st", t_rt - 0.2, 0.35)
c.out("#s7-only", t_rt - 0.2, 0.35)
c.rise("#s7-q", cue(7, "Could the answer only"), 40)
c.pulse("#s7-q .you", cue(7, "Could the answer only") + 1.6, 1.12)
c.rise("#s7-miss", cue(7, "you're missing a block"))
t_lz = cue(7, "And as someone who works")
c.out("#s7-q", t_lz - 0.2)
c.out("#s7-miss", t_lz - 0.2)
lazy = "fix this"
c.snap("#s7-scr", t_lz + 0.2, "click")
c.snap("#s7-eng", cue(7, "works with AI every day"))
c.pulse("#s7-eng", cue(7, "I'll be honest"), 1.06)
c.typeon("s7-c", len(lazy), cue(7, "I still catch myself"), 10)
c.settle("#s7-meter", cue(7, "Then I wonder"), 0.5, "pop")
c.tw("#s7-mi", {"scaleY": 0}, {"scaleY": 1}, cue(7, "Then I wonder") + 0.3, 0.7, "igOut")
c.slam("#s7-lazy", cue(7, "the answer is lazy"))
HTML[7] = f"""
<div class="cmp7" id="s7-cmp">
  <div class="col7"><div class="in-silk lab7">1 block</div><div class="vwrap" style="position:relative">{va.html()}</div></div>
  <div class="col7"><div class="in-silk lab7" style="color:var(--pink)">4 blocks</div><div class="vwrap" style="position:relative">{vb.html()}</div></div>
</div>
<div class="in-stamp stamp7" id="s7-st">ANYONE&rsquo;S MUM</div>
<div class="chip3 only7" id="s7-only"><i class="in-led on"></i>Only for <b>your</b> mum</div>
<div class="q7" id="s7-q"><h2 class="in-h">Could the answer<br/>only be for <span class="you" style="color:var(--blue);display:inline-block">you?</span></h2></div>
<p class="in-body miss7" id="s7-miss">If not, you&rsquo;re missing a block. Usually <b style="color:var(--blue)">context</b>.</p>
<div class="in-screen scr7" id="s7-scr">&gt;&nbsp;{chars("s7-c", lazy)}<span class="in-cursor"></span></div>
<div class="in-silk eng7" id="s7-eng">Software engineer &middot; AI every day &middot; still guilty</div>
<div class="meter7" id="s7-meter"><div class="col"><i id="s7-mi"></i></div><span class="w">answer</span><span class="v">lazy</span></div>
<div class="in-stamp stamp7b" id="s7-lazy">LAZY IN, LAZY OUT.</div>"""

# ---- 8. The cheat code: ask me questions first (screenshot 5)
c = scene(8)
v8 = Viewer(c, "v8", "05", 1440, 600)
c.rise("#s8-bh", at(8, 0.1))
t_al = cue(8, "Add this line to any prompt")
c.snap("#s8-scr", t_al, "click")
p8 = "Before you answer, ask me any questions you need."
c.typeon("s8-c", len(p8), cue(8, '"Before you answer'), 20)
t_ig = cue(8, "Instead of guessing")
c.out("#s8-scr", t_ig - 0.3)
c.settle("#v8", t_ig - 0.2, 0.6, "pop")
v8.start(None, t_ig - 0.2)
v8.zoom(box("05", find_words("05", "Tone:") + find_words("05", "Signing off: How do you usually sign things to her"), 20), t_ig + 0.4, 1.1, 20, 1.3)
for ph, spoken, nxt in [("Tone:", "What tone?", "How long?"), ("Length:", "How long?", "Is it a milestone"),
                        ("Milestone birthday?:", "Is it a milestone", "Card, text"), ("How will you deliver it?: Card, text, speech", "Card, text", "How do you usually"),
                        ("Signing off:", "How do you usually", "You answer")]:
    v8.sweep(ph, cue(8, spoken), cue(8, nxt) - 0.15, "y")
c.snap("#s8-think", cue(8, "you barely had to think"))
HTML[8] = f"""
<div class="bh" id="s8-bh"><span class="num-b p">The cheat code</span><h2 class="in-h bt">Ask me questions first</h2></div>
<div class="in-screen scr8" id="s8-scr">&gt;&nbsp;{chars("s8-c", p8)}<span class="in-cursor"></span></div>
<div class="vwrap" style="left:384px;top:330px">{v8.html()}</div>
<div class="chip3 think8" id="s8-think"><i class="in-led on"></i>All four blocks. You barely had to think.</div>"""

# ---- 9. Recap (keys back in the hero row) + Tokyo
c = scene(9)
HTML[9] = f"""
<h2 class="in-h hd9" id="s9-h">So.</h2>
<div class="in-screen scr9" id="s9-a">&gt;&nbsp;What time is it in Tokyo?<span class="lab9">task only &middot; fine</span></div>
<div class="in-screen scr9" id="s9-b">&gt;&nbsp;Birthday message for my mum&hellip;<span class="lab9 p">anything personal &middot; all four</span></div>"""
c.rise("#s9-h", at(9, 0.1))
c.out("#s9-h", cue(9, "You don't need all four") - 0.1)
c.snap("#s9-a", cue(9, "Asking what time"), "click")
c.pulse("#s9-a .lab9", cue(9, "doesn't need your life story"), 1.12)
t_ap = cue(9, "But anything personal")
c.out("#s9-a", t_ap - 0.2)
c.snap("#s9-b", t_ap, "click")
c.pulse("#s9-b", cue(9, "anything you'd actually send"), 1.03)
c.pulse("#s9-b .lab9", cue(9, "give it the blocks"), 1.12)

# ---- 10. Next video teaser + end card
c = scene(10)
HTML[10] = """
<div class="tz" id="s10-tz">
  <div class="in-silk">Same prompt. Twice.</div>
  <div class="two10"><div class="in-screen a10" id="s10-a">Happy 60th, Mum! Thirty years of nursing&hellip;</div>
    <div class="in-screen a10" id="s10-b">Happy 60th, Mum! Thirty years of bossing doctors&hellip;</div></div>
  <div class="in-key in-key--y die" id="s10-die"><span class="num">NEXT<i class="in-led on y"></i></span><span class="lab">Why AI rolls the dice</span></div>
</div>
<div class="end10" id="s10-end">
  <h1 class="in-h sign" id="s10-sign">I gotchu<span class="in-dot"></span></h1>
  <div class="in-screen slot10" id="s10-s1" style="left:128px">NEXT VIDEO</div>
  <div class="in-screen slot10" id="s10-s2" style="left:800px">BEST FOR YOU</div>
  <div class="in-key in-key--p sub10" id="s10-s3"><span class="in-silk" style="color:var(--graphite)">Subscribe</span></div>
</div>"""
c.rise("#s10-tz .in-silk", at(10, 0.1))
c.snap("#s10-a", cue(10, "Ask the same prompt twice"))
c.snap("#s10-b", cue(10, "you get two different answers"))
c.pulse("#s10-a", cue(10, "Is that a bug"), 1.04)
c.snap("#s10-die", cue(10, "Next video"))
c.press("#s10-die", cue(10, "rolls the dice"))
t_g = cue(10, "I gotchu")
c.out("#s10-tz", t_g - 0.35, 0.3)
c.tw("#s10-sign", {"opacity": 0, "filter": "blur(12px)", "scale": 1.03}, {"opacity": 1, "filter": "blur(0px)", "scale": 1}, t_g - 0.2, 0.7, "igOut")
for i in range(3):
    c.snap(f"#s10-s{i+1}", t_g + 0.8 + i * 0.15)

for n, name in CHAPS:
    t0 = T[n]["start"] + 0.5
    world.set("#chap", {"innerHTML": name}, t0)
    world.tw("#chap", {"opacity": 0, "x": -16}, {"opacity": 1, "x": 0}, t0, 0.4, "igOut")
    world.to("#chap", {"opacity": 0}, t0 + 2.5, 0.4, "none")


# ================================================================ STYLES (Type Lab: Instrument + Condensed Grotesque)
FONTS = (
    '@font-face{font-family:"Bricolage Grotesque";font-weight:200 800;font-stretch:75% 100%;src:url(assets/fonts/bricolage-grotesque-latin-wdth-normal.woff2) format("woff2")}'
    + "".join(f'@font-face{{font-family:"DM Sans";font-weight:{w};src:url(assets/fonts/dm-sans-latin-{w}-normal.woff2) format("woff2")}}' for w in (500, 600, 700))
    + "".join(f'@font-face{{font-family:"JetBrains Mono";font-weight:{w};src:url(assets/fonts/jetbrains-mono-latin-{w}-normal.woff2) format("woff2")}}' for w in (500, 700)))

BASE = """
*{box-sizing:border-box}
:root{--panel:#e3e8e4;--panel-hi:#f0f4f1;--panel-lo:#c3ccc6;--key:#f7faf8;--graphite:#131a17;--graphite-2:#262f2b;--soft:#4a5751;--dim:#66736c;
 --blue:#2343e0;--blue-hi:#9db1ff;--pink:#ff3d7f;--pink-text:#c8195a;--yellow:#ffd21a;--red:#d8261c;--screen:#0c1310;
 --f-d:"Bricolage Grotesque","Arial Narrow",sans-serif;--f-b:"DM Sans",Arial,sans-serif;--f-m:"JetBrains Mono",ui-monospace,monospace}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:var(--panel)}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:var(--panel);color:var(--graphite);font-family:var(--f-b);font-weight:500}
.layer{position:absolute;left:0;top:0;width:1920px;height:1080px}
/* shared Instrument components (igotchu Type Lab) */
.in-screw{position:absolute;width:24px;height:24px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fbfdfc,#b3beb7 70%);box-shadow:inset 0 0 0 2px #a3afa8,0 1px 0 #fff;z-index:3}
.in-screw::after{content:"";position:absolute;left:5px;right:5px;top:11px;height:2px;background:#8b978f;transform:rotate(-35deg)}
.in-silk{position:absolute;font-family:var(--f-m);font-weight:700;font-size:28px;letter-spacing:.12em;text-transform:uppercase;color:var(--soft)}
.in-h{font-family:var(--f-d);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75;letter-spacing:-.02em;line-height:.88;margin:0}
.in-body{font-size:52px;line-height:1.25;font-weight:500;color:var(--soft);margin:0}
.in-led{display:inline-block;width:22px;height:22px;border-radius:50%;background:#b3bdb6;box-shadow:inset 0 2px 3px rgba(0,0,0,.25);vertical-align:middle}
.in-led.on{background:var(--pink);box-shadow:0 0 0 5px rgba(255,61,127,.16),0 0 22px var(--pink)}
.in-led.on.b{background:#4f6bff;box-shadow:0 0 0 5px rgba(35,67,224,.15),0 0 22px #4f6bff}
.in-led.on.y{background:var(--yellow);box-shadow:0 0 0 5px rgba(255,210,26,.2),0 0 22px var(--yellow)}
.in-dot{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:var(--pink);box-shadow:0 0 0 .05em rgba(255,61,127,.16),0 0 .25em var(--pink);margin-left:.04em}
.in-key{position:absolute;display:flex;flex-direction:column;justify-content:space-between;border-radius:36px;padding:32px 34px;background:var(--key);color:var(--graphite);
 box-shadow:inset 0 -5px 0 rgba(0,0,0,.07),0 12px 0 var(--panel-lo),0 30px 44px rgba(19,26,23,.16)}
.in-key--g{background:var(--graphite);color:#f7faf8;box-shadow:inset 0 -5px 0 rgba(255,255,255,.06),0 12px 0 #000,0 30px 44px rgba(19,26,23,.2)}
.in-key--b{background:var(--blue);color:#fff;box-shadow:inset 0 -5px 0 rgba(0,0,0,.12),0 12px 0 #172e9e,0 30px 44px rgba(19,26,23,.2)}
.in-key--p{background:var(--pink);color:var(--graphite);box-shadow:inset 0 -5px 0 rgba(0,0,0,.1),0 12px 0 #b8194f,0 30px 44px rgba(19,26,23,.2)}
.in-key--y{background:var(--yellow);color:var(--graphite);box-shadow:inset 0 -5px 0 rgba(0,0,0,.08),0 12px 0 #b89400,0 30px 44px rgba(19,26,23,.2)}
.in-key .num{font-family:var(--f-m);font-weight:700;font-size:30px;letter-spacing:.1em;display:flex;align-items:center;justify-content:space-between}
.in-key .lab{font-family:var(--f-d);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75;font-size:72px;line-height:.92;letter-spacing:-.01em}
.in-screen{position:absolute;background:var(--screen);border-radius:28px;box-shadow:inset 0 0 0 12px var(--graphite-2),inset 0 0 80px rgba(0,0,0,.7),0 2px 0 var(--panel-hi),0 -2px 0 var(--panel-lo);
 color:var(--blue-hi);font-family:var(--f-m);font-weight:500;text-shadow:0 0 18px rgba(157,177,255,.55)}
.in-cursor{display:inline-block;width:.55em;height:.9em;background:var(--blue-hi);vertical-align:-.1em;box-shadow:0 0 16px rgba(157,177,255,.8)}
.in-stamp{position:absolute;border:12px solid var(--red);border-radius:18px;padding:14px 42px 22px;color:var(--red);font-family:var(--f-d);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75;
 font-size:130px;line-height:.9;letter-spacing:.01em;transform:rotate(-7deg);background:rgba(247,250,248,.8);box-shadow:inset 0 0 0 5px var(--key),inset 0 0 0 10px var(--red);opacity:0;z-index:6}
.ch{display:none}
/* screenshot viewer: a device screen; the camera moves inside it */
.vwrap{position:absolute}
.viewer{position:relative;overflow:hidden;border-radius:30px;background:#1f1f1e;box-shadow:inset 0 0 0 12px var(--graphite-2),0 2px 0 var(--panel-hi),0 30px 50px rgba(19,26,23,.22)}
.viewer.light{background:#f8f9fb}
.viewer::after{content:"";position:absolute;inset:0;border-radius:30px;box-shadow:inset 0 0 0 12px var(--graphite-2);pointer-events:none;z-index:3}
.vdrift{position:absolute;inset:0;transform-origin:50% 50%}
.vcam{position:absolute;left:0;top:0;transform-origin:0 0}
.vcam img{position:absolute;left:0;top:0;display:block}
.hl{position:absolute;display:block;transform-origin:0 50%;border-radius:6px;opacity:0}
.viewer.dark .hl{mix-blend-mode:screen}.viewer.light .hl{mix-blend-mode:multiply}
.viewer.dark .hl.c{background:rgba(92,120,255,.55)}.viewer.dark .hl.b{background:rgba(70,100,255,.6)}.viewer.dark .hl.y{background:rgba(255,200,0,.55)}.viewer.dark .hl.p{background:rgba(255,61,127,.55)}
.viewer.light .hl.y{background:rgba(255,210,26,.85)}.viewer.light .hl.p{background:rgba(255,61,127,.5)}
.link{position:absolute;left:0;top:0;overflow:visible}
.link ellipse,.link path{fill:none;stroke:var(--pink);stroke-width:6;stroke-linecap:round;filter:drop-shadow(0 0 8px rgba(255,61,127,.9));opacity:0}
/* scene furniture */
.sc{position:absolute;inset:0}.sc-cam{position:absolute;inset:0;transform-origin:60% 50%}
.bh{position:absolute;left:384px;top:118px;right:128px;display:flex;align-items:baseline;gap:30px;flex-wrap:wrap}
.num-b{font-family:var(--f-m);font-weight:700;font-size:30px;letter-spacing:.1em;text-transform:uppercase;padding:10px 18px;border-radius:14px;background:var(--graphite);color:#f7faf8;align-self:center}
.num-b.b{background:var(--blue);color:#fff}.num-b.y{background:var(--yellow);color:var(--graphite)}.num-b.p{background:var(--pink);color:var(--graphite)}
.bt{font-size:130px}.bs{font-size:44px;width:100%;margin-top:6px}
.chip3{position:absolute;display:flex;align-items:center;gap:18px;padding:22px 32px;border-radius:26px;background:var(--key);font-size:40px;font-weight:700;color:var(--graphite);
 box-shadow:inset 0 -4px 0 rgba(0,0,0,.07),0 10px 0 var(--panel-lo),0 24px 36px rgba(19,26,23,.14);opacity:0;z-index:5}
.tg{display:inline-block;padding:16px 28px;border-radius:22px;font-family:var(--f-m);font-weight:700;font-size:34px;letter-spacing:.08em;text-transform:uppercase;opacity:0;
 box-shadow:inset 0 -4px 0 rgba(0,0,0,.1),0 10px 0 var(--panel-lo),0 22px 30px rgba(19,26,23,.14)}
.tg.b{background:var(--blue);color:#fff}.tg.y{background:var(--yellow);color:var(--graphite)}
/* world */
.rack{position:absolute;inset:0}
.key{position:absolute;width:370px;height:380px;transform-origin:0 0}.key .kb{position:absolute;inset:0}
.tag{right:96px;top:40px;display:none;align-items:center;gap:16px;z-index:3}.tag span{margin-left:10px}
.chap{position:absolute;left:96px;bottom:34px;font-family:var(--f-m);font-weight:700;font-size:28px;letter-spacing:.12em;text-transform:uppercase;color:var(--blue);opacity:0}
#pline{position:absolute;left:0;right:0;bottom:0;height:8px;background:var(--panel-lo)}
#pfill{position:absolute;left:0;bottom:0;width:1920px;height:8px;background:var(--blue);transform-origin:0 50%}
"""

SCENE_CSS = {
    1: """.hd1{position:absolute;left:128px;top:110px;font-size:150px;opacity:0}
.sub1{position:absolute;left:1000px;top:170px;opacity:0;font-size:50px}.sub1 .arr{display:inline-block;color:var(--pink)}
.note1{left:128px;top:870px;opacity:0}
.scr1{left:128px;top:840px;width:980px;height:130px;display:flex;align-items:center;padding:0 48px;font-size:52px;opacity:0}
.better1{position:absolute;left:1180px;top:860px;width:612px;display:flex;flex-direction:column;gap:16px;opacity:0}
.bar1{height:44px;border-radius:14px;background:var(--screen);box-shadow:inset 0 0 0 6px var(--graphite-2);padding:9px;overflow:hidden}
.bar1 i{display:block;height:100%;border-radius:8px;background:repeating-linear-gradient(90deg,#4f6bff 0 22px,transparent 22px 30px);transform-origin:0 50%}
.cheat1{left:1330px;top:830px;width:462px;height:170px;padding:22px 30px;opacity:0}.cheat1 .lab{font-size:58px}""",
    2: """.scr2{left:384px;top:120px;width:1440px;height:140px;display:flex;align-items:center;padding:0 52px;font-size:50px;opacity:0}
.stamp2{left:1210px;top:560px}
.any{left:384px;top:1010px;opacity:0;font-size:26px}""",
    3: """.scr3{left:384px;top:470px;width:1440px;height:170px;display:flex;align-items:center;padding:0 56px;font-size:60px;opacity:0}
.ln3{white-space:nowrap}.task-hl{background:linear-gradient(90deg,rgba(157,177,255,.3),rgba(157,177,255,.3)) no-repeat 0 0/0% 100%;border-radius:8px;color:#fff}
.scr3 .rest{color:#5a6c9c;text-shadow:none}
.bh{opacity:0}
.chip3{left:384px;top:720px}
.ghosts3{position:absolute;left:1020px;top:700px;display:flex;gap:30px;align-items:center;opacity:0}
.gk{width:130px;height:130px;border-radius:26px;border:5px dashed var(--dim);display:grid;place-items:center;font-family:var(--f-m);font-weight:700;font-size:34px;color:var(--dim)}
.gk.b{border-color:var(--blue);color:var(--blue)}.gk.y{border-color:#c9a400;color:#9a7d00}.gk.p{border-color:var(--pink);color:var(--pink-text)}
.ghl{position:absolute;left:0;top:160px;white-space:nowrap}""",
    4: """.bh{opacity:0}.viewer{opacity:0}
.tags4{position:absolute;left:1030px;top:860px;display:flex;gap:26px;z-index:5}""",
    5: """.bh{opacity:0}.viewer{opacity:0}
.rules5{position:absolute;left:384px;top:275px;display:flex;gap:26px}
.cut5{left:420px;top:900px}
.stamp5{left:1180px;top:560px}
.ok5{left:420px;top:900px}""",
    6: """.bh{opacity:0}.viewer{opacity:0}
.never6{left:420px;top:880px}.nb6{left:384px;top:500px}
.eb6{position:absolute;left:384px;top:300px;opacity:0}
.vs6{position:absolute;left:384px;top:420px;right:96px;display:grid;grid-template-columns:1fr 1.5fr;gap:60px}
.vs6 .in-key{position:relative;height:470px;opacity:0}
.vs6 .vague{background:var(--key);color:var(--dim)}.vs6 .vague .lab{font-size:110px}
.vs6 .bp .lab{font-size:66px}
.vs6 .cap{font-family:var(--f-m);font-weight:700;font-size:32px;letter-spacing:.1em;text-transform:uppercase}""",
    7: """.cmp7{position:absolute;left:384px;top:150px;right:96px;display:grid;grid-template-columns:1fr 1fr;gap:60px;opacity:0}
.col7{display:flex;flex-direction:column;gap:22px}.lab7{position:relative}
.stamp7{left:520px;top:420px;font-size:96px}
.only7{left:1150px;top:800px}
.q7{position:absolute;left:384px;top:260px;opacity:0}.q7 .in-h{font-size:170px}
.miss7{position:absolute;left:384px;top:680px;opacity:0}
.scr7{left:384px;top:300px;width:900px;height:170px;display:flex;align-items:center;padding:0 56px;font-size:64px;opacity:0}
.meter7{position:absolute;left:1420px;top:170px;display:flex;flex-direction:column;align-items:center;gap:16px;opacity:0}
.meter7 .col{position:relative;width:130px;height:460px;border-radius:18px;background:var(--screen);box-shadow:inset 0 0 0 8px var(--graphite-2);overflow:hidden}
.meter7 .col i{position:absolute;left:16px;right:16px;bottom:16px;height:70px;background:repeating-linear-gradient(0deg,var(--pink) 0 22px,transparent 22px 30px);transform-origin:50% 100%}
.meter7 .w{font-family:var(--f-d);font-weight:800;font-stretch:75%;font-size:64px;line-height:1}.meter7 .v{font-family:var(--f-m);font-weight:700;font-size:32px;color:var(--pink-text)}
.stamp7b{left:420px;top:600px;font-size:110px}.eng7{left:384px;top:500px;opacity:0}""",
    8: """.bh{opacity:0}.viewer{opacity:0}
.scr8{left:384px;top:470px;width:1440px;height:170px;display:flex;align-items:center;padding:0 52px;font-size:46px;opacity:0}
.think8{left:900px;top:890px}""",
    9: """.hd9{position:absolute;left:128px;top:140px;font-size:200px;opacity:0}
.scr9{left:128px;top:850px;width:1664px;height:130px;display:flex;align-items:center;padding:0 48px;font-size:48px;opacity:0}
.lab9{display:inline-block;margin-left:auto;font-family:var(--f-m);font-weight:700;font-size:28px;letter-spacing:.1em;text-transform:uppercase;color:#7c8c86;text-shadow:none}.lab9.p{color:var(--pink)}""",
    10: """.tz{position:absolute;inset:0}.tz .in-silk{left:128px;top:150px;opacity:0}
.two10{position:absolute;left:128px;top:220px;right:128px;display:grid;grid-template-columns:1fr 1fr;gap:40px}
.a10{position:relative;height:300px;padding:44px 48px;font-size:44px;line-height:1.35;opacity:0}
.die{left:128px;top:620px;width:760px;height:300px;opacity:0}.die .lab{font-size:96px}
.end10{position:absolute;inset:0}
.sign{position:absolute;left:128px;top:110px;font-size:290px;opacity:0}
.slot10{top:560px;width:620px;height:349px;display:flex;align-items:flex-end;padding:30px 40px;font-size:30px;opacity:0}
.sub10{left:1480px;top:570px;width:320px;height:320px;border-radius:50%;align-items:center;justify-content:center;opacity:0}""",
}


# ================================================================ WRITE FILES
def comp_file(cid, inner, css, A, dur, extra_attr=""):
    return f"""<template id="{cid}-template">
  <div data-composition-id="{cid}" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080"{extra_attr}>
    {inner}
    <style>
      [data-composition-id="{cid}"]{{position:absolute;inset:0;overflow:hidden}}
      {css}
    </style>
    <script>
      (() => {{
        const SLOT = {dur};
        const tl = gsap.timeline({{ paused: true }});
{chr(10).join('        ' + a for a in A)}
        tl.set({{}}, {{}}, SLOT);
        window.__timelines = window.__timelines || {{}};
        window.__timelines["{cid}"] = tl;
      }})();
    </script>
  </div>
</template>
"""


def scoped(cid, css):
    """Prefix every rule of a scene's CSS with its composition scope (kit convention)."""
    out = []
    for rule in re.findall(r"[^{}]+\{[^{}]*\}", css):
        sel, body = rule.split("{", 1)
        sels = ",".join(f'[data-composition-id="{cid}"] {s.strip()}' for s in sel.split(","))
        out.append(sels + "{" + body)
    return "\n".join(out)


os.makedirs("video/compositions", exist_ok=True)
os.makedirs("video/assets/screens", exist_ok=True)
os.makedirs("video/assets/fonts", exist_ok=True)
for f in ["gsap.min.js", "CustomEase.min.js"]:
    shutil.copy(f"../v4/video/assets/{f}", f"video/assets/{f}")
for f in os.listdir("../v4/video/assets/fonts"):
    if f.startswith(("bricolage", "dm-sans", "jetbrains")):
        shutil.copy(f"../v4/video/assets/fonts/{f}", "video/assets/fonts/")
for f in os.listdir("assets/screens"):
    shutil.copy(f"assets/screens/{f}", "video/assets/screens/")

open("video/compositions/world.html", "w").write(comp_file("world", world_html, "", world.A, TOTAL))
mounts = ['<div class="layer" id="world" data-composition-id="world" data-composition-src="compositions/world.html" data-start="0" '
          f'data-duration="{TOTAL}" data-track-index="0" data-width="1920" data-height="1080"></div>']
for n in range(1, 11):
    c = SCENES[n]
    cid = c.cid
    anchor = re.split(r"[.,?!]", SL[n]["text"])[0][:40].replace('"', "").replace("Here's where", "where")
    inner = f'<div class="sc"><div class="sc-cam">{HTML[n]}</div></div>'
    # scene timelines use scoped selectors: ids are unique already; bare classes get the scope prefix
    A = [re.sub(r'tl\.(fromTo|to|set)\("(\.[^"]+)"', lambda m: f'tl.{m.group(1)}(\'[data-composition-id="{cid}"] {m.group(2)}\'', a) for a in c.A]
    open(f"video/compositions/{cid}.html", "w").write(comp_file(cid, inner, scoped(cid, SCENE_CSS[n]), A, c.dur, f' data-anchor="{anchor}"'))
    mounts.append(f'<div class="layer" id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                  f'data-start="{c.start}" data-duration="{c.dur}" data-track-index="{1 + n % 2}" data-width="1920" data-height="1080" '
                  f'data-anchor="{anchor}"></div>')

root = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<title>igotchu Ep 07: Anatomy of a prompt</title>
<script src="assets/gsap.min.js"></script><script src="assets/CustomEase.min.js"></script>
<script>
  gsap.registerPlugin(CustomEase);
  CustomEase.create("igOut","0.2,0.8,0.2,1");
  CustomEase.create("igSnap","0.3,1.45,0.5,1");
  CustomEase.create("igSlam","0.7,0,0.84,0");
  CustomEase.create("igIO","0.65,0,0.35,1");
  CustomEase.create("igIn","0.5,0,0.75,0");
  CustomEase.create("igSettle","0.22,1,0.36,1");
</script>
<style>{FONTS}{BASE}</style></head>
<body>
<div id="root" data-composition-id="anatomy" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
  <audio id="vo" src="assets/mix.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-volume="1"></audio>
  {chr(10).join('  ' + m for m in mounts)}
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  tl.set({{}}, {{}}, {TOTAL});
  window.__timelines["anatomy"] = tl;
</script>
</body></html>
"""
open("video/index.html", "w").write(root)

# word-level transcript for the kit's validate-beat-sync.mjs (the kit expects Scribe/Whisper words; we
# generate them free from the phrase aligner: each word's time is interpolated inside its phrase)
words = []
for n in range(1, 11):
    for m in re.finditer(r"\S+", SL[n]["text"]):
        words.append({"text": re.sub(r'^[\"\u201c(]+|[\"\u201d),.?!:;]+$', "", m.group(0)), "start": time_at_char(n, m.start())})
json.dump({"words": words}, open("video/assets/transcript.json", "w"))

# frozen-frame check (kit: animation-map dead zones; ours: > 3.2 s with nothing new)
spans = sorted(MOTION)
gaps, cur = [], 0.0
for a, b in spans:
    if a - cur > 3.2:
        gaps.append((round(cur, 2), round(a, 2)))
    cur = max(cur, b)
print(f"wrote video/index.html + {len(SCENES) + 1} compositions, {TOTAL}s")
print("frozen stretches > 3.2 s:", gaps if gaps else "none")
json.dump(SFX, open("sfx_events.json", "w"))
