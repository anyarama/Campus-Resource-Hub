#!/usr/bin/env python3
"""Hit smoke URLs and print status + CSS check."""
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
    print("| Role | URL | Status | Has enterprise.css |")
    print("|------|-----|--------|--------------------|")
    for role, url in entries:
        client = build_client(app, role, creds)
        resp = client.get(url, follow_redirects=True)
        html = resp.get_data(as_text=True)
        css_flag = 'yes' if ('/static/dist/' in html and '.css' in html) else 'no'
        print(f"| {role} | {url} | {resp.status_code} | {css_flag} |")

if __name__ == '__main__':
    main()
