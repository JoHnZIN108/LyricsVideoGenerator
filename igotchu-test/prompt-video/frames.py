"""igotchu Ep 07, "Anatomy of a good prompt": the "Ep 07 Frames" design (the user's artifact
DSaXXh4rTgUz92BLBWYUK1), built in the student-kit structure into video_frames/.

Design rules from the Frames page:
- one colour per block, everywhere: task graphite/paper, context pink, rules yellow, examples blue
- two beats per block: a full-screen colour card names the block, then the prompt-and-reply frame proves it
- the prompt is real typed text that grows; each new part gets its numbered tag and a highlight sweep in
  its block colour while the voice reads it; the AI answers in a white card, word by word
- giant condensed type, one idea per frame, nothing under 26 px
User rules added on top: no screenshots (text only); nothing is revealed before the voice gets to it
(the opening shows the four colour bars with their names blurred; each name appears with its block).

Timing, voice, SFX and the mix are shared with build.py (cue() aligner, mix.py).
"""
import json
import os
import re
import shutil

_src = open("build.py").read()
exec(_src.split("# ================================================================ WORLD")[0])
exec("def comp_file" + _src.split("def comp_file")[1].split("os.makedirs")[0])
exec("FONTS" + _src.split("\nFONTS")[1].split("\nBASE")[0])
XO = 0.45
OUT = "video_frames"

INK, PAPER, PAPER2, MUTED = "#111614", "#E7ECE8", "#DCE3DE", "#5B6862"
PINK, YELLOW, BLUE = "#FF3D7F", "#FFD21A", "#2343E0"
BLOCKS = [("01", "The task", PAPER, INK), ("02", "The context", PINK, INK), ("03", "The rules", YELLOW, INK),
          ("04", "What good looks like", BLUE, "#fff")]
HLC = {1: "rgba(17,22,20,.13)", 2: "rgba(255,61,127,.34)", 3: "rgba(255,210,26,.9)", 4: "rgba(35,67,224,.22)"}
TGC = {1: (INK, "#fff"), 2: (PINK, "#fff"), 3: ("#E5B800", INK), 4: (BLUE, "#fff")}
PROMPT = {1: "Write a birthday message for my mum.",
          2: "She’s turning sixty. She just retired after thirty years as a nurse. She’s funny, a bit sarcastic, "
             "and she’d cringe at anything too soppy.",
          3: "Keep it under fifty words. It’s going in a card, so no emojis. Don’t say ‘queen’.",
          4: "Here are a few texts I’ve sent her, so you can match how I write: “Mum I finally used the slow cooker. "
             "Nobody got food poisoning, you’d be proud” “Did you actually watch the whole series in one night?? "
             "Who even are you” “Tell Dad the fence he ‘fixed’ has fallen over again”"}


