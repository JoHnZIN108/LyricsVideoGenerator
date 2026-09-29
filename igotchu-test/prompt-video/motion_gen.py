"""Ep 07 "Anatomy of a good prompt", motion-broll build on the user's own voice.

One clip per recorded section (myvoice/sections.json), each one continuous shape that morphs between states
(motion-broll engine, .claude/skills/motion-broll). Every reveal, highlight and typed line is timed from the
word timings in myvoice/words.json: highlights sweep across a phrase while it is spoken, typing runs over the
spoken span, chips and ticks land on their word.

Look: motion-broll default (warm grey canvas, black and white shapes) with the four block colours as accents.
A strip of four block slots sits at the top of every clip; each label stays blurred until that block is spoken.
Writes motion/clips/NN-name.html and motion/plan.json.
"""
import html
import json
import os
import re

W = json.load(open("myvoice/words.json"))
S = json.load(open("myvoice/sections.json"))
WORDS = W["words"]
PARAS = [s["text"] for s in S]
OFF, o = [], 0
for p in PARAS:
    OFF.append(o)
    o += len(p) + 1

INK, CANVAS, CARD, SKEL = "#0B0B0B", "#E9E7E2", "#FFFFFF", "#E3DFD8"
BLK = [("01", "The task", "#2B302D", "#FFFFFF", "rgba(43,48,45,.17)"),
       ("02", "The context", "#FF3D7F", "#FFFFFF", "rgba(255,61,127,.30)"),
       ("03", "The rules", "#FFC21A", INK, "rgba(255,194,26,.55)"),
       ("04", "The examples", "#2343E0", "#FFFFFF", "rgba(35,67,224,.22)")]


# ---------------------------------------------------------------- timing from the user's words
def _find(k, phrase, nth=0):
    txt = PARAS[k].lower()
    i = -1
    for _ in range(nth + 1):
        i = txt.find(phrase.lower(), i + 1)
    if i < 0:
        raise KeyError(f"section {k + 1}: {phrase!r}")
    return OFF[k] + i


def _word_at(gi):
    best = WORDS[0]
    for w in WORDS:
        if w["char"] <= gi:
            best = w
        else:
            break
    return best


def wt(k, phrase, nth=0):
    """Clip-local time when `phrase` starts being spoken in section k."""
    return round(_word_at(_find(k, phrase, nth))["start"] - S[k]["start"], 3)


def span(k, first, last):
    """Clip-local (start, end) from the first word of `first` to the last word of `last`."""
    a = _find(k, first)
    b = _find(k, last) + len(last) - 1
    return round(_word_at(a)["start"] - S[k]["start"], 3), round(_word_at(b)["end"] - S[k]["start"], 3)


# ---------------------------------------------------------------- html helpers (timed by data attributes)
e = html.escape


def ap(inner, tin, tout=None, cls="", style=""):
    out = f' data-out="{tout}"' if tout is not None else ""
    return f'<div class="ap {cls}" data-in="{tin}"{out} style="{style}">{inner}</div>'


def hl(text, t0, t1, color):
    """Highlight sweeping word by word across `text` between t0 and t1 (letter share)."""
    ws = text.split(" ")
    lens = [max(1, len(re.sub(r"\W", "", x))) for x in ws]
    tot, t, out = sum(lens), t0, []
    for x, n in zip(ws, lens):
        d = (t1 - t0) * n / tot
        out.append(f'<span class="hw" data-a="{t:.3f}" data-b="{t + d * 0.95:.3f}" '
                   f'style="background-image:linear-gradient({color},{color})">{e(x)}</span>')
        t += d
    return " ".join(out)


def typed(text, t0, t1):
    return f'<span class="ty" data-a="{t0}" data-b="{t1}" data-text="{e(text)}"></span><span class="caret"></span>'


def skel(widths, top, gap=34, color=SKEL, h=16, left=0):
    return "".join(f'<div class="sk" style="left:{left}px;top:{top + i * gap}px;width:{w}px;height:{h}px;background:{color}"></div>'
                   for i, w in enumerate(widths))


FULL = {
    "01": ["Here's a warm, general birthday message you can use as it is or adapt:", "<b>Happy Birthday, Mum!</b>",
           "{Q}", "So much of who I am comes from you: your kindness, your strength, and the way you always make home feel like home.",
           "I hope today brings you as much joy as you've given everyone around you. You deserve every bit of celebration, and so much more.",
           "I love you more than words can say.", "With all my love,<br>Johnson"],
    "02": ["Happy 60th, Mum!", "Thirty years of nursing, and you've finally retired. {Q}",
           "Sixty suits you. You've spent three decades telling people to rest, drink more water and stop googling their symptoms, so now it's your turn. Try following your own advice for once. (I know you won't.)",
           "Thanks for being the funniest person in any room, including the waiting room. I promise not to make this soppy, so I'll just say you're alright, really.",
           "Love you (there, I said it, don't make it weird),<br>[Your name]"],
    "03": ["Happy 60th, Mum! {Q} Lucky us. Enjoy retirement. You've earned the lie-ins, the gossip and the right to diagnose everyone at dinner. Here's to the next thirty. Love you (don't make it weird)."],
    "04": ["Happy 60th, Mum! Thirty years of bossing doctors around, and now you're free to boss us full-time. Lucky us. {Q}"],
}
QUOTE = {
    "01": "Thank you for the love, the patience, and all the times you believed in me before I believed in myself.",
    "02": "The NHS will have to find someone else to give that look to patients who say “it's probably nothing.”",
    "03": "Thirty years of bossing doctors around, and now you're free to boss us full-time.",
    "04": "Thanks for every plaster, every pep talk, and every “I told you so.” Love you (don't get soppy).",
}
DAD = ("Happy 62nd, Dad. Still the only man who reads the instructions after breaking the thing. Thanks for every lift, "
       "every loan, and every lecture about tyre pressure. Love you (don't get emotional).")
PROMPT = {1: "Write a birthday message for my mum.",
          2: "She's turning sixty. She just retired from thirty years as a nurse. She's funny, a bit sarcastic, and she would cringe at anything too soppy.",
          3: "Keep it under fifty words. It's going in a card, so no emojis, and don't use the word 'queen'.",
          4: "Here's the birthday message I wrote for my dad this year. Use it as a style and length example."}


def reply(key, t0, t1, color, extra=""):
    q = hl(QUOTE[key], t0, t1, color) if t0 is not None else e(QUOTE[key])
    ps = "".join(f'<p class="rp">{p.replace("{Q}", q)}</p>' for p in FULL[key])
    return f'<div class="rhd"><span class="ai">AI</span><span class="mono lbl">Reply</span></div>{ps}{extra}'


