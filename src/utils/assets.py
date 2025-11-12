from __future__ import annotations
import json
import logging
import os
import threading
from typing import Any, Dict

from flask import current_app, url_for

logger = logging.getLogger(__name__)

_manifest_cache: Dict[str, Any] | None = None
_manifest_mtime: float = 0.0
_lock = threading.Lock()


def _manifest_path() -> str:
    # Try .vite/manifest.json first (Vite 3+), fallback to root manifest.json
    vite_path = os.path.join(current_app.root_path, "static", "dist", ".vite", "manifest.json")
    if os.path.exists(vite_path):
        return vite_path
    return os.path.join(current_app.root_path, "static", "dist", "manifest.json")


def _load_manifest() -> dict:
    global _manifest_cache, _manifest_mtime
    path = _manifest_path()
    if not os.path.exists(path):
        return {}
    mtime = os.path.getmtime(path)
    with _lock:
        if _manifest_cache is None or mtime != _manifest_mtime:
            with open(path, "r") as f:
                _manifest_cache = json.load(f)
                _manifest_mtime = mtime
    return _manifest_cache or {}


def get_asset_url(entry: str) -> str:
    """
    Resolve a logical entry ('style', 'enterpriseJs') or a source path
    to the hashed file under /static/dist/assets/.

    Supports lookups by:
    1. Direct key match (e.g., 'src/static/js/enterprise.js')
    2. Name field match (e.g., 'enterpriseJs')
    3. Suffix match (e.g., 'main.scss')
    4. Special mappings for common names
    """
    man = _load_manifest()

    # Strategy 1: Direct key match
    if entry in man and "file" in man[entry]:
        return url_for("static", filename=f"dist/{man[entry]['file']}")

    # Strategy 2: Match by 'name' field in manifest entries
    for k, v in man.items():
        if isinstance(v, dict) and v.get("name") == entry and "file" in v:
            return url_for("static", filename=f"dist/{v['file']}")

    # Strategy 3: Special mappings for common entry names
    # Map logical names to manifest source file paths
    special_mappings = {
        "app.css": "style.css",
        "style": "src/static/scss/enterprise.scss",
        "style.css": "src/static/scss/enterprise.scss",
        "main": "src/static/scss/enterprise.scss",
        "enterprise": "src/static/scss/enterprise.scss",
        "enterpriseJs": "src/static/js/enterprise.js",
        "enterprise.js": "src/static/js/enterprise.js",
        "charts": "src/static/js/charts.js",
        "dashboardData": "src/static/js/adapters/dashboardData.js",
    }

    if entry in special_mappings:
        mapped_key = special_mappings[entry]
        if mapped_key in man and "file" in man[mapped_key]:
            return url_for("static", filename=f"dist/{man[mapped_key]['file']}")

    # Strategy 4: Suffix match on keys (e.g., 'main.scss', 'enterprise.js')
    for k, v in man.items():
        if isinstance(v, dict) and k.endswith(entry) and "file" in v:
            return url_for("static", filename=f"dist/{v['file']}")

    # Fallback for development (no manifest or entry not found)
    # Only return fallback if file actually exists on disk
    fallback_map = {
        "style": "dist/assets/style.css",
        "style.css": "dist/assets/style.css",
        "enterpriseJs": "dist/assets/enterprise.js",
        "enterprise.js": "dist/assets/enterprise.js",
    }

    if entry in fallback_map:
        fallback_path = fallback_map[entry]
        full_path = os.path.join(current_app.root_path, "static", fallback_path)

        if os.path.exists(full_path):
            logger.warning(
                f"get_asset_url('{entry}'): Using fallback '{fallback_path}' "
                f"(manifest lookup failed, but file exists)"
            )
            return url_for("static", filename=fallback_path)
        else:
            logger.warning(
                f"get_asset_url('{entry}'): Fallback '{fallback_path}' does not exist on disk. "
                f"Manifest may be stale or build incomplete."
            )

    # Last resort: check if generic path exists
    generic_path = f"dist/{entry}"
    full_generic_path = os.path.join(current_app.root_path, "static", generic_path)

    if os.path.exists(full_generic_path):
        logger.warning(
            f"get_asset_url('{entry}'): Using generic path '{generic_path}' "
            f"(no manifest entry found)"
        )
        return url_for("static", filename=generic_path)

    # Absolute last resort: log error and return a safe non-404 path
    # Return path to static root to avoid 404, but log the issue
    logger.error(
        f"get_asset_url('{entry}'): FAILED to resolve asset. "
        f"Manifest lookup failed and no file found. Returning safe fallback."
    )
    # Return empty path or a known placeholder to avoid 404
    return url_for("static", filename="dist/.placeholder")


# Backwards compatibility: expose asset_url alias expected by templates/docs
asset_url = get_asset_url