# ---------------------------------------------------------------- Frames motion vocabulary
def wipe(c, sel, t, dur=0.5, sound="whoosh"):
    if sound:
        SFX.append((t, sound))
    c.tw(sel, {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, t, dur, "igWipe")


def lines_html(pid, texts):
    return "".join(f'<span class="ln"><span id="{pid}{i}">{t}</span></span>' for i, t in enumerate(texts))


def rise_lines(c, pid, n, t, gap=0.09):
    for i in range(n):
        c.tw(f"#{pid}{i}", {"yPercent": 125}, {"yPercent": 0}, t + i * gap, 0.9, "igOut")


def drop_lines(c, pid, n, t):
    for i in range(n):
        c.tw(f"#{pid}{i}", {"yPercent": 0}, {"yPercent": -125}, t, 0.45, "igIn")


def pop(c, sel, t, r=-4, sound="pop"):
    if sound:
        SFX.append((t, sound))
    c.tw(sel, {"opacity": 0, "scale": 0.7, "rotation": r - 6}, {"opacity": 1, "scale": 1, "rotation": r}, t, 0.55, "igPop")


def words_html(pid, text):
    return " ".join(f'<span class="w" id="{pid}{i}">{w}</span>' for i, w in enumerate(text.split()))


def type_words(c, pid, text, t0, t1):
    ws = text.split()
    lens = [len(w) + 1 for w in ws]
    tot, t = sum(lens), t0
    for i, ln in enumerate(lens):
        c.tw(f"#{pid}{i}", {"opacity": 0, "y": 18}, {"opacity": 1, "y": 0}, t, 0.35, "igOut")
        t += (t1 - t0) * ln / tot


def hl_html(pid, text, k):
    return " ".join(f'<span class="hw"><i class="hb" id="{pid}{i}" style="background:{HLC[k]}"></i><span>{w}</span></span>'
                    for i, w in enumerate(text.split()))


def sweep(c, pid, text, t0, t1, sound="tick"):
    ws = text.split()
    lens = [max(1, len(re.sub(r"\W", "", w))) for w in ws]
    tot, t = sum(lens), t0
    if sound:
        SFX.append((t0, sound))
    for i, ln in enumerate(lens):
        d = (t1 - t0) * ln / tot
        c.tw(f"#{pid}{i}", {"scaleX": 0}, {"scaleX": 1}, t, max(0.08, d * 0.95), "none")
        t += d


def tag(k):
    bg, fg = TGC[k]
    return f'<i class="tg" style="background:{bg};color:{fg}">{k}</i>'


def old_prompt(ks):
    """Earlier prompt parts: small, grey, already highlighted in their colours."""
    return " ".join(f'{tag(k)}<span class="hl-old" style="background:{HLC[k]}">{PROMPT[k]}</span>' for k in ks)


def chrome(pid, on=0, wm=True):
    bars = "".join(f'<i id="{pid}-pb{k}" class="{"on" if k < on else ""}"></i>' for k in range(4))
    return (f'<div class="m tl" id="{pid}-tl">Ep 07 — Anatomy of a prompt</div>'
            + (f'<div class="wm">igotchu<i>.</i></div>' if wm else "") + f'<div class="prog">{bars}</div>')


def chrome_in(c, pid, t):
    c.fade(f"#{pid}-tl", t + 0.2, 0.5)


def reply_html(pid, text, extra=""):
    return (f'<div class="rc" id="{pid}"><div class="hd"><span class="ai">AI</span><span class="m sm">Reply</span></div>'
            f'<div class="tx">{words_html(pid + "w", text)}</div>{extra}</div>')


FULL = {
    "01": ["Here\u2019s a warm, general birthday message you can use as it is or adapt:", "<b>Happy Birthday, Mum!</b>",
           "Thank you for the love, the patience, and all the times you believed in me before I believed in myself. So much of who I am comes from you: your kindness, your strength, and the way you always make home feel like home.",
           "I hope today brings you as much joy as you\u2019ve given everyone around you. You deserve every bit of celebration, and so much more.",
           "I love you more than words can say.", "With all my love,<br>Johnson",
           "If you\u2019d like a different version, tell me the tone (funny, sentimental, short for a card or text) or share a memory or inside joke, and I\u2019ll make it more personal to her."],
    "02": ["Happy 60th, Mum!",
           "Thirty years of nursing, and you\u2019ve finally retired. The NHS will have to find someone else to give that look to patients who say \u201cit\u2019s probably nothing.\u201d",
           "Sixty suits you. You\u2019ve spent three decades telling people to rest, drink more water and stop googling their symptoms, so now it\u2019s your turn. Try following your own advice for once. (I know you won\u2019t.)",
           "Thanks for being the funniest person in any room, including the waiting room. I promise not to make this soppy, so I\u2019ll just say you\u2019re alright, really.",
           "Love you (there, I said it, don\u2019t make it weird),<br>[Your name]"],
    "03": ["Happy 60th, Mum! Thirty years of bossing doctors around, and now you\u2019re free to boss us full-time. Lucky us. Enjoy retirement. You\u2019ve earned the lie-ins, the gossip and the right to diagnose everyone at dinner. Here\u2019s to the next thirty. Love you (don\u2019t make it weird)."],
    "04": ["Happy 60th Mum! Thirty years of keeping strangers alive, and now you\u2019re stuck at home with Dad full time. Toughest shift yet. Retirement looks good on you, though. Love you (yes, I\u2019m allowed to say it once a year, stop rolling your eyes).",
           "That\u2019s 43 words."]}


def reply_full_html(pid, shot, quote, k, extra="", style=""):
    """Claude's whole reply, exactly as in the user's screenshot; the quoted line is wrapped for a highlight sweep."""
    ps = []
    for i, p in enumerate(FULL[shot]):
        if quote in p:
            a, b = p.split(quote, 1)
            p = a + hl_html(pid + "-q", quote, k) + b
        ps.append(f'<p class="rp" id="{pid}-p{i}">{p}</p>')
    return (f'<div class="rc full" id="{pid}" style="{style}"><div class="hd"><span class="ai">AI</span><span class="m sm">Reply</span></div>'
            f'{"".join(ps)}{extra}</div>')


def reply_in(c, pid, shot, t):
    c.rise(f"#{pid}", t, 40, 0.6)
    for i in range(len(FULL[shot])):
        c.tw(f"#{pid}-p{i}", {"opacity": 0, "y": 14}, {"opacity": 1, "y": 0}, t + 0.25 + i * 0.12, 0.4, "igOut")


def ring_svg(rid):
    return (f'<svg class="ring" viewBox="0 0 200 100" preserveAspectRatio="none"><path id="{rid}" pathLength="1" '
            'd="M22 58 C14 22 112 6 170 20 C206 32 198 80 128 90 C62 98 6 86 12 54 C16 34 50 22 92 18"/></svg>')


def draw(c, sel, t, dur=0.7):
    SFX.append((t, "whoosh_s"))
    c.tw(sel, {"strokeDashoffset": 1}, {"strokeDashoffset": 0}, t, dur, "igOut")


def card_html(pid, k, title_lines, sub, sub2=""):
    num, _, bg, fg = BLOCKS[k - 1]
    stroke = {1: PAPER, 2: INK, 3: INK, 4: "#fff"}[k]
    return (f'<div class="pn" id="{pid}" style="background:{bg if k > 1 else INK};color:{fg if k > 1 else PAPER}">'
            f'{chrome(pid, k)}<div class="num" id="{pid}-num" style="-webkit-text-stroke-color:{stroke}">{num}</div>'
            f'<div class="m" id="{pid}-lab" style="left:120px;top:230px">Block {num} / 04</div>'
            f'<h2 class="d cardh">{lines_html(pid + "-h", title_lines)}</h2>'
            f'<p class="b cs" id="{pid}-s">{sub}</p>' + (f'<p class="b cs2" id="{pid}-s2">{sub2}</p>' if sub2 else "") + "</div>")


def card_in(c, pid, t, n_lines):
    c.tw(f"#{pid}-num", {"opacity": 0, "xPercent": 18}, {"opacity": 0.3, "xPercent": 0}, t, 1.1, "igOut")
    c.fade(f"#{pid}-lab", t + 0.15)
    rise_lines(c, pid + "-h", n_lines, t + 0.2)
    chrome_in(c, pid, t)


def evidence_html(pid, k, on, reply_text=None, reply_extra="", extra=""):
    """Prompt-and-reply frame: old parts small and grey, part k large with its highlight, reply card right."""
    old = old_prompt(range(1, k)) if k > 1 else ""
    fs = {1: 54, 2: 54, 3: 54, 4: 40}[k]
    body = (f'<div class="pn" id="{pid}" style="background:{PAPER};color:{INK}">{chrome(pid, on)}'
            f'<div class="m" id="{pid}-lab" style="left:120px;top:190px;color:{MUTED}">Your prompt</div>'
            f'<div class="pcol">' + (f'<p class="old" id="{pid}-old">{old}</p>' if old else "")
            + f'<p class="new" id="{pid}-new" style="font-size:{fs}px">{tag(k)}{hl_html(pid + "-h", PROMPT[k], k)}</p></div>')
    if reply_text:
        body += reply_text
    return body + extra + "</div>"


SCENES, HTML = {}, {}


def scene(n):
    s = T[n]["start"] - (XO if n > 1 else 0)
    d = T[n]["dur"] + (XO if n > 1 else 0)
    c = Comp(f"s{n:02d}", s, d)
    SCENES[n] = c
    if n > 1:
        wipe(c, ".sc", s, XO, "whoosh")
    return c


# ================================================================ 1. Title: four blocks, names blurred
c = scene(1)
t4, t_one, t_bat = cue(1, "four small parts"), cue(1, "Most people only use one"), cue(1, "one block at a time")
t_wb, t_tr = cue(1, "watch the answer get better"), cue(1, "a trick that basically")
rise_lines(c, "s1-h", 3, 0.1)
pop(c, "#s1-use", cue(1, "a useless AI answer") + 0.2, -3)
pop(c, "#s1-bri", cue(1, "a brilliant one") + 0.1, 2)
c.out("#s1-use", t4 - 0.1)
c.out("#s1-bri", t4 - 0.1)
c.pulse("#s1-L0", cue(1, "build a prompt from scratch"), 1.04)
chrome_in(c, "s1a", 0)
c.fade("#s1-sub", 1.1, 0.6)
for i in range(4):
    wipe(c, f"#s1-L{i}", t4 + 0.1 + i * 0.14, 0.8, "click")
c.fade("#s1-one", t_one + 0.1)
for i in (1, 2, 3):
    c.to(f"#s1-L{i}", {"opacity": 0.22}, t_one + 0.2, 0.4, "none")
c.pulse("#s1-L0", t_one + 0.3, 1.04)
c.out("#s1-one", t_bat - 0.2)
for i in (1, 2, 3):
    c.to(f"#s1-L{i}", {"opacity": 1}, t_bat + 0.25 * i, 0.3, "none")
    SFX.append((t_bat + 0.25 * i, "click"))
c.fade("#s1-q", t_wb - 0.1)
for i in range(4):
    c.tw(f"#s1-qb{i}", {"scaleX": 0}, {"scaleX": 1}, t_wb + 0.2 + i * 0.35, 0.4, "igOut")
    SFX.append((t_wb + 0.2 + i * 0.35, "tick"))
pop(c, "#s1-cheat", t_tr + 0.3, -4)
layers = "".join(
    f'<div class="layer1" id="s1-L{i}" style="background:{bg};color:{fg}"><span class="m" style="letter-spacing:.12em">{num}</span>'
    f'<span class="d blur">{lab}</span></div>' for i, (num, lab, bg, fg) in enumerate(BLOCKS))
qbars = "".join(f'<i id="s1-qb{i}" style="background:{BLOCKS[i][2]}"></i>' for i in range(4))
HTML[1] = f"""<div class="pn" id="s1a" style="background:{INK};color:{PAPER}">{chrome("s1a", 0)}
<h1 class="d" style="left:112px;top:150px;font-size:230px">{lines_html("s1-h", ["Anatomy", "of a", '<span style="color:var(--pink)">prompt.</span>'])}</h1>
<div class="stack1">{layers}</div>
<div class="m" id="s1-one" style="left:1160px;top:900px;color:var(--pink);opacity:0">Most people use 1</div>
<div class="q1" id="s1-q"><span class="m" style="font-size:26px;color:#9FB0A7">Answer quality</span><div class="qb">{qbars}</div></div>
<div class="stk" id="s1-use" style="left:120px;top:770px;background:#2A322E;color:#9FB0A7">Useless answer</div>
<div class="stk" id="s1-bri" style="left:470px;top:770px;background:var(--pink);color:#fff">→ Brilliant answer</div>
<p class="b" id="s1-sub" style="left:120px;top:890px;font-size:44px;color:#9FB0A7;opacity:0">The 4 parts most people skip.</p>
<div class="stk" id="s1-cheat" style="left:1180px;top:890px;background:var(--yellow);color:var(--ink)">+ a cheat code at the end</div></div>"""

# ================================================================ 2. What most people type
c = scene(2)
p0 = T[2]["start"] - XO
chrome_in(c, "s2a", p0)
c.fade("#s2-lab", p0 + 0.3)
rise_lines(c, "s2-q", 3, cue(2, '"Write a birthday'), 0.12)
reply_in(c, "s2-r", "01", cue(2, "And you get back"))
r2 = "Thank you for the love, the patience, and all the times you believed in me before I believed in myself."
sweep(c, "s2-r-q", r2, cue(2, '"Thank you'), cue(2, "It's fine") - 0.3)
pop(c, "#s2-fine", cue(2, "It's fine"), 3)
pop(c, "#s2-pet", cue(2, "petrol station"), -3)
pop(c, "#s2-any", cue(2, "anyone's mum"), -5)
t_ob = cue(2, "you only gave it one block")
c.pulse("#s2a-pb0", t_ob, 1.4)
c.fade("#s2-1of4", t_ob + 0.1)
HTML[2] = f"""<div class="pn" id="s2a" style="background:{PAPER};color:{INK}">{chrome("s2a", 1)}
<div class="m" id="s2-lab" style="left:120px;top:190px;color:var(--pink);opacity:0">What most people type</div>
<h2 class="d" style="left:112px;top:250px;font-size:124px;white-space:nowrap">{lines_html("s2-q", ["“Write a", "birthday message", "for my mum.”"])}</h2>
{reply_full_html("s2-r", "01", r2, 1, style="left:1040px;top:150px;width:760px")}
<div class="stk" id="s2-fine" style="left:120px;top:620px;background:var(--ink);color:var(--paper)">It’s fine.</div>
<div class="stk" id="s2-pet" style="left:130px;top:720px;background:#fff;color:var(--ink)">Petrol station card</div>
<div class="stk" id="s2-any" style="left:520px;top:800px;background:var(--yellow);color:var(--ink)">Could be anyone’s mum</div>
<div class="m" id="s2-1of4" style="right:440px;top:985px;opacity:0">1 block of 4</div></div>"""
# the reply card's own id was renamed above; animate the card, type the words

# ================================================================ 3. Block 1: the task (dark card)
c = scene(3)
p0 = T[3]["start"] - XO
card_in(c, "s3a", p0 + 0.1, 1)
c.rise("#s3a-s", cue(3, "What you want"))
pop(c, "#s3-task", cue(3, '"Write a birthday message" is a task'), -2)
c.rise("#s3-every", cue(3, "Everybody gets this block"))
t_o3 = cue(3, "the other three")
for k, col in ((1, PINK), (2, YELLOW), (3, BLUE)):
    c.tw(f"#s3a-pb{k}", {"backgroundColor": PAPER, "opacity": 0.16}, {"backgroundColor": col, "opacity": 1}, t_o3 + 0.15 * k, 0.3, "none")
    c.pulse(f"#s3a-pb{k}", t_o3 + 0.15 * k, 1.3)
    SFX.append((t_o3 + 0.15 * k, "click"))
HTML[3] = card_html("s3a", 1, ["The task."], "What you want it to do.").replace(
    "</div>", "", 0) + ""
HTML[3] = HTML[3][:-6] + (f'<div class="stk" id="s3-task" style="left:120px;top:690px;background:{PAPER};color:{INK}">'
                          '“Write a birthday message” = the task</div>'
                          '<p class="b" id="s3-every" style="left:120px;top:830px;font-size:44px;opacity:0;width:1500px">'
                          'Everybody gets this block. It’s the other three that make the magic.</p></div>')

# ================================================================ 4. Block 2: the context (pink card, then proof)
c = scene(4)
p0 = T[4]["start"] - XO
card_in(c, "s4a", p0 + 0.1, 1)
c.rise("#s4a-s", cue(4, "The stuff"))
t_ev = cue(4, '"My mum') - 0.35
wipe(c, "#s4b", t_ev)
chrome_in(c, "s4b", t_ev)
c.fade("#s4b-old", t_ev + 0.2)
c.rise("#s4b-new", t_ev + 0.3)
sweep(c, "s4b-h", PROMPT[2], cue(4, '"My mum'), cue(4, "Now look at the answer") - 0.2)
r4 = "The NHS will have to find someone else to give that look to patients who say “it’s probably nothing.”"
reply_in(c, "s4b-r", "02", cue(4, "Now look at the answer"))
sweep(c, "s4b-r-q", r4, cue(4, '"The NHS'), cue(4, "Suddenly") - 0.2)
for i, ph in enumerate(["The nursing", "the retirement", "the sense of humor"]):
    pop(c, f"#s4-t{i}", cue(4, ph), [-4, 3, -2][i])
c.rise("#s4-same", cue(4, "Same AI"))
HTML[4] = card_html("s4a", 2, ["The context."], "The stuff in your head that the AI can’t see.") + evidence_html("s4b", 2, 2, reply_full_html("s4b-r", "02", r4, 2, style="left:1110px;top:170px;width:700px"), extra="".join(
    f'<div class="stk" id="s4-t{i}" style="left:{x}px;top:760px;background:var(--pink);color:#fff">{w}</div>'
    for i, (x, w) in enumerate([(120, "Nursing"), (410, "Retirement"), (770, "Humour")])) + \
    '<p class="b" id="s4-same" style="left:120px;top:880px;font-size:44px;opacity:0">Same AI. You just let it into your head.</p>')

# ================================================================ 5. Block 3: the rules (yellow card, then proof)
c = scene(5)
p0 = T[5]["start"] - XO
card_in(c, "s5a", p0 + 0.1, 1)
for i, ph in enumerate(["Length", "tone,", "what to avoid"]):
    c.rise(f"#s5-r{i}", cue(5, ph), 30, 0.45)
    SFX.append((cue(5, ph), "click"))
t_ev = cue(5, '"Keep it under') - 0.35
wipe(c, "#s5b", t_ev)
chrome_in(c, "s5b", t_ev)
c.fade("#s5b-old", t_ev + 0.2)
c.rise("#s5b-new", t_ev + 0.3)
sweep(c, "s5b-h", PROMPT[3], cue(5, '"Keep it under'), cue(5, "You'd be surprised") - 0.2)
c.pulse("#s5b-new", cue(5, "You'd be surprised"), 1.03)
c.slam("#s5-stamp", cue(5, "call your mum a queen") + 0.4)
pop(c, "#s5-stop", cue(5, "The rules stop"), -3)
t_ns = cue(5, "Now it's short")
c.out("#s5-stamp", t_ns - 0.3)
r5 = "Thirty years of bossing doctors around, and now you’re free to boss us full-time."
reply_in(c, "s5b-r", "03", t_ns)
sweep(c, "s5b-r-q", r5, cue(5, '"Thirty years'), at(5, SEG[5][-1][1]) - 0.2)
HTML[5] = card_html("s5a", 3, ["The rules."], "") + evidence_html("s5b", 3, 3, reply_full_html("s5b-r", "03", r5, 3, style="left:1110px;top:170px;width:700px"), extra=(
    '<div class="stamp" id="s5-stamp" style="left:1180px;top:380px">NO<br>QUEENS.</div>'
    '<div class="stk" id="s5-stop" style="left:120px;top:800px;background:var(--ink);color:var(--paper)">Stops what you’d delete anyway</div>'))
HTML[5] = HTML[5].replace('<p class="b cs" id="s5a-s"></p>', '<p class="b cs" id="s5a-s">' + "".join(
    f'<span class="rw" id="s5-r{i}">{w}</span>' for i, w in enumerate(["Length,", "tone,", "what to avoid."])) + "</p>")

# ================================================================ 6. Block 4: what good looks like (blue card, proof, blueprint)
c = scene(6)
p0 = T[6]["start"] - XO
card_in(c, "s6a", p0 + 0.1, 2)
c.rise("#s6a-s", cue(6, "Show it what good"))
c.rise("#s6a-s2", cue(6, "almost nobody uses"))
pop(c, "#s6-pow", cue(6, "most powerful"), 4)
t_ev = cue(6, "Paste in a few texts") - 0.35
wipe(c, "#s6b", t_ev)
chrome_in(c, "s6b", t_ev)
c.fade("#s6b-old", t_ev + 0.2)
c.rise("#s6b-new", t_ev + 0.3)
words4 = PROMPT[4].split()
cut = next(i for i, w in enumerate(words4) if w.startswith("“Tell"))
part_a, part_b = " ".join(words4[:cut]), " ".join(words4[cut:])
sweep(c, "s6b-h", part_a, cue(6, "Paste in a few texts") + 0.3, cue(6, '"Tell Dad') - 0.15)
# second part continues the same id sequence
_ids_b = len(part_a.split())
ws_b = part_b.split()
tb0, tb1 = cue(6, '"Tell Dad'), cue(6, "Look what came back") - 0.2
lens_b = [max(1, len(re.sub(r"\W", "", w))) for w in ws_b]
tt = tb0
for j, ln in enumerate(lens_b):
    d = (tb1 - tb0) * ln / sum(lens_b)
    c.tw(f"#s6b-h{_ids_b + j}", {"scaleX": 0}, {"scaleX": 1}, tt, max(0.08, d * 0.95), "none")
    tt += d
SFX.append((tb0, "tick"))
r6 = "now you’re stuck at home with Dad full time. Toughest shift yet."
reply_in(c, "s6b-r", "04", cue(6, "Look what came back"))
sweep(c, "s6b-r-q", r6, cue(6, '"Now you'), cue(6, "It picked up") - 0.2)
t_pd = cue(6, "It picked up Dad")
draw(c, "#s6-ring1", t_pd + 0.2)
draw(c, "#s6-ring2", t_pd + 0.5)
c.fade("#s6-from", cue(6, "I never asked"))
t_eb = cue(6, "An example beats")
wipe(c, "#s6c", t_eb - 0.3)
chrome_in(c, "s6c", t_eb - 0.3)
rise_lines(c, "s6-eb", 2, t_eb - 0.1)
c.settle("#s6-vague", cue(6, 'Telling it "be casual"'), 0.5, "pop")
c.fade("#s6-vl", cue(6, "is vague"))
c.settle("#s6-show", cue(6, "Showing it how"), 0.5, "pop")
c.fade("#s6-bl", cue(6, "that's a blueprint"))
c.pulse("#s6-show", cue(6, "that's a blueprint"), 1.04)
HTML[6] = card_html("s6a", 4, ["What good", "looks like."], "Show it. Don’t describe it.", "The one almost nobody uses.")
HTML[6] = HTML[6][:-6] + '<div class="stk" id="s6-pow" style="left:1380px;top:780px;background:var(--yellow);color:var(--ink)">The most powerful</div></div>'
ev6 = evidence_html("s6b", 4, 4, reply_full_html("s6b-r", "04", r6, 4, style="left:1110px;top:170px;width:700px", extra='<div class="m" id="s6-from" style="margin-top:22px;color:var(--pink);font-size:26px;opacity:0;position:relative">'
                    '↑ From my texts. I never asked.</div>'))
# rings around both "Dad"s: in the prompt ("Tell Dad") and in the reply ("with Dad")
i_dad_p = _ids_b + 1
ev6 = ev6.replace(f'<i class="hb" id="s6b-h{i_dad_p}"', f'{ring_svg("s6-ring2")}<i class="hb" id="s6b-h{i_dad_p}"', 1)
i_dad_r = r6.split().index("Dad")
ev6 = ev6.replace(f'<i class="hb" id="s6b-r-q{i_dad_r}"', f'{ring_svg("s6-ring1")}<i class="hb" id="s6b-r-q{i_dad_r}"', 1)
HTML[6] += ev6
HTML[6] += f"""<div class="pn" id="s6c" style="background:{PAPER2};color:{INK}">{chrome("s6c", 4)}
<h2 class="d" style="left:112px;top:190px;font-size:150px">{lines_html("s6-eb", ["An example beats", "a description."])}</h2>
<div class="vcard" id="s6-vague"><span class="m">Describe</span><span class="d" style="font-size:120px;color:{MUTED}">“be casual”</span>
<span class="m" id="s6-vl" style="opacity:0">Vague</span></div>
<div class="vcard show" id="s6-show"><span class="m">Show</span><span class="d" style="font-size:70px;line-height:.95">“Tell Dad the fence he ‘fixed’ has fallen over again”</span>
<span class="m" id="s6-bl" style="opacity:0">A blueprint</span></div></div>"""

# ================================================================ 7. Before and after; the real test; lazy prompts
c = scene(7)
p0 = T[7]["start"] - XO
c.tw("#s7-dark", {"clipPath": "inset(0% 100% 0% 0%)"}, {"clipPath": "inset(0% 0% 0% 0%)"}, p0 + 0.1, 0.8, "igWipe")
chrome_in(c, "s7a", p0)
c.fade("#s7-bl", p0 + 0.5)
c.rise("#s7-bt", cue(7, "The first message"))
pop(c, "#s7-any", cue(7, "could be for anyone") + 0.3, -4)
c.fade("#s7-al", p0 + 0.8)
rise_lines(c, "s7-pt", 1, p0 + 0.3)
c.to("#s7-ptw", {"opacity": 0}, cue(7, "The first message") - 0.3, 0.3, "none")
c.rise("#s7-at", cue(7, "The new one"))
pop(c, "#s7-only", cue(7, "could only be for your mum") + 0.4, 3)
c.fade("#s7-rt", cue(7, "That's the real test"))
c.rise("#s7-q", cue(7, "Could the answer only"))
t_mb = cue(7, "If it could be for anyone")
wipe(c, "#s7b", t_mb - 0.3)
chrome_in(c, "s7b", t_mb - 0.3)
rise_lines(c, "s7-mh", 1, t_mb)
for i in range(4):
    wipe(c, f"#s7-L{i}", t_mb + 0.3 + i * 0.12, 0.6, "click")
t_uc = cue(7, "Usually context")
for i in (0, 2, 3):
    c.to(f"#s7-L{i}", {"opacity": 0.2}, t_uc, 0.35, "none")
c.pulse("#s7-L1", t_uc + 0.1, 1.04)
pop(c, "#s7-uc", t_uc + 0.2, -4)
t_sw = cue(7, "And as someone")
wipe(c, "#s7c", t_sw - 0.3)
chrome_in(c, "s7c", t_sw - 0.3)
c.fade("#s7-eng", t_sw)
rise_lines(c, "s7-ev", 1, cue(7, "works with AI every day"))
drop_lines(c, "s7-ev", 1, cue(7, "I'll be honest") - 0.2)
rise_lines(c, "s7-ho", 1, cue(7, "I'll be honest"))
c.settle("#s7-bar", cue(7, "I still catch myself"), 0.45, "click")
c.typeon("s7-c", len("fix this"), cue(7, "I still catch myself") + 0.4, 9)
c.fade("#s7-1b", cue(7, "lazy one-block prompts"))
c.rise("#s7-rc", cue(7, "Then I wonder"), 40, 0.6)
c.slam("#s7-lazy", cue(7, "the answer is lazy"))
HTML[7] = f"""<div class="pn" id="s7a" style="background:{PAPER};color:{INK}">
<div id="s7-dark" style="left:0;top:0;width:960px;height:1080px;background:var(--ink)"></div>{chrome("s7a", 4, False)}
<h2 class="d" id="s7-ptw" style="left:112px;top:520px;font-size:110px;color:var(--paper);z-index:3;white-space:nowrap">{lines_html("s7-pt", ["Put them together."])}</h2>
<div class="m" id="s7-bl" style="left:120px;top:190px;color:#9FB0A7;opacity:0">Before · 1 block</div>
<p id="s7-bt" style="left:120px;top:250px;width:720px;margin:0;font-size:56px;line-height:1.3;color:#9FB0A7;opacity:0">“Thank you for the love, the patience, and all the times you believed in me before I believed in myself.”</p>
<div class="stk" id="s7-any" style="left:120px;top:720px;background:var(--yellow);color:var(--ink)">Could be anyone’s mum</div>
<div class="m" id="s7-al" style="left:1080px;top:190px;color:var(--blue);opacity:0">After · 4 blocks</div>
<p id="s7-at" style="left:1080px;top:250px;width:720px;margin:0;font-size:72px;line-height:1.18;font-weight:700;letter-spacing:-.01em;opacity:0">“Now you’re stuck at home with Dad full time. Toughest shift yet.”</p>
<div class="stk" id="s7-only" style="left:1080px;top:640px;background:var(--pink);color:#fff">Only your mum</div>
<div class="m" id="s7-rt" style="left:1080px;top:770px;color:{MUTED};opacity:0">The real test</div>
<p class="d" id="s7-q" style="left:1076px;top:820px;font-size:84px;line-height:.92;width:760px;opacity:0">Could the answer only be for you?</p></div>
<div class="pn" id="s7b" style="background:{PAPER};color:{INK}">{chrome("s7b", 4)}
<h2 class="d" style="left:112px;top:170px;font-size:170px">{lines_html("s7-mh", ["Missing a block?"])}</h2>
<div class="stack7">""" + "".join(
    f'<div class="layer1" id="s7-L{i}" style="background:{bg if i else INK};color:{fg if i else PAPER}"><span class="m">{num}</span>'
    f'<span class="d">{lab}</span></div>' for i, (num, lab, bg, fg) in enumerate(BLOCKS)) + f"""</div>
<div class="stk" id="s7-uc" style="left:1300px;top:470px;background:var(--ink);color:var(--paper)">Usually context</div></div>
<div class="pn" id="s7c" style="background:{INK};color:{PAPER}">{chrome("s7c", 4)}
<div class="m" id="s7-eng" style="left:120px;top:190px;color:var(--yellow);opacity:0">Software engineer · AI every day</div>
<h2 class="d" style="left:112px;top:250px;font-size:170px">{lines_html("s7-ev", ["AI. Every day."])}</h2>
<h2 class="d" style="left:112px;top:250px;font-size:170px">{lines_html("s7-ho", ["I’ll be honest."])}</h2>
<div class="pbar" id="s7-bar" style="opacity:0"><span class="m" style="color:#9FB0A7">&gt;</span>&nbsp;{chars("s7-c", "fix this")}<span class="cur"></span>
<span class="m" id="s7-1b" style="margin-left:auto;font-size:26px;color:var(--pink);opacity:0">1 block</span></div>
<div class="rc small" id="s7-rc" style="left:1130px;top:520px;opacity:0"><div class="hd"><span class="ai">AI</span><span class="m sm">Reply</span></div>
<i class="sk" style="width:92%"></i><i class="sk" style="width:78%"></i><i class="sk" style="width:85%"></i><i class="sk" style="width:40%"></i></div>
<div class="stamp" id="s7-lazy" style="left:180px;top:720px;font-size:120px">LAZY IN, LAZY OUT.</div></div>"""

# ================================================================ 8. The cheat code; it interviews you
c = scene(8)
p0 = T[8]["start"] - XO
chrome_in(c, "s8a", p0)
c.fade("#s8-lab", p0 + 0.2)
rise_lines(c, "s8-t", 2, cue(8, "the trick I promised") - 0.2)
t_dk = cue(8, "If you don't know")
c.rise("#s8-dk", t_dk)
t_fo = cue(8, "make the AI figure it out")
drop_lines(c, "s8-t", 2, t_fo - 0.2)
rise_lines(c, "s8-f", 2, t_fo)
t_al = cue(8, "Add this line to any prompt")
drop_lines(c, "s8-f", 2, t_al - 0.2)
c.out("#s8-dk", t_al - 0.2)
c.out("#s8-lab", t_al - 0.1)
pop(c, "#s8-add", t_al + 0.1, -3)
for i, ph in enumerate(['"Before you answer', "ask me any questions", "you need"]):
    c.tw(f"#s8-c{i}", {"yPercent": 125}, {"yPercent": 0}, cue(8, ph) - 0.1, 0.8, "igOut")
t_ig = cue(8, "Instead of guessing")
wipe(c, "#s8b", t_ig - 0.3)
chrome_in(c, "s8b", t_ig - 0.3)
c.fade("#s8-wl", t_ig)
rise_lines(c, "s8-iv", 3, t_ig + 0.3)
QS = [("What tone?", '"What tone', "#E5B800"), ("How long?", "How long", "#E5B800"),
      ("Is it a milestone birthday?", "Is it a milestone", PINK), ("Card, text or speech?", "Card, text", "#E5B800"),
      ("How do you usually sign off?", "How do you usually", BLUE)]
for i, (_, ph, _) in enumerate(QS):
    c.rise(f"#s8-q{i}", cue(8, ph) - 0.1, 40, 0.5)
    SFX.append((cue(8, ph) - 0.1, "pop"))
c.fade("#s8-fill", cue(8, "You answer"))
t_ff = cue(8, "All four blocks")
for k in range(4):
    c.tw(f"#s8b-pb{k}", {"opacity": 0.16}, {"opacity": 1}, t_ff + 0.15 * k, 0.2, "none")
    c.pulse(f"#s8b-pb{k}", t_ff + 0.15 * k, 1.3)
    SFX.append((t_ff + 0.15 * k, "click"))
pop(c, "#s8-think", cue(8, "you barely had to think"), -3)
qs_html = "".join(f'<div class="bub" id="s8-q{i}"><span class="dot" style="background:{col}"></span>{q}</div>' for i, (q, _, col) in enumerate(QS))
HTML[8] = f"""<div class="pn" id="s8a" style="background:{YELLOW};color:{INK}">{chrome("s8a", 0)}
<div class="m" id="s8-lab" style="left:120px;top:190px;opacity:0">The cheat code</div>
<div class="stk" id="s8-add" style="left:120px;top:170px;background:var(--ink);color:var(--yellow)">Add this line to any prompt</div>
<h2 class="d" style="left:112px;top:260px;font-size:200px">{lines_html("s8-t", ["The trick", "I promised."])}</h2>
<h2 class="d" style="left:112px;top:260px;font-size:200px">{lines_html("s8-f", ["Make the AI", "figure it out."])}</h2>
<p class="b" id="s8-dk" style="left:120px;top:700px;font-size:56px;font-weight:600;opacity:0">Don’t know what context to give?</p>
<h2 class="d" style="left:112px;top:300px;font-size:176px">{lines_html("s8-c", ["“Before you answer,", "ask me any questions", "you need.”"])}</h2></div>
<div class="pn" id="s8b" style="background:{PAPER};color:{INK}">{chrome("s8b", 0)}
<div class="m" id="s8-wl" style="left:120px;top:190px;color:{MUTED};opacity:0">What comes back</div>
<h2 class="d" style="left:112px;top:250px;font-size:200px">{lines_html("s8-iv", ["It", "interviews", "you."])}</h2>
<p class="b" id="s8-fill" style="left:120px;top:830px;font-size:40px;color:{MUTED};width:760px;opacity:0">Each answer fills one of your blocks.</p>
<div class="qs8">{qs_html}</div>
<div class="stk" id="s8-think" style="left:1000px;top:880px;background:var(--yellow);color:var(--ink)">All four blocks. You barely had to think.</div></div>"""

# ================================================================ 9. Recap: the anatomy, then Tokyo
c = scene(9)
p0 = T[9]["start"] - XO
chrome_in(c, "s9a", p0)
rise_lines(c, "s9-so", 1, p0 + 0.2)
ROWS = ["Write a birthday message for my mum.", "Turning sixty. Retired nurse. Funny, sarcastic, hates soppy.",
        "Under 50 words. No emojis. Don’t say “queen”.", "Texts I’ve actually sent her."]
for i, ph in enumerate(["The task", "The context", "The rules", "And an example"]):
    wipe(c, f"#s9-R{i}", cue(9, ph), 0.55, "click")
t_dn = cue(9, "You don't need all four")
for i in (1, 2, 3):
    c.to(f"#s9-R{i}", {"opacity": 0.18}, t_dn + 0.1, 0.4, "none")
t_tk = cue(9, "Asking what time it is in Tokyo")
c.to("#s9-r0a", {"opacity": 0}, t_tk, 0.25, "none")
c.fade("#s9-r0b", t_tk + 0.2, 0.3)
pop(c, "#s9-fine", cue(9, "doesn't need your life story"), -3)
t_bp = cue(9, "But anything personal")
c.to("#s9-r0b", {"opacity": 0}, t_bp, 0.25, "none")
c.fade("#s9-r0a", t_bp + 0.2, 0.3)
c.out("#s9-fine", t_bp)
for i in (1, 2, 3):
    c.to(f"#s9-R{i}", {"opacity": 1}, t_bp + 0.3 + 0.2 * i, 0.3, "none")
for i in range(4):
    c.pulse(f"#s9-R{i}", cue(9, "anything you'd actually send") + 0.12 * i, 1.02)
t_gb = cue(9, "give it the blocks")
drop_lines(c, "s9-so", 1, t_gb - 0.2)
rise_lines(c, "s9-gb", 1, t_gb)
rows = "".join(
    f'<div class="row9" id="s9-R{i}" style="background:{bg};color:{fg}"><span class="d" style="font-size:66px;line-height:.95">{num} {lab}</span>'
    + (f'<span class="rt"><span id="s9-r0a">{ROWS[0]}</span><span id="s9-r0b" style="position:absolute;left:0;opacity:0">What time is it in Tokyo?</span></span>'
       if i == 0 else f'<span class="rt">{ROWS[i]}</span>') + "</div>"
    for i, (num, lab, bg, fg) in enumerate(BLOCKS))
HTML[9] = f"""<div class="pn" id="s9a" style="background:{INK};color:{PAPER}">{chrome("s9a", 4)}
<h2 class="d" style="left:112px;top:130px;font-size:130px">{lines_html("s9-so", ["So."])}</h2>
<h2 class="d" style="left:112px;top:130px;font-size:130px">{lines_html("s9-gb", ["Give it the blocks."])}</h2>
<div class="stack9">{rows}</div>
<div class="stk" id="s9-fine" style="left:1200px;top:880px;background:var(--yellow);color:var(--ink)">Task only. Fine.</div></div>"""

# ================================================================ 10. Same prompt twice; end card
c = scene(10)
p0 = T[10]["start"] - XO
chrome_in(c, "s10a", p0)
rise_lines(c, "s10-q", 1, p0 + 0.3)
drop_lines(c, "s10-q", 1, cue(10, "Ask the same prompt twice") - 0.25)
t_sp = cue(10, "Ask the same prompt twice")
rise_lines(c, "s10-h", 1, t_sp)
t_2a = cue(10, "two different answers")
c.rise("#s10-a", t_2a, 40, 0.6)
c.rise("#s10-b", t_2a + 0.35, 40, 0.6)
pop(c, "#s10-bug", cue(10, "Is that a bug"), -4)
draw(c, "#s10-x", cue(10, "Nope"), 0.35)
t_nv = cue(10, "Next video")
wipe(c, "#s10b", t_nv - 0.3)
rise_lines(c, "s10-g", 1, t_nv)
c.fade("#s10-next", t_nv + 0.6)
c.fade("#s10-s1", t_nv + 0.9)
c.fade("#s10-s2", t_nv + 1.05)
pop(c, "#s10-sub", t_nv + 1.2, 0)
pop(c, "#s10-dot", cue(10, "I gotchu"), 0, "ding")
sk = lambda ws: "".join(f'<i class="sk" style="width:{w}%"></i>' for w in ws)
HTML[10] = f"""<div class="pn" id="s10a" style="background:{INK};color:{PAPER}">{chrome("s10a", 4)}
<h2 class="d" style="left:112px;top:170px;font-size:150px">{lines_html("s10-q", ["Quick thing…"])}</h2>
<h2 class="d" style="left:112px;top:170px;font-size:150px">{lines_html("s10-h", ["Same prompt. Twice."])}</h2>
<div class="rc small" id="s10-a" style="left:120px;top:420px;width:780px;opacity:0"><div class="hd"><span class="ai">AI</span><span class="m sm">Answer A</span></div>{sk([94, 71, 88, 52])}</div>
<div class="rc small" id="s10-b" style="left:1000px;top:420px;width:780px;opacity:0"><div class="hd"><span class="ai">AI</span><span class="m sm">Answer B</span></div>{sk([66, 90, 58, 80, 35])}</div>
<div class="stk" id="s10-bug" style="left:760px;top:820px;background:var(--yellow);color:var(--ink);font-size:44px">A bug?
<svg class="xout" viewBox="0 0 100 10" preserveAspectRatio="none"><path id="s10-x" pathLength="1" d="M0 6 L100 4"/></svg></div></div>
<div class="pn" id="s10b" style="background:{INK};color:{PAPER}">
<div class="m tl" style="opacity:.72">Ep 07 — Anatomy of a prompt</div>
<h1 class="d" style="left:104px;top:120px;font-size:330px">{lines_html("s10-g", ['I gotchu<span id="s10-dot" style="display:inline-block;color:var(--pink)">.</span>'])}</h1>
<div class="m" id="s10-next" style="left:120px;top:500px;color:var(--pink);opacity:0">Next ▸ Why AI gives a different answer every time</div>
<div class="slot" id="s10-s1" style="left:120px"><span class="m" style="font-size:26px;opacity:.7">Next video</span></div>
<div class="slot" id="s10-s2" style="left:790px"><span class="m" style="font-size:26px;opacity:.7">Best for you</span></div>
<div class="sub" id="s10-sub"><span class="m" style="color:#fff;font-size:26px">Subscribe</span></div></div>"""

# ================================================================ STYLES
GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
         "type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .5 0 0 0 0 .5 0 0 0 0 .5 0 0 0 .9 0'/%3E"
         "%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")")
