#!/usr/bin/env python3
"""
Cleanup Utility for Orphaned Upload Files

Scans the uploads directory and removes files that are not referenced
in any database records. This helps maintain storage hygiene.

Safety features:
- Dry-run mode by default (use --execute to actually delete)
- Backup recommendations before deletion
- Detailed logging of actions

Usage:
    python scripts/cleanup_uploads.py          # Dry run (safe)
    python scripts/cleanup_uploads.py --execute  # Actually delete files

AI Contribution: Cline generated cleanup utility structure
Reviewed and configured by developer on 2025-11-05
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.app import create_app
from src.repositories.resource_repo import ResourceRepository


UPLOAD_DIR = "src/static/uploads/resources"


def get_referenced_files():
    """
    Get all files currently referenced in database.

    Returns:
        set: Set of filenames that are referenced in resources
    """
    app = create_app("development")
    referenced_files = set()

    with app.app_context():
        # Get all resources
        all_resources = ResourceRepository.get_all()

        for resource in all_resources:
            if resource.images:
                try:
                    images = json.loads(resource.images)
                    for image_path in images:
                        # Extract just the filename from path like "uploads/resources/abc123.jpg"
                        filename = os.path.basename(image_path)
                        referenced_files.add(filename)
                except (json.JSONDecodeError, TypeError):
                    print(f"⚠️  Warning: Could not parse images for resource {resource.resource_id}")
                    continue

    return referenced_files


def get_filesystem_files():
    """
    Get all files in the uploads directory.

    Returns:
        set: Set of all filenames in uploads directory
    """
    upload_path = Path(UPLOAD_DIR)

    if not upload_path.exists():
        print(f"⚠️  Upload directory does not exist: {UPLOAD_DIR}")
        return set()

    filesystem_files = set()
    for file in upload_path.iterdir():
        if file.is_file() and not file.name.startswith("."):
            filesystem_files.add(file.name)

    return filesystem_files


def get_file_info(filename):
    """
    Get file information (size, modified date).

    Args:
        filename: Name of the file

    Returns:
        dict: File information
    """
    filepath = Path(UPLOAD_DIR) / filename
    stats = filepath.stat()

    return {
        "size": stats.st_size,
        "size_mb": stats.st_size / (1024 * 1024),
        "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    }


def format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def cleanup_uploads(dry_run=True):
    """
    Clean up orphaned upload files.

    Args:
        dry_run: If True, only report what would be deleted
    """
    print("🧹 Campus Resource Hub - Upload Cleanup Utility")
    print("=" * 60)
    print()

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be deleted")
        print("   Use --execute flag to actually delete files")
    else:
        print("⚠️  EXECUTE MODE - Files will be permanently deleted!")
        response = input("   Continue? (type 'YES' to confirm): ")
        if response != "YES":
            print("❌ Cleanup cancelled")
            return

    print()
    print("-" * 60)

    # Get file lists
    print("📊 Analyzing files...")
    referenced_files = get_referenced_files()
    filesystem_files = get_filesystem_files()

    print(f"   Files in database: {len(referenced_files)}")
    print(f"   Files on disk:     {len(filesystem_files)}")
    print()

    # Find orphaned files
    orphaned_files = filesystem_files - referenced_files

    if not orphaned_files:
        print("✅ No orphaned files found! Storage is clean.")
        print()
        return

    print(f"🗑️  Found {len(orphaned_files)} orphaned file(s):")
    print()

    total_size = 0
    file_list = []

    for filename in sorted(orphaned_files):
        info = get_file_info(filename)
        total_size += info["size"]
        file_list.append((filename, info))
        print(f"   • {filename}")
        print(f"     Size: {format_size(info['size'])}, Modified: {info['modified']}")

    print()
    print(f"📦 Total size of orphaned files: {format_size(total_size)}")
    print()

    if dry_run:
        print("💡 To actually delete these files, run:")
        print("   python scripts/cleanup_uploads.py --execute")
        print()
        print("⚠️  RECOMMENDED: Backup uploads directory before deleting:")
        print(f"   cp -r {UPLOAD_DIR} {UPLOAD_DIR}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        print()
    else:
        # Actually delete files
        print("🗑️  Deleting orphaned files...")
        deleted_count = 0
        failed_count = 0

        for filename, info in file_list:
            filepath = Path(UPLOAD_DIR) / filename
            try:
                filepath.unlink()
                print(f"   ✅ Deleted: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ Failed to delete {filename}: {e}")
                failed_count += 1

        print()
        print(f"✨ Cleanup complete!")
        print(f"   Deleted: {deleted_count}")
        print(f"   Failed:  {failed_count}")
        print(f"   Space freed: {format_size(total_size)}")
        print()


def check_database_integrity():
    """Check for database records with missing files."""
    print("\n🔍 Checking database integrity...")
    print("-" * 60)

    app = create_app("development")
    with app.app_context():
        all_resources = ResourceRepository.get_all()
        problems = []

        for resource in all_resources:
            if resource.images:
                try:
                    images = json.loads(resource.images)
                    for image_path in images:
                        filepath = Path("src/static") / image_path
                        if not filepath.exists():
                            problems.append({
                                "resource_id": resource.resource_id,
                                "title": resource.title,
                                "missing_file": image_path
                            })
                except (json.JSONDecodeError, TypeError):
                    continue

        if problems:
            print(f"⚠️  Found {len(problems)} database record(s) with missing files:")
            print()
            for problem in problems:
                print(f"   Resource #{problem['resource_id']}: {problem['title']}")
                print(f"   Missing: {problem['missing_file']}")
                print()
            print("💡 Consider updating/removing these resources via the admin panel")
        else:
            print("✅ All database records reference existing files")

    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Clean up orphaned upload files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/cleanup_uploads.py              # Dry run
  python scripts/cleanup_uploads.py --execute    # Actually delete
  python scripts/cleanup_uploads.py --check      # Check database integrity
        """
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete files (default is dry run)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check database for missing file references"
    )

    args = parser.parse_args()

    try:
        if args.check:
            check_database_integrity()
        else:
            cleanup_uploads(dry_run=not args.execute)

        sys.exit(0)

    except KeyboardInterrupt:
        print("\n⚠️  Cleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Cleanup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
