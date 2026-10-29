// Tira os prints de uma referência do swipe.
// Uso:
//   node capturar.js <id> <url>             site: capa (tela de abertura) + página inteira + celular
//   node capturar.js <id> <arquivo.png|jpg> imagem local (carrossel, story): só a capa
// Saída em prints/: <id>.jpg (capa), <id>-full.jpg (página inteira), <id>-cel.jpg (celular).
const { chromium } = require("playwright-core");
const fs = require("fs");
const path = require("path");

const PW = path.join(process.env.LOCALAPPDATA, "ms-playwright");
const CR = fs.readdirSync(PW).filter((d) => /^chromium-\d+$/.test(d)).sort().pop();
const CHROME = path.join(PW, CR, "chrome-win64", "chrome.exe");
const SAIDA = path.join(__dirname, "prints");
const ALTURA_MAX = 9000; // corta páginas muito longas

const [id, alvo] = process.argv.slice(2);
if (!id || !alvo) {
  console.error("uso: node capturar.js <id> <url | arquivo de imagem>");
  process.exit(1);
}

// Rola a página inteira pra disparar animação de entrada e imagem preguiçosa.
async function rolarTudo(page) {
  await page.evaluate(async () => {
    const passo = innerHeight * 0.8;
    for (let y = 0; y < document.documentElement.scrollHeight; y += passo) {
      scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 120));
    }
    scrollTo(0, 0);
  });
  await page.waitForTimeout(600);
}

(async () => {
  fs.mkdirSync(SAIDA, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME, args: ["--force-color-profile=srgb", "--hide-scrollbars"] });
  const local = !/^https?:\/\//.test(alvo);

  if (local) {
    const arq = path.resolve(alvo);
    const page = await browser.newPage({ viewport: { width: 720, height: 900 } });
    // Abre a imagem direto (página em branco não pode carregar file://).
    await page.goto("file:///" + arq.replace(/\\/g, "/"));
    await page.addStyleTag({ content: "body{margin:0;background:#0A0A0A} img{display:block;width:720px;height:auto}" });
    const img = page.locator("img");
    await img.evaluate((el) => (el.complete && el.naturalWidth) || new Promise((r) => (el.onload = r)));
    await img.screenshot({ path: path.join(SAIDA, `${id}.jpg`), type: "jpeg", quality: 82 });
    console.log(JSON.stringify({ id, capa: `prints/${id}.jpg` }));
    await browser.close();
    return;
  }

  // Desktop: capa e página inteira. Movimento reduzido pra pegar o estado final.
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto(alvo, { waitUntil: "networkidle", timeout: 60000 }).catch(() => {});
  await page.waitForTimeout(1500);
  const titulo = await page.title();
  await page.screenshot({ path: path.join(SAIDA, `${id}.jpg`), type: "jpeg", quality: 80 });
  await rolarTudo(page);
  const altura = await page.evaluate(() => document.documentElement.scrollHeight);
  await page.screenshot({
    path: path.join(SAIDA, `${id}-full.jpg`), type: "jpeg", quality: 70,
    fullPage: altura <= ALTURA_MAX,
    clip: altura > ALTURA_MAX ? { x: 0, y: 0, width: 1440, height: ALTURA_MAX } : undefined,
  });

  // Celular.
  const cel = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, reducedMotion: "reduce" });
  const pc = await cel.newPage();
  await pc.goto(alvo, { waitUntil: "networkidle", timeout: 60000 }).catch(() => {});
  await pc.waitForTimeout(1200);
  await pc.screenshot({ path: path.join(SAIDA, `${id}-cel.jpg`), type: "jpeg", quality: 78 });

  await browser.close();
  console.log(JSON.stringify({ id, titulo, altura, capa: `prints/${id}.jpg`, full: `prints/${id}-full.jpg`, cel: `prints/${id}-cel.jpg` }));
})().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
