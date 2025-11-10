# Campus-Resource-Hub

Campus Resource Hub is the AiDD 2025 capstone project: a full‑stack platform where departments, student orgs, and individuals list, discover, and book campus assets. Features include advanced search & filtering, booking workflows with conflict detection, role-based approvals, review/rating systems, and admin analytics.

---

## Developer Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install

make init-db
make seed-db        # optional demo data
```

- `make run` starts the Flask API on `http://localhost:5001`.
- `npm run dev` launches Vite for hot-reloaded JS/CSS during UI work.

For additional operational guidance (environments, deployment, common scripts) see [`docs/OPERATIONS.md`](docs/OPERATIONS.md).

---

## Quality & Testing

| Command | Description |
| --- | --- |
| `make fmt` | Black + Ruff formatting pass |
| `make lint` | Static type checks with mypy |
| `make test` | Full pytest suite (unit + integration + smoke) |
| `make ui-smoke` | Playwright + axe-core accessibility smoke tests |
| `make test-cov` | Pytest with coverage + HTML report |
| `make all` | fmt + lint + pytest + Playwright + build (CI-equivalent gate) |

> The Playwright suite boots Flask via `scripts/run_e2e_server.sh`, re-seeding SQLite automatically.

---

## Asset Pipeline

- Local dev: `npm run dev` (Vite dev server) – `vite_asset()` swaps to dev mode automatically.
- Production build: `make build` (alias for `npm run build`) to emit hashed assets in `src/static/dist/`.
- Legacy manifest verification remains available via `make web-assets`.

---

## Continuous Integration

`.github/workflows/ci.yml` runs on pushes and pull requests to `main`:

1. `npm ci`
2. `npm run build`
3. `pytest tests`
4. `npx playwright install --with-deps`
5. `npm run test:playwright`

Keep CI green before merging.

---

## Useful References

- `scripts/codemods/normalize_templates.py` – enforces IU template conventions (extends, macros, design tokens).
- `scripts/run_e2e_server.sh` – resets DB + seeds demo accounts for UI tests.
- `/reports` – audit artifacts (architecture, route map, asset pipeline, UI consistency, etc.).
