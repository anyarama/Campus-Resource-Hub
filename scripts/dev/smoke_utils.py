#!/usr/bin/env python3
"""Shared helpers for smoke audits."""
from __future__ import annotations
from pathlib import Path
import sys
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.repositories.user_repo import UserRepository
from src.repositories.resource_repo import ResourceRepository
from src.repositories.booking_repo import BookingRepository
from src.repositories.message_repo import MessageRepository
from src.models.resource import Resource

SMOKE_FILE = Path(__file__).with_name('smoke_urls.txt')
DEFAULT_PASSWORD = "Demo123!"


def load_smoke_entries():
    entries = []
    for raw in SMOKE_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) == 1:
            role, path = 'public', parts[0]
        else:
            role, path = parts
        entries.append((role.lower(), path.strip()))
    return entries


def _ensure_user(email: str, name: str, role: str):
    user = UserRepository.get_by_email(email)
    if user:
        return user
    return UserRepository.create(name=name, email=email, password=DEFAULT_PASSWORD, role=role)


def _ensure_resource(owner_id: int, title: str, location: str):
    existing = Resource.query.filter_by(title=title).first()
    if existing:
        return existing
    return ResourceRepository.create(
        owner_id=owner_id,
        title=title,
        category='study_room',
        description=f'{title} enterprise smoke resource',
        location=location,
        capacity=12,
        status='published',
    )


def _ensure_booking(resource_id: int, requester_id: int):
    booking = BookingRepository.get_by_id(1)
    if booking:
        return booking
    start = datetime.utcnow() + timedelta(days=2)
    end = start + timedelta(hours=2)
    return BookingRepository.create(
        resource_id=resource_id,
        requester_id=requester_id,
        start_datetime=start,
        end_datetime=end,
        status='approved',
    )


def _ensure_messages(student_id: int, staff_id: int):
    convo = MessageRepository.get_conversation(student_id, staff_id)
    if convo:
        return
    MessageRepository.create(
        sender_id=student_id,
        receiver_id=staff_id,
        content="Hi! Can I book this resource tomorrow?",
        thread_id=1,
    )
    MessageRepository.create(
        sender_id=staff_id,
        receiver_id=student_id,
        content="Absolutely—it's available after 3 PM.",
        thread_id=1,
    )


def seed_demo_data():
    admin = _ensure_user('admin@smoke.local', 'Admin Smoke', 'admin')
    staff = _ensure_user('staff@smoke.local', 'Staff Smoke', 'staff')
    student = _ensure_user('student@smoke.local', 'Student Smoke', 'student')

    res1 = _ensure_resource(staff.user_id, 'Smoke Resource Alpha', 'Innovation Hub A1')
    res2 = _ensure_resource(staff.user_id, 'Smoke Resource Beta', 'Innovation Hub B2')
    booking = _ensure_booking(res1.resource_id, student.user_id)
    _ensure_messages(student.user_id, staff.user_id)

    return {
        'admin': {'email': 'admin@smoke.local', 'password': DEFAULT_PASSWORD},
        'staff': {'email': 'staff@smoke.local', 'password': DEFAULT_PASSWORD},
        'student': {'email': 'student@smoke.local', 'password': DEFAULT_PASSWORD},
        'resource_ids': [res1.resource_id, res2.resource_id],
        'booking_id': booking.booking_id,
        'staff_user_id': staff.user_id,
    }


def build_client(app, role: str, creds: dict):
    client = app.test_client()
    if role == 'public':
        return client
    info = creds.get(role)
    if not info:
        raise KeyError(f"No credentials for role {role}")
    client.post(
        '/auth/login',
        data={'email': info['email'], 'password': info['password']},
        follow_redirects=True,
    )
    return client
