#!/usr/bin/env python3
"""
Seed script for creating demo authentication accounts.

Creates three demo users:
- admin@example.com (role: admin)
- staff@example.com (role: staff)
- student@example.com (role: student)

All accounts use password: Demo123!

Usage:
    python scripts/seed_auth_demo.py

AI Contribution: Cline generated seed script structure
Reviewed and configured by developer on 2025-11-05
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.app import create_app, db
from src.models.user import User
from src.repositories.user_repo import UserRepository


def seed_demo_users():
    """Create demo users for authentication testing."""
    app = create_app("development")

    with app.app_context():
        print("🌱 Seeding demo authentication accounts...")
        print("-" * 50)

        # Demo accounts configuration
        demo_accounts = [
            {
                "name": "Admin Demo User",
                "email": "admin@example.com",
                "password": "Demo123!",
                "role": "admin",
                "department": "Administration",
            },
            {
                "name": "Staff Demo User",
                "email": "staff@example.com",
                "password": "Demo123!",
                "role": "staff",
                "department": "Facilities",
            },
            {
                "name": "Student Demo User",
                "email": "student@example.com",
                "password": "Demo123!",
                "role": "student",
                "department": "Computer Science",
            },
        ]

        created_count = 0
        skipped_count = 0

        for account in demo_accounts:
            # Check if user already exists
            existing_user = UserRepository.get_by_email(account["email"])

            if existing_user:
                print(f"⏭️  Skipped: {account['email']} (already exists)")
                skipped_count += 1
                continue

            # Create new user
            user = User(
                name=account["name"],
                email=account["email"],
                role=account["role"],
                department=account["department"],
            )
            user.password = account["password"]  # Uses property setter for hashing

            try:
                UserRepository.create(user)
                print(f"✅ Created: {account['email']} ({account['role']})")
                created_count += 1
            except Exception as e:
                print(f"❌ Error creating {account['email']}: {e}")

        print("-" * 50)
        print(f"✨ Seeding complete!")
        print(f"   Created: {created_count}")
        print(f"   Skipped: {skipped_count}")
        print(f"   Total:   {len(demo_accounts)}")
        print()
        print("📝 Demo Accounts:")
        print("   admin@example.com   | Demo123! | admin")
        print("   staff@example.com   | Demo123! | staff")
        print("   student@example.com | Demo123! | student")
        print()
        print("🚀 You can now login with these accounts!")


def main():
    """Main entry point for seed script."""
    try:
        seed_demo_users()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n⚠️  Seeding interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
