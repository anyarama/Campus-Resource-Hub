import pytest
from datetime import datetime, timedelta

from src.repositories.user_repo import UserRepository
from src.repositories.resource_repo import ResourceRepository
from src.repositories.booking_repo import BookingRepository
from src.repositories.message_repo import MessageRepository
from src.models.resource import Resource

SMOKE_MATRIX = [
    ("public", "/auth/login"),
    ("public", "/auth/register"),
    ("public", "/resources"),
    ("public", "/resources/1"),
    ("student", "/dashboard"),
    ("student", "/resources/create"),
    ("student", "/resources/1/edit"),
    ("student", "/bookings/new?resource_id=1"),
    ("student", "/bookings/my-bookings"),
    ("student", "/messages"),
    ("admin", "/admin/dashboard"),
    ("admin", "/admin/users"),
    ("admin", "/admin/analytics"),
]

DEFAULT_PASSWORD = "SmokePass123!"


def _ensure_user(email: str, name: str, role: str):
    user = UserRepository.get_by_email(email)
    if user:
        return user
    return UserRepository.create(name=name, email=email, password=DEFAULT_PASSWORD, role=role)


def _ensure_resource(owner_id: int, title: str):
    existing = Resource.query.filter_by(title=title).first()
    if existing:
        return existing
    return ResourceRepository.create(
        owner_id=owner_id,
        title=title,
        category="study_room",
        description="Smoke resource",
        location="Enterprise Hub",
        capacity=12,
        status="published",
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
        status="approved",
    )


def _ensure_messages(student_id: int, staff_id: int):
    if MessageRepository.get_conversation(student_id, staff_id):
        return
    MessageRepository.create(
        sender_id=student_id,
        receiver_id=staff_id,
        content="Smoke test message",
        thread_id=1,
    )
    MessageRepository.create(
        sender_id=staff_id,
        receiver_id=student_id,
        content="Smoke test reply",
        thread_id=1,
    )


@pytest.fixture()
def smoke_context(app):
    with app.app_context():
        admin = _ensure_user("admin+smoke@example.com", "Admin Smoke", "admin")
        staff = _ensure_user("staff+smoke@example.com", "Staff Smoke", "staff")
        student = _ensure_user("student+smoke@example.com", "Student Smoke", "student")
        resource = _ensure_resource(staff.user_id, "Smoke Resource Alpha")
        _ensure_resource(staff.user_id, "Smoke Resource Beta")
        _ensure_booking(resource.resource_id, student.user_id)
        _ensure_messages(student.user_id, staff.user_id)
        creds = {
            "admin": {"email": admin.email, "password": DEFAULT_PASSWORD},
            "staff": {"email": staff.email, "password": DEFAULT_PASSWORD},
            "student": {"email": student.email, "password": DEFAULT_PASSWORD},
        }
        yield creds


def build_client(app, creds, role):
    client = app.test_client()
    if role == "public":
        return client
    info = creds[role]
    client.post(
        "/auth/login",
        data={"email": info["email"], "password": info["password"]},
        follow_redirects=True,
    )
    return client


@pytest.mark.parametrize("role,path", SMOKE_MATRIX)
def test_smoke_routes_render(role, path, app, smoke_context):
    client = build_client(app, smoke_context, role)
    response = client.get(path, follow_redirects=True)
    html = response.get_data(as_text=True)
    assert response.status_code == 200, f"{path} returned {response.status_code}"
    assert "/static/dist/" in html and ".css" in html
