import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    manifest: true,
    outDir: 'src/static/dist',
    assetsDir: 'assets',
    rollupOptions: {
      input: {
        enterprise: resolve(__dirname, 'src/static/scss/enterprise.scss'),
        app: resolve(__dirname, 'src/static/js/enterprise.js'),
        charts: resolve(__dirname, 'src/static/js/charts.js'),
        dashboardData: resolve(__dirname, 'src/static/js/adapters/dashboardData.js'),
        resourceFilters: resolve(__dirname, 'src/static/js/resource-filters.js'),
        imageCarousel: resolve(__dirname, 'src/static/js/image-carousel.js'),
        bookingDrawer: resolve(__dirname, 'src/static/js/booking-drawer.js'),
        messages: resolve(__dirname, 'src/static/js/messages.js'),
        adminDashboard: resolve(__dirname, 'src/static/js/admin-dashboard.js'),
      },
      output: {
        entryFileNames: (chunkInfo) => {
          // Output app.js for JavaScript entries
          return chunkInfo.name === 'app' ? 'assets/[name]-[hash].js' : 'assets/[name]-[hash].js';
        },
        assetFileNames: (assetInfo) => {
          // Output enterprise.css for SCSS entries
          if (assetInfo.name && assetInfo.name.endsWith('.css')) {
            return 'assets/enterprise-[hash].css';
          }
          return 'assets/[name]-[hash][extname]';
        },
      },
    },
  },
  base: '/static/dist/',
})
