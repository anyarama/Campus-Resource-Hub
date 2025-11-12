# Campus Resource Hub – Operations Runbook

This document captures the day-to-day commands required to build, run, and troubleshoot the project across development and production environments.

---

## 1. Prerequisites

- **Python** 3.12+
- **Node.js** 18+ (we use Node 20 in CI)
- **npm** (bundled with Node)
- SQLite (default dev DB) – no extra install on macOS/Linux

Optional tooling: `make`, `pyenv`, `direnv`.

---

## 2. Environment Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install
```

Initialize and seed the development database:

```bash
make init-db      # creates the schema
make seed-db      # optional: load sample data
```

To clear everything (⚠️ destructive):

```bash
make reset-db
```

---

## 3. Local Development

### Flask API

```bash
make run
```

This runs Flask with `FLASK_ENV=development` on `http://localhost:5001`.

### Asset Dev Server

While Flask serves prebuilt assets, live UI work is easier with Vite:

```bash
npm run dev
```

The Vite dev server injects hot-reloaded JS/CSS; `vite_asset()` handles the proxying automatically in development.

---

## 4. Testing & Quality Gates

- Backend/unit/integration tests: `make test`
- UI smoke + axe scans (Playwright): `make ui-smoke`
- UI lint guardrails (bootstrap/grid/tokens): `make ui-lint`
- Formatting & linting: `make fmt`, `make lint`
- Full gate (fmt + lint + pytest + Playwright + build): `make all`

For coverage reports: `make test-cov` and open `htmlcov/index.html`.

End-to-end smoke runs inside CI via `npm run test:playwright`; locally you can use the same command or `make ui-smoke`.

---

## 5. Building Assets

Prod-equivalent builds:

```bash
make build         # npm run build
make web-assets    # legacy manifest verification helper
```

Artifacts land in `src/static/dist/` and are read via `vite_asset()` at runtime.

---

## 6. Playwright / Axe Notes

- Browsers are installed via `npx playwright install --with-deps`.
- Tests live under `tests/playwright` and `tests/ui`.
- Config (`playwright.config.ts`) automatically boots the Flask app using `scripts/run_e2e_server.sh`, which wipes and seeds the SQLite DB.

Useful during debugging:

```bash
npm run test:playwright -- --debug
```

---

## 7. Production Checklist

1. `make all` – must pass locally.
2. Ensure CI (`.github/workflows/ci.yml`) is green (runs npm build, pytest, Playwright).
3. Build assets: `npm run build`.
4. Set `FLASK_ENV=production` (and configure `APP_SETTINGS` if needed).
5. Run via `gunicorn 'src.app:create_app()'` or container entrypoint of your choice.
6. Provision persistent storage for `instance/` if using SQLite, or point SQLAlchemy to Postgres/MySQL.

---

## 8. Troubleshooting

| Symptom | Mitigation |
| --- | --- |
| Missing hashed assets in HTML | Re-run `npm run build`, ensure `vite_asset()` sees `manifest.json`. |
| Playwright fails connecting to Flask | Check `scripts/run_e2e_server.sh` logs; ensure port 5001 is free. |
| “extended multiple times” template error | Re-run `python scripts/codemods/normalize_templates.py` to dedupe extends blocks. |
| Seed data missing | `make reset-db && make seed-db` or run `scripts/run_e2e_server.sh` locally. |

---

## 9. Useful Scripts

- `scripts/run_e2e_server.sh` – resets DB, seeds demo data, runs Flask for Playwright.
- `scripts/audit_routes.py`, `scripts/audit_templates.py`, `scripts/audit_assets.py` – reporting utilities from Phase A.
- `scripts/dev/mark_dead.py` – dead code detector; outputs `/reports/DEAD_CODE.md`.
- `scripts/codemods/normalize_templates.py` – enforces IU template conventions.

Keep these in mind when onboarding new contributors or automating additional workflows. Updates to this runbook are welcome whenever the deployment story changes.
