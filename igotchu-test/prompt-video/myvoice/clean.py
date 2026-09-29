"""Clean the user's own voice recording: de-click, keep only the speech, rebuild the pauses to an even rhythm
(every gap between phrases ends up between MIN_GAP and MAX_GAP, the gaps themselves are true silence so no mouth
clicks survive), then gentle compression and a -16 LUFS level. Writes clean.wav + regions.json (old->new times)."""
import json, subprocess
import numpy as np
SR = 48000
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "raw.mp3", "-ac", "1", "-ar", str(SR),
                "-af", "highpass=f=75,adeclick=w=55:o=75,adeclip", "-f", "f32le", "pre.f32"], check=True)
x = np.fromfile("pre.f32", dtype=np.float32)
hop = int(0.01 * SR)
rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
db = 20 * np.log10(rms)
floor = np.percentile(db, 10)
thr = max(floor + 14, -48)
voiced = db > thr
# speech regions: voiced runs, bridged over short dips (< 180 ms), dropping blips under 120 ms (clicks, breaths)
regs, i, n = [], 0, len(voiced)
while i < n:
    if voiced[i]:
        j = i
        while j < n and voiced[j]:
            j += 1
        regs.append([i, j]); i = j
    else:
        i += 1
merged = []
for a, b in regs:
    if merged and a - merged[-1][1] < 18:
        merged[-1][1] = b
    else:
        merged.append([a, b])
merged = [[a, b] for a, b in merged if b - a >= 12]
# pad each region so soft word edges survive
PAD_IN, PAD_OUT = 0.06, 0.12
spans = [[max(0, a / 100 - PAD_IN), min(len(x) / SR, b / 100 + PAD_OUT)] for a, b in merged]
MIN_GAP, MAX_GAP = 0.22, 0.48
out, mapping, t_new = [], [], 0.0
fade = int(0.012 * SR)
for k, (a, b) in enumerate(spans):
    if k:
        gap = a - spans[k - 1][1]
        g = min(MAX_GAP, max(MIN_GAP, gap))
        out.append(np.zeros(int(g * SR), dtype=np.float32)); t_new += g
    seg = x[int(a * SR):int(b * SR)].copy()
    ramp = np.linspace(0, 1, fade, dtype=np.float32)
    seg[:fade] *= ramp; seg[-fade:] *= ramp[::-1]
    mapping.append({"old": [round(a, 3), round(b, 3)], "new": [round(t_new, 3), round(t_new + (b - a), 3)]})
    out.append(seg); t_new += b - a
y = np.concatenate(out)
y.astype(np.float32).tofile("joined.f32")
json.dump(mapping, open("regions.json", "w"))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "joined.f32",
                "-af", "acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7",
                "-ar", "48000", "clean.wav"], check=True)
print(f"threshold {thr:.1f} dB (floor {floor:.1f}); {len(spans)} speech regions; {len(x)/SR:.1f}s -> {t_new:.1f}s")
