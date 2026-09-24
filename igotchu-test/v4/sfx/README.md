# Free SFX kit (synthesized with FFmpeg, no credits)

```bash
ffmpeg -f lavfi -i "aevalsrc='0.55*sin(2*PI*(950-3000*t)*t)*exp(-38*t)':s=44100:d=0.14" -ac 1 pop.wav
ffmpeg -f lavfi -i "aevalsrc='0.6*(random(0)*2-1)*exp(-260*t)':s=44100:d=0.04" -af highpass=f=1800 -ac 1 click.wav
ffmpeg -f lavfi -i "anoisesrc=d=0.5:c=pink:r=44100:a=0.6:seed=7" -af "bandpass=f=1400:t=h:w=1800,afade=t=in:d=0.28,afade=t=out:st=0.3:d=0.2" -ac 1 whoosh.wav
ffmpeg -f lavfi -i "aevalsrc='0.9*sin(2*PI*62*t)*exp(-11*t)+0.35*(random(1)*2-1)*exp(-90*t)':s=44100:d=0.45" -af lowpass=f=1800 -ac 1 thud.wav
ffmpeg -f lavfi -i "aevalsrc='0.32*(sin(2*PI*1318*t)+0.45*sin(2*PI*2637*t)+0.2*sin(2*PI*1975*t))*exp(-5.5*t)':s=44100:d=0.9" -ac 1 ding.wav
```

Mixed under the voice by the end of `build_v3.py` (gains: pop .28, click .22, whoosh .35, thud .7, ding .3).

v4 additions: the whoosh recipe now uses `t=h` (without it ffmpeg reads w=1800 as Q=1800 and the whoosh peaks at -56 dBFS, silent).
buzz.wav (phone vibrate): `aevalsrc='0.5*sin(2*PI*180*t)*(0.5+0.5*sin(2*PI*28*t))*exp(-3*t)':d=0.45`, fade out last 0.15 s.
tick.wav (predicted word locks in): `aevalsrc='0.35*sin(2*PI*1320*t)*exp(-40*t)':d=0.08`.
