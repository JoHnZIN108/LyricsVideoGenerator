"""Trim each voice clip's edge silence, normalize to -20 LUFS, add designed pauses, join into slides.
Writes assets/vo/w/slideNN.wav, assets/vo/voiceover.wav and timing.json."""
import json, re, subprocess
V = "assets/vo"
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
def bounds(f):
    err = subprocess.run(["ffmpeg","-hide_banner","-i",f,"-af","silencedetect=n=-45dB:d=0.05","-f","null","-"],capture_output=True,text=True).stderr
    d = dur(f); s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)",err)]; e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)",err)]
    a = e[0] if s and s[0] < 0.01 and e else 0.0
    b = s[-1] if s and (len(e) < len(s) or e[-1] >= d - 0.01) else d
    return max(0, a - 0.03), min(d, b + 0.08)
def trim(k):
    a, b = bounds(f"{V}/{k}.mp3")
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"{V}/{k}.mp3","-af",f"atrim={a}:{b},asetpts=N/SR/TB,atempo=1.08,loudnorm=I=-20:TP=-2:LRA=11:linear=true",
                    "-ar","44100","-ac","1",f"{V}/w/{k}.wav"],check=True, timeout=120)
parts = {1:["s01"],2:["s02"],3:["s03"],4:["s04a","P2.2","s04b"],5:["s05"],6:["s06"],7:["s07a","P1.4","s07b"],8:["s08"],9:["s09"],10:["s10"]}
import sys
if "--skip-trim" not in sys.argv:
    for k in [p for v in parts.values() for p in v if not p.startswith("P")]:
        trim(k)
LEAD, TAIL, END = 0.15, 0.4, 5.5
timing = []; t = 0; files = []
for n in range(1, 11):
    cmd = ["ffmpeg","-y","-v","error","-f","lavfi","-i",f"anullsrc=r=44100:cl=mono:d={LEAD}"]
    k = 1
    for p in parts[n]:
        cmd += ["-f","lavfi","-i",f"anullsrc=r=44100:cl=mono:d={p[1:]}"] if p.startswith("P") else ["-i",f"{V}/w/{p}.wav"]
        k += 1
    cmd += ["-f","lavfi","-i",f"anullsrc=r=44100:cl=mono:d={END if n == 10 else TAIL}"]; k += 1
    cmd += ["-filter_complex","".join(f"[{i}]" for i in range(k)) + f"concat=n={k}:v=0:a=1[a]","-map","[a]",f"{V}/w/slide{n:02d}.wav"]
    subprocess.run(cmd, check=True, timeout=120)
    d = dur(f"{V}/w/slide{n:02d}.wav")
    timing.append({"start": round(t, 3), "dur": round(d, 3)}); files.append(f"{V}/w/slide{n:02d}.wav"); t += d
open("concat.txt","w").write("".join(f"file '{f}'\n" for f in files))
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i","concat.txt","-c:a","pcm_s16le",f"{V}/voiceover.wav"],check=True)
json.dump(timing, open("timing.json","w"), indent=1)
print([(x["start"], x["dur"]) for x in timing], "total", round(t, 2))
