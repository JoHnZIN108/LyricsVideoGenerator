"""Add a held beat after each block name ("The task." / "Block two is the context," / ...), so the block's
title card lands before the explanation starts. Each pause goes in the middle of the real silence after the
word (found with silencedetect), never inside speech. Writes voice_paused.wav + words_paused.json."""
import json, re, subprocess
import numpy as np

PAUSE = 0.9
SR = 48000
W = json.load(open("words.json"))
words = W["words"]
full = " ".join(p.strip() for p in open("transcript.txt").read().strip().split("\n") if p.strip())
TARGETS = ["The task.", "Block two is the context,", "Block three, the rules.", "Block four, the examples."]

err = subprocess.run(["ffmpeg", "-hide_banner", "-i", "voice.wav", "-af", "silencedetect=n=-40dB:d=0.12", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
sil = list(zip(map(float, re.findall(r"silence_start: ([\d.]+)", err)), map(float, re.findall(r"silence_end: ([\d.]+)", err))))

cuts = []
for ph in TARGETS:
    i = full.index(ph) + len(ph) - 1
    wi = max(k for k, w in enumerate(words) if w["char"] <= i)
    end, nxt = words[wi]["end"], words[wi + 1]["start"]
    cands = [(a, b) for a, b in sil if b > end - 0.35 and a < nxt + 0.5]
    a, b = min(cands, key=lambda s: abs((s[0] + s[1]) / 2 - (end + nxt) / 2))
    cuts.append(((a + b) / 2, wi))
    print(f"{ph!r}: word ends ~{end:.2f}, silence {a:.2f}-{b:.2f}, pause at {(a + b) / 2:.2f}")

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "voice.wav", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
parts, prev = [], 0
for t, _ in cuts:
    s = int(t * SR)
    parts += [x[prev:s], np.zeros(int(PAUSE * SR), dtype=np.float32)]
    prev = s
parts.append(x[prev:])
y = np.concatenate(parts)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "voice_paused.wav"],
               input=y.tobytes(), check=True)

out = []
for k, w in enumerate(words):
    sh = PAUSE * sum(1 for t, wi in cuts if k > wi)
    out.append({**w, "start": round(w["start"] + sh, 3), "end": round(w["end"] + sh, 3)})
json.dump({"duration": round(len(y) / SR, 3), "words": out, "pauses": [round(t, 3) for t, _ in cuts]}, open("words_paused.json", "w"), indent=0)
print(f"{len(x) / SR:.2f}s -> {len(y) / SR:.2f}s")
