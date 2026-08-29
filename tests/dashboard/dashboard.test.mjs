import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { URL } from 'node:url';

const source = await readFile(new URL('../../src/main.tsx', import.meta.url), 'utf8');
const html = await readFile(new URL('../../index.html', import.meta.url), 'utf8');

test('all eight URL-addressable dashboard routes exist', () => {
  for (const route of ['executive','landing-zone','identity','soc','incident','risk','cost','methodology']) {
    assert.match(source, new RegExp(`['"]${route}['"]`));
  }
});

test('English, German, and the exact synthetic-data notice are present', () => {
  assert.match(source, /Security evidence, made inspectable/);
  assert.match(source, /Sicherheitsnachweise, klar nachvollziehbar/);
  assert.match(source, /Synthetic portfolio data — no real tenant, identity, incident, or customer information/);
});

test('required validation statuses and evidence claims are explicit', () => {
  for (const status of ['FIXTURE_VALIDATED','PLAN_VALIDATED','READY_NOT_AUTHENTICATED','READY_LICENSE_REQUIRED','SKIPPED_COST_GUARD']) assert.match(source, new RegExp(status));
  assert.match(source, /14\/14/);
  assert.match(source, /27/);
  assert.match(source, /No authenticated Azure subscription/);
});

test('static metadata has social preview and no remote runtime dependency', () => {
  assert.match(html, /og:image/);
  assert.match(html, /twitter:card/);
  assert.doesNotMatch(source, /fetch\(|axios|azure\.com\/subscriptions/);
});
