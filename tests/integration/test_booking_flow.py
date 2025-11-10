"""
Integration Tests for Booking Flow
Campus Resource Hub - Phase 6

Tests the complete booking workflow including:
- Creating bookings
- Conflict detection
- Approval workflow
- Cancellation
- Status transitions
"""

import pytest
from datetime import datetime, timedelta
from src.repositories.booking_repo import BookingRepository
from src.repositories.resource_repo import ResourceRepository
from src.repositories.user_repo import UserRepository


def _require_user(email: str):
    user = UserRepository.get_by_email(email)
    if not user:  # pragma: no cover
        raise AssertionError(f"Seeded user {email} missing")
    return user


def _login(client, email: str, password: str):
    client.post("/auth/login", data={"email": email, "password": password}, follow_redirects=True)


class TestBookingFlow:
    """Integration tests for booking workflow"""

    @pytest.fixture(autouse=True)
    def setup(self, app, demo_seed):
        """Attach seeded users/resources before each test."""
        with app.app_context():
            self.student_creds = demo_seed["student"]
            self.staff_creds = demo_seed["staff"]
            self.admin_creds = demo_seed["admin"]
            self.student = _require_user(self.student_creds["email"])
            self.staff = _require_user(self.staff_creds["email"])
            self.admin = _require_user(self.admin_creds["email"])
            resource = ResourceRepository.get_by_id(demo_seed["resource_ids"][0])
            if not resource:  # pragma: no cover
                raise AssertionError("Seeded resource missing")
            self.resource = resource
            yield

    def test_create_booking_success(self, client, app):
        """Test successful booking creation"""
        with app.app_context():
            # Login as student
            _login(client, self.student_creds["email"], self.student_creds["password"])

            # Create booking
            start = (datetime.now() + timedelta(days=1)).replace(second=0, microsecond=0)
            end = start + timedelta(hours=2)

            response = client.post(
                "/bookings",
                data={
                    "resource_id": self.resource.resource_id,
                    "start_date": start.strftime("%Y-%m-%d"),
                    "start_time": start.strftime("%H:%M"),
                    "end_date": end.strftime("%Y-%m-%d"),
                    "end_time": end.strftime("%H:%M"),
                    "notes": "Test booking",
                },
                follow_redirects=True,
            )

            assert response.status_code == 200

            # Verify booking was created
            bookings = BookingRepository.get_by_requester(self.student.user_id)
            created = [
                b
                for b in bookings
                if b.resource_id == self.resource.resource_id
                and abs((b.start_datetime - start).total_seconds()) < 1
            ]
            assert created, "New booking not persisted for expected slot"
            assert created[0].status in {"pending", "approved"}

    def test_booking_conflict_detection(self, client, app):
        """Test that overlapping bookings are prevented"""
        with app.app_context():
            # Create first booking
            start1 = datetime.now() + timedelta(days=1)
            end1 = start1 + timedelta(hours=2)

            BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start1,
                end_datetime=end1,
                status="approved",
            )

            # Login as different student
            student2 = UserRepository.create(
                name="Student Two",
                email="student2@test.com",
                password="password123",
                role="student",
            )

            _login(client, student2.email, "password123")

            # Try to create overlapping booking
            start2 = start1 + timedelta(minutes=30)  # Overlaps with first booking
            end2 = end1 + timedelta(minutes=30)

            client.post(
                "/bookings",
                data={
                    "resource_id": self.resource.resource_id,
                    "start_date": start2.strftime("%Y-%m-%d"),
                    "start_time": start2.strftime("%H:%M"),
                    "end_date": end2.strftime("%Y-%m-%d"),
                    "end_time": end2.strftime("%H:%M"),
                },
                follow_redirects=True,
            )

            # Verify second booking was not created
            bookings = BookingRepository.get_by_requester(student2.user_id)
            assert len(bookings) == 0

    def test_staff_approve_booking(self, client, app):
        """Test staff can approve pending bookings"""
        with app.app_context():
            # Create pending booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)

            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status="pending",
            )

            # Login as staff
            _login(client, self.staff_creds["email"], self.staff_creds["password"])

            # Approve booking
            response = client.post(f"/bookings/{booking.booking_id}/approve", follow_redirects=True)

            assert response.status_code == 200

            # Verify booking was approved
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == "approved"

    def test_staff_reject_booking(self, client, app):
        """Test staff can reject pending bookings"""
        with app.app_context():
            # Create pending booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)

            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status="pending",
            )

            # Login as staff
            _login(client, self.staff_creds["email"], self.staff_creds["password"])

            # Reject booking
            response = client.post(
                f"/bookings/{booking.booking_id}/reject",
                data={"rejection_reason": "Resource not available"},
                follow_redirects=True,
            )

            assert response.status_code == 200

            # Verify booking was rejected
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == "rejected"

    def test_user_cancel_booking(self, client, app):
        """Test user can cancel their own booking"""
        with app.app_context():
            # Create approved booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)

            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status="approved",
            )

            # Login as student
            _login(client, self.student_creds["email"], self.student_creds["password"])

            # Cancel booking
            response = client.post(f"/bookings/{booking.booking_id}/cancel", follow_redirects=True)

            assert response.status_code == 200

            # Verify booking was cancelled
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == "cancelled"

    def test_admin_complete_booking(self, client, app):
        """Test admin can mark booking as completed"""
        with app.app_context():
            # Create approved booking
            start = datetime.now() - timedelta(days=1)  # Past booking
            end = start + timedelta(hours=2)

            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status="approved",
            )

            # Login as admin
            _login(client, self.admin_creds["email"], self.admin_creds["password"])

            # Mark as complete
            response = client.post(
                f"/bookings/{booking.booking_id}/complete", follow_redirects=True
            )

            assert response.status_code == 200

            # Verify booking was completed
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == "completed"

    def test_unauthorized_approval_denied(self, client, app):
        """Test that students cannot approve bookings"""
        with app.app_context():
            # Create pending booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)

            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status="pending",
            )

            # Login as student
            _login(client, self.student_creds["email"], self.student_creds["password"])

            # Try to approve booking (should fail)
            response = client.post(f"/bookings/{booking.booking_id}/approve", follow_redirects=True)

            # Should be denied (403 or redirect with error)
            assert response.status_code in [200, 302, 403]

            # Verify booking is still pending
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == "pending"

    def test_view_my_bookings(self, client, app):
        """Test user can view their bookings dashboard"""
        with app.app_context():
            # Create multiple bookings with different statuses
            now = datetime.now()

            # Pending booking
            BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=now + timedelta(days=1),
                end_datetime=now + timedelta(days=1, hours=2),
                status="pending",
            )

            # Approved booking
            BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=now + timedelta(days=2),
                end_datetime=now + timedelta(days=2, hours=2),
                status="approved",
            )

            # Completed booking
            BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=now - timedelta(days=1),
                end_datetime=now - timedelta(days=1) + timedelta(hours=2),
                status="completed",
            )

            # Login as student
            _login(client, self.student_creds["email"], self.student_creds["password"])

            # View my bookings
            response = client.get("/bookings/my-bookings")

            assert response.status_code == 200
            assert b"My Bookings" in response.data

    def test_booking_detail_view(self, client, app):
        """Test viewing booking details"""
        with app.app_context():
            # Create booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)

            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status="pending",
            )

            # Login as student
            _login(client, self.student_creds["email"], self.student_creds["password"])

            # View booking detail
            response = client.get(f"/bookings/{booking.booking_id}")

            assert response.status_code == 200
            assert b"Booking Details" in response.data
            assert self.resource.title.encode() in response.data