def fit_h(paras, width, font=30, lh=1.42, gap=14, head=76, pad=76):
    """Rough height of a text block: lines per paragraph from character count (Geist ~0.52 em per char)."""
    import math
    per = max(1, int(width / (font * 0.47)))
    lines = sum(max(1, math.ceil(len(re.sub(r"<[^>]+>", "", p)) / per)) + p.count("<br>") for p in paras)
    return int(head + pad + lines * font * lh + len(paras) * gap)


def reply_h(key, width):
    return fit_h([p.replace("{Q}", QUOTE[key]) for p in FULL[key]], width - 80)


def tag(k, size=40):
    num, _, bg, fg, _ = BLK[k - 1]
    return f'<span class="tg" style="background:{bg};color:{fg};width:{size}px;height:{size}px">{k}</span>'


def words_in(s):
    return len(re.findall(r"[A-Za-z0-9'’]+", re.sub(r"<[^>]+>", " ", s)))


# ---------------------------------------------------------------- clip template
CSS = """
.L .box{position:absolute;box-sizing:border-box}
.ap{position:relative}
.hw{position:relative;background-repeat:no-repeat;background-size:0% 86%;background-position:0 70%;border-radius:6px;padding:0 2px;margin:0 -2px;-webkit-box-decoration-break:clone}
.caret{display:inline-block;width:3px;height:1em;background:#0B0B0B;vertical-align:-0.12em;margin-left:3px}
.sk{position:absolute;border-radius:8px}
.chap{position:absolute;transform:translate(-50%,-50%);display:flex;align-items:center;gap:26px;white-space:nowrap;font-weight:650;letter-spacing:-.02em}
.chap .n{font-family:'Geist Mono';font-size:30px;opacity:.7}
.card{position:absolute;box-sizing:border-box;text-align:left}
.rhd{display:flex;align-items:center;gap:14px;margin-bottom:16px}
.ai{width:44px;height:44px;border-radius:50%;background:#2343E0;color:#fff;display:grid;place-items:center;font:600 18px/1 'Geist Mono'}
.lbl{font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:#8A867F}
.rp{margin:0 0 14px;font-size:30px;line-height:1.42;color:#0B0B0B}
.tg{display:inline-grid;place-items:center;border-radius:50%;font:600 20px/1 'Geist Mono';margin-right:14px;vertical-align:2px;flex:none}
.pline{display:flex;align-items:flex-start;margin:0 0 16px}
.old{font-size:24px;line-height:1.5;color:#8A867F}
.new{font-size:40px;line-height:1.36;font-weight:550;color:#0B0B0B}
.chip{display:inline-flex;align-items:center;gap:12px;padding:14px 26px;border-radius:999px;font-size:30px;font-weight:600;white-space:nowrap}
.slot{position:absolute;width:300px;height:64px;border-radius:32px;display:flex;align-items:center;gap:16px;padding:0 24px;box-sizing:border-box;transform-origin:50% 50%}
.slot .sn{font:600 20px/1 'Geist Mono';opacity:.75}
.slot .sl{font-size:25px;font-weight:650;letter-spacing:-.01em;white-space:nowrap}
.strike{position:absolute;left:-4px;right:-4px;top:52%;height:4px;background:#0B0B0B;transform-origin:0 50%}
.dq{border-left:5px solid #2343E0;padding:6px 0 6px 22px;font-size:25px;line-height:1.45;color:#0B0B0B;background:rgba(35,67,224,.06);border-radius:0 12px 12px 0}
"""

COMMON_JS = """
const $=id=>document.getElementById(id);
const APS=[...document.querySelectorAll('.ap')].map(el=>[el,+el.dataset.in,el.dataset.out!==undefined?+el.dataset.out:null]);
const HWS=[...document.querySelectorAll('.hw')].map(el=>[el,+el.dataset.a,+el.dataset.b]);
const TYS=[...document.querySelectorAll('.ty')].map(el=>[el,+el.dataset.a,+el.dataset.b,el.dataset.text]);
const STR=[...document.querySelectorAll('.strike')].map(el=>[el,+el.dataset.a]);
function common(t){
 for(const [el,a,b] of APS){const v=M.vis(t,a,b,{din:0,lin:0.3,lout:0.18}); if(v.o<0.002){el.style.visibility='hidden';continue;}
   el.style.visibility='visible'; el.style.opacity=v.o.toFixed(3); el.style.filter=v.blur>0.05?`blur(${v.blur.toFixed(2)}px)`:'none';
   el.style.transform=`translateY(${((1-v.a)*14).toFixed(2)}px)`;}
 for(const [el,a,b] of HWS){el.style.backgroundSize=(M.clamp((t-a)/Math.max(0.04,b-a))*100).toFixed(2)+'% 86%';}
 for(const [el,a,b,s] of TYS){M.setText(el,s.slice(0,Math.round(s.length*M.clamp((t-a)/Math.max(0.05,b-a)))));}
 for(const [el,a] of STR){el.style.transform=`scaleX(${M.eio((t-a)/0.35).toFixed(3)})`;}
}
function slots(t){
 for(let i=0;i<4;i++){const c=SLOTS[i], el=$('slot'+i), lab=$('slotl'+i);
  const v=M.vis(t,c.show,null,{din:0,lin:0.35}); if(v.o<0.002){el.style.visibility='hidden';continue;} el.style.visibility='visible';
  const rv=c.rev===null?0:(c.rev<0?1:M.eo((t-c.rev)/0.55)); const bl=14*(1-rv);
  lab.style.filter=bl>0.05?`blur(${bl.toFixed(2)}px)`:'none';
  let s=1; for(const p of c.pulse){const u=(t-p)/0.45; if(u>0&&u<1) s+=0.12*Math.sin(Math.PI*u);}
  el.style.opacity=(v.o*OPS[i](t)).toFixed(3); el.style.transform=`translateY(${((1-v.a)*-20).toFixed(1)}px) scale(${s.toFixed(4)})`;}
}
"""


def slot_html():
    xs = [-495, -165, 165, 495]
    out = []
    for i, (num, lab, bg, fg, _) in enumerate(BLK):
        out.append(f'<div class="slot" id="slot{i}" style="left:{xs[i] - 150}px;top:-482px;background:{bg};color:{fg}">'
                   f'<span class="sn">{num}</span><span class="sl" id="slotl{i}">{lab}</span></div>')
    return "".join(out)


