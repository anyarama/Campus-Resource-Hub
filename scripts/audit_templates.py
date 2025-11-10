#!/usr/bin/env python3
"""Scan templates for extends/includes/macros."""
from pathlib import Path
import sys
from pathlib import Path as _Path_for_sys
ROOT = _Path_for_sys(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import re

TEMPLATE_DIR = Path('src/templates')

extends_re = re.compile(r"\{\%\s*extends\s+\"(?P<parent>[^\"]+)\"\s*\%\}")
include_re = re.compile(r"\{\%\s*include\s+\"(?P<child>[^\"]+)\"\s*\%\}")
from_re = re.compile(r"\{\%\s*from\s+\"(?P<macro>[^\"]+)\"\s+import\s+(?P<names>[^\%]+)\%\}")

def analyze(path: Path):
    text = path.read_text()
    extends = extends_re.findall(text)
    includes = include_re.findall(text)
    macros = [match.group('macro') for match in from_re.finditer(text)]
    return extends, includes, macros

def main():
    files = sorted(TEMPLATE_DIR.rglob('*.html'))
    print(f"Inspecting {len(files)} templates under {TEMPLATE_DIR}...\n")
    for path in files:
        extends, includes, macros = analyze(path)
        print(f"## {path.relative_to(TEMPLATE_DIR)}")
        print(f"- extends: {extends or ['<base ??>']}")
        print(f"- includes: {includes or ['<none>']}")
        print(f"- macros: {macros or ['<none>']}")
        print()

if __name__ == '__main__':
    main()
