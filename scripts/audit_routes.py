#!/usr/bin/env python3
import sys
from pathlib import Path as _Path_for_sys
ROOT = _Path_for_sys(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

"""List Flask routes with templates/handlers."""
from src.app import create_app

IGNORED = {'static'}

def main():
    app = create_app('development')
    app.config['TESTING'] = True
    rows = []
    with app.app_context():
        for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
            if rule.endpoint in IGNORED:
                continue
            methods = ','.join(sorted(m for m in rule.methods if m not in {'HEAD', 'OPTIONS'}))
            rows.append((rule.rule, rule.endpoint, methods))
    print(f"Found {len(rows)} application routes:\n")
    print("| Route | Endpoint | Methods |")
    print("|-------|----------|---------|")
    for route, endpoint, methods in rows:
        print(f"| {route} | {endpoint} | {methods} |")

if __name__ == '__main__':
    main()
