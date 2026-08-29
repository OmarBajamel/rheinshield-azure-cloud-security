import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { withDashboard } from './browser-runtime.mjs';

const output = new URL('../../assets/screenshots/', import.meta.url);
await mkdir(output, { recursive: true });
const captures = [
  ['executive','01-executive-security-overview-desktop.png','en',1440,1000,'Recruiter hero and executive assurance summary'],
  ['landing-zone','02-landing-zone-governance-desktop.png','en',1440,1000,'Enterprise versus lab architecture'],
  ['soc','03-soc-detection-coverage-desktop.png','en',1440,1000,'Detection catalog and fixture results'],
  ['incident','04-incident-investigation-desktop.png','en',1440,1000,'INC-001 investigation timeline'],
  ['risk','05-risk-compliance-desktop.png','en',1440,1000,'Risk treatment and framework mapping'],
  ['identity','06-zero-trust-identity-desktop.png','en',1440,1000,'Identity and Zero Trust design'],
  ['executive','07-german-dashboard-desktop.png','de',1440,1000,'German recruiter view'],
  ['executive','08-executive-security-overview-mobile.png','en',390,844,'Mobile executive view'],
];

const items = await withDashboard(async browser => {
  const results = [];
  for (const [route, filename, language, width, height, use] of captures) {
    const page = await browser.newPage({ viewport: { width, height } });
    const errors = [];
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`http://127.0.0.1:4173/#/${route}?lang=${language}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(100);
    const fileUrl = new URL(filename, output);
    await page.screenshot({ path: fileURLToPath(fileUrl), fullPage: true });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    if (errors.length || overflow) throw new Error(`${filename}: console=${errors.join(';')} overflow=${overflow}`);
    const buffer = await readFile(fileUrl);
    results.push({ path:`assets/screenshots/${filename}`, route:`#/${route}?lang=${language}`, viewport:`${width}x${height}`, language, dataMode:'public-demo', validationMode:'FIXTURE_VALIDATED', sha256:createHash('sha256').update(buffer).digest('hex'), privacyReview:'PASS', intendedUse:use, altText:`${use}. Synthetic RheinShield portfolio dashboard; no real tenant data.` });
    await page.close();
  }
  return results;
});

let commit = 'UNCOMMITTED';
try { commit = execFileSync('git', ['rev-parse','HEAD'], { encoding:'utf8' }).trim(); } catch { /* initial build */ }
await writeFile(new URL('../../artifacts/evidence/screenshot-manifest.json', import.meta.url), JSON.stringify({ schemaVersion:'1.0.0', capturedAt:new Date().toISOString(), commitSha:commit, items }, null, 2) + '\n');
console.log(JSON.stringify({ screenshots:items.length, privacyReview:'PASS' }));
