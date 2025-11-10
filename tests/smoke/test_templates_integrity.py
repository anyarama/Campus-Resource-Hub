from pathlib import Path
import pytest
from flask import current_app

TEMPLATE_DIR = Path("src/templates")


def should_skip(path: Path) -> bool:
    rel = path.relative_to(TEMPLATE_DIR).as_posix()
    if rel.startswith("components/") or rel.endswith(".before_migrate.html"):
        return True
    text = path.read_text()
    return "{% macro" in text


@pytest.mark.usefixtures("app")
def test_all_templates_load(app):
    missing = []
    with app.app_context():
        env = current_app.jinja_env
        for path in TEMPLATE_DIR.rglob("*.html"):
            if should_skip(path):
                continue
            rel = path.relative_to(TEMPLATE_DIR).as_posix()
            try:
                env.get_template(rel)
            except Exception as exc:  # pragma: no cover
                missing.append(f"{rel}: {exc}")
    assert not missing, "Template load failures:\n" + "\n".join(missing)
