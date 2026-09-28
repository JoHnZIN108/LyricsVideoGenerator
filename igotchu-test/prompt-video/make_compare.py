"""One short listening file per slide: take a, beep, take b, beep, take c (first 12 s of each, at the video's 1.08x)."""
import subprocess, sys
for n in sys.argv[1:]:
    ins, fc = [], []
    for i, t in enumerate("abc"):
        ins += ["-i", f"assets/vo/takes/s{n}_{t}.mp3"]
        fc.append(f"[{i}]atrim=0:12,atempo=1.08,aresample=44100,aformat=channel_layouts=mono,afade=t=out:st=10.6:d=0.5[a{i}]")
    ins += ["-f", "lavfi", "-i", "sine=f=880:d=0.25"]
    fc.append("[3]aresample=44100,aformat=channel_layouts=mono,asplit=2[b0][b1]")
    fc.append("anullsrc=r=44100:cl=mono,atrim=0:0.5,asplit=4[z0][z1][z2][z3]")
    fc.append("[a0][z0][b0][z1][a1][z2][b1][z3][a2]concat=n=9:v=0:a=1")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-b:a", "128k", f"compare-slide{n}.mp3"], check=True)
    print("compare-slide" + n)
