"""
Unit Tests for Booking Service - Campus Resource Hub
Tests business logic in services/booking_service.py.

Per .clinerules: Test conflict detection, status transitions, error handling.
"""

import pytest
from datetime import datetime
from src.models import User, Resource
from src.services.booking_service import BookingService, BookingConflictError, BookingStatusError
from src.app import db


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(
            name="Test User",
            email="test@example.com",
            password="TestPassword123",
            role="student",
        )
        db.session.add(user)
        db.session.commit()
        yield user


@pytest.fixture
def sample_resource(app, sample_user):
    """Create a sample resource for testing."""
    with app.app_context():
        resource = Resource(
            owner_id=sample_user.user_id,
            title="Test Study Room",
            description="A quiet study room",
            category="study_room",
            location="Library Floor 2",
            capacity=4,
            status="published",
        )
        db.session.add(resource)
        db.session.commit()
        yield resource


class TestBookingServiceConflictDetection:
    """Test conflict detection logic."""

    def test_no_conflict_when_no_bookings_exist(self, app, sample_resource, sample_user):
        """Test that booking is allowed when no other bookings exist."""
        with app.app_context():
            start = datetime(2025, 12, 1, 10, 0)
            end = datetime(2025, 12, 1, 12, 0)

            # Should not raise error
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=start,
                end_datetime=end,
            )

            assert booking.status == "pending"
            assert not BookingService.is_conflicting(sample_resource.resource_id, start, end)

    def test_conflict_with_approved_booking(self, app, sample_resource, sample_user):
        """Test that overlapping approved bookings create conflict."""
        with app.app_context():
            # Create and approve first booking
            booking1 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.approve_booking(booking1.booking_id, check_conflicts=False)

            # Try to create overlapping booking
            start = datetime(2025, 12, 1, 11, 0)
            end = datetime(2025, 12, 1, 13, 0)

            assert BookingService.is_conflicting(sample_resource.resource_id, start, end)

            with pytest.raises(BookingConflictError):
                BookingService.create_booking(
                    resource_id=sample_resource.resource_id,
                    requester_id=sample_user.user_id,
                    start_datetime=start,
                    end_datetime=end,
                )

    def test_no_conflict_with_pending_booking(self, app, sample_resource, sample_user):
        """Test that pending bookings do not create conflicts."""
        with app.app_context():
            # Create pending booking (not approved)
            BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )

            # Overlapping time should NOT conflict (first is still pending)
            start = datetime(2025, 12, 1, 11, 0)
            end = datetime(2025, 12, 1, 13, 0)

            assert not BookingService.is_conflicting(sample_resource.resource_id, start, end)

    def test_no_conflict_with_back_to_back_bookings(self, app, sample_resource, sample_user):
        """Test that touching endpoints (back-to-back) do not conflict."""
        with app.app_context():
            # Create and approve first booking
            booking1 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.approve_booking(booking1.booking_id, check_conflicts=False)

            # Create booking starting exactly when first ends
            start = datetime(2025, 12, 1, 12, 0)  # Same as booking1.end
            end = datetime(2025, 12, 1, 14, 0)

            assert not BookingService.is_conflicting(sample_resource.resource_id, start, end)

            booking2 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=start,
                end_datetime=end,
            )
            assert booking2.status == "pending"


class TestBookingServiceCreation:
    """Test booking creation logic."""

    def test_create_booking_success(self, app, sample_resource, sample_user):
        """Test successful booking creation."""
        with app.app_context():
            start = datetime(2025, 12, 1, 10, 0)
            end = datetime(2025, 12, 1, 12, 0)

            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=start,
                end_datetime=end,
            )

            assert booking.booking_id is not None
            assert booking.status == "pending"
            assert booking.resource_id == sample_resource.resource_id
            assert booking.requester_id == sample_user.user_id

    def test_create_booking_invalid_time_range(self, app, sample_resource, sample_user):
        """Test that end_datetime must be after start_datetime."""
        with app.app_context():
            start = datetime(2025, 12, 1, 12, 0)
            end = datetime(2025, 12, 1, 10, 0)  # Before start!

            with pytest.raises(ValueError, match="end_datetime must be after start_datetime"):
                BookingService.create_booking(
                    resource_id=sample_resource.resource_id,
                    requester_id=sample_user.user_id,
                    start_datetime=start,
                    end_datetime=end,
                )

    def test_create_booking_skip_conflict_check(self, app, sample_resource, sample_user):
        """Test creating overlapping booking when conflict check disabled."""
        with app.app_context():
            # Create and approve first booking
            booking1 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.approve_booking(booking1.booking_id, check_conflicts=False)

            # Create overlapping booking with conflict check disabled
            booking2 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 11, 0),
                end_datetime=datetime(2025, 12, 1, 13, 0),
                check_conflicts=False,
            )

            assert booking2.status == "pending"


