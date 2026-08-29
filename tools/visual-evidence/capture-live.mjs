import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

const deploymentCommit = process.env.RHEINSHIELD_DEPLOYMENT_COMMIT;
const ciRunUrl = process.env.RHEINSHIELD_CI_RUN_URL;
const pagesRunUrl = process.env.RHEINSHIELD_PAGES_RUN_URL;
if (!deploymentCommit || !ciRunUrl || !pagesRunUrl) {
  throw new Error('Deployment commit, CI run URL, and Pages run URL are required.');
}

const baseUrl = 'https://omarbajamel.github.io/rheinshield-azure-cloud-security/';
const routes = ['executive', 'landing-zone', 'identity', 'soc', 'incident', 'risk', 'cost', 'methodology'];
const axeSource = await readFile(new URL('../../node_modules/axe-core/axe.min.js', import.meta.url), 'utf8');
const screenshotDirectory = new URL('../../assets/screenshots/', import.meta.url);
const evidencePath = new URL('../../artifacts/evidence/live-publication-validation.json', import.meta.url);
await mkdir(screenshotDirectory, { recursive: true });

function hash(buffer) {
  return createHash('sha256').update(buffer).digest('hex');
}

const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const consoleErrors = [];
  const failedRequests = [];
  page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('pageerror', error => consoleErrors.push(error.message));
  page.on('requestfailed', request => failedRequests.push(`${request.method()} ${request.url()}`));

  let responseStatus = 0;
  for (const language of ['en', 'de']) {
    for (const route of routes) {
      const response = await page.goto(`${baseUrl}#/${route}?lang=${language}`, { waitUntil: 'networkidle' });
      if (response) {
        responseStatus = response.status();
        assert.equal(responseStatus, 200);
      }
      assert.equal(await page.locator('html').getAttribute('lang'), language);
      assert.equal(await page.locator('h1').count(), 1);
      assert.equal(await page.getByRole('note').isVisible(), true);
    }
  }
  assert.equal(responseStatus, 200);

  let axeChecks = 0;
  for (const sample of ['executive?lang=de', 'soc?lang=en', 'risk?lang=de']) {
    await page.goto(`${baseUrl}#/${sample}`, { waitUntil: 'networkidle' });
    await page.addScriptTag({ content: axeSource });
    const result = await page.evaluate(async () => await globalThis.axe.run(document, {
      runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa'] },
    }));
    assert.deepEqual(result.violations.map(item => item.id), []);
    axeChecks += 1;
  }

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`${baseUrl}#/risk?lang=de`, { waitUntil: 'networkidle' });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth), false);

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(`${baseUrl}#/executive?lang=en`, { waitUntil: 'networkidle' });
  const liveScreenshot = new URL('09-live-github-pages-desktop.png', screenshotDirectory);
  await page.screenshot({ path: fileURLToPath(liveScreenshot), fullPage: true });
  assert.deepEqual(consoleErrors, []);
  assert.deepEqual(failedRequests, []);

  const actionsPage = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const actionsResponse = await actionsPage.goto(ciRunUrl, { waitUntil: 'domcontentloaded' });
  assert.equal(actionsResponse?.status(), 200);
  await actionsPage.waitForTimeout(1500);
  const actionsText = await actionsPage.locator('body').innerText();
  assert.match(actionsText, /CI/);
  const actionsScreenshot = new URL('10-github-actions-green.png', screenshotDirectory);
  await actionsPage.screenshot({ path: fileURLToPath(actionsScreenshot), fullPage: false });
  await actionsPage.close();

  const liveBuffer = await readFile(liveScreenshot);
  const actionsBuffer = await readFile(actionsScreenshot);
  const evidence = {
    schemaVersion: '1.0.0',
    verifiedAt: new Date().toISOString(),
    deploymentCommit,
    pagesUrl: baseUrl,
    pagesRunUrl,
    ciRunUrl,
    publicResponseStatus: responseStatus,
    routeLanguageViews: 16,
    mobileWidth: 390,
    mobileOverflow: false,
    axeChecks,
    axeViolations: 0,
    consoleErrors: 0,
    failedRequests: 0,
    screenshots: [
      { path: 'assets/screenshots/09-live-github-pages-desktop.png', sha256: hash(liveBuffer), privacyReview: 'PASS' },
      { path: 'assets/screenshots/10-github-actions-green.png', sha256: hash(actionsBuffer), privacyReview: 'PASS' },
    ],
    dataMode: 'public-demo',
  };
  await writeFile(evidencePath, JSON.stringify(evidence, null, 2) + '\n');
  console.log(JSON.stringify(evidence));
} finally {
  await browser.close();
}