def clip(cid, name, k, T, states, start, seq, layers, slots, cursor=None, world="", extra_js="", ops=None):
    """states: {name:(w,h,r,bg)}; layers: [(html, tin, tout, anchor)]; slots: per slot {show,rev,pulse};
    ops: per slot list of [t, opacity] keys."""
    SH = {n: {"w": w, "h": h, "r": r, "bg": bg, "cam": 1} for n, (w, h, r, bg) in states.items()}
    L_html, L_cfg = [], []
    for i, (h, tin, tout, an) in enumerate(layers):
        L_html.append(f'<div class="L" id="L{i}">{h}</div>')
        L_cfg.append({"el": f"L{i}", "tin": tin, "tout": tout, "anchor": an, "o": {"din": 0.05}})
    ops = ops or [[] for _ in range(4)]
    js = (COMMON_JS
          + f"const SLOTS={json.dumps(slots)};\n"
          + "const OPS=" + json.dumps(ops) + ".map(k=>M.track(1,k,M.SOFT));\n"
          + extra_js
          + "M.scene({W:1920,H:1080,bg:'" + CANVAS + "',T:" + str(T) + ",intro:" + ("0.12" if k == 0 else "null") + ","
          + "SH:" + json.dumps(SH) + ",start:" + json.dumps(start) + ",SEQ:" + json.dumps(seq) + ","
          + "layers:" + json.dumps(L_cfg) + ","
          + ("cursor:" + json.dumps(cursor) + "," if cursor else "")
          + "geom:(t,g)=>{g.cy=58; if(typeof GEOM==='function') GEOM(t,g); return g;},"
          + "extra:(t,g)=>{common(t);slots(t); if(typeof EXTRA==='function') EXTRA(t,g);}});\n")
    frag = (f"<title>{cid} {name}</title>\n<style>{CSS}</style>\n"
            f'<div data-slot="world">{slot_html()}</div><!--/world-->\n'
            f'<div data-slot="shape">{"".join(L_html)}</div><!--/shape-->\n<div data-slot="over">{world}</div><!--/over-->\n<script>{js}</script>\n')
    os.makedirs("motion/clips", exist_ok=True)
    fn = f"motion/clips/{cid}-{name}.html"
    open(fn, "w").write(frag)
    return fn


def dur(k):
    return round(S[k]["end"] - S[k]["start"], 3)


REV = [None, None, None, None]  # when each slot label was revealed (clip-local only in its own clip; -1 after)


def slotcfg(show=None, rev=None, pulse=None):
    out = []
    for i in range(4):
        out.append({"show": (show[i] if show else -1), "rev": (rev[i] if rev else None), "pulse": (pulse[i] if pulse else [])})
    return out


PLAN = []


def add_plan(k, cid, name, fn, title):
    PLAN.append({"id": cid, "title": title, "line": PARAS[k][:90] + "…", "in": S[k]["start"], "out": S[k]["end"],
                 "kind": "full", "html": fn, "file": f"out/{cid}-{name}.mp4"})


# ================================================================ 1. Intro
k = 0
T = dur(k)
t_use, t_bri, t_four = wt(k, "useless"), wt(k, "brilliant"), wt(k, "four small parts")
t_one, t_build, t_bat = wt(k, "Most people only use one"), wt(k, "We're going to build"), wt(k, "one block at a time")
t_every, t_end, t_trick = wt(k, "watch the answer"), wt(k, "And at the end"), wt(k, "a trick")
title = f'<div class="chap" style="color:#fff;font-size:66px">Anatomy of a good prompt</div>'
cmp_ = (f'<div class="card" style="left:-620px;top:70px;width:1240px">'
        f'<div style="position:absolute;left:0;top:0;width:560px">'
        + ap(f'<div class="mono lbl" style="margin-bottom:26px">Useless answer</div><div style="position:relative;height:200px">{skel([520, 460, 500, 300], 0)}</div>', t_use)
        + "</div>"
        f'<div style="position:absolute;left:660px;top:0;width:580px">'
        + ap('<div class="mono lbl" style="margin-bottom:26px;color:#0B0B0B">Brilliant answer</div><div style="position:relative;height:200px">'
             + "".join(f'<div class="sk" style="left:0;top:{i * 34}px;width:{w}px;height:16px;background:{BLK[i][2]}"></div>'
                       for i, w in enumerate([540, 470, 510, 330])) + "</div>", t_bri)
        + "</div></div>")
segs = "".join(f'<div id="seg{i}" style="position:absolute;left:{-560 + i * 285}px;top:100px;width:265px;height:70px;border-radius:18px;'
               f'border:3px dashed #BDB8B0;box-sizing:border-box"></div>' for i in range(4))
parts = (f'<div class="card" style="left:-560px;top:34px;width:1120px"><div class="mono lbl">Your message</div></div>{segs}')
meter = ('<div class="card" style="left:-520px;top:40px;width:1040px"><div class="mono lbl" style="margin-bottom:22px">Answer quality</div></div>'
         + "".join(f'<div id="q{i}" style="position:absolute;left:{-520 + i * 265}px;top:100px;width:245px;height:44px;border-radius:12px;background:{BLK[i][2]};transform-origin:0 50%"></div>'
                   for i in range(4)))
trick = (f'<div class="chap" style="color:#fff;font-size:48px">{"<span id=spk></span>"}'
         + ap("A trick that writes the entire prompt for you", t_trick) + "</div>")
states = {"title": (1240, 190, 95, INK), "cmp": (1400, 400, 40, CARD), "parts": (1300, 250, 36, CARD),
          "meter": (1200, 220, 36, CARD), "trick": (1260, 150, 75, INK)}
seq = [[t_use - 0.15, "cmp"], [t_four - 0.1, "parts"], [t_build - 0.1, "meter"], [t_end, "trick"]]
layers = [(title, 0.12, t_use - 0.15, "c"), (cmp_, t_use - 0.15, t_four - 0.1, "t"), (parts, t_four - 0.1, t_build - 0.1, "t"),
          (meter, t_build - 0.1, t_end, "t"), (trick, t_end, None, "c")]
sc = slotcfg(show=[t_four + i * 0.14 for i in range(4)], rev=[None] * 4, pulse=[[t_one + 0.2], [], [], []])
ops = [[], [[t_one + 0.2, 0.3], [t_bat + 0.3, 1]], [[t_one + 0.2, 0.3], [t_bat + 0.55, 1]], [[t_one + 0.2, 0.3], [t_bat + 0.8, 1]]]
ex = ("$('spk').innerHTML=M.icon('sparkle',46,'#FFC21A');\n"
      f"const TONE={t_one + 0.15}, TSEG={t_four + 0.3};\n"
      "function EXTRA(t){for(let i=0;i<4;i++){const s=$('seg'+i); if(!s) continue; const f=(i==0?M.eo((t-TONE)/0.4):0);"
      f" s.style.background=f>0?`rgba(43,48,45,${{f.toFixed(3)}})`:'transparent';"
      f" const q=$('q'+i); q.style.transform=`scaleX(${{M.eio((t-{t_every}-0.1-i*0.55)/0.4).toFixed(3)}})`;}}}}\n")
fn = clip("01", "intro", k, T, states, "title", seq, layers, sc, extra_js=ex, ops=ops)
add_plan(k, "01", "intro", fn, "Intro: four blocks, names blurred")

