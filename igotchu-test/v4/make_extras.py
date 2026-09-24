"""YouTube extras from the v4 timing: captions.srt (phrase-level, from the phrase-to-pause alignment).
Captions use the written forms (2025, 34 million) even though the voice script spells them out."""
import json
import re

src = open("build_v4.py").read().split("# ---------------------------------------------------------------- animation helpers")[0]
exec(src)


def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def written(s):
    return s.replace("twenty twenty-five", "2025").replace("thirty-four million", "34 million")


cues = []
for n in range(1, 11):
    text = SL[n]["text"]
    anchors = _align(n)
    for k, (c, t) in enumerate(anchors):
        c_end = anchors[k + 1][0] if k + 1 < len(anchors) else len(text)
        t_end = anchors[k + 1][1] if k + 1 < len(anchors) else SEG[n][-1][1]
        cues.append([at(n, t), at(n, t_end), written(" ".join(text[c:c_end].split()))])
merged = []
for c in cues:
    if merged and len(merged[-1][2]) + len(c[2]) < 70 and c[0] - merged[-1][1] < 0.6:
        merged[-1][1] = c[1]
        merged[-1][2] += " " + c[2]
    else:
        merged.append(c)
with open("captions.srt", "w") as f:
    for i, (a, b, txt) in enumerate(merged, 1):
        f.write(f"{i}\n{ts(a)} --> {ts(max(b, a + 0.8))}\n{txt}\n\n")
print(len(merged), "caption lines")
for n in (1, 4, 6, 8, 10):
    s = T[n]["start"]
    print(f"{int(s // 60)}:{int(s % 60):02d}")
