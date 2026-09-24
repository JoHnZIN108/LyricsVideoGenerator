"""Speech segments per slide (seconds from the slide's start), from silence detection. Free, and accurate
enough for the phrase aligner in build_v4.py. Never use paid transcription for timing."""
import json
import re
import subprocess

segs = {}
for n in range(1, 11):
    f = f"assets/vo/w/slide{n:02d}.wav"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "silencedetect=n=-32dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    # speech = complement of silences
    sil = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))
    sp, cur = [], 0.0
    for a, b in sil:
        if a - cur > 0.05:
            sp.append([round(cur, 3), round(a, 3)])
        cur = b
    if dur - cur > 0.05:
        sp.append([round(cur, 3), round(dur, 3)])
    segs[n] = sp
    print(n, len(sp), sp[:2], sp[-1])
json.dump(segs, open("segments.json", "w"))
