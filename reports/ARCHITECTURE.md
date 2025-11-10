# Architecture Overview

## Stack Summary
- **Backend:** Flask application factory in `src/app.py` wires blueprints from `src/routes` and SQLAlchemy models under `src/models`.
- **Views:** Jinja2 templates in `src/templates` extend `base.html` and rely on shared component partials in `src/templates/components`.
- **Domain Layers:** Repositories (`src/repositories`) wrap database access; services (e.g., `src/services/resource_service.py`, `booking_service.py`, `admin_service.py`) encapsulate business logic.
- **Security:** Flask-Login + CSRF (per config); role-based access via `src/security/rbac.py` and helpers in `src/security/auth_utils.py`.
- **Messaging & Tasks:** Messaging blueprint (`src/routes/messages.py`) surfaces inbox/compose views backed by `message_repo.py` and `message_service.py`.
- **Frontend Build:** Vite (`vite.config.js`) compiles SCSS/JS entries to `src/static/dist`, with runtime resolution through `src/utils/vite.py`.

## Request Lifecycle
1. WSGI server imports `create_app` -> loads config (`src/config.py`).
2. Extensions (SQLAlchemy, LoginManager, CSRF, Migrate) initialize.
3. Blueprints register: `auth`, `resources`, `bookings`, `messages`, `reviews`, `admin`, `concierge`.
4. Incoming request hits blueprint route -> optional service/repository methods -> template render via Jinja.
5. Templates inherit `base.html`, ensuring enterprise UI shell and CSS/JS from Vite manifest.

## Data Layer
- SQLite (dev/testing) via SQLAlchemy ORM models (`User`, `Resource`, `Booking`, `Message`, `Review`).
- Repository layer encapsulates CRUD & search and is the only place emitting SQL.
- Seed scripts (e.g., `scripts/seed_auth_demo.py`) create demo data; migrations managed via Flask-Migrate.

## Frontend Modules
- `enterprise.scss` composes tokens, base, utilities, and page-specific SCSS under `src/static/scss`.
- `app.js` (sourced from `src/static/js/enterprise.js`) bootstraps UI managers (sidebar, drawer, modal, tabs, toasts, etc.).
- Additional entry modules (resource filters, booking drawer, image carousel, admin dashboard, charts) are built independently and lazy loaded where needed.

## Key Files & Directories
- `src/app.py`: application factory, Jinja globals, CLI commands.
- `src/routes/*`: HTTP entry points; each blueprint renders specific templates noted in `ROUTE_MAP.md`.
- `src/templates/base.html`: IU shell, nav, toast area, enterprise CSS/JS injection via `vite_asset`.
- `src/static/scss/pages/*.scss`: page-level layout overrides.
- `src/static/js/*.js`: behavior modules referenced from page templates or bundled into `app.js`.