ALLSHOW = [-1, -1, -1, -1]

# ================================================================ 2. Block 1: the task
k = 1
T = dur(k)
t_task, t_most = wt(k, "The task"), wt(k, "Most people just prompt")
w0, w1 = span(k, "Write a birthday message for my mum", "for my mum")
t_back = wt(k, "and would get back")
q0, q1 = span(k, "Thank you for the love", "believed in myself")
t_fine, t_petrol = wt(k, "It's fine"), wt(k, "petrol station")
t_wbm, t_isa = wt(k, "Write a birthday message is a task"), wt(k, "is a task")
t_every, t_other = wt(k, "Everyone gets this block"), wt(k, "It's the other three")
b0, b1 = span(k, "Write a birthday message is a task", "birthday message is")
chap = f'<div class="chap" style="color:#fff;font-size:64px"><span class="n">01</span>The task</div>'
sub = ap('<div class="chip" style="background:rgba(255,255,255,.12);color:#fff;margin-top:0">The one block everyone gets right</div>', wt(k, "This is the one block"),
         style="position:absolute;left:-230px;top:70px")
bar = (f'<div class="card" style="left:-660px;top:-26px;width:1200px;font-size:40px;font-weight:550;white-space:nowrap">'
       f'<span class="mono" style="color:#8A867F;margin-right:18px">&gt;</span>{typed(PROMPT[1], w0, w1)}</div>'
       f'<div id="send" style="position:absolute;left:560px;top:-40px;width:80px;height:80px;border-radius:50%;background:{INK};display:grid;place-items:center"><span id="sendi"></span></div>')
click = round(w1 + 0.35, 3)
rep = (f'<div class="card" style="left:-640px;top:40px;width:1280px">{reply("01", q0, q1, BLK[0][4])}</div>'
       + ap('<div class="chip" style="background:#FFC21A;color:#0B0B0B;transform:rotate(-3deg)">Greeting card from a petrol station</div>', t_petrol,
            style=f"position:absolute;left:180px;top:{reply_h('01', 1360) - 110}px"))
task2 = (f'<div class="card" style="left:-640px;top:50px;width:1280px;font-size:44px;font-weight:550;white-space:nowrap">'
         f'{tag(1)}{hl("Write a birthday message", b0, b1, BLK[0][4])} for my mum.</div>'
         + ap(f'<div class="chip" style="background:{BLK[0][2]};color:#fff">= the task</div>', t_isa, style="position:absolute;left:-640px;top:150px")
         + ap('<div class="chip" style="background:#fff;border:2px solid #0B0B0B;color:#0B0B0B"><span id="ck"></span>Everyone gets this block</div>', t_every,
              style="position:absolute;left:-350px;top:150px")
         + ap('<div class="chip" style="background:transparent;border:3px dashed #BDB8B0;color:#8A867F">+ three more blocks</div>', t_other,
              style="position:absolute;left:120px;top:150px"))
states = {"chap": (820, 150, 75, BLK[0][2]), "bar": (1400, 150, 75, CARD), "reply": (1360, reply_h("01", 1360), 36, CARD), "task2": (1400, 290, 44, CARD)}
seq = [[t_most - 0.2, "bar"], [click + 0.1, "reply"], [t_wbm - 0.15, "task2"]]
layers = [(chap + sub, None, t_most - 0.2, "c"), (bar, t_most - 0.2, click + 0.1, "c"), (rep, click + 0.1, t_wbm - 0.15, "t"),
          (task2, t_wbm - 0.15, None, "t")]
sc = slotcfg(show=ALLSHOW, rev=[t_task, None, None, None], pulse=[[t_task], [t_other + 0.1], [t_other + 0.3], [t_other + 0.5]])
cur = {"size": 44, "clicks": [click], "keys": [[0, 700, 400], [w1 - 0.6, 700, 400], [click - 0.05, 600, 0], [click + 0.6, 640, 120], [T, 640, 120]]}
ex = "$('sendi').innerHTML=M.icon('arrow',34,'#fff',2.6); $('ck').innerHTML=M.icon('check',24,'#0B0B0B',3);\n"
fn = clip("02", "task", k, T, states, "chap", seq, layers, sc, cursor=cur, extra_js=ex)
add_plan(k, "02", "task", fn, "Block 1: the task")

# ================================================================ 3. Block 2: the context
k = 2
T = dur(k)
t_stuff, t_ex = wt(k, "the stuff"), wt(k, "For example")
c0, c1 = span(k, "my mum's turning sixty", "too soppy")
t_now = wt(k, "Now look at the response")
n0, n1 = span(k, "The NHS will have", "probably nothing")
t_n, t_r, t_h = wt(k, "the nursing"), wt(k, "the retirement"), wt(k, "the sense of humor")
t_same, t_diff = wt(k, "It's the same AI"), wt(k, "The difference is the context")
chap = (f'<div class="chap" style="color:#fff;font-size:64px"><span class="n">02</span>The context</div>'
        + ap('<div class="chip" style="background:rgba(255,255,255,.2);color:#fff">The stuff in your head AI can’t see</div>', t_stuff,
             style="position:absolute;left:-270px;top:70px"))
click = round(t_now - 0.1, 3)
pr = (f'<div class="card" style="left:-700px;top:50px;width:1400px">'
      f'<div class="pline old">{tag(1, 34)}<span>{e(PROMPT[1])}</span></div>'
      f'<div class="pline new">{tag(2)}<span>{hl(PROMPT[2], c0, c1, BLK[1][4])}</span></div></div>'
      f'<div id="send" style="position:absolute;left:600px;top:290px;width:80px;height:80px;border-radius:50%;background:{INK};display:grid;place-items:center"><span id="sendi"></span></div>')
chips = "".join(ap(f'<div class="chip" style="background:{BLK[1][2]};color:#fff">{lab}</div>', tt, style="display:inline-block;margin-right:14px")
                for lab, tt in (("Nursing", t_n), ("Retirement", t_r), ("Sense of humour", t_h)))
rep = (f'<div class="card" style="left:-660px;top:40px;width:1320px">{reply("02", n0, n1, BLK[1][4])}</div>'
       f'<div style="position:absolute;left:-660px;top:{reply_h("02", 1400) - 40}px;width:1320px">{chips}</div>')
