#!/usr/bin/env python3
"""UI lint checks for Campus Resource Hub.

Guards:
1. No residual Bootstrap grid/form classes or data attributes in templates.
2. No hard-coded hashed asset filenames in templates (must use asset_url/vite helpers).
3. No raw hex codes inside `src/static/scss/components` or `src/static/scss/pages`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "src" / "templates"
SCSS_SCAN_DIRS = [
    ("components", ROOT / "src" / "static" / "scss" / "components"),
    ("pages", ROOT / "src" / "static" / "scss" / "pages"),
]

CLASS_ATTR_RE = re.compile(r'class\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
JINJA_EXPR_RE = re.compile(r"\{\{.*?\}\}", re.DOTALL)
BANNED_CLASS_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("Bootstrap grid row", re.compile(r"^row$", re.IGNORECASE)),
    ("Bootstrap grid column", re.compile(r"^col(?:-(?:xs|sm|md|lg|xl|xxl))?-(?:\d+|auto)$", re.IGNORECASE)),
    ("Bootstrap offset utility", re.compile(r"^offset-(?:sm|md|lg|xl|xxl)?-\d+$", re.IGNORECASE)),
    ("Bootstrap gutter utility", re.compile(r"^g(?:x|y)?-\d+$", re.IGNORECASE)),
    ("Bootstrap order utility", re.compile(r"^order-(?:sm|md|lg|xl|xxl)?-(?:\d+|first|last)$", re.IGNORECASE)),
    ("Bootstrap container-fluid", re.compile(r"^container-fluid$", re.IGNORECASE)),
]
HASHED_ASSET_RE = re.compile(r"[\\w./-]*-(?P<hash>[A-Za-z0-9]{6,})\.(?:css|js)")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,6}")
DATA_BS_RE = re.compile(r"data-bs-", re.IGNORECASE)


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _template_files() -> Iterable[Path]:
    for ext in ("*.html", "*.jinja", "*.jinja2"):
        yield from TEMPLATE_DIR.rglob(ext)


def _check_bootstrap_classes() -> list[str]:
    issues: list[str] = []
    for path in _template_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in CLASS_ATTR_RE.finditer(text):
            value = match.group(1)
            cleaned = JINJA_EXPR_RE.sub(" ", value)
            line_no = _line_number(text, match.start())
            for cls in cleaned.split():
                cls = cls.strip()
                if not cls or "{{" in cls or "{%" in cls:
                    continue
                for label, pattern in BANNED_CLASS_RULES:
                    if pattern.match(cls):
                        issues.append(
                            f"[bootstrap-class] {path}:{line_no} → '{cls}' ({label})"
                        )
        for data_match in DATA_BS_RE.finditer(text):
            line_no = _line_number(text, data_match.start())
            issues.append(
                f"[bootstrap-attr] {path}:{line_no} → 'data-bs-*' attributes are not allowed"
            )
    return issues


def _check_hashed_assets() -> list[str]:
    issues: list[str] = []
    for path in _template_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in HASHED_ASSET_RE.finditer(text):
            hashed = match.group("hash")
            if not any(ch.isdigit() for ch in hashed):
                continue
            # require at least one alpha character to avoid flagging date suffixes like -202401
            if not any(ch.isalpha() for ch in hashed):
                continue
            line_no = _line_number(text, match.start())
            snippet = match.group(0)
            issues.append(
                f"[hashed-asset] {path}:{line_no} → '{snippet}' should be resolved via asset_url/vite helpers"
            )
    return issues


def _scss_hex_scan() -> list[str]:
    issues: list[str] = []
    for label, directory in SCSS_SCAN_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*.scss"):
            text = path.read_text(encoding="utf-8")
            for match in HEX_RE.finditer(text):
                line_no = _line_number(text, match.start())
                value = match.group(0)
                issues.append(
                    f"[raw-hex] {label}: {path}:{line_no} → '{value}' must use tokens.scss variables instead"
                )
    return issues


def main() -> int:
    issues = []
    issues.extend(_check_bootstrap_classes())
    issues.extend(_check_hashed_assets())
    issues.extend(_scss_hex_scan())

    if issues:
        print("❌ UI lint failed:")
        for entry in issues:
            print(f" - {entry}")
        return 1

    print("✅ UI lint checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
