"""Pick the take that sounds most like the reference clip (slide 1, the take the user liked).
Score = cosine similarity of mean+std MFCC (voice timbre/accent proxy) plus a pitch-median penalty.
Usage: python3 voice_match.py assets/vo/takes/s02_*.mp3  -> prints scores, best first."""
import sys
import librosa
import numpy as np

REF = "assets/vo/s01.mp3"


def feat(f):
    y, sr = librosa.load(f, sr=22050)
    y, _ = librosa.effects.trim(y, top_db=35)
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)[1:]
    f0 = librosa.yin(y, fmin=60, fmax=300, sr=sr)
    return np.concatenate([m.mean(1), m.std(1)]), float(np.median(f0))


r, rf0 = feat(REF)
out = []
for f in sys.argv[1:]:
    v, f0 = feat(f)
    cos = float(np.dot(r, v) / np.linalg.norm(r) / np.linalg.norm(v))
    out.append((cos - abs(f0 - rf0) / rf0, cos, f0, f))
for s, cos, f0, f in sorted(out, reverse=True):
    print(f"{s:.4f}  cos={cos:.4f}  f0={f0:.0f} (ref {rf0:.0f})  {f}")
