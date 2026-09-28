"""Cut one continuous full-script take into per-slide clips (assets/vo/sNN.mp3).
Every sentence is placed with the same phrase-to-pause aligner the video timing uses (build.py _align), run over
the whole take; each slide boundary is the pause just before that slide's first sentence."""
import json, re, subprocess, sys
src = sys.argv[1]
_b = open("build.py").read()
exec("_ALIGN = {}\n\ndef _align" + _b.split("def _align")[1].split("def time_at_char")[0])
S = [s["text"] for s in json.load(open("slides.json"))]
full = " ".join(S)
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
err = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "silencedetect=n=-32dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
sil = list(zip(st, en + [dur] * (len(st) - len(en))))
sp, cur = [], 0.0
for a, b in sil:
    if a - cur > 0.05:
        sp.append([cur, a])
    cur = b
if dur - cur > 0.05:
    sp.append([cur, dur])
SL = {0: {"text": full}}
SEG = {0: sp}
_ALIGN.clear()
anchors = dict(_align(0))  # char index -> time
starts, pos = [], 0
for t in S:
    starts.append(pos)
    pos += len(t) + 1
cuts = []
for i in starts[1:]:
    t = anchors[i]
    # the silence that ends at (or just before) this sentence's start
    gap = min(sil, key=lambda g: abs(g[1] - t))
    cuts.append((gap[0] + gap[1]) / 2)
    print(f"slide boundary at {cuts[-1]:.2f}s (aligned start {t:.2f}s, pause {gap[0]:.2f}-{gap[1]:.2f})")
edges = [0] + cuts + [dur]
for i in range(10):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{edges[i]:.3f}", "-to", f"{edges[i+1]:.3f}", "-c:a", "libmp3lame", "-q:a", "2", f"assets/vo/s{i+1:02d}.mp3"], check=True)
for i in range(10):
    print(i + 1, round(edges[i + 1] - edges[i], 1), "s", len(S[i]), "chars", round(len(S[i]) / (edges[i + 1] - edges[i]), 1), "cps")
