import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@tailwindcss/vite';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  integrations: [react()],
  vite: {
    plugins: [tailwind()],
  },
  adapter: node({
    mode: 'standalone',
  }),
});