BASE_F = f"""
*{{box-sizing:border-box}}
:root{{--paper:{PAPER};--paper-2:{PAPER2};--ink:{INK};--muted:{MUTED};--pink:{PINK};--yellow:{YELLOW};--blue:{BLUE};
 --f-d:"Bricolage Grotesque","Arial Narrow",sans-serif;--f-b:"DM Sans",Arial,sans-serif;--f-m:"JetBrains Mono",ui-monospace,monospace}}
html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:var(--ink)}}
#root{{position:relative;width:1920px;height:1080px;overflow:hidden;background:var(--ink);font-family:var(--f-b);font-weight:500}}
.layer{{position:absolute;left:0;top:0;width:1920px;height:1080px}}
.grain{{position:absolute;inset:0;background:{GRAIN};opacity:.13;mix-blend-mode:multiply;pointer-events:none}}
.sc{{position:absolute;inset:0}}
.pn{{position:absolute;inset:0;overflow:hidden;isolation:isolate}}
.pn>*{{position:absolute}}
.d{{font-family:var(--f-d);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75;letter-spacing:-.028em;line-height:.84;margin:0}}
.m{{font-family:var(--f-m);font-weight:700;font-size:28px;letter-spacing:.14em;text-transform:uppercase}}
.b{{font-size:52px;line-height:1.28;margin:0}}
.ln{{display:block;overflow:hidden;padding:.02em 0 .1em;margin-bottom:-.1em}}
.ln>span{{display:block}}
.tl{{left:120px;top:64px;opacity:0}}
.wm{{left:120px;bottom:58px;font-family:var(--f-d);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75;font-size:56px;line-height:1;letter-spacing:-.02em}}
.wm i{{font-style:normal;color:var(--pink)}}
.prog{{right:120px;bottom:72px;display:flex;gap:10px}}
.prog i{{width:64px;height:12px;border-radius:6px;background:currentColor;opacity:.16}}
.prog i.on{{opacity:1}}
.num{{font-family:var(--f-d);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75;font-size:1180px;line-height:.72;letter-spacing:-.05em;
 color:transparent;-webkit-text-stroke-width:4px;opacity:0;right:-60px;bottom:-150px}}
.cardh{{left:112px;top:290px;font-size:260px}}
.cs{{left:120px;top:560px;font-size:60px;font-weight:600;max-width:1300px;opacity:0}}
.cs2{{left:120px;top:660px;font-size:44px;opacity:0;max-width:1100px}}
#s6a .cs{{top:780px}}#s6a .cs2{{top:870px}}
.rw{{display:inline-block;margin-right:.3em}}
.stk{{font-family:var(--f-m);font-weight:700;font-size:30px;letter-spacing:.08em;text-transform:uppercase;padding:18px 28px;border-radius:14px;
 box-shadow:0 14px 30px rgba(17,22,20,.2);opacity:0;z-index:5;white-space:nowrap}}
.stamp{{font-family:var(--f-d);font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75;font-size:150px;line-height:.9;color:var(--pink);
 border:12px solid var(--pink);border-radius:22px;padding:18px 44px 28px;background:rgba(231,236,232,.92);opacity:0;z-index:6}}
.layer1{{display:flex;align-items:center;justify-content:space-between;height:150px;padding:0 40px;clip-path:inset(0% 100% 0% 0%)}}
.layer1 .d{{font-size:64px;line-height:1}}
.stack1{{left:1120px;right:0;top:260px;display:grid}}
.blur{{filter:blur(16px);opacity:.85}}
.q1{{left:120px;top:770px;width:820px;opacity:0}}
.qb{{display:flex;gap:10px;margin-top:14px}}.qb i{{flex:1;height:26px;border-radius:8px;transform-origin:0 50%}}
/* prompt + reply */
.pcol{{left:120px;top:250px;width:930px}}
.old{{font-size:34px;line-height:1.5;color:var(--muted);margin:0 0 26px;opacity:0}}
.hl-old{{padding:0 .12em;border-radius:.12em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
#s6b .old{{font-size:30px}}
.new{{margin:0;line-height:1.36;font-weight:600;opacity:0}}
.tg{{display:inline-grid;place-items:center;width:1.25em;height:1.25em;border-radius:50%;font:700 .56em/1 var(--f-m);vertical-align:.18em;margin-right:.3em;font-style:normal}}
.old .tg{{width:1.3em;height:1.3em;font-size:.7em}}
.hw{{position:relative;display:inline-block}}
.hw>span{{position:relative}}
.hb{{position:absolute;left:-.1em;right:-.22em;top:.14em;bottom:.02em;border-radius:.12em;transform-origin:0 50%}}
.rc{{box-sizing:border-box;width:670px;background:#fff;color:var(--ink);border-radius:36px;padding:40px 48px 46px;opacity:0;
 box-shadow:0 40px 90px rgba(17,22,20,.18),0 2px 0 rgba(17,22,20,.05)}}
.rc .hd{{display:flex;align-items:center;gap:16px;margin-bottom:22px}}
.rc .ai{{width:48px;height:48px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center;font:700 20px/1 var(--f-m);letter-spacing:.04em}}
.rc .sm{{font-size:26px;color:var(--muted)}}
.rc .tx{{font-size:50px;line-height:1.28;font-weight:500;letter-spacing:-.005em}}
.rc.full{{position:absolute;padding:34px 42px 38px}}
.rc.full .hd{{margin-bottom:16px}}
.rp{{margin:0 0 14px;font-size:27px;line-height:1.42;font-weight:500;opacity:0}}
#s2-r .rp{{font-size:25px}}
.rp .hb{{top:.08em;bottom:-.02em}}
.rc.small{{position:absolute;width:670px}}
.rc .sk{{display:block;height:30px;border-radius:10px;background:#DCE3DE;margin-top:22px}}
.w{{display:inline-block;opacity:0}}
.ringw{{position:relative}}
.ring{{position:absolute;left:-26%;top:-22%;width:152%;height:150%;overflow:visible}}
.hw .ring{{z-index:2}}
.ring path{{fill:none;stroke:var(--pink);stroke-width:7;stroke-linecap:round;vector-effect:non-scaling-stroke;stroke-dasharray:1;stroke-dashoffset:1}}
.xout{{position:absolute;left:-4%;top:40%;width:108%;height:24px;overflow:visible}}
.xout path{{fill:none;stroke:var(--pink);stroke-width:7;stroke-linecap:round;vector-effect:non-scaling-stroke;stroke-dasharray:1;stroke-dashoffset:1}}
/* blueprint */
.vcard{{top:520px;height:380px;border-radius:30px;padding:36px 44px;display:flex;flex-direction:column;justify-content:space-between;opacity:0;
 left:120px;width:620px;background:transparent;border:5px dashed rgba(17,22,20,.3);color:var(--ink)}}
.vcard.show{{left:800px;width:1000px;background:var(--blue);border:none;color:#fff;box-shadow:0 30px 60px rgba(35,67,224,.3)}}
/* 7 */
.stack7{{left:120px;right:120px;top:420px;display:grid;gap:0}}
.stack7 .layer1{{height:120px}}
.pbar{{left:120px;top:520px;width:900px;height:130px;border-radius:24px;background:#1C2320;display:flex;align-items:center;padding:0 44px;
 font-family:var(--f-m);font-weight:500;font-size:60px;color:var(--paper)}}
.ch{{display:none}}
.cur{{display:inline-block;width:.5em;height:.9em;background:var(--paper);margin-left:.1em}}
/* 8 */
.qs8{{left:1000px;right:120px;top:210px;display:grid;gap:22px;justify-items:start}}
.bub{{position:relative;display:flex;align-items:center;gap:22px;background:#fff;border-radius:28px 28px 28px 8px;padding:22px 32px;
 box-shadow:0 20px 50px rgba(17,22,20,.12);font-size:46px;font-weight:600;opacity:0}}
.bub .dot{{flex:none;width:22px;height:22px;border-radius:50%}}
/* 9 */
.stack9{{left:120px;right:120px;top:300px;display:grid}}
.row9{{display:grid;grid-template-columns:560px 1fr;align-items:center;height:138px;padding:0 48px;clip-path:inset(0% 100% 0% 0%)}}
.row9 .rt{{position:relative;font-size:44px;font-weight:600}}
/* 10 */
.slot{{top:580px;width:620px;height:349px;border-radius:24px;border:3px dashed rgba(231,236,232,.35);display:flex;align-items:flex-end;padding:26px 32px;opacity:0}}
.sub{{left:1480px;top:600px;width:310px;height:310px;border-radius:50%;background:var(--pink);display:grid;place-items:center;opacity:0}}
"""

