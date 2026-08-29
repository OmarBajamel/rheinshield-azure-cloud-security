import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { withDashboard } from '../../tools/visual-evidence/browser-runtime.mjs';

const routes = ['executive','landing-zone','identity','soc','incident','risk','cost','methodology'];
const axeSource = await readFile(new URL('../../node_modules/axe-core/axe.min.js', import.meta.url), 'utf8');

await withDashboard(async browser => {
  const page = await browser.newPage({ viewport: { width:1440, height:1000 } });
  const consoleErrors = [];
  page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('pageerror', error => consoleErrors.push(error.message));
  for (const language of ['en', 'de']) {
    for (const route of routes) {
      await page.goto(`http://127.0.0.1:4173/#/${route}?lang=${language}`, { waitUntil:'networkidle' });
      assert.equal(await page.locator('html').getAttribute('lang'), language);
      assert.equal(await page.locator('h1').count(), 1);
      assert.equal(await page.getByRole('note').isVisible(), true);
    }
  }
  await page.goto('http://127.0.0.1:4173/#/executive?lang=en');
  await page.getByRole('button', { name:'Deutsche Ansicht öffnen' }).click();
  await page.waitForURL(/lang=de/);
  assert.equal(await page.locator('html').getAttribute('lang'), 'de');
  assert.match(await page.locator('h1').innerText(), /Sicherheitsnachweise/);
  for (const sample of ['executive?lang=de', 'soc?lang=en', 'risk?lang=de']) {
    await page.goto(`http://127.0.0.1:4173/#/${sample}`);
    await page.addScriptTag({ content:axeSource });
    const axe = await page.evaluate(async () => await globalThis.axe.run(document, { runOnly:{ type:'tag', values:['wcag2a','wcag2aa','wcag21aa'] } }));
    if (axe.violations.length) console.log(JSON.stringify(axe.violations.map(v => ({ id:v.id, impact:v.impact, nodes:v.nodes.map(n=>({ target:n.target, html:n.html, summary:n.failureSummary })) })), null, 2));
    assert.deepEqual(axe.violations.map(item => item.id), []);
  }
  await page.setViewportSize({ width:390, height:844 });
  await page.goto('http://127.0.0.1:4173/#/risk?lang=de');
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth), false);
  await page.getByRole('button', { name:'Navigation öffnen' }).click();
  assert.equal(await page.getByRole('navigation').isVisible(), true);
  assert.deepEqual(consoleErrors, []);
  console.log(JSON.stringify({ routes:8, languages:2, routeViews:16, mobile:true, axeChecks:3, axeViolations:0, consoleErrors:0 }));
});
