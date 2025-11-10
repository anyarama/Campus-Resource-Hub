# Style Load Audit (Phase A)

- `base.html` now injects a single CSS link (`{{ vite_asset('enterprise.css') }}`) and JS bundle (`{{ vite_asset('app.js') }}`) guaranteeing consistent IU styling.
- Audit scripts (`scripts/audit_assets.py`, `scripts/http_probe.py`) inspect rendered HTML via Flask's test client to ensure `enterprise.css` is referenced on every smoke URL in `scripts/dev/smoke_urls.txt`.
- Known caveats: legacy guest pages (e.g., `/auth/login`) rely on `guest-layout` classes but still inherit enterprise styles through base.
- Upcoming work: ensure dark mode attr toggles update `data-theme` consistently and remove any inline styles flagged by `scripts/audit_templates.py`.

## Current Status
- Audit run: 2025-11-10T01:27:17Z
- Result: All smoke URLs responded with 200 and referenced /static/dist/ assets (see scripts/audit_assets.py output).

