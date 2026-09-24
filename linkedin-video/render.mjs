// Renders scene.html frame-by-frame with headless Chromium and pipes PNGs into ffmpeg.
// Usage: node render.mjs [out.mp4] [--stills t1,t2,...]
import { chromium } from "playwright";
import { spawn, execSync } from "node:child_process";
import { pathToFileURL, fileURLToPath } from "node:url";
import path from "node:path";

const dir = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const stillsIdx = args.indexOf("--stills");
const stills = stillsIdx >= 0 ? args[stillsIdx + 1].split(",").map(Number) : null;
const out = path.resolve(args.find(a => a.endsWith(".mp4")) || path.join(dir, "orchestration-explainer.mp4"));
const FPS = 30;
const ffmpeg = process.env.FFMPEG ||
  execSync(`python3 -c "import imageio_ffmpeg as i; print(i.get_ffmpeg_exe())"`).toString().trim();

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1080 } });
await page.goto(pathToFileURL(path.join(dir, "scene.html")).href + "?render=1");
await page.evaluate(() => window.ready);
const shot = async t => { await page.evaluate(t => window.render(t), t); return page.locator("#c").screenshot({ type: "png" }); };

if (stills) {
  const fs = await import("node:fs");
  for (const t of stills) fs.writeFileSync(path.join(dir, `still-${t}.png`), await shot(t));
} else {
  const duration = await page.evaluate(() => window.DURATION);
  const enc = spawn(ffmpeg, ["-y", "-f", "image2pipe", "-framerate", String(FPS), "-i", "-",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", out],
    { stdio: ["pipe", "ignore", "inherit"] });
  const n = Math.round(duration * FPS);
  for (let i = 0; i < n; i++) {
    const buf = await shot(i / FPS);
    if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once("drain", r));
  }
  enc.stdin.end();
  await new Promise(r => enc.on("close", r));
  console.log(`wrote ${out} (${n} frames)`);
}
await browser.close();
