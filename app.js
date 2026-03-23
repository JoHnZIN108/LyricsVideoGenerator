/* ══════════════════════════════════════════════════════
   Lyric Video Maker — app.js

   Architecture:
   • Setup screens (s1→s2→s3) handle audio upload, lyrics, tap sync
   • Player uses DOM-based lyrics (guaranteed centering) + a small
     <canvas> for the waveform visualizer — exactly like the original
     page file, which is why centering always worked there
   • Recording uses a hidden off-screen <canvas> driven by
     RecordingRenderer, which renders lyrics + waveform + title
     into a 1280×720 frame for MediaRecorder capture
══════════════════════════════════════════════════════ */


/* ─────────────────────────────────────────────────────
   HELPERS & STATE
───────────────────────────────────────────────────── */
const $ = id => document.getElementById(id);
const fmt = s => !s || isNaN(s) ? '0:00' : `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;

function showScreen(id) {
  ['s1', 's2', 's3', 'screen-player'].forEach(s =>
    $(s).classList.toggle('active', s === id)
  );
}

let audioURL  = null;
let songName  = '';
let lyrics    = [];      // [{ text, start, end }]
let isPlaying = false;
let currentIdx = -1;

let audioCtx  = null;
let analyser  = null;
let audioDest = null;   // MediaStreamDestination for recording audio

let vizRunning    = false;   // controls the visualizer RAF loop
let mediaRecorder = null;
let isRecording   = false;
let recRenderer   = null;   // RecordingRenderer instance (only during recording)

const audio = $('audio');


/* ─────────────────────────────────────────────────────
   FLOATING PARTICLES
───────────────────────────────────────────────────── */
for (let i = 0; i < 600; i++) {
  const p = document.createElement('div');
  p.className = 'pt';
  p.style.cssText = [
    `left:${Math.random() * 100}vw`,
    `width:${1 + Math.random() * 3}px`,
    `height:${1 + Math.random() * 3}px`,
    `animation-duration:${8 + Math.random() * 16}s`,
    `animation-delay:${Math.random() * 20}s`,
  ].join(';');
  document.body.appendChild(p);
}


/* ─────────────────────────────────────────────────────
   STEP 1 — AUDIO UPLOAD
───────────────────────────────────────────────────── */
const dropZone = $('drop-zone');
dropZone.addEventListener('click', () => $('file-input').click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('over'));
dropZone.addEventListener('drop', e => { e.preventDefault(); dropZone.classList.remove('over'); loadAudioFile(e.dataTransfer.files[0]); });
$('file-input').addEventListener('change', e => loadAudioFile(e.target.files[0]));

function loadAudioFile(file) {
  if (!file || !file.type.startsWith('audio/')) return;
  if (audioURL) URL.revokeObjectURL(audioURL);
  audioURL = URL.createObjectURL(file);
  audio.src = audioURL;
  const name = file.name.replace(/\.[^.]+$/, '').replace(/[_-]/g, ' ');
  $('dz-label').innerHTML = `<span style="color:var(--accent)">🎵 ${name}</span>`;
  $('s2-name').textContent = name;
  if (!$('song-title-input').value) $('song-title-input').value = name;
  audio.addEventListener('loadedmetadata', () => {
    $('s2-dur').textContent = 'Duration: ' + fmt(audio.duration);
  }, { once: true });
  $('s1-next').disabled = false;
}

$('s1-next').addEventListener('click', () => showScreen('s2'));


/* ─────────────────────────────────────────────────────
   STEP 2 — LYRICS INPUT
───────────────────────────────────────────────────── */
$('s2-back').addEventListener('click', () => showScreen('s1'));
$('s2-next').addEventListener('click', () => {
  if (!$('lyrics-ta').value.trim()) { alert('Please add your lyrics first!'); return; }
  initTapSync($('lyrics-ta').value.trim());
  showScreen('s3');
});


/* ─────────────────────────────────────────────────────
   STEP 3 — TAP SYNC
───────────────────────────────────────────────────── */
let tapLines = [], tapTimestamps = [], tapIdx = 0, tapPlaying = false;

function initTapSync(rawText) {
  tapLines      = rawText.split('\n').map(l => l.trim()).filter(l => l.length > 0);
  tapTimestamps = [];
  tapIdx        = 0;
  tapPlaying    = false;
  audio.currentTime = 0;
  audio.pause();
  $('tap-play-btn').textContent  = '▶ Play';
  $('tap-current').textContent   = 'Press Play to start';
  $('tap-bar-fill').style.width  = '0%';
  $('tap-done-btn').disabled     = true;
  $('tap-progress').textContent  = `Line 0 of ${tapLines.length}`;
}

$('s3-back').addEventListener('click', () => {
  audio.pause(); tapPlaying = false; $('tap-play-btn').textContent = '▶ Play'; showScreen('s2');
});

$('tap-play-btn').addEventListener('click', () => {
  if (tapPlaying) {
    audio.pause(); tapPlaying = false; $('tap-play-btn').textContent = '▶ Play';
  } else {
    audio.play(); tapPlaying = true; $('tap-play-btn').textContent = '⏸ Pause';
    // Show the first line to tap as soon as playback starts
    if (tapIdx === 0 && tapLines[0]) $('tap-current').textContent = tapLines[0];
    resumeAudioCtx(); runTapBar();
  }
});

$('tap-restart-btn').addEventListener('click', () => {
  audio.pause(); audio.currentTime = 0;
  tapPlaying = false; tapIdx = 0; tapTimestamps = [];
  $('tap-play-btn').textContent = '▶ Play';
  $('tap-current').textContent  = 'Press Play to start';
  $('tap-bar-fill').style.width = '0%';
  $('tap-done-btn').disabled    = true;
  $('tap-progress').textContent = `Line 0 of ${tapLines.length}`;
});

function doTap() {
  if (tapIdx >= tapLines.length) return;
  tapTimestamps.push(audio.currentTime);
  tapIdx++;
  // Show the next line the user needs to tap for (or done message)
  $('tap-current').textContent  = tapIdx < tapLines.length ? tapLines[tapIdx] : '✅ All lines synced!';
  $('tap-progress').textContent = `Line ${tapIdx} of ${tapLines.length}`;
  if (tapIdx >= tapLines.length) $('tap-done-btn').disabled = false;
}

$('tap-btn').addEventListener('click', doTap);
document.addEventListener('keydown', e => {
  if ((e.code === 'Space' || e.code === 'Enter') && $('s3').classList.contains('active')) {
    e.preventDefault(); doTap();
  }
});

function runTapBar() {
  if (!tapPlaying) return;
  $('tap-bar-fill').style.width = (audio.currentTime / (audio.duration || 1) * 100) + '%';
  $('tap-time').textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration);
  requestAnimationFrame(runTapBar);
}

audio.addEventListener('ended', () => {
  tapPlaying = false;
  $('tap-play-btn').textContent = '▶ Play';
  if ($('s3').classList.contains('active') && tapTimestamps.length > 0) {
    $('tap-done-btn').disabled  = false;
    $('tap-current').textContent = `✅ Song ended — ${tapTimestamps.length} lines synced. Hit BUILD VIDEO.`;
  }
  if (isRecording) stopRecording();
});

function buildLyricsFromTaps() {
  const dur = audio.duration || 180;
  // Each tap marks the END of the current line / start of the next.
  // Line 0 starts at t=0; each subsequent line starts when the previous tap fired.
  lyrics = tapLines.map((text, i) => ({
    text,
    start: i === 0 ? 0 : tapTimestamps[i - 1],
    end:   i < tapTimestamps.length ? tapTimestamps[i] - 0.05 : dur,
  }));
}

$('tap-done-btn').addEventListener('click', () => {
  audio.pause(); tapPlaying = false;
  $('loading').style.display = 'flex';
  const go = () => {
    buildLyricsFromTaps();
    songName = $('song-title-input').value.trim() || $('s2-name').textContent;
    setTimeout(() => { $('loading').style.display = 'none'; launchPlayer(); }, 400);
  };
  if (audio.readyState >= 1 && audio.duration) go();
  else { audio.addEventListener('loadedmetadata', go, { once: true }); audio.load(); }
});


/* ─────────────────────────────────────────────────────
   AUDIO CONTEXT — set up once on first play
───────────────────────────────────────────────────── */
function setupAudioContext() {
  if (audioCtx) return;
  audioCtx  = new (window.AudioContext || window.webkitAudioContext)();
  analyser  = audioCtx.createAnalyser();
  analyser.fftSize = 256;
  audioDest = audioCtx.createMediaStreamDestination();
  const src = audioCtx.createMediaElementSource(audio);
  src.connect(analyser);
  analyser.connect(audioCtx.destination);
  src.connect(audioDest);
}

function resumeAudioCtx() {
  if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
}


/* ─────────────────────────────────────────────────────
   PLAYER — DOM-based lyrics (browser handles centering)
   This mirrors what the original page file did, which is why
   centering always worked there: text-align:center on a block
   element with width:100% is infallible.
───────────────────────────────────────────────────── */
function launchPlayer() {
  showScreen('screen-player');
  setupAudioContext();

  $('p-title').textContent = songName.toUpperCase();

  currentIdx = -1;
  buildLyricsWindow();     // create DOM lyric divs
  scrollToActive(-1);

  vizRunning = true;
  drawViz();               // start the waveform loop

  audio.currentTime = 0;
  audio.play()
    .then(() => { isPlaying = true; $('play-btn').textContent = '⏸'; resumeAudioCtx(); })
    .catch(() => {});
}

/* Create one <div class="lyric-line"> per lyric */
function buildLyricsWindow() {
  const win = $('lyrics-window');
  win.innerHTML = '';
  lyrics.forEach(line => {
    const el = document.createElement('div');
    el.className   = 'lyric-line';
    el.textContent = line.text;
    el.addEventListener('click', () => {
      audio.currentTime = line.start + 0.05;
      if (!isPlaying) togglePlay();
    });
    win.appendChild(el);
  });
}

/* Slide the strip so the active line sits at the vertical centre */
function scrollToActive(activeIdx) {
  const win = $('lyrics-window');
  const els = win.querySelectorAll('.lyric-line');

  els.forEach((el, i) => {
    el.className = 'lyric-line'; // resets to invisible (opacity:0 in CSS)
    if (activeIdx < 0) {
      // Before the song starts: show line 0 as a faded preview
      if (i === 0) el.classList.add('near');
    } else {
      if (i === activeIdx)                    el.classList.add('active');
      else if (Math.abs(i - activeIdx) === 1) el.classList.add('near');
      // All other lines stay as .lyric-line → opacity 0 (invisible)
    }
  });

  if (activeIdx < 0 || !els[activeIdx]) return;

  const activeEl  = els[activeIdx];
  const stageH    = $('lyrics-stage').offsetHeight;
  const offset    = stageH / 2 - activeEl.offsetTop - activeEl.offsetHeight / 2 + 450;
  win.style.transform = `translateY(${offset}px)`;
}

/* ─────────────────────────────────────────────────────
   VISUALIZER — small canvas, bars rise from the bottom
   Copied from original page file logic and enhanced with
   a gradient so bars fade from brighter base to soft tip.
───────────────────────────────────────────────────── */
function drawViz() {
  if (!vizRunning) return;
  requestAnimationFrame(drawViz);

  const canvas = $('visualizer');
  // Resize canvas buffer to match display size each frame (responsive)
  canvas.width  = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;

  if (!analyser) return;

  const W   = canvas.width, H = canvas.height;
  const ctx = canvas.getContext('2d');
  const buf = new Uint8Array(analyser.frequencyBinCount);
  analyser.getByteFrequencyData(buf);

  ctx.clearRect(0, 0, W, H);

  const bw = (W / buf.length) * 2.5;
  let x = 0;

  ctx.shadowBlur = 0;

  for (let i = 0; i < buf.length; i++) {
    const v = buf[i] / 255;
    if (v < 0.01) { x += bw + 1; continue; }

    const h     = Math.pow(v, 0.7) * H * 1.4;  // boost height, soften curve
    const alpha = 0.35 + v * 0.65;

    // Gradient: bright glowing tip → solid gold base
    const grad = ctx.createLinearGradient(0, H - h, 0, H);
    grad.addColorStop(0,   `rgba(255,230,160,${alpha * 0.9})`);
    grad.addColorStop(0.4, `rgba(232,201,142,${alpha * 0.7})`);
    grad.addColorStop(1,   `rgba(200,169,110,${alpha})`);
    ctx.fillStyle = grad;

    // Glow on tall bars
    if (v > 0.5) {
      ctx.shadowColor = `rgba(232,201,142,${(v - 0.5) * 0.8})`;
      ctx.shadowBlur  = 8 + v * 12;
    } else {
      ctx.shadowBlur = 0;
    }

    ctx.fillRect(x, H - h, Math.max(bw - 1, 1), h);
    x += bw + 1;
  }
  ctx.shadowBlur = 0;
}


/* ─────────────────────────────────────────────────────
   PLAYER CONTROLS
───────────────────────────────────────────────────── */
$('play-btn').addEventListener('click', togglePlay);
function togglePlay() {
  if (isPlaying) { audio.pause(); $('play-btn').textContent = '▶'; isPlaying = false; }
  else           { audio.play();  $('play-btn').textContent = '⏸'; isPlaying = true; resumeAudioCtx(); }
}

$('restart-btn').addEventListener('click', () => {
  audio.currentTime = 0; currentIdx = -1; scrollToActive(-1);
  if (!isPlaying) togglePlay();
});

$('mute-btn').addEventListener('click', function () {
  audio.muted = !audio.muted; this.textContent = audio.muted ? '🔇' : '🔊';
});

$('back-btn').addEventListener('click', () => {
  audio.pause(); isPlaying = false; vizRunning = false; showScreen('s3'); currentIdx = -1;
});

$('prog-wrap').addEventListener('click', function (e) {
  const { left, width } = this.getBoundingClientRect();
  audio.currentTime = ((e.clientX - left) / width) * (audio.duration || 0);
});

/* Sync lyric highlight every time audio advances */
audio.addEventListener('timeupdate', () => {
  const t = audio.currentTime, d = audio.duration || 0;
  $('prog-fill').style.width = (d ? t / d * 100 : 0) + '%';
  $('p-time').textContent    = `${fmt(t)} / ${fmt(d)}`;

  let active = -1;
  for (let i = 0; i < lyrics.length; i++) {
    if (t >= lyrics[i].start && t < lyrics[i].end) { active = i; break; }
  }

  if (active !== currentIdx) {
    currentIdx = active;
    scrollToActive(active);
    recRenderer?.setActiveIndex(active);  // keep recording canvas in sync
  }
});


/* ─────────────────────────────────────────────────────
   RECORDING
   When ⏺ is pressed:
   1. A hidden 1280×720 <canvas> is created off-screen
   2. RecordingRenderer renders lyrics + waveform + title
      onto it every frame  (canvas = no CSS scaling = no centering issue)
   3. canvas.captureStream(30) + audioDest stream → MediaRecorder → .webm
   4. On audio end or ⏹ press → stop, auto-download
───────────────────────────────────────────────────── */
$('record-btn').addEventListener('click', () => {
  if (isRecording) stopRecording();
  else startRecording();
});

function startRecording() {
  if (!audioCtx || !audioDest) { alert('Start playback at least once before recording.'); return; }

  // Canvas must stay in the viewport (even nearly invisible) so the browser
  // composites it — captureStream on a truly off-screen canvas can produce
  // a blank or portrait-shaped stream in Chrome.
  const recCanvas = document.createElement('canvas');
  recCanvas.width  = 1280;
  recCanvas.height = 720;
  recCanvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;opacity:0.001;pointer-events:none;z-index:1;';
  document.body.appendChild(recCanvas);

  // Wait for fonts so Bebas Neue renders in the canvas, then start
  const startRenderer = () => {
    recRenderer = new RecordingRenderer(recCanvas, analyser, lyrics, songName);
    recRenderer.start();
  };
  document.fonts.ready.then(startRenderer);

  // Reset playback from 0
  audio.currentTime = 0;
  currentIdx = -1;
  scrollToActive(-1);
  recRenderer.setActiveIndex(-1);
  if (!isPlaying) togglePlay();

  // Build combined stream
  const canvasStream = recCanvas.captureStream(30);
  const combined = new MediaStream([
    ...canvasStream.getVideoTracks(),
    ...audioDest.stream.getAudioTracks(),
  ]);

  const mime = ['video/webm;codecs=vp9,opus', 'video/webm;codecs=vp8,opus', 'video/webm']
    .find(t => MediaRecorder.isTypeSupported(t)) || 'video/webm';

  const chunks = [];
  mediaRecorder = new MediaRecorder(combined, { mimeType: mime, videoBitsPerSecond: 8_000_000 });
  mediaRecorder.ondataavailable = e => { if (e.data.size > 0) chunks.push(e.data); };
  mediaRecorder.onstop = () => {
    recRenderer.stop();
    recCanvas.remove();
    recRenderer = null;
    downloadBlob(new Blob(chunks, { type: mime }), 'lyric-video.webm');
    setRecordingUI(false);
  };
  mediaRecorder.start(100);
  setRecordingUI(true);
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
}

function setRecordingUI(on) {
  isRecording = on;
  $('record-btn').textContent = on ? '⏹' : '⏺';
  $('record-btn').classList.toggle('recording', on);
  $('record-status').textContent = on ? '● RECORDING — press ⏹ to stop & download' : '';
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a   = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 30_000);
}


/* ─────────────────────────────────────────────────────
   RECORDING RENDERER — 1280×720 landscape canvas
   Mirrors the on-screen player layout exactly:

   Layout (top → bottom):
     • Dark background (#06060a)
     • Lyrics — 3-line drum-roll      (upper area)
     • Waveform bars                  (above controls)
     • Controls panel                 (bottom ~160px)
         – song title · progress bar · time · buttons
───────────────────────────────────────────────────── */
class RecordingRenderer {
  constructor(canvas, analyser, lyrics, songTitle) {
    this.canvas    = canvas;
    this.ctx       = canvas.getContext('2d');
    this.analyser  = analyser;
    this.freqBuf   = analyser ? new Uint8Array(analyser.frequencyBinCount) : null;
    this.lyrics    = lyrics;
    this.songTitle = songTitle.toUpperCase();

    this.scrollPos       = 0;
    this.targetScrollPos = 0;
    this.activeIdx       = -1;
    this.running         = false;
  }

  setActiveIndex(idx) {
    this.activeIdx = idx;
    if (idx >= 0) this.targetScrollPos = idx;
  }

  start() {
    this.running = true;
    const loop = () => {
      if (!this.running) return;
      this._render();
      requestAnimationFrame(loop);
    };
    loop();
  }

  stop() { this.running = false; }

  _render() {
    const { canvas, ctx } = this;
    const W = canvas.width, H = canvas.height;

    // Zone heights
    const CTRL_H = 160;   // bottom controls panel
    const WAVE_H = 70;    // waveform strip above controls
    const LYRIC_H = H - CTRL_H - WAVE_H;  // 490px at 720p

    this.scrollPos += (this.targetScrollPos - this.scrollPos) * 0.09;

    // 1. Background
    ctx.fillStyle = '#06060a';
    ctx.fillRect(0, 0, W, H);

    // 2. Waveform (sits between lyrics and controls)
    this._drawWaveform(W, H, LYRIC_H, WAVE_H);

    // 3. Top fade on lyrics area
    const topFade = ctx.createLinearGradient(0, 0, 0, LYRIC_H * 0.32);
    topFade.addColorStop(0, 'rgba(6,6,10,1)');
    topFade.addColorStop(1, 'rgba(6,6,10,0)');
    ctx.fillStyle = topFade;
    ctx.fillRect(0, 0, W, LYRIC_H * 0.32);

    // Bottom fade on lyrics area (into waveform)
    const botFade = ctx.createLinearGradient(0, LYRIC_H * 0.72, 0, LYRIC_H);
    botFade.addColorStop(0, 'rgba(6,6,10,0)');
    botFade.addColorStop(1, 'rgba(6,6,10,0.9)');
    ctx.fillStyle = botFade;
    ctx.fillRect(0, LYRIC_H * 0.72, W, LYRIC_H * 0.28);

    // 4. Lyrics
    this._drawLyrics(W, LYRIC_H);

    // 5. Controls panel
    this._drawControls(W, H, CTRL_H);
  }

  _drawWaveform(W, _H, yStart, maxBarH) {
    if (!this.analyser) return;
    this.analyser.getByteFrequencyData(this.freqBuf);

    const ctx = this.ctx;
    const buf = this.freqBuf;
    const bw  = (W / buf.length) * 2.5;
    const bot = yStart + maxBarH;  // bottom edge of waveform zone
    let x = 0;

    ctx.save();
    ctx.shadowBlur = 0;
    for (let i = 0; i < buf.length; i++) {
      const v = buf[i] / 255;
      if (v < 0.01) { x += bw + 1; continue; }

      const h     = Math.pow(v, 0.7) * maxBarH * 1.4;
      const alpha = 0.35 + v * 0.65;
      const grad  = ctx.createLinearGradient(0, bot - h, 0, bot);
      grad.addColorStop(0,   `rgba(255,230,160,${alpha * 0.9})`);
      grad.addColorStop(0.4, `rgba(232,201,142,${alpha * 0.7})`);
      grad.addColorStop(1,   `rgba(200,169,110,${alpha})`);
      ctx.fillStyle = grad;
      if (v > 0.5) { ctx.shadowColor = `rgba(232,201,142,${(v-0.5)*0.8})`; ctx.shadowBlur = 8 + v * 12; }
      else ctx.shadowBlur = 0;
      ctx.fillRect(x, bot - h, Math.max(bw - 1, 1), h);
      x += bw + 1;
    }
    ctx.shadowBlur = 0;
    ctx.restore();
  }

  _drawControls(W, H, CTRL_H) {
    const ctx    = this.ctx;
    const panelY = H - CTRL_H;
    const cx     = W / 2;

    // Panel gradient (fade in from transparent)
    const pg = ctx.createLinearGradient(0, panelY, 0, H);
    pg.addColorStop(0,   'rgba(6,6,10,0)');
    pg.addColorStop(0.15,'rgba(6,6,10,0.95)');
    pg.addColorStop(1,   'rgba(6,6,10,1)');
    ctx.fillStyle = pg;
    ctx.fillRect(0, panelY, W, CTRL_H);

    // Song title
    const titleY = panelY + 24;
    ctx.save();
    ctx.font         = `${Math.round(W * 0.018)}px 'Bebas Neue', sans-serif`;
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle    = '#c8a96e';
    ctx.globalAlpha  = 0.72;
    ctx.fillText(this.songTitle, cx, titleY);
    ctx.restore();

    // Progress bar
    const prog  = audio.duration ? audio.currentTime / audio.duration : 0;
    const barY  = panelY + 54;
    const barX  = W * 0.1;
    const barW  = W * 0.8;
    const barH  = 2;

    ctx.save();
    ctx.fillStyle = 'rgba(240,236,224,0.1)';
    ctx.fillRect(barX, barY, barW, barH);

    const fillG = ctx.createLinearGradient(barX, 0, barX + barW, 0);
    fillG.addColorStop(0, '#c8a96e');
    fillG.addColorStop(1, '#e8c98e');
    ctx.fillStyle = fillG;
    ctx.fillRect(barX, barY, barW * prog, barH);

    if (prog > 0) {
      ctx.shadowColor = '#c8a96e'; ctx.shadowBlur = 8;
      ctx.fillStyle = '#e8c98e';
      ctx.beginPath();
      ctx.arc(barX + barW * prog, barY + 1, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
    }
    ctx.restore();

    // Time
    const timeY = barY + 20;
    ctx.save();
    ctx.font         = `${Math.round(W * 0.012)}px 'Inter', sans-serif`;
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle    = 'rgba(240,236,224,0.42)';
    ctx.fillText(`${fmt(audio.currentTime)} / ${fmt(audio.duration)}`, cx, timeY);
    ctx.restore();

    // Buttons row
    const btnY = timeY + 38;
    const playR = Math.round(W * 0.028);

    // Restart icon (↩)
    ctx.save();
    ctx.font         = `${Math.round(W * 0.022)}px Arial`;
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle    = 'rgba(240,236,224,0.38)';
    ctx.fillText('↩', cx - 80, btnY);
    ctx.restore();

    // Play/Pause circle
    ctx.save();
    const pg2 = ctx.createRadialGradient(cx, btnY, 0, cx, btnY, playR);
    pg2.addColorStop(0, '#e8c98e'); pg2.addColorStop(1, '#c8a96e');
    ctx.fillStyle  = pg2;
    ctx.shadowColor = 'rgba(200,169,110,0.6)'; ctx.shadowBlur = 22;
    ctx.beginPath(); ctx.arc(cx, btnY, playR, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#06060a';
    if (audio.paused) {
      const ps = playR * 0.42;
      ctx.beginPath();
      ctx.moveTo(cx - ps * 0.55, btnY - ps);
      ctx.lineTo(cx + ps,        btnY);
      ctx.lineTo(cx - ps * 0.55, btnY + ps);
      ctx.closePath(); ctx.fill();
    } else {
      const ps = playR * 0.38;
      ctx.fillRect(cx - ps - 4, btnY - ps, ps * 0.75, ps * 2);
      ctx.fillRect(cx + 4,      btnY - ps, ps * 0.75, ps * 2);
    }
    ctx.restore();

    // Speaker icon (🔊)
    ctx.save();
    ctx.font         = `${Math.round(W * 0.021)}px Arial`;
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle    = 'rgba(240,236,224,0.38)';
    ctx.fillText(audio.muted ? '🔇' : '🔊', cx + 80, btnY);
    ctx.restore();
  }

  _drawLyrics(W, LYRIC_H) {
    if (!this.lyrics.length) return;

    const ctx     = this.ctx;
    const centerY = LYRIC_H * 0.52;
    const lineGap = LYRIC_H * 0.22;
    const maxFont = W * 0.062;
    const minFont = W * 0.026;

    const fromI = Math.floor(this.scrollPos - 1.6);
    const toI   = Math.ceil(this.scrollPos + 1.6);

    const entries = [];
    for (let i = fromI; i <= toI; i++) {
      if (i < 0 || i >= this.lyrics.length) continue;
      const dist = i - this.scrollPos, absDist = Math.abs(dist);
      if (absDist > 1.6) continue;
      entries.push({ i, dist, absDist });
    }
    entries.sort((a, b) => b.absDist - a.absDist);

    for (const { i, dist, absDist } of entries) {
      const y       = centerY + dist * lineGap;
      const opacity = Math.max(0, 1 - Math.pow(absDist, 0.75) * 0.78);
      const sizeT   = Math.max(0, 1 - absDist);
      const fontSize = Math.round(minFont + (maxFont - minFont) * sizeT);
      const goldT   = this.activeIdx >= 0 ? Math.max(0, 1 - absDist * 2.8) : 0;

      const r = Math.round(232 * goldT + 200 * (1 - goldT));
      const g = Math.round(201 * goldT + 192 * (1 - goldT));
      const b = Math.round(142 * goldT + 176 * (1 - goldT));

      ctx.save();
      ctx.globalAlpha  = opacity;
      ctx.textAlign    = 'center';
      ctx.textBaseline = 'middle';

      ctx.font = `${fontSize}px 'Bebas Neue', sans-serif`;
      const measured = ctx.measureText(this.lyrics[i].text).width;
      if (measured > W * 0.88) {
        ctx.font = `${Math.round(fontSize * (W * 0.88 / measured))}px 'Bebas Neue', sans-serif`;
      }

      if (goldT > 0.05) { ctx.shadowColor = `rgba(232,201,142,${goldT * 0.85})`; ctx.shadowBlur = 55 * goldT; }
      ctx.fillStyle = `rgb(${r},${g},${b})`;

      const squish = Math.max(0.65, 1 - absDist * 0.14);
      ctx.setTransform(1, 0, 0, squish, 0, y * (1 - squish));
      ctx.fillText(this.lyrics[i].text, W / 2, y);
      ctx.restore();
    }
  }
}