class TestBookingServiceApproval:
    """Test booking approval logic."""

    def test_approve_pending_booking(self, app, sample_resource, sample_user):
        """Test approving a pending booking."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )

            approved = BookingService.approve_booking(booking.booking_id)

            assert approved.status == "approved"
            assert approved.booking_id == booking.booking_id

    def test_approve_conflicts_with_existing(self, app, sample_resource, sample_user):
        """Test that approving creates conflict check."""
        with app.app_context():
            # Create two overlapping pending bookings
            booking1 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
                check_conflicts=False,
            )

            booking2 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 11, 0),
                end_datetime=datetime(2025, 12, 1, 13, 0),
                check_conflicts=False,
            )

            # Approve first booking
            BookingService.approve_booking(booking1.booking_id)

            # Approving second should fail due to conflict
            with pytest.raises(BookingConflictError):
                BookingService.approve_booking(booking2.booking_id)

    def test_approve_non_pending_booking(self, app, sample_resource, sample_user):
        """Test that only pending bookings can be approved."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.approve_booking(booking.booking_id)

            # Try to approve already-approved booking
            with pytest.raises(BookingStatusError):
                BookingService.approve_booking(booking.booking_id)

    def test_approve_nonexistent_booking(self, app):
        """Test approving booking that doesn't exist."""
        with app.app_context():
            with pytest.raises(ValueError, match="Booking 999 not found"):
                BookingService.approve_booking(999)


class TestBookingServiceDenial:
    """Test booking denial/rejection logic."""

    def test_deny_pending_booking(self, app, sample_resource, sample_user):
        """Test denying a pending booking."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )

            denied = BookingService.deny_booking(booking.booking_id)

            assert denied.status == "rejected"

    def test_deny_non_pending_booking(self, app, sample_resource, sample_user):
        """Test that only pending bookings can be denied."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.approve_booking(booking.booking_id)

            # Try to deny approved booking
            with pytest.raises(BookingStatusError):
                BookingService.deny_booking(booking.booking_id)


class TestBookingServiceCancellation:
    """Test booking cancellation logic."""

    def test_cancel_pending_booking(self, app, sample_resource, sample_user):
        """Test cancelling a pending booking."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )

            cancelled = BookingService.cancel_booking(booking.booking_id)

            assert cancelled.status == "cancelled"

    def test_cancel_approved_booking(self, app, sample_resource, sample_user):
        """Test cancelling an approved booking."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.approve_booking(booking.booking_id)

            cancelled = BookingService.cancel_booking(booking.booking_id)

            assert cancelled.status == "cancelled"

    def test_cannot_cancel_completed_booking(self, app, sample_resource, sample_user):
        """Test that completed bookings cannot be cancelled."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.approve_booking(booking.booking_id)
            BookingService.complete_booking(booking.booking_id)

            with pytest.raises(BookingStatusError):
                BookingService.cancel_booking(booking.booking_id)


class TestBookingServiceCompletion:
    """Test booking completion logic."""

    def test_complete_approved_booking(self, app, sample_resource, sample_user):
        """Test completing an approved booking."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.approve_booking(booking.booking_id)

            completed = BookingService.complete_booking(booking.booking_id)

            assert completed.status == "completed"

    def test_cannot_complete_pending_booking(self, app, sample_resource, sample_user):
        """Test that pending bookings cannot be completed."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )

            with pytest.raises(BookingStatusError, match="Must be approved first"):
                BookingService.complete_booking(booking.booking_id)


class TestBookingServiceQueries:
    """Test booking query methods."""

    def test_get_booking(self, app, sample_resource, sample_user):
        """Test retrieving a booking by ID."""
        with app.app_context():
            booking = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )

            retrieved = BookingService.get_booking(booking.booking_id)

            assert retrieved.booking_id == booking.booking_id

    def test_get_user_bookings(self, app, sample_resource, sample_user):
        """Test getting all bookings for a user."""
        with app.app_context():
            # Create multiple bookings
            BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 2, 10, 0),
                end_datetime=datetime(2025, 12, 2, 12, 0),
            )

            bookings = BookingService.get_user_bookings(sample_user.user_id)

            assert len(bookings) == 2

    def test_get_booking_statistics(self, app, sample_resource, sample_user):
        """Test getting booking statistics."""
        with app.app_context():
            # Create bookings with different statuses
            _booking1 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 1, 10, 0),
                end_datetime=datetime(2025, 12, 1, 12, 0),
            )
            booking2 = BookingService.create_booking(
                resource_id=sample_resource.resource_id,
                requester_id=sample_user.user_id,
                start_datetime=datetime(2025, 12, 2, 10, 0),
                end_datetime=datetime(2025, 12, 2, 12, 0),
            )
            BookingService.approve_booking(booking2.booking_id)

            stats = BookingService.get_booking_statistics()

            assert stats["total"] == 2
            assert stats["pending"] == 1
            assert stats["approved"] == 1
