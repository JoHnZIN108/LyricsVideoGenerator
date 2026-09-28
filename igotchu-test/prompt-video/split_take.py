"""Cut one continuous full-script take into per-slide clips (assets/vo/sNN.mp3).
Slide boundaries = the longest pause near where the character count says each paragraph ends."""
import json, re, subprocess, sys
src = sys.argv[1]
S = [s["text"] for s in json.load(open("slides.json"))]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
err = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "silencedetect=n=-38dB:d=0.25", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
sil = list(zip(st, en))
tot = sum(len(t) for t in S)
cuts, acc = [], 0
for t in S[:-1]:
    acc += len(t)
    exp = dur * acc / tot
    cand = [(b - a, a, b) for a, b in sil if abs((a + b) / 2 - exp) < 4.0 and (not cuts or a > cuts[-1] + 3)]
    L, a, b = max(cand)
    cuts.append((a + b) / 2)
    print(f"slide {len(cuts)}->{len(cuts)+1}: expected {exp:.1f}s, pause {a:.2f}-{b:.2f} ({L:.2f}s)")
edges = [0] + cuts + [dur]
for i in range(10):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{edges[i]:.3f}", "-to", f"{edges[i+1]:.3f}", "-c:a", "libmp3lame", "-q:a", "2", f"assets/vo/s{i+1:02d}.mp3"], check=True)
print("wrote assets/vo/s01..s10.mp3")
