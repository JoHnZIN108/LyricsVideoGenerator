"""Assemble Ep 07 from the rendered motion clips + the user's cleaned voice.

Each clip is trimmed/padded to exact frame boundaries of its voice section, so sync never drifts.
Run after motion_gen.py and render.js:  python3 motion_assemble.py
"""
import json, os, subprocess

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "motion/plan.json")))
voice = os.path.join(HERE, "myvoice/voice.wav")
work = os.path.join(HERE, "motion/work")
os.makedirs(work, exist_ok=True)


def run(*a):
    subprocess.run(a, check=True)


parts, total = [], 0
for i, c in enumerate(plan["clips"]):
    last = i == len(plan["clips"]) - 1
    src = os.path.join(HERE, "motion/out", os.path.basename(c["html"]).replace(".html", ".mp4"))
    end = c["out"] + (5.0 if last else 0)            # outro holds 5 s after the voice ends
    n = round(end * FPS) - round(c["in"] * FPS)
    dst = os.path.join(work, f"fit-{c['id']}.mp4")
    run("ffmpeg", "-loglevel", "error", "-y", "-i", src, "-vf",
        f"fps={FPS},tpad=stop_mode=clone:stop=30,trim=end_frame={n},setpts=PTS-STARTPTS",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", dst)
    parts.append(dst)
    total += n
lst = os.path.join(work, "concat.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
silent = os.path.join(work, "video-silent.mp4")
run("ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent)

out = os.path.join(HERE, "anatomy-of-a-good-prompt.mp4")
dur = total / FPS
run("ffmpeg", "-loglevel", "error", "-y", "-i", silent, "-i", voice, "-filter_complex",
    f"[1:a]apad,atrim=0:{dur},aresample=192000,volume=3.6dB,alimiter=limit=0.8:attack=1:release=10:level=false,aresample=48000[a]",
    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", out)
print(f"{out}  {dur:.2f}s  {os.path.getsize(out) / 1e6:.1f} MB")