# ================================================================ WRITE FILES
os.makedirs(f"{OUT}/compositions", exist_ok=True)
os.makedirs(f"{OUT}/assets/fonts", exist_ok=True)
for f in ["gsap.min.js", "CustomEase.min.js"]:
    shutil.copy(f"video/assets/{f}", f"{OUT}/assets/{f}")
for f in os.listdir("video/assets/fonts"):
    shutil.copy(f"video/assets/fonts/{f}", f"{OUT}/assets/fonts/")

grain = Comp("grain", 0, TOTAL)
open(f"{OUT}/compositions/grain.html", "w").write(comp_file("grain", '<div class="grain"></div>', "", grain.A, TOTAL))
mounts = []
for n in range(1, 11):
    c = SCENES[n]
    cid = c.cid
    anchor = re.split(r"[.,?!]", SL[n]["text"])[0][:40].replace('"', "").replace("Here's where", "where")
    inner = f'<div class="sc">{HTML[n]}</div>'
    A = [re.sub(r'tl\.(fromTo|to|set)\("(\.[^"]+)"', lambda m: f'tl.{m.group(1)}(\'[data-composition-id="{cid}"] {m.group(2)}\'', a) for a in c.A]
    open(f"{OUT}/compositions/{cid}.html", "w").write(comp_file(cid, inner, "", A, c.dur, f' data-anchor="{anchor}"'))
    mounts.append(f'<div class="layer" id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                  f'data-start="{c.start}" data-duration="{c.dur}" data-track-index="{1 + n % 2}" data-width="1920" data-height="1080" '
                  f'data-anchor="{anchor}"></div>')
