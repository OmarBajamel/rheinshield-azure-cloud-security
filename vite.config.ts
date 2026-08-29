import { sites } from '@openai/sites-vite-plugin';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  base: process.env.GITHUB_ACTIONS ? '/rheinshield-azure-cloud-security/' : '/',
  plugins: [react(), sites()],
  build: { sourcemap: false, target: 'es2022' },
});
