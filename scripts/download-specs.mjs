#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'patchright';

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = join(__dirname, '..');
const configPath = join(rootDir, 'generation.yaml');
const specsDir = join(rootDir, 'specs');

function parseSpecs(yamlText) {
  const lines = yamlText.split(/\r?\n/);
  const specs = [];
  let inside = false;
  for (const line of lines) {
    if (/^specs:\s*$/.test(line)) { inside = true; continue; }
    if (inside && /^\S/.test(line)) { inside = false; }
    if (!inside) continue;
    const m = line.match(/^\s*-\s+(.+?)\s*$/);
    if (m) specs.push(m[1]);
  }
  return specs;
}

const urls = parseSpecs(readFileSync(configPath, 'utf8')).filter((s) => /^https?:\/\//.test(s));
if (urls.length === 0) {
  console.error(`Error: no HTTP(S) specs found in ${configPath}`);
  process.exit(1);
}

mkdirSync(specsDir, { recursive: true });

// WB's WBAAS v2 anti-bot (rolled out Aug 2026) blocks headless browsers with a
// "suspicious activity" challenge that never resolves. Running headful with the
// real Google Chrome channel passes it. CI has no display, so the caller wraps
// this in xvfb-run; locally the OS display is used. Override via env if needed.
const channel = process.env.WB_BROWSER_CHANNEL || 'chrome';
const headless = process.env.WB_HEADLESS === '1';
const browser = await chromium.launch({ headless, channel });
const context = await browser.newContext({
  userAgent:
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  locale: 'ru-RU',
  viewport: { width: 1280, height: 800 },
  extraHTTPHeaders: {
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
  },
});
const page = await context.newPage();

async function ensureAntibotPassed(probeUrl) {
  const deadline = Date.now() + 180_000;
  await page.goto(probeUrl, { waitUntil: 'domcontentloaded', timeout: 60_000 });
  let lastHead = '';
  while (Date.now() < deadline) {
    try {
      const head = await page.evaluate(() => (document.body?.innerText || '').slice(0, 80));
      if (head.startsWith('openapi:')) return;
      if (head !== lastHead) {
        console.log(`  [antibot] ${head.replace(/\s+/g, ' ').slice(0, 80)}`);
        lastHead = head;
      }
    } catch {
      // navigation in progress — ignore and retry
    }
    await page.waitForTimeout(2000);
  }
  throw new Error(`Antibot challenge did not resolve within timeout for ${probeUrl}`);
}

await ensureAntibotPassed(urls[0]);

let failed = 0;
for (const url of urls) {
  const filename = basename(url.split('?')[0]);
  const dest = join(specsDir, filename);
  process.stdout.write(`Downloading ${filename}\n`);

  const result = await page.evaluate(async (u) => {
    const r = await fetch(u, { credentials: 'include' });
    return { status: r.status, text: await r.text() };
  }, url);

  if (result.status !== 200) {
    console.error(`  failed: HTTP ${result.status} for ${url}`);
    failed += 1;
    continue;
  }
  if (!result.text.startsWith('openapi:')) {
    console.error(`  failed: response does not look like OpenAPI YAML for ${url}`);
    failed += 1;
    continue;
  }
  writeFileSync(dest, result.text);
}

await browser.close();

if (failed > 0) {
  console.error(`Error: ${failed} spec(s) failed to download`);
  process.exit(1);
}
