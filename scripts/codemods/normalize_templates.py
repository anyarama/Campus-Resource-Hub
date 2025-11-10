#!/usr/bin/env python3
"""
Normalize Jinja templates to conform with the IU design system guidelines.

Operations performed (idempotent):
  - Ensure `{% extends "base.html" %}` is present on page templates.
  - Wrap content in `{% block main_content %}` if no block exists.
  - Replace plain hex colors with IU design tokens.
  - Ensure form/table/button elements carry the expected utility classes.
  - Add `data-col` attributes to `.layout-col` containers.
  - Normalize icon usage to Lucide/Bootstrap Icon conventions.
"""

from __future__ import annotations

import re
from pathlib import Path

TEMPLATE_ROOT = Path("src/templates").resolve()
SKIP_TOP_LEVEL = {"components", "layouts"}
EXTENDS_RE = re.compile(r'{%\s*extends\s*["\']base\.html["\']\s*%}')
HEX_RE = re.compile(r"#([0-9a-fA-F]{3,6})")
LAYOUT_RE = re.compile(r'(<(?P<tag>\w+)(?P<attrs>[^>]*class="[^"]*layout-col[^"]*"[^>]*))(>)', re.IGNORECASE)
ICON_RE = re.compile(r"<i\b[^>]*>", re.IGNORECASE)

HEX_TOKEN_MAP = {
    "fff": "var(--surface-0)",
    "ffffff": "var(--surface-0)",
    "000": "var(--ink-900)",
    "000000": "var(--ink-900)",
    "f5f5f5": "var(--surface-50)",
    "e5e5e5": "var(--surface-100)",
    "1d4ed8": "var(--brand-600)",
    "2563eb": "var(--brand-500)",
    "e11d48": "var(--alert-error)",
}
DEFAULT_TOKEN = "var(--brand-600)"


def should_skip(path: Path) -> bool:
    rel = path.relative_to(TEMPLATE_ROOT)
    if rel.name.startswith("_"):
        return True
    if rel.parts[0] in SKIP_TOP_LEVEL:
        return True
    if rel.name == "base.html":
        return True
    return False


def dedupe_extends(content: str) -> str:
    matches = list(EXTENDS_RE.finditer(content))
    if len(matches) <= 1:
        return content
    keep = matches[0]
    head = content[: keep.end()]
    tail = content[keep.end():]
    tail = EXTENDS_RE.sub("", tail)
    return head + tail


def ensure_extends(content: str) -> str:
    content = dedupe_extends(content)
    if EXTENDS_RE.search(content):
        return content
    return '{% extends "base.html" %}\n' + content.lstrip()


def split_after_extends(content: str) -> tuple[str, str]:
    match = EXTENDS_RE.search(content)
    if not match:
        return "", content
    end = match.end()
    head = content[:end].rstrip()
    tail = content[end:].lstrip("\n")
    return head, tail


def ensure_block(content: str) -> str:
    if "{% block main_content %}" in content or "{% block content %}" in content:
        return content
    head, tail = split_after_extends(content)
    block = "{% block main_content %}\n" + tail.strip() + "\n{% endblock %}\n"
    if head:
        return head + "\n\n" + block
    return block


def replace_hex(match: re.Match[str]) -> str:
    value = match.group(1).lower()
    token = HEX_TOKEN_MAP.get(value, DEFAULT_TOKEN)
    return token


def add_classes_to_tag(tag: str, classes: list[str]) -> str:
    class_match = re.search(r'class="([^"]*)"', tag)
    required = classes[:]
    if class_match:
        existing = class_match.group(1).split()
        changed = False
        for cls in required:
            if cls not in existing:
                existing.append(cls)
                changed = True
        if changed:
            new_attr = 'class="' + " ".join(existing) + '"'
            tag = tag[: class_match.start()] + new_attr + tag[class_match.end() :]
    else:
        insert = ' class="' + " ".join(required) + '"'
        if tag.endswith("/>"):
            tag = tag[:-2] + insert + " />"
        else:
            tag = tag[:-1] + insert + ">"
    return tag


