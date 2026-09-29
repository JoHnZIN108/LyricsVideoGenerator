"""Split the recording at pauses and recognise each piece offline (pocketsphinx). Writes chunks.json."""
import json, re, subprocess, wave
from pocketsphinx import Decoder
err = subprocess.run(["ffmpeg","-hide_banner","-i","raw16.wav","-af","silencedetect=n=-38dB:d=0.3","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",err)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",err)]
w=wave.open("raw16.wav"); sr=w.getframerate(); pcm=w.readframes(w.getnframes()); dur=w.getnframes()/sr
sil=list(zip(st,en+[dur]*(len(st)-len(en))))
chunks=[];cur=0.0
for a,b in sil:
    if a-cur>0.12: chunks.append([cur,a])
    cur=b
if dur-cur>0.12: chunks.append([cur,dur])
dec=Decoder()
out=[]
for a,b in chunks:
    seg=pcm[int(max(0,a-0.1)*sr)*2:int(min(dur,b+0.1)*sr)*2]
    dec.start_utt(); dec.process_raw(seg,full_utt=True); dec.end_utt()
    h=dec.hyp(); out.append({"s":round(a,2),"e":round(b,2),"txt":h.hypstr if h else ""})
json.dump(out,open("chunks.json","w"),indent=0)
for c in out: print(f'{c["s"]:7.2f}-{c["e"]:7.2f}  {c["txt"]}')
