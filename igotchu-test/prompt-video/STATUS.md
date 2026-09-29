# Ep 07 "Anatomy of a good prompt": status

**Current cut:** `final/igotchu-ep07-frames.mp4`. It's built by `frames.py` → `video_frames/`, with a one-take clone voice (`assets/vo/takes/full_a.mp3`, split into `assets/vo/s01..s10.mp3`).

## Agreed changes not built yet

1. **Block 4 is renamed "The examples"** (was "What good looks like", which confused the user). The Tell Dad texts and the Dad circle are dropped. New narration for slide 6:

   > Block four. The examples. Don't describe the message you want. Show it one.
   >
   > This is the one almost nobody uses, and it's probably the most powerful. Paste in something you've written before that you actually liked. Like: "Here's a birthday message I wrote for my dad this year that I really liked."
   >
   > Now look what came back: "Thanks for every plaster, every pep talk, and every 'I told you so.' Love you, don't get soppy."
   >
   > Same kind of list. Same kind of sign-off. Same length. You never had to explain your style.
   >
   > Telling it "be casual" is vague. Showing it an example... that's a blueprint.

   - **On-screen prompt part 4:** "Here's a birthday message I wrote for my dad this year that I really liked:" followed by "Happy 62nd, Dad. Still the only man who reads the instructions after breaking the thing. Thanks for every lift, every loan, and every lecture about tyre pressure. Love you (don't get emotional)."
   - **Reply card (chosen by the user; it builds on the block 3 reply):** "Happy 60th, Mum! Thirty years of bossing doctors around, and now you're free to boss us full-time. Lucky us. Thanks for every plaster, every pep talk, and every "I told you so." Love you (don't get soppy)."
   - **Reply source:** this reply was written by Claude in chat. If the user runs the prompt in the Claude app and gets a different reply, use that instead.
   - **Slide 7:** its "after" quote must use a line from this new reply.
2. **Recap (slide 9):** "So. The task. The context. The rules. And the examples. …"
3. **Outro (slide 10): changed from "why AI rolls the dice" to SOPs and skills.** The favourite draft:

   > One problem. Nobody's typing four blocks every time they want a birthday message. So write them once, like a recipe, and let the AI follow it. Businesses call that an SOP. In Claude, it's called a skill. Next video, I'll show you how to make your first one. I gotchu.

   - **Final wording:** not settled; the user asked only for an opening other than "Quick thing".
   - **End card:** "Next ▸ Turn your prompt into a skill".
4. **Voice:** the user plans to **record the script themselves**; the full script with these changes was given in chat. When the recording arrives, split it with `split_take.py`, then rerun `make_vo.py`, `make_segments.py`, `frames.py` and `mix.py`, and render.
5. **Extras:** update `youtube-extras.md` (block 4 chapter name, next-video line) and the Claude Doc "igotchu Video Scripts" (Script 7).
