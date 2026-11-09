// Captura cada tarjeta de _fuente/tarjetas.py en 1200×630, sin movimiento (la escena ya completa).
// Uso: node _fuente/tarjetas.js <url-de-las-tarjetas> <lista.json> <carpeta-de-salida>
const fs = require('fs');
const { chromium } = require('playwright');
const [base, lista, salida] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  for (const slug of JSON.parse(fs.readFileSync(lista, 'utf8'))) {
    await p.goto(`${base}${slug}.html`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `${salida}/${slug}.jpg`, type: 'jpeg', quality: 86 });
  }
  await b.close();
})();