mounts.append('<div class="layer" id="grain" data-composition-id="grain" data-composition-src="compositions/grain.html" data-start="0" '
              f'data-duration="{TOTAL}" data-track-index="5" data-width="1920" data-height="1080" style="z-index:50;pointer-events:none"></div>')
root = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<title>igotchu Ep 07: Anatomy of a prompt (Frames)</title>
<script src="assets/gsap.min.js"></script><script src="assets/CustomEase.min.js"></script>
<script>
  gsap.registerPlugin(CustomEase);
  CustomEase.create("igOut","0.2,0.8,0.2,1");
  CustomEase.create("igSnap","0.3,1.45,0.5,1");
  CustomEase.create("igPop","0.34,1.56,0.64,1");
  CustomEase.create("igSlam","0.7,0,0.84,0");
  CustomEase.create("igIO","0.65,0,0.35,1");
  CustomEase.create("igIn","0.5,0,0.75,0");
  CustomEase.create("igSettle","0.22,1,0.36,1");
  CustomEase.create("igWipe","0.75,0,0.2,1");
</script>
<style>{FONTS}{BASE_F}</style></head>
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
open(f"{OUT}/index.html", "w").write(root)
words = []
for n in range(1, 11):
    for m in re.finditer(r"\S+", SL[n]["text"]):
        words.append({"text": re.sub(r'^[\"“(]+|[\"”),.?!:;]+$', "", m.group(0)), "start": time_at_char(n, m.start())})
json.dump({"words": words}, open(f"{OUT}/assets/transcript.json", "w"))
spans = sorted(MOTION)
gaps, cur = [], 0.0
for a, b in spans:
    if a - cur > 3.2:
        gaps.append((round(cur, 2), round(a, 2)))
    cur = max(cur, b)
print(f"wrote {OUT}/index.html + {len(SCENES) + 1} compositions, {TOTAL}s")
print("frozen stretches > 3.2 s:", gaps if gaps else "none")
json.dump(SFX, open("sfx_events_frames.json", "w"))
