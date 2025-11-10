#!/usr/bin/env python3
"""
Seed script for creating demo authentication accounts and resources.

Creates three demo users:
- admin@example.com (role: admin)
- staff@example.com (role: staff)
- student@example.com (role: student)

Creates 8 demo resources across various categories.

All accounts use password: Demo123!

Usage:
    python scripts/seed_auth_demo.py

AI Contribution: Cline generated seed script structure
Reviewed and extended by developer on 2025-11-05
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.app import create_app, db
from src.models.user import User
from src.repositories.user_repo import UserRepository
from src.repositories.resource_repo import ResourceRepository


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

            # Create new user using repository method
            try:
                user = UserRepository.create(
                    name=account["name"],
                    email=account["email"],
                    password=account["password"],
                    role=account["role"],
                    department=account["department"],
                )
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


def seed_demo_resources():
    """Create demo resources for testing and demonstration."""
    app = create_app("development")

    with app.app_context():
        print("\n🏢 Seeding demo resources...")
        print("-" * 50)

        # Get staff user as owner
        staff_user = UserRepository.get_by_email("staff@example.com")
        if not staff_user:
            print("⚠️  Staff user not found. Please run user seeding first.")
            return

        # Demo resources configuration
        demo_resources = [
            {
                "title": "Main Library Study Room A",
                "description": "Quiet study room perfect for group work. Seats 6 people comfortably. Equipped with whiteboard, markers, and power outlets at every seat.",
                "category": "study_room",
                "location": "Main Library, 2nd Floor, Room 201",
                "capacity": 6,
                "status": "published",
            },
            {
                "title": "Innovation Lab - 3D Printing Station",
                "description": "Access to professional-grade 3D printers including Prusa i3 MK3S+ and Ultimaker S5. Perfect for prototyping and course projects. Safety training required.",
                "category": "lab",
                "location": "Engineering Building, Room 105",
                "capacity": 4,
                "status": "published",
            },
            {
                "title": "MacBook Pro 16\" (M2 Max, 2023)",
                "description": "Latest MacBook Pro available for 7-day checkout. Includes charger and carrying case. Pre-loaded with Adobe Creative Suite, Final Cut Pro, and Xcode.",
                "category": "equipment",
                "location": "IT Services Desk, Student Center",
                "capacity": 1,
                "status": "published",
            },
            {
                "title": "Conference Room B - Skylight Hall",
                "description": "Premium conference room for large events and presentations. Capacity 50 people theater-style. Includes projector, wireless presentation system, and professional audio setup.",
                "category": "space",
                "location": "Student Center, 3rd Floor",
                "capacity": 50,
                "status": "published",
            },
            {
                "title": "Photography Equipment Bundle",
                "description": "Professional photography kit including Canon EOS R6 mirrorless camera, 24-70mm f/2.8 lens, tripod, and lighting equipment. Perfect for student journalism and projects.",
                "category": "equipment",
                "location": "Media Lab, Basement Level",
                "capacity": 1,
                "status": "published",
            },
            {
                "title": "Seminar Room 305",
                "description": "Mid-sized classroom ideal for workshops and seminars. Flexible seating for up to 25 people. Smartboard, projector, and video conferencing capabilities.",
                "category": "space",
                "location": "Academic Building, 3rd Floor",
                "capacity": 25,
                "status": "published",
            },
            {
                "title": "Podcast Recording Studio",
                "description": "Professional podcast recording setup with Shure SM7B microphones, mixing board, and soundproofing. Free training session included with first booking.",
                "category": "lab",
                "location": "Media Center, Room B12",
                "capacity": 4,
                "status": "published",
            },
            {
                "title": "VR Development Lab",
                "description": "Virtual reality development space with Meta Quest 3, HTC Vive Pro 2, and high-performance gaming PCs. Ideal for XR development courses and research.",
                "category": "lab",
                "location": "Computer Science Building, Room 220",
                "capacity": 8,
                "status": "published",
            },
        ]

        created_count = 0
        skipped_count = 0

        for resource_data in demo_resources:
            # Check if resource already exists (by title)
            existing_resources = ResourceRepository.search(query_str=resource_data["title"])
            if existing_resources:
                print(f"⏭️  Skipped: {resource_data['title']} (already exists)")
                skipped_count += 1
                continue

            try:
                ResourceRepository.create(
                    owner_id=staff_user.user_id,
                    title=resource_data["title"],
                    category=resource_data["category"],
                    description=resource_data["description"],
                    location=resource_data["location"],
                    capacity=resource_data["capacity"],
                    status=resource_data["status"],
                    availability_rules={
                        "requires_approval": False,
                        "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                        "hours": {"start": "08:00", "end": "20:00"},
                    },
                )
                print(f"✅ Created: {resource_data['title']}")
                created_count += 1
            except Exception as e:
                print(f"❌ Error creating {resource_data['title']}: {e}")

        print("-" * 50)
        print(f"✨ Resource seeding complete!")
        print(f"   Created: {created_count}")
        print(f"   Skipped: {skipped_count}")
        print(f"   Total:   {len(demo_resources)}")
        print()
        print("🎯 Demo resources include:")
        print("   • Study spaces")
        print("   • Technology equipment")
        print("   • Lab facilities")
        print("   • Event spaces")
        print()
        print("🌐 Visit /resources to see them!")


def main():
    """Main entry point for seed script."""
    try:
        seed_demo_users()
        seed_demo_resources()
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
