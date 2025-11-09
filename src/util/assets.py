from __future__ import annotations
import json, os, threading
from flask import current_app, url_for

_manifest_cache = None
_manifest_mtime = 0
_lock = threading.Lock()

def _manifest_path() -> str:
    # Try .vite/manifest.json first (Vite 3+), fallback to root manifest.json
    vite_path = os.path.join(current_app.root_path, 'static', 'dist', '.vite', 'manifest.json')
    if os.path.exists(vite_path):
        return vite_path
    return os.path.join(current_app.root_path, 'static', 'dist', 'manifest.json')

def _load_manifest() -> dict:
    global _manifest_cache, _manifest_mtime
    path = _manifest_path()
    if not os.path.exists(path):
        return {}
    mtime = os.path.getmtime(path)
    with _lock:
        if _manifest_cache is None or mtime != _manifest_mtime:
            with open(path, 'r') as f:
                _manifest_cache = json.load(f)
                _manifest_mtime = mtime
    return _manifest_cache or {}

def asset_url(entry: str) -> str:
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
    if entry in man and 'file' in man[entry]:
        return url_for('static', filename=f"dist/{man[entry]['file']}")
    
    # Strategy 2: Match by 'name' field in manifest entries
    for k, v in man.items():
        if isinstance(v, dict) and v.get('name') == entry and 'file' in v:
            return url_for('static', filename=f"dist/{v['file']}")
    
    # Strategy 3: Special mappings for common entry names
    # Map logical names to manifest source file paths
    special_mappings = {
        'style': 'src/static/scss/main.scss',
        'main': 'src/static/scss/main.scss',
    }
    
    if entry in special_mappings:
        mapped_key = special_mappings[entry]
        if mapped_key in man and 'file' in man[mapped_key]:
            return url_for('static', filename=f"dist/{man[mapped_key]['file']}")
    
    # Strategy 4: Suffix match on keys (e.g., 'main.scss', 'enterprise.js')
    for k, v in man.items():
        if isinstance(v, dict) and k.endswith(entry) and 'file' in v:
            return url_for('static', filename=f"dist/{v['file']}")
    
    # Fallback for development (no manifest or entry not found)
    fallback_map = {
        'style': 'dist/assets/style.css',
        'enterpriseJs': 'dist/assets/enterprise.js',
    }
    
    if entry in fallback_map:
        return url_for('static', filename=fallback_map[entry])
    
    # Last resort: pass through as-is
    return url_for('static', filename=f'dist/{entry}')