def remove_class_from_tag(tag: str, cls: str) -> str:
    class_match = re.search(r'class="([^"]*)"', tag)
    if not class_match:
        return tag
    classes = class_match.group(1).split()
    if cls not in classes:
        return tag
    classes = [c for c in classes if c != cls]
    start, end = class_match.span()
    if classes:
        new_attr = 'class="' + " ".join(classes) + '"'
        return tag[:start] + new_attr + tag[end:]
    prefix = tag[:start].rstrip()
    suffix = tag[end:]
    if suffix and not suffix.startswith((">", "/>")) and prefix and not prefix.endswith(" "):
        prefix += " "
    return prefix + suffix


def ensure_tag_classes(content: str, tag: str, classes: list[str]) -> str:
    pattern = re.compile(rf"<{tag}\b[^>]*>", re.IGNORECASE)

    def repl(match: re.Match[str]) -> str:
        return add_classes_to_tag(match.group(0), classes)

    return pattern.sub(repl, content)


def ensure_layout_cols(content: str) -> str:
    def repl(match: re.Match[str]) -> str:
        full = match.group(0)
        attrs = match.group("attrs")
        if "data-col" in attrs:
            return full
        return full[:-1] + ' data-col="12">'

    return LAYOUT_RE.sub(repl, content)


def normalize_icon(match: re.Match[str]) -> str:
    tag = match.group(0)
    lower = tag.lower()
    if "data-lucide=" in lower:
        return add_classes_to_tag(tag, ["icon", "icon-sm"])
    if 'class="' in tag.lower() and "bi" in lower:
        return add_classes_to_tag(tag, ["icon"])

    icon_name = "sparkles"
    class_match = re.search(r'class="([^"]*)"', tag)
    if class_match:
        classes = class_match.group(1).split()
        cleaned = []
        for cls in classes:
            if cls.startswith("icon-") and len(cls.split("-", 1)) == 2 and cls.split("-", 1)[1]:
                icon_name = cls.split("-", 1)[1]
            else:
                cleaned.append(cls)
        cleaned.extend(["icon", "icon-sm"])
        new_attr = 'class="' + " ".join(dict.fromkeys(cleaned)) + '"'
        tag = tag[: class_match.start()] + new_attr + tag[class_match.end() :]
    else:
        tag = tag[:-1] + ' class="icon icon-sm">'

    if "data-lucide" not in tag.lower():
        tag = tag[:-1] + f' data-lucide="{icon_name}">'
    return tag


def enforce_icons(content: str) -> str:
    return ICON_RE.sub(normalize_icon, content)


def ensure_text_inputs(content: str) -> str:
    allowed = {"text", "email", "password", "number", "search", "tel", "url", "date", "time", "datetime-local"}
    input_pattern = re.compile(r"<input\b[^>]*>", re.IGNORECASE)

    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        type_match = re.search(r'type="([^"]*)"', tag, re.IGNORECASE)
        input_type = type_match.group(1).lower() if type_match else "text"
        if input_type in allowed:
            return add_classes_to_tag(tag, ["form-control"])
        return remove_class_from_tag(tag, "form-control")

    return input_pattern.sub(repl, content)


def transform(content: str) -> str:
    updated = ensure_extends(content)
    updated = ensure_block(updated)
    updated = HEX_RE.sub(replace_hex, updated)
    updated = ensure_tag_classes(updated, "button", ["btn", "btn--primary"])
    updated = ensure_tag_classes(updated, "table", ["table", "table--interactive"])
    updated = ensure_text_inputs(updated)
    updated = ensure_tag_classes(updated, "select", ["form-control"])
    updated = ensure_tag_classes(updated, "textarea", ["form-control"])
    updated = ensure_layout_cols(updated)
    updated = enforce_icons(updated)
    return updated


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text = transform(text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for template in TEMPLATE_ROOT.rglob("*.html"):
        if should_skip(template):
            continue
        if process_file(template):
            changed.append(template.relative_to(TEMPLATE_ROOT))

    if changed:
        print(f"Normalized {len(changed)} templates:")
        for rel in changed:
            print(f" - {rel}")
    else:
        print("Templates already normalized.")


if __name__ == "__main__":
    main()
