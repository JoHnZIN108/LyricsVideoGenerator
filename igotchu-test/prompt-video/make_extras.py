"""YouTube extras from the prompt-video timing: captions.srt (phrase-level, from the phrase-to-pause
alignment in build.py) and the chapter list."""
src = open("build.py").read().split("class Comp:")[0]
exec(src)


def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


cues = []
for n in range(1, 11):
    text = SL[n]["text"]
    anchors = _align(n)
    for k, (c, t) in enumerate(anchors):
        c_end = anchors[k + 1][0] if k + 1 < len(anchors) else len(text)
        t_end = anchors[k + 1][1] if k + 1 < len(anchors) else SEG[n][-1][1]
        cues.append([at(n, t), at(n, t_end), " ".join(text[c:c_end].split()), n])
merged = []
for c in cues:
    if merged and merged[-1][3] == c[3] and len(merged[-1][2]) + len(c[2]) < 70 and c[0] - merged[-1][1] < 0.6:
        merged[-1][1] = c[1]
        merged[-1][2] += " " + c[2]
    else:
        merged.append(c)


def split_long(cs, limit=84):
    """Cut a long cue at the punctuation (or space) nearest its middle; time is shared by characters."""
    out = []
    for a, b, txt, *_ in cs:
        if len(txt) <= limit:
            out.append([a, b, txt])
            continue
        mid = len(txt) / 2
        spaces = [i for i, ch in enumerate(txt) if ch == " " and 15 <= i <= len(txt) - 15]
        cuts = [i for i in spaces if txt[i - 1] in ".,?!'\"" ] or spaces
        k = min(cuts, key=lambda i: abs(i - mid))
        tm = a + (b - a) * k / len(txt)
        out += split_long([[a, tm, txt[:k].strip()], [tm, b, txt[k:].strip()]], limit)
    return out


def two_lines(txt, width=42):
    if len(txt) <= width:
        return txt
    sp = [i for i, ch in enumerate(txt) if ch == " "]
    k = min(sp, key=lambda i: abs(i - len(txt) / 2))
    return txt[:k] + "\n" + txt[k + 1:]


merged = split_long(merged)
with open("captions.srt", "w") as f:
    for i, (a, b, txt) in enumerate(merged, 1):
        f.write(f"{i}\n{ts(a)} --> {ts(max(b, a + 0.8))}\n{two_lines(txt)}\n\n")
print(len(merged), "caption lines")
for n in range(1, 11):
    s = T[n]["start"]
    print(n, f"{int(s // 60)}:{int(s % 60):02d}")
