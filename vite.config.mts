import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  root: __dirname,
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern',
      },
    },
  },
  build: {
    // Emit to wherever your backend serves static files from:
    outDir: path.resolve(__dirname, 'src/static/dist'),
    assetsDir: '',                  // put files directly in dist
    emptyOutDir: false,             // don’t blow away other assets
    manifest: true,                 // generate manifest.json
    cssCodeSplit: false,            // single CSS file
    rollupOptions: {
      input: {
        // Name the CSS asset in the manifest as "app.css"
        'app.css': path.resolve(__dirname, 'ui-system/scss/index.scss'),
      },
      output: {
        // Force deterministic CSS file name
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith('.css')) {
            return 'app.[hash].css';
          }
          return '[name].[hash][extname]';
        },
      },
    },
  },
});