same = (f'<div class="chap" style="color:#fff;font-size:50px">' + ap("Same AI.", t_same) + ap("&nbsp;The difference is the context.", t_diff) + "</div>")
states = {"chap": (1000, 150, 75, BLK[1][2]), "prompt": (1520, 400, 36, CARD), "reply": (1400, reply_h("02", 1400) + 60, 36, CARD), "same": (1300, 150, 75, BLK[1][2])}
seq = [[t_ex - 0.2, "prompt"], [click + 0.1, "reply"], [t_same - 0.15, "same"]]
layers = [(chap, None, t_ex - 0.2, "c"), (pr, t_ex - 0.2, click + 0.1, "t"), (rep, click + 0.1, t_same - 0.15, "t"), (same, t_same - 0.15, None, "c")]
sc = slotcfg(show=ALLSHOW, rev=[-1, 0.15, None, None], pulse=[[], [0.15, t_diff], [], []])
cur = {"size": 44, "clicks": [click], "keys": [[0, 760, 420], [c1 - 0.4, 760, 420], [click - 0.05, 640, 240], [click + 0.6, 700, 360], [T, 700, 360]]}
ex = "$('sendi').innerHTML=M.icon('arrow',34,'#fff',2.6);\n"
fn = clip("03", "context", k, T, states, "chap", seq, layers, sc, cursor=cur, extra_js=ex)
add_plan(k, "03", "context", fn, "Block 2: the context")

# ================================================================ 4. Block 3: the rules
k = 3
T = dur(k)
t_len, t_tone, t_avoid = wt(k, "length"), wt(k, "tone"), wt(k, "what to avoid")
t_ex = wt(k, "For example")
r0, r1 = span(k, "keep it under fifty words", "the word queen")
t_call, t_stop, t_now = wt(k, "call your mum queen"), wt(k, "The rules stop"), wt(k, "Now the AI response")
b0, b1 = span(k, "Thirty years of bossing", "full time")
chips = "".join(ap(f'<div class="chip" style="background:#fff;color:#0B0B0B">{lab}</div>', tt, style="display:inline-block;margin-right:16px")
                for lab, tt in (("Length", t_len), ("Tone", t_tone), ("What to avoid", t_avoid)))
chap = (f'<div class="chap" style="color:#0B0B0B;font-size:64px"><span class="n">03</span>The rules</div>'
        f'<div style="position:absolute;left:-330px;top:90px;white-space:nowrap">{chips}</div>')
rules_txt = hl(PROMPT[3], r0, r1, BLK[2][4]).replace("&#x27;queen&#x27;.</span>", '&#x27;queen&#x27;.<i class="strike" data-a="' + str(t_call) + '"></i></span>')
assert 'class="strike"' in rules_txt
click = round(t_now - 0.1, 3)
pr = (f'<div class="card" style="left:-700px;top:50px;width:1400px">'
      f'<div class="pline old">{tag(1, 34)}<span>{e(PROMPT[1])} {e(PROMPT[2])}</span></div>'
      f'<div class="pline new">{tag(3)}<span>{rules_txt}</span></div></div>'
      + ap('<div class="chip" style="background:#0B0B0B;color:#fff">Stops the stuff you’d delete anyway</div>', t_stop, style="position:absolute;left:-700px;top:380px")
      + f'<div id="send" style="position:absolute;left:600px;top:370px;width:80px;height:80px;border-radius:50%;background:{INK};display:grid;place-items:center"><span id="sendi"></span></div>')
nw = words_in(FULL["03"][0].replace("{Q}", QUOTE["03"]))
rep = (f'<div class="card" style="left:-660px;top:40px;width:1320px">{reply("03", b0, b1, BLK[2][4])}</div>'
       + ap(f'<div class="chip" style="background:{BLK[2][2]};color:#0B0B0B">{nw} words · no emojis · no “queen”</div>', b1 + 0.2,
            style=f"position:absolute;left:-660px;top:{reply_h('03', 1400) - 30}px"))
states = {"chap": (900, 150, 75, BLK[2][2]), "prompt": (1520, 470, 36, CARD), "reply": (1400, reply_h("03", 1400) + 70, 36, CARD)}
seq = [[t_ex - 0.2, "prompt"], [click + 0.1, "reply"]]
layers = [(chap, None, t_ex - 0.2, "c"), (pr, t_ex - 0.2, click + 0.1, "t"), (rep, click + 0.1, None, "t")]
sc = slotcfg(show=ALLSHOW, rev=[-1, -1, 0.15, None], pulse=[[], [], [0.15], []])
cur = {"size": 44, "clicks": [click], "keys": [[0, 760, 420], [t_stop, 760, 420], [click - 0.05, 640, 270], [click + 0.6, 700, 380], [T, 700, 380]]}
ex = "$('sendi').innerHTML=M.icon('arrow',34,'#fff',2.6);\n"
fn = clip("04", "rules", k, T, states, "chap", seq, layers, sc, cursor=cur, extra_js=ex)
add_plan(k, "04", "rules", fn, "Block 3: the rules")

# ================================================================ 5. Block 4: the examples
k = 4
T = dur(k)
t_desc, t_prov, t_one, t_pow = wt(k, "Don't just describe"), wt(k, "Provide an example"), wt(k, "This is the one"), wt(k, "most powerful")
t_style, t_mirror, t_provit = wt(k, "If you have a specific style"), wt(k, "mirror"), wt(k, "provide it")
h0, h1 = span(k, "Here's the birthday message", "length example")
t_look = wt(k, "Now look at a portion")
x0, x1 = span(k, "Thanks for every plaster", "get soppy")
t_list, t_sign, t_samelen = wt(k, "Same kind of list"), wt(k, "same kind of sign-off"), wt(k, "same length")
t_never, t_cas, t_show, t_blue = wt(k, "You never had to explain"), wt(k, "Telling AI be casual"), wt(k, "Showing it an example"), wt(k, "that's a blueprint")
chap = f'<div class="chap" style="color:#fff;font-size:64px"><span class="n">04</span>The examples</div>'
duo = ('<div class="chap" style="font-size:46px;color:#0B0B0B;gap:40px">'
       + ap('<span style="position:relative;display:inline-block">Describe it<i class="strike" data-a="' + str(t_prov) + '"></i></span>', t_desc)
       + ap(f'<span class="chip" style="background:{BLK[3][2]};color:#fff;font-size:40px">Show it an example</span>', t_prov) + "</div>")
pw = ('<div class="chap" style="color:#fff;font-size:46px">' + ap("The one most people don’t use", t_one)
      + ap('<span class="chip" style="background:#FFC21A;color:#0B0B0B;margin-left:22px"><span id="spk"></span>Most powerful</span>', t_pow) + "</div>")
drop = round(t_provit + 0.1, 3)
pr = (f'<div class="card" style="left:-720px;top:44px;width:1440px">'
      f'<div class="pline old">{tag(1, 30)}<span style="font-size:20px">{e(PROMPT[1])} {e(PROMPT[2])} {e(PROMPT[3])}</span></div>'
      + ap(f'<div class="pline new" style="font-size:30px">{tag(4)}<span>{hl(PROMPT[4], h0, h1, BLK[3][4])}</span></div>'
           f'<div class="dq">{e(DAD)}</div>', drop)
      + "</div>"
      f'<div id="send" style="position:absolute;left:620px;top:520px;width:80px;height:80px;border-radius:50%;background:{INK};display:grid;place-items:center"><span id="sendi"></span></div>')
