import { spawn } from 'node:child_process';
import { chromium } from 'playwright-core';

export async function waitFor(url, timeout = 20000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    try { if ((await fetch(url)).ok) return; } catch { /* server is starting */ }
    await new Promise(resolve => setTimeout(resolve, 200));
  }
  throw new Error(`Timed out waiting for ${url}`);
}

export async function withDashboard(callback) {
  const server = spawn(process.execPath, ['node_modules/vite/bin/vite.js', 'preview', '--host', '127.0.0.1', '--port', '4173'], { stdio: 'ignore', windowsHide: true });
  let browser;
  try {
    await waitFor('http://127.0.0.1:4173/');
    browser = await chromium.launch({ channel: 'chrome', headless: true });
    return await callback(browser);
  } finally {
    if (browser) await browser.close();
    server.kill('SIGTERM');
  }
}
