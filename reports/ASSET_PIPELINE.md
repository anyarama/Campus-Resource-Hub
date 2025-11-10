# Asset Pipeline

1. **Source Entries:**
   - SCSS: `src/static/scss/enterprise.scss` (imports tokens, base, utilities, components, pages).
   - JS: `src/static/js/enterprise.js` (UI shell), plus feature modules (charts, resource filters, booking drawer, messages, admin dashboard, adapters).
2. **Build Tool:** Vite 5 (`vite.config.js`)
   - Output dir: `src/static/dist`
   - Manifest: `src/static/dist/.vite/manifest.json`
   - Inputs mapped under `rollupOptions.input`.
3. **Runtime Resolution:** `src/utils/vite.py:vite_asset(name)` reads manifest and returns hashed URLs; registered as `vite_asset` Jinja global in `src/app.py`.
4. **Templates:** `base.html` includes only `{{ vite_asset('enterprise.css') }}` and `{{ vite_asset('app.js') }}` so every page inherits compiled styles/scripts. Page-specific bundles (e.g., `resourceFilters`, `bookingDrawer`) are imported dynamically inside those entry files.
5. **Commands:**
   - `npm run dev` for Vite dev server (if configured).
   - `npm run build` or `make web-assets` to produce hashed artifacts + manifest.
   - CI (to be added in later phases) must run `npm ci && npm run build` before `pytest` to ensure manifest exists.
