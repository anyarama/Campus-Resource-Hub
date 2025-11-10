"""
Vite Asset Pipeline Integration
Provides manifest-aware asset URL resolution for Vite-built assets.
"""
from __future__ import annotations
import json
import os
from flask import current_app, url_for


def vite_asset(name: str) -> str:
    """
    Resolve a Vite build entry name to its hashed asset URL.

    Reads the Vite manifest.json and returns the Flask url_for()
    path to the built, hashed asset file.

    Args:
        name: Entry name from vite.config.js (e.g., 'enterprise.css', 'app.js')
              OR the manifest key (e.g., 'src/static/scss/main.scss')

    Returns:
        URL path to the hashed asset file (e.g., '/static/dist/assets/style-abc123.css')

    Examples:
        >>> vite_asset('enterprise.css')  # Tries to find main.scss
        '/static/dist/assets/style-BajwvXt8.css'

        >>> vite_asset('app.js')  # Looks for enterprise.js
        '/static/dist/assets/enterpriseJs-CNnJ7BZk.js'

    Raises:
        FileNotFoundError: If manifest.json doesn't exist
        KeyError: If the entry name is not found in the manifest
    """
    manifest_path = os.path.join(current_app.root_path, "static", "dist", ".vite", "manifest.json")

    if not os.path.exists(manifest_path):
        # Development fallback - try to construct path without manifest
        if current_app.debug:
            current_app.logger.warning(
                f"Vite manifest not found at {manifest_path}. "
                f"Run 'npm run build' to generate it."
            )
            # Return a safe fallback path
            return url_for("static", filename=f"dist/{name}")
        raise FileNotFoundError(f"Vite manifest not found: {manifest_path}")

    # Load manifest
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    # Strategy 1: Direct key lookup (e.g., 'src/static/scss/main.scss')
    if name in manifest:
        return url_for("static", filename=f"dist/{manifest[name]['file']}")

    # Strategy 2: Match by 'name' field in manifest entries
    for key, entry in manifest.items():
        if isinstance(entry, dict) and entry.get("name") == name:
            return url_for("static", filename=f"dist/{entry['file']}")

    # Strategy 3: Smart mapping for common entry names
    # Map friendly names to manifest keys
    name_mappings = {
        "enterprise.css": "src/static/scss/enterprise.scss",
        "style": "src/static/scss/enterprise.scss",
        "main.css": "src/static/scss/enterprise.scss",
        "app.js": "src/static/js/enterprise.js",
        "enterprise.js": "src/static/js/enterprise.js",
    }

    if name in name_mappings:
        manifest_key = name_mappings[name]
        if manifest_key in manifest:
            return url_for("static", filename=f"dist/{manifest[manifest_key]['file']}")

    # Strategy 4: Partial key match (ends with)
    for key, entry in manifest.items():
        if isinstance(entry, dict) and key.endswith(name):
            return url_for("static", filename=f"dist/{entry['file']}")

    # Not found - raise descriptive error
    available_keys = ", ".join(manifest.keys())
    raise KeyError(
        f"Asset '{name}' not found in Vite manifest. " f"Available keys: {available_keys}"
    )
