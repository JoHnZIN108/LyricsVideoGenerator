"""Ep 07 in the Claude Design "motion-first" style: re-time Claude Design's finished video to the user's voice.

Claude Design (https://claude.ai/artifact/8chmuwWBa7vCPdM3cDGJQ4) rendered the whole episode as one silent video,
timed to an estimate. That page is never changed; we work on a downloaded copy (cdmotion/source-claude-design.mp4).

Each ANCHOR ties a moment in their video to the words in the user's recording that it illustrates. Between two
anchors the footage is mapped onto the voice: sped up if the voice is quicker; played at normal speed and then held
on the last frame if the voice is much slower (slowing moving footage a lot looks choppy). A (cut_from, resume_at)
anchor skips footage the user doesn't say (yet).

Voice: myvoice/voice_paused.wav (cleaned recording, 0.9 s beat after each block name), word times in words_paused.json.
When the user re-records the two missing lines, splice them in and restore the two scenes marked MISSING.
"""
import json, os, re, subprocess

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "cdmotion/source-claude-design.mp4")
WORK = os.path.join(HERE, "cdmotion/work")
OUT = os.path.join(HERE, "cdmotion/igotchu-ep07-motion-first.mp4")
VOICE = os.path.join(HERE, "myvoice/voice_paused.wav")
V = json.load(open(os.path.join(HERE, "myvoice/words_paused.json")))
WORDS = V["words"]
FULL = " ".join(p.strip() for p in open(os.path.join(HERE, "myvoice/transcript.txt")).read().strip().split("\n") if p.strip())
SRC_END = 237.28
HOLD = 3.0          # "I gotchu." hold after the last word
SLOWEST = 0.8       # below this playback rate, play at 1x and hold instead

_pos = [0]


def said(phrase, off=0.0):
    """Voice time when `phrase` starts; phrases are looked up in script order."""
    i = FULL.find(phrase, _pos[0])
    if i < 0:
        raise KeyError(phrase)
    _pos[0] = i
    k = max(q for q in range(len(WORDS)) if WORDS[q]["char"] <= i)
    w = WORDS[k]
    f = min(1.0, (i - w["char"]) / max(1, len(w["text"])))
    return round(w["start"] + (w["end"] - w["start"]) * f + off, 3)


# (time in Claude Design's video, voice time). A pair (cut_from, resume_at) as the first item skips footage.
A = [
    (0.0, 0.0),
    # intro
    (1.0, said("useless")), (3.2, said("a brilliant one")), (3.69, said("four small parts")),
    (5.76, said("Most people only use one")), (7.37, said("We're going to build")), (8.0, said("a prompt from scratch")),
    (11.34, said("one block at a time")), (12.0, said("and watch the answer")), (16.35, said("And at the end")),
    (16.7, said("a trick that basically")),
    # block 1: the task
    (18.8, said("The task. This", -0.9)), (19.0, said("The task. This", -0.15)), (19.9, said("This is the one block")),
    # MISSING (re-record): "say you're trying to write a birthday message for your mum" -> Mum's tile 21.9-27.1
    ((22.4, 27.11), said("Most people just prompt")), (28.5, said('"Write a birthday')), (30.4, said("and would get back")),
    (32.6, said('"Thank you')), (37.8, said("It's fine")), (39.83, said("greeting card")),
    # "Could be anyone's mum" wall (41.9-43.6) isn't said: skip it
    ((41.6, 43.61), said("Write a birthday message is a task")), (48.8, said("Everyone gets this block")),
    (49.68, said("It's the other three")), (51.0, said("makes the difference")),
    # block 2: the context
    (52.0, said("Block two", -0.35)), (53.0, said("the context,")), (54.7, said("the stuff")),
    (57.63, said("For example")), (58.6, said("turning sixty")), (59.7, said("She just retired")),
    (60.7, said("thirty years as a nurse")), (62.6, said("She's funny")), (63.7, said("a bit sarcastic")),
    (65.6, said("cringe at anything")), (68.2, said("Now look at the response")), (69.6, said("The NHS")),
    (77.4, said("Suddenly it's about her")), (78.4, said("the nursing")), (80.13, said("It's the same AI")),
    (81.6, said("The difference is the context")), (83.4, said("Block three", -0.6)),
    # block 3: the rules
    (84.4, said("Block three", -0.1)), (86.6, said("This covers")), (87.4, said("length")),
    (88.86, said("For example, keep")), (90.3, said("It's going in a card")), (92.6, said("and don't use the word")),
    (94.05, said("'cause you'd be surprised")), (97.2, said("The rules stop")), (100.2, said("Now the AI response", -0.8)),
    (102.0, said("Now the AI response", 0.2)), (103.0, said("Thirty years of bossing")),
    (108.0, said("Block four", -1.3)),
    # block 4: the examples
    (109.3, said("Block four", -0.1)), (110.3, said("Don't just describe")), (110.9, said("Provide an example")),
    (111.58, said("This is the one most people")), (114.6, said("probably the most powerful")),
    (116.45, said("If you have a specific style")), (118.6, said("mirror and draw")),
    (120.8, said("Here's the birthday message")), (123.6, said("Use it as a style")),
    (126.1, said("Now look at a portion")), (127.6, said('"Thanks for every')), (131.6, said("Same kind of list")),
    (133.4, said("same kind of sign-off")), (134.4, said("same length")), (134.8, said("You never had")),
    (136.67, said("Telling AI be casual")), (137.2, said("is vague")), (138.3, said("Showing it an example")),
    # compare
    (140.0, said("Put them all together")), (143.0, said("The first message")), (145.4, said("The new one could only")),
    # MISSING (re-record): "the real test / if it could be for anyone, you're probably missing the context" 146.7-153
    ((146.6, 153.3), said("Usually, context")),
    (156.84, said("And as someone who works")), (162.6, said("I still catch myself")), (164.9, said("Then I wonder")),
    (165.9, said("the answer is lazy")), (167.0, said("Garbage in")),
    # the trick
    (167.35, said("Okay, the trick", -0.1)), (168.8, said("the trick I promised")), (170.4, said("If you don't know")),
    (171.8, said("make AI figure it out")), (172.8, said("request it from you")), (175.19, said("Add this one line")),
    (176.8, said("Before you answer")), (180.4, said("Instead of AI guessing")), (182.6, said("What tone")),
    (183.6, said("How long")), (184.5, said("Is it a milestone")), (185.6, said("Card, text")),
    (186.6, said("How do you usually")), (188.4, said("You answer")), (190.2, said("all four blocks")),
    (192.59, said("your final prompt produces")),
    # recap
    (196.0, said("So that's it")), (196.9, said("The task, the")), (197.9, said("the context, the rules")),
    (198.8, said("the rules, and")), (199.6, said("and an example")), (201.4, said("You don't need all four")),
    (202.6, said("Asking what's the time")), (205.6, said("doesn't need your life story")),
    (208.14, said("But for anything personal")), (211.6, said("binary response")), (212.8, said("give it the four blocks")),
    # make it a skill
    # reordered to the voice: skill first (recipe -> SOP -> skill pill), then the x37 pile for "every single time"
    (215.5, said("For a prompt that you use")), ((216.0, 221.0), said("you can create a skill")),
    ((222.4, 226.9), said("around that task")), ((228.6, 216.3), said("so that you don't have to type")),
    ((219.4, 229.38), said("In future videos")),
    (230.8, said("turn your best prompt")), (234.38, said("I gotchu", -0.1)),
    (SRC_END, round(V["duration"] + HOLD, 3)),
]


