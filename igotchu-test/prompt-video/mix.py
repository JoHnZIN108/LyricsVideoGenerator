"""Voice + synthesized SFX (events from build.py), two-pass loudnorm to -14 LUFS / -1 dBTP (YouTube)."""
import array, json, os, subprocess, wave
T = json.load(open("timing.json")); TOTAL = T[-1]["start"] + T[-1]["dur"]
SFX = json.load(open(os.environ.get("MIX_EVENTS", "sfx_events.json")))
OUT = os.environ.get("MIX_OUT", "video/assets/mix.mp3")
GAIN = {"pop": 0.18, "click": 0.16, "whoosh": 0.4, "whoosh_s": 0.18, "thud": 0.25, "ding": 0.24, "buzz": 0.35, "tick": 0.2}
SRC = {"whoosh_s": "whoosh"}
SPACING = {"click": 0.07}
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/vo/voiceover.wav", "-ac", "1", "-ar", "44100", "sfx/_voice.wav"], check=True)
with wave.open("sfx/_voice.wav") as w:
    voice = array.array("h", w.readframes(w.getnframes()))
n_total = int((TOTAL + 1) * 44100)
mix = [0.0] * n_total
for i, v in enumerate(voice[:n_total]):
    mix[i] = float(v)
clips = {}
for name in GAIN:
    with wave.open(f"sfx/{SRC.get(name, name)}.wav") as w:
        clips[name] = array.array("h", w.readframes(w.getnframes()))
last, used = {}, 0
for t, name in sorted(SFX):
    if t - last.get(name, -9) < SPACING.get(name, 0.3):
        continue
    last[name] = t; used += 1
    st = int(t * 44100)
    for k, v in enumerate(clips[name]):
        if 0 <= st + k < n_total:
            mix[st + k] += v * GAIN[name]
peak = max(abs(x) for x in mix) or 1
sc = min(1.0, 32000 / peak)
with wave.open("sfx/_mix.wav", "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(array.array("h", (int(x * sc) for x in mix)).tobytes())
# The raw mix sits near -20 LUFS with -2 dBTP peaks, so loudnorm can't reach -14 linearly (it fell back to
# dynamic mode and landed at -15.2). Lift it 7 dB into a fast peak limiter first, then normalize linearly.
PRE = "volume=7dB,alimiter=limit=0.6:attack=4:release=60:level=false"
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", "sfx/_mix.wav", "-af", PRE + ",loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"{PRE},loudnorm=I=-14:TP=-1:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "sfx/_mix.wav", "-af", af, "-ar", "48000", "-ac", "2", "-b:a", "192k", OUT], check=True)
print(f"mixed {used} of {len(SFX)} sound events")