world = (f'<div class="a" id="file" style="left:430px;top:300px;width:420px;height:96px;border-radius:22px;background:#fff;'
         f'box-shadow:0 10px 30px -8px rgba(20,18,14,.25);display:flex;align-items:center;gap:16px;padding:0 24px;box-sizing:border-box;font-size:24px;visibility:hidden">'
         f'<span id="fic"></span><span class="mono">dad-birthday-message.txt</span></div>')
click = round(t_look - 0.15, 3)
tags = "".join(ap(f'<div class="chip" style="background:{BLK[3][2]};color:#fff">{lab}</div>', tt, style="display:inline-block;margin-right:14px")
               for lab, tt in (("Same kind of list", t_list), ("Same kind of sign-off", t_sign)))
dw, rw = words_in(DAD), words_in(FULL["04"][0].replace("{Q}", QUOTE["04"]))
tags += ap(f'<div class="chip" style="background:{BLK[3][2]};color:#fff">Same length: {dw} → {rw} words</div>', t_samelen, style="display:inline-block")
rep = (f'<div class="card" style="left:-660px;top:40px;width:1320px">{reply("04", x0, x1, BLK[3][4])}</div>'
       f'<div style="position:absolute;left:-660px;top:{reply_h("04", 1400) - 30}px;width:1320px">{tags}</div>'
       + ap('<div class="chip" style="background:#0B0B0B;color:#fff">You never had to explain your style</div>', t_never, style=f"position:absolute;left:-660px;top:{reply_h('04', 1400) + 60}px"))
bp = ('<div style="position:absolute;left:-700px;top:60px;width:1400px;display:flex;gap:40px;align-items:stretch">'
      + ap('<div style="width:520px;height:330px;border-radius:30px;border:4px dashed #BDB8B0;box-sizing:border-box;padding:34px;display:flex;flex-direction:column;justify-content:space-between">'
           '<span class="mono lbl">Describe</span><span style="font-size:70px;font-weight:650;color:#8A867F">“Be casual”</span><span class="mono lbl">Vague</span></div>', t_cas)
      + ap(f'<div style="width:840px;height:330px;border-radius:30px;background:{BLK[3][2]};color:#fff;box-sizing:border-box;padding:34px;display:flex;flex-direction:column;justify-content:space-between">'
           f'<span class="mono lbl" style="color:rgba(255,255,255,.8)">Show</span><span style="font-size:30px;line-height:1.4;font-weight:550">{e(DAD)}</span>'
           + ap('<span class="mono lbl" style="color:#fff">A blueprint</span>', t_blue) + "</div>", t_show)
      + "</div>")
states = {"chap": (960, 150, 75, BLK[3][2]), "duo": (1100, 170, 85, CARD), "pw": (1260, 150, 75, INK), "prompt": (1520, 640, 36, CARD),
          "reply": (1400, reply_h("04", 1400) + 170, 36, CARD), "bp": (1480, 450, 40, CARD)}
seq = [[t_desc - 0.15, "duo"], [t_one - 0.15, "pw"], [t_style - 0.15, "prompt"], [click + 0.1, "reply"], [t_cas - 0.15, "bp"]]
layers = [(chap, None, t_desc - 0.15, "c"), (duo, t_desc - 0.15, t_one - 0.15, "c"), (pw, t_one - 0.15, t_style - 0.15, "c"),
          (pr, t_style - 0.15, click + 0.1, "t"), (rep, click + 0.1, t_cas - 0.15, "t"), (bp, t_cas - 0.15, None, "t")]
sc = slotcfg(show=ALLSHOW, rev=[-1, -1, -1, 0.15], pulse=[[], [], [], [0.15]])
grab = round(t_provit - 0.7, 3)
cur = {"size": 44, "drags": [[grab, drop]], "clicks": [click],
       "keys": [[0, 820, 460], [t_mirror, 820, 460], [grab, 620, 350], [drop, 0, 260], [click - 0.4, 0, 260], [click - 0.05, 660, 560], [click + 0.6, 720, 640], [T, 720, 640]]}
ex = ("$('sendi').innerHTML=M.icon('arrow',34,'#fff',2.6); $('fic').innerHTML=M.icon('file',30,'#0B0B0B'); $('spk').innerHTML=M.icon('sparkle',28,'#0B0B0B');\n"
      f"const CP=M.path({json.dumps(cur['keys'])}); const T_SHOWF={t_style + 0.3}, T_GRAB={grab}, T_DROP={drop};\n"
      "function EXTRA(t){const f=$('file').style; const v=M.vis(t,T_SHOWF,T_DROP,{din:0,lin:0.3,lout:0.15});"
      " if(v.o<0.002){f.visibility='hidden';return;} f.visibility='visible'; f.opacity=v.o;"
      " let x=430,y=300; if(t>=T_GRAB){const c=CP(Math.min(t,T_DROP)); x=c.x-190; y=c.y-40;} f.left=x+'px'; f.top=y+'px';}\n")
fn = clip("05", "examples", k, T, states, "chap", seq, layers, sc, cursor=cur, world=world, extra_js=ex)
add_plan(k, "05", "examples", fn, "Block 4: the examples")

# ================================================================ 6. Put them together
k = 5
T = dur(k)
t_first, t_new, t_usu = wt(k, "The first message"), wt(k, "The new one"), wt(k, "Usually, context")
t_eng, t_hon = wt(k, "And as someone"), wt(k, "I'll be honest")
l0, l1 = span(k, "I still catch myself", "one-liner prompts")
t_won, t_garb = wt(k, "Then I wonder"), wt(k, "Garbage in")
cmpc = ('<div style="position:absolute;left:-720px;top:40px;width:1440px;display:flex;gap:40px">'
        '<div style="width:700px">' + ap('<div class="mono lbl" style="margin-bottom:18px">Before · 1 block</div>'
                                         f'<div style="font-size:30px;line-height:1.4;color:#8A867F">“{e(QUOTE["01"])}”</div>', 0.1)
        + ap('<div class="chip" style="background:#FFC21A;color:#0B0B0B;margin-top:22px">Could be anyone’s mum</div>', t_first + 0.8) + "</div>"
        '<div style="width:700px">' + ap(f'<div class="mono lbl" style="margin-bottom:18px;color:{BLK[3][2]}">After · 4 blocks</div>'
                                         f'<div style="font-size:30px;line-height:1.4;font-weight:550">“Thirty years of bossing doctors around, and now you’re free to boss us full-time. Lucky us. {e(QUOTE["04"])}”</div>', t_new - 0.2)
        + ap(f'<div class="chip" style="background:{BLK[1][2]};color:#fff;margin-top:22px">Only your mum</div>', t_new + 1.0) + "</div></div>"
        + ap(f'<div class="chip" style="background:#0B0B0B;color:#fff">Missing a block? Usually context.</div>', t_usu, style="position:absolute;left:-720px;top:470px"))
