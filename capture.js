const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const WIDTH = 1280;
const HEIGHT = 800;
const DURATION = 90; // seconds (matches ANIM_DURATION in animation.html)
const FPS = 16;
const TOTAL_FRAMES = Math.floor(DURATION * FPS);
const FRAME_DIR = path.join(__dirname, 'frames');
const OUTPUT = path.join(__dirname, 'animation.mp4');

if (!fs.existsSync(FRAME_DIR)) fs.mkdirSync(FRAME_DIR, { recursive: true });

// Clean old frames
for (const f of fs.readdirSync(FRAME_DIR)) {
  fs.unlinkSync(path.join(FRAME_DIR, f));
}

async function capture() {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
    ],
    headless: 'new',
  });

  const page = await browser.newPage();
  await page.setViewport({ width: WIDTH, height: HEIGHT });

  const filePath = 'file://' + path.resolve(__dirname, 'animation.html');
  console.log('Loading:', filePath);
  await page.goto(filePath, { waitUntil: 'networkidle0', timeout: 30000 });

  // Start capturing immediately at the start of animation
  const total = TOTAL_FRAMES;
  console.log(`Capturing ${total} frames at ${FPS} fps...`);

  for (let i = 0; i < total; i++) {
    await new Promise(r => setTimeout(r, 1000 / FPS));

    // Capture the canvas via screenshot
    const frameFile = path.join(FRAME_DIR, `frame_${String(i).padStart(5, '0')}.png`);
    await page.screenshot({ path: frameFile, type: 'png', omitBackground: true });

    const pct = Math.round((i / total) * 100);
    process.stdout.write(`\r  Frame ${i + 1}/${total} (${pct}%)`);
  }
  console.log('\nEncoding video...');

  await browser.close();

  // Encode with ffmpeg
  const ffmpegCmd = [
    'ffmpeg', '-y',
    '-framerate', String(FPS),
    '-i', path.join(FRAME_DIR, 'frame_%05d.png'),
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-crf', '20',
    '-preset', 'fast',
    OUTPUT
  ];

  const { execSync } = require('child_process');
  execSync(ffmpegCmd.join(' '), { stdio: 'inherit' });

  console.log(`\nDone! Video saved to: ${OUTPUT}`);
}

capture().catch(err => { console.error(err); process.exit(1); });