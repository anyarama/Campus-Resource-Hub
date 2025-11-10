#!/usr/bin/env python3
"""Verify that smoke URLs render enterprise CSS."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.app import create_app
from scripts.dev.smoke_utils import load_smoke_entries, seed_demo_data, build_client


def main():
    entries = load_smoke_entries()
    app = create_app('development')
    app.config['TESTING'] = True
    with app.app_context():
        creds = seed_demo_data()
    failures = []
    for role, url in entries:
        client = build_client(app, role, creds)
        resp = client.get(url, follow_redirects=True)
        html = resp.get_data(as_text=True)
        if resp.status_code != 200:
            failures.append((url, role, f"HTTP {resp.status_code}"))
        elif '/static/dist/' not in html or '.css' not in html:
            failures.append((url, role, 'css-missing'))
    if failures:
        print('❌ Style audit failures:')
        for url, role, reason in failures:
            print(f" - [{role}] {url}: {reason}")
    else:
        print(f"✅ All {len(entries)} smoke URLs include enterprise.css")

if __name__ == '__main__':
    main()