term = ('<div class="card mono" style="left:-560px;top:40px;width:1120px;color:#E9E7E2;font-size:24px">'
        + ap('<div style="color:#8A867F;letter-spacing:.12em;text-transform:uppercase;font-size:20px;margin-bottom:26px">Software engineer · AI every day</div>', t_eng)
        + f'<div style="font-size:44px"><span style="color:#8A867F">&gt; </span>{typed("fix this", l0 + 0.4, l1)}</div>'
        + ap('<div style="margin-top:34px;position:relative;height:120px">'
             + "".join(f'<div class="sk" style="left:0;top:{i * 34}px;width:{w}px;height:16px;background:#3A3F3C"></div>' for i, w in enumerate([900, 760, 520]))
             + '</div><div style="color:#8A867F;font-size:22px">answer: lazy</div>', t_won) + "</div>")
garb = '<div class="chap" style="color:#fff;font-size:58px">' + ap("Garbage in, garbage out.", t_garb) + "</div>"
states = {"cmp": (1520, 560, 40, CARD), "term": (1200, 420, 28, "#161A18"), "garb": (1060, 160, 80, INK)}
seq = [[t_eng - 0.15, "term"], [t_garb - 0.15, "garb"]]
layers = [(cmpc, 0.05, t_eng - 0.15, "t"), (term, t_eng - 0.15, t_garb - 0.15, "t"), (garb, t_garb - 0.15, None, "c")]
sc = slotcfg(show=ALLSHOW, rev=[-1, -1, -1, -1], pulse=[[0.2], [0.35, t_usu], [0.5], [0.65]])
fn = clip("06", "compare", k, T, states, "cmp", seq, layers, sc)
add_plan(k, "06", "compare", fn, "Before and after; lazy one-liners")

# ================================================================ 7. The trick
k = 6
T = dur(k)
t_dk, t_fig, t_req, t_add = wt(k, "If you don't know"), wt(k, "make AI figure it out"), wt(k, "request it from you"), wt(k, "Add this one line")
p0, p1 = span(k, "Before you answer, ask me", "questions you need")
t_inst = wt(k, "Instead of AI guessing")
QS = [("What tone?", "What tone", 3), ("How long?", "How long", 3), ("Is it a milestone birthday?", "Is it a milestone", 2),
      ("Card, text or speech?", "Card, text", 3), ("How do you usually sign off?", "How do you usually", 4)]
t_ans, t_all, t_fin = wt(k, "You answer and boom"), wt(k, "all four blocks"), wt(k, "your final prompt")
chap = '<div class="chap" style="color:#fff;font-size:64px"><span id="spk"></span>The trick</div>'
dk = ('<div class="chap" style="font-size:44px;color:#0B0B0B;flex-direction:column;gap:18px">'
      + ap("Don’t know what context to give?", t_dk) + ap(f'<span class="chip" style="background:{INK};color:#fff;font-size:40px">Make AI ask you for it</span>', t_fig) + "</div>")
click = round(p1 + 0.35, 3)
bar = (f'<div class="card" style="left:-700px;top:-26px;width:1300px;font-size:38px;font-weight:550;white-space:nowrap">'
       f'<span class="mono" style="color:#8A867F;margin-right:18px">&gt;</span>{typed("Before you answer, ask me questions you need.", p0, p1)}</div>'
       f'<div id="send" style="position:absolute;left:600px;top:-40px;width:80px;height:80px;border-radius:50%;background:{INK};display:grid;place-items:center"><span id="sendi"></span></div>')
qrows = "".join(ap(f'<div style="display:flex;align-items:center;gap:18px;font-size:34px;font-weight:550;margin-bottom:20px">'
                   f'<span style="width:20px;height:20px;border-radius:50%;background:{BLK[b - 1][2]};flex:none"></span>{e(q)}</div>', wt(k, ph))
                for q, ph, b in QS)
qs = (f'<div class="card" style="left:-440px;top:40px;width:880px"><div class="rhd"><span class="ai">AI</span><span class="mono lbl">Asks first</span></div>{qrows}</div>'
      + ap(f'<div class="chip" style="background:#fff;border:2px solid #0B0B0B;color:#0B0B0B">All four blocks, filled in</div>', t_all, style="position:absolute;left:-400px;top:450px"))
fin = '<div class="chap" style="color:#fff;font-size:50px"><span id="ck2"></span>' + ap("A response you can work with", t_fin) + "</div>"
states = {"chap": (820, 150, 75, INK), "dk": (1100, 260, 50, CARD), "bar": (1440, 150, 75, CARD), "qs": (980, 580, 36, CARD), "fin": (1100, 150, 75, INK)}
seq = [[t_dk - 0.15, "dk"], [t_add - 0.15, "bar"], [click + 0.1, "qs"], [t_fin - 0.15, "fin"]]
layers = [(chap, None, t_dk - 0.15, "c"), (dk, t_dk - 0.15, t_add - 0.15, "c"), (bar, t_add - 0.15, click + 0.1, "c"), (qs, click + 0.1, t_fin - 0.15, "t"),
          (fin, t_fin - 0.15, None, "c")]
sc = slotcfg(show=ALLSHOW, rev=[-1, -1, -1, -1], pulse=[[t_ans + 0.2 + 0], [t_ans + 0.4], [t_ans + 0.6], [t_ans + 0.8]])
cur = {"size": 44, "clicks": [click], "keys": [[0, 760, 400], [p1 - 0.5, 760, 400], [click - 0.05, 640, 0], [click + 0.6, 700, 140], [T, 700, 140]]}
ex = "$('sendi').innerHTML=M.icon('arrow',34,'#fff',2.6); $('spk').innerHTML=M.icon('sparkle',50,'#FFC21A'); $('ck2').innerHTML=M.icon('check',46,'#FFC21A',3);\n"
fn = clip("07", "trick", k, T, states, "chap", seq, layers, sc, cursor=cur, extra_js=ex)
add_plan(k, "07", "trick", fn, "The trick: ask me questions first")

# ================================================================ 8. Recap
k = 7
T = dur(k)
times = [wt(k, "The task"), wt(k, "the context"), wt(k, "the rules"), wt(k, "and an example")]
t_dont, t_tok, t_pers, t_bin, t_give = wt(k, "You don't need all four"), wt(k, "Asking what's the time"), wt(k, "But for anything personal"), wt(k, "binary response"), wt(k, "give it the four blocks")
RT = ["Write a birthday message for my mum.", "Turning sixty. Retired nurse. Funny, sarcastic, hates soppy.",
      "Under 50 words. No emojis. Don’t use the word “queen”.", "Here’s the message I wrote for my dad. Use it as a style example."]
