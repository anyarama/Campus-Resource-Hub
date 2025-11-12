# Phase Report – Campus Resource Hub

## Phase 1 — Asset Resolver

- **Manifest helper**: Introduced `src/utils/assets.py#get_asset_url`, added friendly aliases (`asset_url`) and special mappings for `style.css`/`enterprise.js`, plus thread-safe manifest caching with fallback logging.
- **Flask wiring**: `src/app.py` now imports the new helper, registers `asset_url` globally, and `_debug_assets` uses the same path so CLI/debug endpoints stay in sync.
- **Base template**: `src/templates/base.html` loads CSS/JS via `{{ asset_url('style.css') }}` and `{{ asset_url('enterprise.js') }}` to eliminate brittle hashed paths.

### Verification

| Check | Command | Result |
| --- | --- | --- |
| Vite build | `npm run build` | ✅ (Dart Sass legacy warnings remain from upstream mixins) |
| Format & lint | `make fmt && make lint` | ✅ |
| Python tests | `make test` | ✅ 188 tests |
| Grep – hashed assets | `grep -R "style-.*\\.css\\|enterpriseJs-.*\\.js" src/templates` | ✅ no matches |

### Remaining Risks / Follow-ups

1. Other templates still call `vite_asset(...)` or inline hashed module imports (e.g., `src/templates/resources/dashboard.html:129-135`) — will be cleaned during later phases.
2. Backup/legacy templates (`*.bak`, `.before_migrate`) continue to trigger Bootstrap/escaped HTML greps until removed in Phase 6.
3. Sass deprecation warnings (legacy API, global built-ins) surface during `npm run build`; addressing them is out-of-scope for Phase 1 but should be tracked for the tokens cleanup phase.

## Phase 2 — Template & Macro Safety

- **Booking templates restored**: Rebuilt `bookings/detail.html`, `bookings/my_bookings.html`, `_booking_card.html`, and `bookings/new.html` with clean markup (no escaped strings), accessible sections, and fully-formed forms/buttons. Forms now include CSRF tokens and proper action URLs instead of orphaned literal strings.
- **Profile template sanitized**: `auth/profile.html` reauthored to remove malformed fragments and ensure avatar, metadata, and admin links render through real markup.
- **Component hygiene**: Booking card macro now produces structured HTML instead of template fragments, keeping badge/status logic centralized and safe for reuse.

### Verification

| Check | Command | Result |
| --- | --- | --- |
| Vite build | `npm run build` | ✅ |
| Format & lint | `make fmt && make lint` | ✅ |
| Python tests | `make test` | ✅ |
| Escaped buttons | `grep -R "class=\\\"btn" src/templates | sed -n '1,40p'` | ✅ Only shows real markup (no literal fragments) |
| Browse CTA | `grep -R "<a href=.*>\\s*Browse" src/templates` | ✅ Only valid anchor tags remain |

### Remaining Risks / Follow-ups

1. Tabs experience on `bookings/my_bookings.html` is now sectional rather than interactive; a future pass should wire it into the shared tabs component or a11y JS once `tabs.js` is implemented.
2. Legacy backups under `src/templates/bookings/*.before_migrate.html` still exist; they'll be removed during Phase 6 cleanup.
3. Sidebar/layout SCSS still references Bootstrap-era selectors; addressed in later phases focused on sidebar polish and dead code removal.

## Phase 3 — Chart.js Enablement

- **Server-driven dashboard data**: `src/routes/resources.py` now composes KPIs, upcoming bookings, recent activity, and chart-ready datasets directly from SQLAlchemy queries via new helper functions (`_build_dashboard_context`, `_build_dashboard_chart_config`, etc.). The `/dashboard` route passes `dashboard_kpis`, `upcoming_bookings`, `recent_activity`, and `dashboard_chart_config` to the template.
- **Template rebuild**: `src/templates/resources/dashboard.html` renders the KPIs, lists, and cards on the server and exposes two canvases (`#chart-bookings`, `#chart-categories`). Inline module imports were removed; instead the template drops a small script that calls `window.initDashboardCharts(...)` with the serialized config.
- **Enterprise bundle owns charts**: `src/static/js/enterprise.js` now imports `chart.js/auto`, exports `initDashboardCharts`, and attaches it to `window`. Charts re-render whenever the theme toggles (ThemeManager emits `crh-theme-change`). The helper handles line/doughnut configs, palette assignment, and theme-aware tooltips/grids.

### Verification

| Check | Command | Result |
| --- | --- | --- |
| Build assets | `npm run build` | ✅ (same Sass warnings as Phase 1) |
| Format & lint | `make fmt && make lint` | ✅ |
| Tests | `make test` | ✅ 188 tests |

### Remaining Risks / Follow-ups

1. `admin/analytics.html` still imports `charts.js` directly; future cleanup could migrate that page to the shared `initDashboardCharts` helper.
2. Dashboard KPIs currently show absolute totals; trend deltas from the old mock data aren’t reinstated yet.
3. The chart config relies on 7-day and owner-category snapshots; specs may evolve to require richer analytics or pagination.

## Phase 5 — IU Tokens Applied

