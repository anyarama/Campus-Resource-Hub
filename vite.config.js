import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    manifest: true,
    outDir: 'src/static/dist',
    assetsDir: 'assets',
    rollupOptions: {
      input: {
        style: resolve(__dirname, 'src/static/scss/main.scss'),
        enterpriseJs: resolve(__dirname, 'src/static/js/enterprise.js'),
      },
    },
  },
  base: '/static/dist/',
})