rows = ""
for i, (num, lab, bg, fg, _) in enumerate(BLK):
    txt = e(RT[i]) if i else ('<span id="r0a">' + e(RT[0]) + '</span><span id="r0b" style="position:absolute;left:0;opacity:0">What’s the time in Tokyo?</span>')
    rows += ap(f'<div id="row{i}" style="display:grid;grid-template-columns:330px 1fr;align-items:center;height:118px;padding:0 36px;border-radius:24px;margin-bottom:14px;background:{bg};color:{fg}">'
               f'<span style="font-size:38px;font-weight:650">{num} {lab}</span><span style="position:relative;font-size:28px;font-weight:550">{txt}</span></div>', times[i])
recap = (f'<div style="position:absolute;left:-720px;top:30px;width:1440px">{rows}</div>'
         + ap('<div class="chip" style="background:#fff;border:2px solid #0B0B0B;color:#0B0B0B">Quick fact? Task only.</div>', t_tok + 0.5, t_pers, style="position:absolute;left:-720px;top:560px")
         + ap('<div class="chip" style="background:#0B0B0B;color:#fff">Anything personal? All four.</div>', t_pers, style="position:absolute;left:-720px;top:560px"))
states = {"recap": (1520, 660, 40, "#F4F2EE")}
ops = [[], [[t_dont + 0.2, 0.25], [t_pers + 0.3, 1]], [[t_dont + 0.2, 0.25], [t_pers + 0.45, 1]], [[t_dont + 0.2, 0.25], [t_pers + 0.6, 1]]]
sc = slotcfg(show=ALLSHOW, rev=[-1, -1, -1, -1], pulse=[[times[0]], [times[1]], [times[2]], [times[3]]])
ex = (f"const ROWOP=[null].concat([1,2,3].map(i=>M.track(1,[[{t_dont + 0.2},0.25],[{t_pers + 0.3}+0.15*(i-1),1]],M.SOFT)));\n"
      f"function EXTRA(t){{for(let i=1;i<4;i++){{const r=$('row'+i); if(r) r.style.opacity=ROWOP[i](t).toFixed(3);}}"
      f" const x=M.clamp((t-{t_tok})/0.36)-M.clamp((t-{t_pers})/0.36); $('r0a').style.opacity=Math.max(0,1-2*x).toFixed(3); $('r0b').style.opacity=Math.max(0,2*x-1).toFixed(3);"
      f" for(let i=0;i<4;i++){{const r=$('row'+i); let s=1; const u=(t-{t_give}-0.12*i)/0.45; if(u>0&&u<1) s+=0.03*Math.sin(Math.PI*u); r.style.transform=`scale(${{s.toFixed(4)}})`;}}}}\n")
fn = clip("08", "recap", k, T, states, "recap", [], [(recap, 0.05, None, "t")], sc, extra_js=ex, ops=ops)
add_plan(k, "08", "recap", fn, "Recap: the four blocks; Tokyo vs personal")

# ================================================================ 9. Outro: make it a skill
k = 8
T = round(dur(k) + 5.0, 3)
t_skill, t_type, t_fut, t_turn, t_got = wt(k, "create a skill"), wt(k, "type out the four blocks"), wt(k, "In future videos"), wt(k, "turn your best prompt"), wt(k, "I gotchu")
bars = "".join(f'<div style="height:60px;border-radius:16px;margin-bottom:12px;background:{bg};color:{fg};display:flex;align-items:center;padding:0 26px;font-size:28px;font-weight:650">{num} {lab}</div>'
               for num, lab, bg, fg, _ in BLK)
stack = (f'<div style="position:absolute;left:-360px;top:36px;width:720px">{bars}</div>'
         + ap('<div class="chip" style="background:#fff;border:2px solid #0B0B0B;color:#0B0B0B">Typing all four every time?</div>', 0.6, style="position:absolute;left:-360px;top:330px"))
skill = (f'<div class="chap" style="font-size:40px;color:#0B0B0B;gap:22px;margin-top:-50px"><span id="fic2"></span><span class="mono">birthday-message.skill</span>'
         f'<span class="chip" style="background:#0B0B0B;color:#fff;font-size:24px"><span id="ck3"></span>Saved</span></div>'
         + ap('<div class="chip" style="background:transparent;color:#8A867F;font-size:26px">Task · Context · Rules · Examples, written once</div>', t_type,
              style="position:absolute;left:-310px;top:40px"))
nx0 = '<div class="chap" style="color:#fff;font-size:40px"><span class="mono" style="opacity:.8">NEXT VIDEO</span></div>'
nxt = '<div class="chap" style="color:#fff;font-size:46px"><span class="mono" style="font-size:28px;opacity:.7;margin-right:22px">NEXT</span>Turn your best prompt into a skill</div>'
end = ('<div class="chap" style="color:#fff;font-size:120px;letter-spacing:-.03em">I gotchu<span id="dot" style="color:#FF3D7F">.</span></div>')
states = {"stack": (820, 470, 36, CARD), "skill": (980, 300, 50, CARD), "next0": (420, 150, 75, INK), "next": (1260, 150, 75, INK), "end": (760, 240, 120, INK)}
seq = [[t_skill - 0.15, "skill"], [t_fut - 0.15, "next0"], [t_turn - 0.15, "next"], [t_got - 0.1, "end"]]
layers = [(stack, 0.05, t_skill - 0.15, "t"), (skill, t_skill - 0.15, t_fut - 0.15, "c"), (nx0, t_fut - 0.15, t_turn - 0.15, "c"), (nxt, t_turn - 0.15, t_got - 0.1, "c"), (end, t_got - 0.1, None, "c")]
sc = slotcfg(show=ALLSHOW, rev=[-1, -1, -1, -1], pulse=[[t_skill], [t_skill + 0.1], [t_skill + 0.2], [t_skill + 0.3]])
ops = [[[t_got, 0]], [[t_got, 0]], [[t_got, 0]], [[t_got, 0]]]
ex = "$('fic2').innerHTML=M.icon('file',44,'#0B0B0B'); $('ck3').innerHTML=M.icon('check',22,'#fff',3);\n"
fn = clip("09", "outro", k, T, states, "stack", seq, layers, sc, extra_js=ex, ops=ops)
add_plan(k, "09", "outro", fn, "Outro: turn your prompt into a skill; I gotchu")

json.dump({"title": "Anatomy of a good prompt (motion-broll, user's voice)", "voice": "myvoice/anatomy-voice-clean.mp3", "fps": "30",
           "clips": PLAN, "notes": ["The block 4 reply was written by Claude in chat for this example; all other replies are from the user's Claude screenshots."]},
          open("motion/plan.json", "w"), indent=1)
print("wrote", len(PLAN), "clips")
