#!/usr/bin/env python3
"""
Grid Normalizer - Jinja-aware template migrator
Normalizes grid classes to layout-col with data-col attributes
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple

class GridNormalizer:
    def __init__(self):
        self.changes = []
        
    def normalize_file(self, filepath: Path) -> Tuple[str, List[str]]:
        """Normalize a single template file"""
        content = filepath.read_text()
        original = content
        file_changes = []
        
        # 1. Replace layout-col2 → layout-col + data-col="2"
        pattern = r'class="([^"]*)\blayout-col2\b([^"]*)"'
        def replace_col2(m):
            classes = m.group(1) + m.group(2)
            if 'layout-col' not in classes or 'layout-col2' in classes:
                classes = classes.replace('layout-col2', 'layout-col')
            if 'data-col' not in m.group(0):
                # Add data-col="2" after the tag
                return f'class="{classes}" data-col="2"'
            return f'class="{classes}"'
        
        new_content = re.sub(pattern, replace_col2, content)
        if new_content != content:
            file_changes.append("  - Replaced layout-col2 → layout-col + data-col=\"2\"")
            content = new_content
        
        # 2. Replace grid-col-{bp}-{n} → layout-col + data-col-{bp}="{n}"
        pattern = r'class="([^"]*)grid-col-((?:sm|md|lg|xl)-)?(\d+)([^"]*)"'
        def replace_grid_col(m):
            prefix_classes = m.group(1)
            bp = m.group(2).rstrip('-') if m.group(2) else ''
            col_num = m.group(3)
            suffix_classes = m.group(4)
            
            # Remove grid-col-* and ensure layout-col
            all_classes = prefix_classes + suffix_classes
            all_classes = re.sub(r'\bgrid-col-[a-z]+-\d+\b', '', all_classes)
            all_classes = re.sub(r'\s+', ' ', all_classes).strip()
            
            if 'layout-col' not in all_classes:
                all_classes = 'layout-col ' + all_classes
            
            # Build data-col attribute
            data_attr = f'data-col-{bp}="{col_num}"' if bp else f'data-col="{col_num}"'
            
            return f'class="{all_classes.strip()}" {data_attr}'
        
        new_content = re.sub(pattern, replace_grid_col, content)
        if new_content != content:
            file_changes.append("  - Replaced grid-col-{bp}-{n} patterns → layout-col + data-col-{bp}")
            content = new_content
        
        # 3. Replace grid-layout-col → layout-col
        pattern = r'\bgrid-layout-col\b'
        new_content = re.sub(pattern, 'layout-col', content)
        if new_content != content:
            file_changes.append("  - Replaced grid-layout-col → layout-col")
            content = new_content
        
        # 4. Ensure all layout-col have data-col* attribute
        # Find all divs with layout-col class
        pattern = r'<div([^>]*class="[^"]*layout-col[^"]*"[^>]*)>'
        matches = list(re.finditer(pattern, content))
        
        for match in reversed(matches):  # Process in reverse to maintain positions
            tag_content = match.group(1)
            full_tag = match.group(0)
            
            # Check if already has data-col
            if 'data-col' not in tag_content:
                # Add data-col="12" before closing >
                new_tag = full_tag[:-1] + ' data-col="12">'
                content = content[:match.start()] + new_tag + content[match.end():]
                if "  - Added default data-col=\"12\" to layout-col elements" not in file_changes:
                    file_changes.append("  - Added default data-col=\"12\" to layout-col elements")
        
        # 5. Remove duplicate layout-col classes
        pattern = r'class="([^"]*\blayout-col\b[^"]*)"'
        def dedupe_layout_col(m):
            classes = m.group(1).split()
            seen = set()
            unique = []
            for cls in classes:
                if cls not in seen:
                    seen.add(cls)
                    unique.append(cls)
            return f'class="{" ".join(unique)}"'
        
        content = re.sub(pattern, dedupe_layout_col, content)
        
        return content, file_changes
    
    def process_templates(self, template_dir: Path):
        """Process all active template files"""
        exclude_patterns = ['.bak', '.backup', '.before_migrate', '.bootstrap_backup']
        
        for template_file in template_dir.rglob('*.html'):
            # Skip backup files
            if any(pattern in str(template_file) for pattern in exclude_patterns):
                continue
            
            try:
                new_content, file_changes = self.normalize_file(template_file)
                
                if file_changes:
                    # Write updated content
                    template_file.write_text(new_content)
                    rel_path = template_file.relative_to(template_dir.parent.parent)
                    print(f"\n✓ {rel_path}")
                    for change in file_changes:
                        print(change)
                    self.changes.append((str(rel_path), file_changes))
            except Exception as e:
                print(f"✗ Error processing {template_file}: {e}", file=sys.stderr)
        
        return len(self.changes)

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    template_dir = project_root / 'src' / 'templates'
    
    if not template_dir.exists():
        print(f"Template directory not found: {template_dir}", file=sys.stderr)
        return 1
    
    normalizer = GridNormalizer()
    print("=" * 60)
    print("GRID NORMALIZATION - Jinja-aware template migrator")
    print("=" * 60)
    
    count = normalizer.process_templates(template_dir)
    
    print("\n" + "=" * 60)
    print(f"COMPLETE: Modified {count} files")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