def segments():
    segs, prev_c, prev_v = [], 0.0, 0.0
    for c, v in A[1:]:
        c_end, c_next = c if isinstance(c, tuple) else (c, c)
        assert v >= prev_v, (c, v, prev_v)
        if v > prev_v:
            segs.append((prev_c, c_end, prev_v, v))
        prev_c, prev_v = c_next, v
    return segs


def build():
    os.makedirs(WORK, exist_ok=True)
    parts = []
    for k, (c0, c1, v0, v1) in enumerate(segments()):
        n = round(v1 * FPS) - round(v0 * FPS)
        if n <= 0:
            continue
        rate = (c1 - c0) / (v1 - v0)
        if rate >= SLOWEST:
            vf = f"setpts=(PTS-STARTPTS)/{rate:.5f},fps={FPS},tpad=stop_mode=clone:stop=30,trim=end_frame={n}"
        else:  # play at 1x, hold the last frame for the rest
            vf = f"setpts=PTS-STARTPTS,fps={FPS},tpad=stop_mode=clone:stop={n + 30},trim=end_frame={n}"
        dst = os.path.join(WORK, f"seg{k:03d}.mp4")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{c0:.3f}", "-t", f"{max(c1 - c0, 1 / FPS):.3f}",
                        "-i", SRC, "-vf", vf + ",setpts=PTS-STARTPTS", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14",
                        "-pix_fmt", "yuv420p", dst], check=True)
        parts.append(dst)
    lst = os.path.join(WORK, "concat.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    silent = os.path.join(WORK, "silent.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
    total = round(V["duration"] + HOLD, 3)
    af = (f"apad,atrim=0:{total},aresample=192000,volume=3.6dB,alimiter=limit=0.8:attack=1:release=10:level=false,"
          "aresample=48000")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", silent, "-i", VOICE, "-filter_complex", f"[1:a]{af}[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(total), OUT], check=True)
    print(OUT, total, f"{os.path.getsize(OUT) / 1e6:.1f} MB")


if __name__ == "__main__":
    for c0, c1, v0, v1 in segments():
        r = (c1 - c0) / (v1 - v0)
        flag = "HOLD" if r < SLOWEST else ("FAST" if r > 1.8 else "")
        print(f"cd {c0:7.2f}-{c1:7.2f}  voice {v0:7.2f}-{v1:7.2f}  rate {r:4.2f} {flag}")
    build()
