// Render de carrossel com motion: PNG (estado final) e MP4 (animacao CSS quadro a quadro, 30 fps, H.264).
// Uso: node render-motion.js <pasta-dos-slides> <slides: 1,2,3 | all> [png|mp4|both]
// Duracao por slide: <body data-duracao="6500"> no HTML (padrao 7000 ms).
// Dependencias (instalar numa pasta temporaria, fora do repo): npm i playwright-core@1.47.2 ffmpeg-static@5.2.0
// e rodar com NODE_PATH apontando pra node_modules dela. Usa o Chromium que o Playwright ja baixou em %LOCALAPPDATA%/ms-playwright.
const { chromium } = require("playwright-core");
const ffmpeg = require("ffmpeg-static");
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const PW = path.join(process.env.LOCALAPPDATA, "ms-playwright");
const CR = fs.readdirSync(PW).filter((d) => /^chromium-\d+$/.test(d)).sort().pop();
const CHROME = path.join(PW, CR, "chrome-win64", "chrome.exe");
const FPS = 30;

(async () => {
  const [dir, quais, modo = "both"] = process.argv.slice(2);
  const nums = quais === "all"
    ? fs.readdirSync(dir).map((f) => (f.match(/^slide-(\d+)\.html$/) || [])[1]).filter(Boolean).map(Number).sort((a, b) => a - b)
    : quais.split(",").map(Number);
  const browser = await chromium.launch({ executablePath: CHROME, args: ["--force-color-profile=srgb", "--hide-scrollbars"] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });

  for (const n of nums) {
    const nome = "slide-" + String(n).padStart(2, "0");
    const html = path.join(dir, nome + ".html");
    if (!fs.existsSync(html)) { console.log("pula", nome); continue; }
    await page.goto("file:///" + html.replace(/\\/g, "/"), { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    const seek = (t) => page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), t);
    const dur = await page.evaluate(() => +document.body.dataset.duracao || 7000);

    if (modo !== "mp4") {
      await seek(dur - 300);
      await page.screenshot({ path: path.join(dir, nome + ".png") });
      console.log("png", nome);
    }
    if (modo !== "png") {
      const tmp = fs.mkdtempSync(path.join(require("os").tmpdir(), "quadros-"));
      const total = Math.round((dur / 1000) * FPS);
      for (let f = 0; f < total; f++) {
        await seek((f * 1000) / FPS);
        await page.screenshot({ path: path.join(tmp, "f" + String(f).padStart(4, "0") + ".jpg"), type: "jpeg", quality: 96 });
      }
      const saida = path.join(dir, nome + ".mp4");
      execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(tmp, "f%04d.jpg"),
        "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p", "-movflags", "+faststart", saida]);
      fs.rmSync(tmp, { recursive: true, force: true });
      console.log("mp4", nome, (fs.statSync(saida).size / 1e6).toFixed(1) + "MB");
    }
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