- **Token palette extended**: Added supporting accent variables in `src/static/scss/tokens.scss` (sky/indigo/purple/amber/emerald/blue shades) so we can reference IU-compliant hues without resorting to raw hex codes.
- **Component refactors**: Updated `activity-feed.scss`, `filter-drawer.scss`, `button.scss`, `alert.scss`, `kpi-tile.scss`, and `modal.scss` to pull from the token set. This covers icon badges, KPI tiles, alert variants, modals, and category chips. Also replaced legacy `rgba(var(--color...` patterns with `color-mix` to keep spec-compliant color math.
- **Global polish**: `navbar.scss` and `sidebar.scss` now express focus states via `color-mix`, keeping the new token system consistent even outside the targeted components.

### Verification

| Check | Command | Result |
| --- | --- | --- |
| Vite build | `npm run build` | ✅ |
| Format | `make fmt` | ✅ |
| Tests | `make test` | ✅ 188 tests |
| Hex scan | `grep -R "#[0-9a-fA-F]\\{3,6\\}" src/static/scss/components` | ✅ No matches |

### Remaining Risks / Follow-ups

1. We now lean on `color-mix` for translucent brand shades; if legacy browsers without `color-mix` support are in scope we may need a Sass fallback.
2. Accent tokens live alongside the Crimson palette in `tokens.scss`; future contributors should continue routing any new supporting colors through that file to avoid regressions.
3. Some page-level SCSS (e.g., page-specific charts) still uses legacy color logic; if we extend Phase 5 later we should propagate the same token discipline beyond the components directory.

## Phase 6 — Cleanup & UI Guardrails

- **Legacy template purge**: Removed all `.bak`, `.before_migrate.html`, and `.bootstrap_backup` files under `src/templates/` so greps and Playwright runs no longer trip over dead markup.
- **Bootstrap remnants removed**: Deleted `src/static/scss/compat/bootstrap-bridge.scss`, its empty parent directory, and the unused `scripts/migrate_bootstrap_removal.sh`. `src/static/scss/main.scss` now documents that the bridge is gone, and admin dashboards swap the last `g-3` gutter utilities for the native `gap-lg` helper.
- **UI lint workflow**: Added `scripts/ui_lint.py` plus the `make ui-lint` target (and docs entry) to block Bootstrap grid classes, hashed asset filenames, and raw hex usage inside `src/static/scss/components`. This target now ships with `make all`, and now covers page-level SCSS plus `data-bs-*` attributes.

### Verification

| Check | Command | Result |
| --- | --- | --- |
| UI lint | `make ui-lint` | ✅ |
| Formatters | `make fmt` | ✅ |
| Backend tests | `make test` | ✅ 188 tests |
| Vite build | `npm run build` | ✅ (same Sass legacy warnings noted in earlier phases) |

### Remaining Risks / Follow-ups

1. `ui_lint.py` now scans components and pages but still ignores `base/` + `utilities/` SCSS; extend coverage there once those files complete the token migration.
2. Sass still emits the legacy `type-of` warning from `utilities/spacing.scss`; the planned design-token refactor should swap in `meta.type-of` before Dart Sass 3.0.

## Phase 7 — UI Smoke & A11y Coverage

- **Playwright coverage**: Expanded `tests/playwright/smoke.spec.ts` with reusable console tracking plus new smoke cases for `/dashboard`, `/resources`, and `/bookings/my-bookings` that assert chart canvases, sidebar tooltips, and axe scans stay clean. These tests now fail fast on console warnings and ensure tooltip metadata is present on every `.app-sidebar .sidebar-link`.
- **Template wiring**: Replaced every `data-bs-*` modal/tab/dropdown trigger with the enterprise helpers in `src/templates/bookings/detail.html`, `src/templates/admin/user_detail.html`, `src/templates/resources/my_resources.html`, and `src/templates/reviews/_review_list.html` so smoke tests interact with the same attributes the JS managers expect.
- **Contrast fixes**: Updated the guest/auth styles (`src/static/scss/pages/auth.scss`) to reuse the Crimson token for primary CTAs and footer links, bringing the login page back into WCAG 2.1 AA compliance (axe no longer flags the header register button).
- **ui-lint guardrail**: `scripts/ui_lint.py` now checks both `components/` and `pages/` SCSS trees for stray hex codes and bans `data-bs-*` attributes entirely, keeping the test suite and lint pass aligned.

### Verification

| Check | Command | Result |
| --- | --- | --- |
| UI lint | `make ui-lint` | ✅ |
| Playwright smoke + axe | `npm run test:playwright` | ✅ (14 specs) |
| Vite build | `npm run build` | ✅ (same Sass legacy warnings noted above) |

### Remaining Risks / Follow-ups

1. Console tracking in the smoke suite currently treats warnings and errors equally; if we introduce intentional warnings we may need a more granular allowlist.
2. Modal/tab helpers now rely on data attributes but we still duplicate some markup in admin views; consider consolidating via shared macros to reduce drift.
3. Playwright still seeds the dev database via SQLite each run; if future suites mutate data heavily we may need to parallelize via isolated DB files.
