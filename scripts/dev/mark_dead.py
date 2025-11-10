#!/usr/bin/env python3
"""Phase B dead-code inventory utility."""
from __future__ import annotations
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)

SRC_DIR = ROOT / 'src'
TEMPLATE_DIR = SRC_DIR / 'templates'
STATIC_SCSS_DIR = SRC_DIR / 'static' / 'scss'
STATIC_JS_DIR = SRC_DIR / 'static' / 'js'
STATIC_DIR = SRC_DIR / 'static'

RENDER_RE = re.compile(r"render_template\(\s*[\'\"]([^\'\"]+)")
INCLUDE_RE = re.compile(r"\{\%\s*include\s+\"([^\"]+)\"\s*\%\}")
EXTENDS_RE = re.compile(r"\{\%\s*extends\s+\"([^\"]+)\"\s*\%\}")


def run_ruff_unused() -> list[str]:
    cmd = ['ruff', '--quiet', '--output-format', 'json', '--select', 'F401,F841', 'src', 'tests']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []
    try:
        entries = json.loads(result.stdout or '[]')
    except json.JSONDecodeError:
        return []
    files = sorted({entry['filename'] for entry in entries if 'filename' in entry})
    return files


def list_templates() -> set[str]:
    all_templates = set()
    for path in TEMPLATE_DIR.rglob('*.html'):
        rel = path.relative_to(TEMPLATE_DIR).as_posix()
        all_templates.add(rel)
    return all_templates


def referenced_templates() -> set[str]:
    referenced = set()
    # Python render_template calls
    for path in SRC_DIR.rglob('*.py'):
        text = path.read_text()
        for match in RENDER_RE.findall(text):
            referenced.add(match)
    # Template extends/includes
    for template in TEMPLATE_DIR.rglob('*.html'):
        text = template.read_text()
        for pattern in (INCLUDE_RE, EXTENDS_RE):
            for match in pattern.findall(text):
                referenced.add(match)
    return referenced


def scss_usage() -> set[str]:
    entry = (STATIC_SCSS_DIR / 'enterprise.scss')
    used = set()
    if not entry.exists():
        return used
    text = entry.read_text()
    for match in re.findall(r"@(?:use|forward)\s+['\"]([^'\"]+)['\"]", text):
        used.add(match.strip())
    return used


def js_usage() -> set[str]:
    entry = STATIC_JS_DIR / 'enterprise.js'
    used = set()
    if not entry.exists():
        return used
    text = entry.read_text()
    for match in re.findall(r"import\s+.*?from\s+['\"]([^'\"]+)['\"]", text):
        used.add(match.strip())
    return used


def find_unused_templates():
    all_templates = list_templates()
    refs = referenced_templates()
    unused = sorted(tmpl for tmpl in all_templates if tmpl not in refs and not tmpl.startswith('components/'))
    return unused


def find_unused_scss():
    used = scss_usage()
    unused = []
    for path in STATIC_SCSS_DIR.rglob('*.scss'):
        rel = path.relative_to(STATIC_SCSS_DIR).as_posix()
        if rel == 'enterprise.scss':
            continue
        key = rel[:-5] if rel.endswith('.scss') else rel
        if key not in used:
            unused.append(rel)
    return sorted(unused)


def find_unused_js():
    used = js_usage()
    unused = []
    for path in STATIC_JS_DIR.rglob('*.js'):
        rel = path.relative_to(STATIC_JS_DIR).as_posix()
        name = rel[:-3] if rel.endswith('.js') else rel
        if name not in used and path.name not in {'enterprise.js'}:
            unused.append(rel)
    return sorted(unused)


def find_orphan_images():
    images = []
    for ext in ('*.png', '*.jpg', '*.jpeg', '*.svg', '*.gif'):
        images.extend(STATIC_DIR.rglob(ext))
    orphan = []
    search_space = SRC_DIR
    corpus = '\n'.join(p.read_text(errors='ignore') for p in search_space.rglob('*') if p.is_file() and p.suffix in {'.py', '.html', '.js', '.scss', '.md'})
    for img in images:
        rel = img.relative_to(STATIC_DIR).as_posix()
        if rel not in corpus:
            orphan.append(rel)
    return sorted(orphan)


def write_reports(data: dict):
    timestamp = datetime.utcnow().isoformat(timespec='seconds') + 'Z'
    deprecated = REPORTS / 'DEPRECATED.md'
    dead = REPORTS / 'DEAD_CODE.md'

    deprecated.write_text('\n'.join([
        '# Deprecated Inventory',
        f'- Generated: {timestamp}',
        '',
        '## Potentially unused templates',
        *(f'- {item}' for item in data['unused_templates'] or ['(none)']),
        '',
        '## Potentially unused SCSS',
        *(f'- {item}' for item in data['unused_scss'] or ['(none)']),
        '',
        '## Potentially unused JS',
        *(f'- {item}' for item in data['unused_js'] or ['(none)']),
        '',
        '## Orphaned images',
        *(f'- {item}' for item in data['orphan_images'] or ['(none)']),
    ]) + '\n')

    dead.write_text('\n'.join([
        '# Dead Code Report',
        f'- Generated: {timestamp}',
        '',
        '## Ruff unused modules (F401/F841)',
        *(f'- {item}' for item in data['ruff_unused'] or ['(none)']),
        '',
        '## Files flagged for deletion',
        '(populate after apply_deletions.sh runs)'
    ]) + '\n')


def main():
    payload = {
        'ruff_unused': run_ruff_unused(),
        'unused_templates': find_unused_templates(),
        'unused_scss': find_unused_scss(),
        'unused_js': find_unused_js(),
        'orphan_images': find_orphan_images(),
    }
    write_reports(payload)
    print('Dead-code scan complete. See reports/DEPRECATED.md and reports/DEAD_CODE.md')


if __name__ == '__main__':
    main()
