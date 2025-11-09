import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: 'src/static',
  base: '/static/',
  
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        enterprise: resolve(__dirname, 'src/static/scss/enterprise.scss'),
        enterpriseJs: resolve(__dirname, 'src/static/js/enterprise.js'),
      },
    },
    cssCodeSplit: false,
  },
  
  server: {
    port: 5173,
    strictPort: true,
    origin: 'http://localhost:5173',
  },
  
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "sass:math"; @use "sass:color";`,
      },
    },
  },
});
