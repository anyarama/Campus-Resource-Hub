#!/usr/bin/env python3
"""
Button Normalizer - Replace Bootstrap-style btn-outline-* with custom variants
"""
import re
import sys
from pathlib import Path

# Replacement mapping
REPLACEMENTS = {
    # Unified outline style for primary actions
    'btn-outline-primary': 'btn-outline',
    
    # Ghost (text-only) for secondary/subtle actions
    'btn-outline-secondary': 'btn-ghost',
    'btn-outline-info': 'btn-ghost',
    
    # Semantic colors - use base class
    'btn-outline-danger': 'btn-danger',
    'btn-outline-success': 'btn-success',
    'btn-outline-warning': 'btn-secondary',  # Warning → subtle secondary
}

# BEM size normalization
SIZE_REPLACEMENTS = {
    r'\bbtn-sm\b': 'btn--sm',
    r'\bbtn-lg\b': 'btn--lg',
}

def normalize_buttons(content: str) -> tuple[str, list[str]]:
    """Normalize button classes. Returns (new_content, changes_list)"""
    changes = []
    original = content
    
    # Replace outline variants
    for old_class, new_class in REPLACEMENTS.items():
        pattern = rf'\b{re.escape(old_class)}\b'
        if re.search(pattern, content):
            count = len(re.findall(pattern, content))
            content = re.sub(pattern, new_class, content)
            changes.append(f"  - {old_class} → {new_class} ({count}x)")
    
    # Normalize sizes to BEM
    for old_pattern, new_class in SIZE_REPLACEMENTS.items():
        if re.search(old_pattern, content):
            count = len(re.findall(old_pattern, content))
            content = re.sub(old_pattern, new_class, content)
            changes.append(f"  - {old_pattern} → {new_class} ({count}x)")
    
    return content, changes

def process_file(filepath: Path, base_dir: Path) -> bool:
    """Process a single template file. Returns True if changed."""
    try:
        original_content = filepath.read_text(encoding='utf-8')
        new_content, changes = normalize_buttons(original_content)
        
        if new_content != original_content:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"\n✓ {filepath.relative_to(base_dir)}")
            for change in changes:
                print(change)
            return True
        return False
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}", file=sys.stderr)
        return False

def main():
    base_dir = Path.cwd()
    templates_dir = base_dir / 'src' / 'templates'
    
    if not templates_dir.exists():
        print(f"Error: {templates_dir} not found", file=sys.stderr)
        sys.exit(1)
    
    # Find all HTML files (exclude backups)
    html_files = [
        f for f in templates_dir.rglob('*.html')
        if not any(x in f.name for x in ['.before_migrate', '.bak', '.backup'])
    ]
    
    print(f"=== Button Normalizer ===")
    print(f"Processing {len(html_files)} templates...")
    
    changed_count = sum(1 for f in html_files if process_file(f, base_dir))
    
    print(f"\n=== Summary ===")
    print(f"Modified: {changed_count}/{len(html_files)} files")
    
    return 0 if changed_count > 0 else 1

if __name__ == '__main__':
    sys.exit(main())
