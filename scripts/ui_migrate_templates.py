#!/usr/bin/env python3
"""
Jinja-aware Bootstrap → Enterprise UI class migrator
Safely transforms Bootstrap classes while preserving Jinja templates
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass

try:
    from bs4 import BeautifulSoup
    from termcolor import colored
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install beautifulsoup4 html5lib termcolor")
    sys.exit(1)


@dataclass
class MigrationResult:
    """Result of migrating a single template"""
    path: Path
    success: bool
    classes_removed: Set[str]
    classes_added: Set[str]
    error: str = ""


# Bootstrap → Enterprise class mapping
BOOTSTRAP_MAP = {
    # Buttons (keep btn base, transform modifiers)
    "btn-primary": "btn-primary",
    "btn-secondary": "btn-secondary", 
    "btn-success": "btn-success",
    "btn-danger": "btn-danger",
    "btn-warning": "btn-warning",
    "btn-outline-primary": "btn-ghost",
    "btn-outline-secondary": "btn-ghost",
    "btn-sm": "btn--sm",
    "btn-lg": "btn--lg",
    
    # Grid → layout primitives
    "row": "layout-grid",
    
    # Display/Flex
    "d-flex": "flex",
    "d-block": "display-block",
    "d-inline-block": "display-inline-block",
    "align-items-center": "items-center",
    "align-items-start": "items-start",
    "justify-content-between": "justify-between",
    "justify-content-center": "justify-center",
    "flex-grow-1": "flex-1",
    
    # Text utilities
    "text-center": "text-center",
    "text-end": "text-end",
    "text-start": "text-start",
    "text-muted": "text-dim",
    "text-danger": "text-danger",
    "text-success": "text-success",
    "text-warning": "text-warning",
    "text-white": "text-inverse",
    
    # Sizing
    "w-100": "width-full",
    "h-100": "height-full",
    
    # Borders/Rounded
    "rounded-circle": "rounded-full",
    "rounded-pill": "rounded-full",
    "border-0": "",  # Remove
    
    # Shadows
    "shadow-sm": "",  # Handled by component styles
    
    # Backgrounds
    "bg-light": "bg-neutral",
    "bg-white": "bg-white",
    "bg-primary": "bg-primary",
    "bg-secondary": "bg-secondary",
    
    # List groups → item lists
    "list-group": "item-list",
    "list-group-item": "item-list-item",
    "list-group-flush": "item-list-flush",
    "list-group-item-action": "item-list-item-action",
}


def split_jinja_segments(html: str) -> List[Tuple[str, bool]]:
    """
    Split HTML into segments, marking which are Jinja and which are HTML.
    Returns: [(segment_text, is_jinja), ...]
    """
    segments = []
    jinja_pattern = r'(\{[{%#].*?[}%#]\})'
    parts = re.split(jinja_pattern, html, flags=re.DOTALL)
    
    for part in parts:
        if not part:
            continue
        is_jinja = part.startswith(('{%', '{{', '{#'))
        segments.append((part, is_jinja))
    
    return segments


def transform_class_list(classes: List[str]) -> Tuple[List[str], Dict[str, str], Set[str], Set[str]]:
    """
    Transform a list of Bootstrap classes to enterprise classes.
    Returns: (new_classes, data_attrs, removed, added)
    """
    new_classes = []
    data_attrs = {}
    removed = set()
    added = set()
    
    for cls in classes:
        # Handle col-* grid classes
        col_match = re.match(r'^col(-(?:sm|md|lg|xl))?-(\d+)$', cls)
        if col_match:
            breakpoint = col_match.group(1) or ""
            span = col_match.group(2)
            if "layout-col" not in new_classes:
                new_classes.append("layout-col")
                added.add("layout-col")
            
            data_key = f"data-col{breakpoint}" if breakpoint else "data-col"
            data_attrs[data_key] = span
            removed.add(cls)
            continue
        
        # Handle spacing utilities (mb-3, px-2, etc.)
        spacing_match = re.match(r'^([mp])([trblxy])?-(\d+)$', cls)
        if spacing_match:
            prefix = "space" if spacing_match.group(1) == 'm' else "pad"
            direction = spacing_match.group(2) or ""
            size = spacing_match.group(3)
            
            if direction:
                new_cls = f"{prefix}-{direction}-{size}"
            else:
                new_cls = f"{prefix}-{size}"
            
            new_classes.append(new_cls)
            removed.add(cls)
            added.add(new_cls)
            continue
        
        # Handle badge bg-* classes
        badge_match = re.match(r'^bg-(success|danger|warning|info|primary|secondary)$', cls)
        if badge_match and 'badge' in classes:
            variant = badge_match.group(1)
            new_cls = f"badge-{variant}"
            new_classes.append(new_cls)
            removed.add(cls)
            added.add(new_cls)
            continue
        
        # Direct mapping
        if cls in BOOTSTRAP_MAP:
            replacement = BOOTSTRAP_MAP[cls]
            if replacement and replacement not in new_classes:
                new_classes.append(replacement)
                added.add(replacement)
            removed.add(cls)
        else:
            # Keep unchanged
            new_classes.append(cls)
    
    return new_classes, data_attrs, removed, added


def migrate_html_segment(html: str) -> Tuple[str, Set[str], Set[str]]:
    """
    Migrate Bootstrap classes in an HTML segment (non-Jinja).
    Returns: (transformed_html, removed_classes, added_classes)
    """
    soup = BeautifulSoup(html, 'html5lib')
    all_removed = set()
    all_added = set()
    
    # Find all elements with class attribute
    for element in soup.find_all(class_=True):
        original_classes = element.get('class', [])
        if isinstance(original_classes, str):
            original_classes = original_classes.split()
        
        new_classes, data_attrs, removed, added = transform_class_list(original_classes)
        
        # Update classes
        if new_classes != original_classes:
            element['class'] = new_classes
        
        # Add data attributes for grid
        for key, value in data_attrs.items():
            element[key] = value
        
        all_removed.update(removed)
        all_added.update(added)
    
    # Extract body content (html5lib adds full document)
    body = soup.find('body')
    if body:
        result = ''.join(str(child) for child in body.children)
    else:
        result = str(soup)
    
    return result, all_removed, all_added


def migrate_template(filepath: Path, backup: bool = True) -> MigrationResult:
    """
    Migrate a single template file.
    """
    try:
        content = filepath.read_text(encoding='utf-8')
        
        # Backup original
        if backup:
            backup_path = filepath.with_suffix('.before_migrate.html')
            backup_path.write_text(content, encoding='utf-8')
        
        # Split into Jinja and HTML segments
        segments = split_jinja_segments(content)
        
        # Transform each HTML segment
        new_segments = []
        all_removed = set()
        all_added = set()
        
        for segment, is_jinja in segments:
            if is_jinja:
                # Preserve Jinja exactly
                new_segments.append(segment)
            else:
                # Transform HTML
                transformed, removed, added = migrate_html_segment(segment)
                new_segments.append(transformed)
                all_removed.update(removed)
                all_added.update(added)
        
        # Reassemble
        new_content = ''.join(new_segments)
        
        # Write transformed content
        filepath.write_text(new_content, encoding='utf-8')
        
        return MigrationResult(
            path=filepath,
            success=True,
            classes_removed=all_removed,
            classes_added=all_added
        )
        
    except Exception as e:
        return MigrationResult(
            path=filepath,
            success=False,
            classes_removed=set(),
            classes_added=set(),
            error=str(e)
        )


def main():
    parser = argparse.ArgumentParser(description='Migrate Bootstrap classes to enterprise UI')
    parser.add_argument('files', nargs='+', help='Template files to migrate')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup creation')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without writing')
    
    args = parser.parse_args()
    
    print(colored("🔧 Bootstrap → Enterprise UI Migrator", 'cyan', attrs=['bold']))
    print()
    
    results = []
    for filepath in args.files:
        path = Path(filepath)
        if not path.exists():
            print(colored(f"⚠️  Skipping {filepath} (not found)", 'yellow'))
            continue
        
        print(f"📝 Processing {path.name}...")
        
        if args.dry_run:
            content = path.read_text()
            segments = split_jinja_segments(content)
            removed, added = set(), set()
            for segment, is_jinja in segments:
                if not is_jinja:
                    _, r, a = migrate_html_segment(segment)
                    removed.update(r)
                    added.update(a)
            
            result = MigrationResult(path, True, removed, added)
        else:
            result = migrate_template(path, backup=not args.no_backup)
        
        results.append(result)
        
        if result.success:
            if result.classes_removed or result.classes_added:
                print(colored(f"  ✅ {len(result.classes_removed)} removed, {len(result.classes_added)} added", 'green'))
                if result.classes_removed:
                    print(f"     - Removed: {', '.join(sorted(result.classes_removed))}")
                if result.classes_added:
                    print(f"     + Added: {', '.join(sorted(result.classes_added))}")
            else:
                print(colored(f"  ℹ️  No changes needed", 'blue'))
        else:
            print(colored(f"  ❌ Error: {result.error}", 'red'))
    
    print()
    success_count = sum(1 for r in results if r.success)
    print(colored(f"✨ Completed: {success_count}/{len(results)} files migrated", 'green', attrs=['bold']))
    
    if any(not r.success for r in results):
        sys.exit(1)


if __name__ == '__main__':
    main()
