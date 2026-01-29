// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import svelte from '@astrojs/svelte';

import node from '@astrojs/node';

// https://astro.build/config
export default defineConfig({
  output: 'server',
  integrations: [
    svelte(),
  ],
  vite: {
    plugins: [tailwindcss(), svelte()]
  },
  adapter: node({
    mode: 'standalone'
  }),
});