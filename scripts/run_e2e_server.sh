#!/usr/bin/env bash
set -euo pipefail

export FLASK_APP=${FLASK_APP:-src.app:create_app}
export FLASK_ENV=${FLASK_ENV:-development}
export PYTHONPATH=${PYTHONPATH:-.}
export FLASK_RUN_PORT=${FLASK_RUN_PORT:-5001}

log() {
  echo "[e2e] $*"
}

log "Resetting SQLite database for smoke tests"
python -m flask init-db --drop

log "Seeding demo users/resources"
python scripts/seed_auth_demo.py

log "DB summary after seed"
python - <<'PY'
from src.app import create_app
app = create_app('development')
with app.app_context():
    from src.models.resource import Resource
    from src.models.user import User
    print(f"[e2e] users: {User.query.count()} | resources: {Resource.query.count()}")
PY

log "Starting Flask server on port ${FLASK_RUN_PORT}"
exec python -m flask run --host=127.0.0.1 --port="${FLASK_RUN_PORT}" --no-reload
