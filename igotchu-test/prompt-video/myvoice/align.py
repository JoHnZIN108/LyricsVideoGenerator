"""Word timings for the cleaned recording: the phrase-to-pause aligner (same as build.py) over the whole
transcript, word times interpolated inside each phrase. Writes words.json, sections.json, captions.srt."""
import json, re, subprocess
_b = open("../build.py").read()
exec("_ALIGN = {}\n\ndef _align" + _b.split("def _align")[1].split("def time_at_char")[0])
paras = [p.strip() for p in open("transcript.txt").read().strip().split("\n") if p.strip()]
full = " ".join(paras)
src = "clean.wav"
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
err = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "silencedetect=n=-40dB:d=0.18", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
sil = list(zip(st, en + [dur] * (len(st) - len(en))))
sp, cur = [], 0.0
for a, b in sil:
    if a - cur > 0.05: sp.append([cur, a])
    cur = b
if dur - cur > 0.05: sp.append([cur, dur])
SL = {0: {"text": full}}; SEG = {0: sp}
anchors = sorted(_align(0))
def t_at(i):
    k = max(q for q in range(len(anchors)) if anchors[q][0] <= i)
    c0, t0 = anchors[k]; c1, t1 = anchors[k + 1] if k + 1 < len(anchors) else (len(full), sp[-1][1])
    return t0 + (t1 - t0) * (i - c0) / max(1, c1 - c0)
words = [{"text": m.group(0), "start": round(t_at(m.start()), 3), "end": round(t_at(m.end()), 3), "char": m.start()} for m in re.finditer(r"\S+", full)]
json.dump({"duration": round(dur, 3), "words": words}, open("words.json", "w"), indent=0)
secs, pos = [], 0
for p in paras:
    secs.append({"start": round(t_at(pos), 3), "text": p}); pos += len(p) + 1
for k in range(len(secs)):
    secs[k]["end"] = secs[k + 1]["start"] if k + 1 < len(secs) else round(dur, 3)
json.dump(secs, open("sections.json", "w"), indent=1)
for k, s in enumerate(secs): print(k + 1, f'{s["start"]:6.1f}-{s["end"]:6.1f}', s["text"][:60])
