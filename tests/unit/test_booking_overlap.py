"""
Unit Tests for Booking Overlap Detection - Campus Resource Hub
Tests interval overlap rules for conflict detection.

Overlap Rules (per requirements):
- Half-open intervals: [start, end)
- Touching endpoints allowed (back-to-back bookings OK)
- Only approved bookings count for conflicts
- Bookings on different resources never conflict

Overlap condition: (new.start < existing.end) AND (new.end > existing.start)

Per .clinerules: TDD approach with edge cases and unhappy paths.
"""

from datetime import datetime
from src.models import db, User, Resource, Booking


class TestBookingOverlapDetection:
    """Test booking interval overlap detection algorithm."""

    def test_exact_overlap(self, app):
        """Test exact same time range overlaps."""
        with app.app_context():
            start = datetime(2025, 11, 10, 10, 0)
            end = datetime(2025, 11, 10, 12, 0)

            # Create test booking
            booking = Booking(resource_id=1, requester_id=1, start_datetime=start, end_datetime=end)

            # Should overlap with itself
            assert booking.overlaps_with(start, end) is True

    def test_partial_overlap_start_during(self, app):
        """Test new booking starts during existing booking."""
        with app.app_context():
            # Existing: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 11:00 - 13:00 (starts during existing)
            new_start = datetime(2025, 11, 10, 11, 0)
            new_end = datetime(2025, 11, 10, 13, 0)

            assert booking.overlaps_with(new_start, new_end) is True

    def test_partial_overlap_end_during(self, app):
        """Test new booking ends during existing booking."""
        with app.app_context():
            # Existing: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 09:00 - 11:00 (ends during existing)
            new_start = datetime(2025, 11, 10, 9, 0)
            new_end = datetime(2025, 11, 10, 11, 0)

            assert booking.overlaps_with(new_start, new_end) is True

    def test_complete_overlap_surrounds(self, app):
        """Test new booking completely surrounds existing booking."""
        with app.app_context():
            # Existing: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 09:00 - 13:00 (completely surrounds existing)
            new_start = datetime(2025, 11, 10, 9, 0)
            new_end = datetime(2025, 11, 10, 13, 0)

            assert booking.overlaps_with(new_start, new_end) is True

    def test_complete_overlap_within(self, app):
        """Test new booking completely within existing booking."""
        with app.app_context():
            # Existing: 10:00 - 14:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 14, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 11:00 - 12:00 (completely within existing)
            new_start = datetime(2025, 11, 10, 11, 0)
            new_end = datetime(2025, 11, 10, 12, 0)

            assert booking.overlaps_with(new_start, new_end) is True

    def test_no_overlap_before(self, app):
        """Test new booking completely before existing booking."""
        with app.app_context():
            # Existing: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 08:00 - 09:00 (completely before existing)
            new_start = datetime(2025, 11, 10, 8, 0)
            new_end = datetime(2025, 11, 10, 9, 0)

            assert booking.overlaps_with(new_start, new_end) is False

    def test_no_overlap_after(self, app):
        """Test new booking completely after existing booking."""
        with app.app_context():
            # Existing: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 13:00 - 14:00 (completely after existing)
            new_start = datetime(2025, 11, 10, 13, 0)
            new_end = datetime(2025, 11, 10, 14, 0)

            assert booking.overlaps_with(new_start, new_end) is False

    def test_touching_endpoints_no_overlap(self, app):
        """Test back-to-back bookings (end==start) do NOT overlap."""
        with app.app_context():
            # Existing: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 12:00 - 14:00 (starts exactly when existing ends)
            new_start = datetime(2025, 11, 10, 12, 0)
            new_end = datetime(2025, 11, 10, 14, 0)

            # Half-open interval [start, end): start=end is allowed
            assert booking.overlaps_with(new_start, new_end) is False

    def test_touching_endpoints_reverse_no_overlap(self, app):
        """Test back-to-back bookings (new ends when existing starts) do NOT overlap."""
        with app.app_context():
            # Existing: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 08:00 - 10:00 (ends exactly when existing starts)
            new_start = datetime(2025, 11, 10, 8, 0)
            new_end = datetime(2025, 11, 10, 10, 0)

            # Half-open interval [start, end): new.end = existing.start is allowed
            assert booking.overlaps_with(new_start, new_end) is False

    def test_one_minute_overlap(self, app):
        """Test even one minute overlap is detected."""
        with app.app_context():
            # Existing: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)

            booking = Booking(
                resource_id=1,
                requester_id=1,
                start_datetime=existing_start,
                end_datetime=existing_end,
            )

            # New: 11:59 - 13:00 (1 minute overlap)
            new_start = datetime(2025, 11, 10, 11, 59)
            new_end = datetime(2025, 11, 10, 13, 0)

            assert booking.overlaps_with(new_start, new_end) is True


class TestBookingConflictDetectionIntegration:
    """Integration tests for booking conflicts with database."""

    def test_approved_booking_blocks_new_booking(self, app):
        """Test approved booking prevents overlapping bookings."""
        with app.app_context():
            # Create user and resource
            user = User(name="User", email="user@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            # Create approved booking: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)
            existing_booking = Booking(
                resource_id=resource.resource_id,
                requester_id=user.user_id,
                start_datetime=existing_start,
                end_datetime=existing_end,
                status="approved",
            )
            db.session.add(existing_booking)
            db.session.commit()

            # Query approved bookings for conflict
            new_start = datetime(2025, 11, 10, 11, 0)
            new_end = datetime(2025, 11, 10, 13, 0)

            conflicts = Booking.query.filter(
                Booking.resource_id == resource.resource_id,
                Booking.status == "approved",
                Booking.start_datetime < new_end,
                Booking.end_datetime > new_start,
            ).all()

            assert len(conflicts) == 1
            assert conflicts[0].booking_id == existing_booking.booking_id

    def test_pending_booking_does_not_block(self, app):
        """Test pending bookings do NOT prevent new bookings."""
        with app.app_context():
            user = User(name="User", email="user@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            # Create pending booking: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)
            pending_booking = Booking(
                resource_id=resource.resource_id,
                requester_id=user.user_id,
                start_datetime=existing_start,
                end_datetime=existing_end,
                status="pending",
            )
            db.session.add(pending_booking)
            db.session.commit()

            # Query approved bookings for conflict (should find none)
            new_start = datetime(2025, 11, 10, 11, 0)
            new_end = datetime(2025, 11, 10, 13, 0)

            conflicts = Booking.query.filter(
                Booking.resource_id == resource.resource_id,
                Booking.status == "approved",
                Booking.start_datetime < new_end,
                Booking.end_datetime > new_start,
            ).all()

            assert len(conflicts) == 0

    def test_cancelled_booking_does_not_block(self, app):
        """Test cancelled bookings do NOT prevent new bookings."""
        with app.app_context():
            user = User(name="User", email="user@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            # Create cancelled booking: 10:00 - 12:00
            existing_start = datetime(2025, 11, 10, 10, 0)
            existing_end = datetime(2025, 11, 10, 12, 0)
            cancelled_booking = Booking(
                resource_id=resource.resource_id,
                requester_id=user.user_id,
                start_datetime=existing_start,
                end_datetime=existing_end,
                status="cancelled",
            )
            db.session.add(cancelled_booking)
            db.session.commit()

            # Query approved bookings for conflict (should find none)
            new_start = datetime(2025, 11, 10, 11, 0)
            new_end = datetime(2025, 11, 10, 13, 0)

            conflicts = Booking.query.filter(
                Booking.resource_id == resource.resource_id,
                Booking.status == "approved",
                Booking.start_datetime < new_end,
                Booking.end_datetime > new_start,
            ).all()

            assert len(conflicts) == 0

    def test_different_resources_no_conflict(self, app):
        """Test bookings on different resources never conflict."""
        with app.app_context():
            user = User(name="User", email="user@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource1 = Resource(owner_id=user.user_id, title="Room A", category="study_room")
            resource2 = Resource(owner_id=user.user_id, title="Room B", category="study_room")
            db.session.add_all([resource1, resource2])
            db.session.commit()

            # Create approved booking for Resource 1: 10:00 - 12:00
            start = datetime(2025, 11, 10, 10, 0)
            end = datetime(2025, 11, 10, 12, 0)
            booking1 = Booking(
                resource_id=resource1.resource_id,
                requester_id=user.user_id,
                start_datetime=start,
                end_datetime=end,
                status="approved",
            )
            db.session.add(booking1)
            db.session.commit()

            # Check for conflicts on Resource 2 (should find none)
            conflicts = Booking.query.filter(
                Booking.resource_id == resource2.resource_id,
                Booking.status == "approved",
                Booking.start_datetime < end,
                Booking.end_datetime > start,
            ).all()

            assert len(conflicts) == 0

    def test_multiple_non_overlapping_bookings(self, app):
        """Test multiple approved bookings without conflicts."""
        with app.app_context():
            user = User(name="User", email="user@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            # Create three back-to-back approved bookings
            bookings = [
                Booking(
                    resource_id=resource.resource_id,
                    requester_id=user.user_id,
                    start_datetime=datetime(2025, 11, 10, 8, 0),
                    end_datetime=datetime(2025, 11, 10, 10, 0),
                    status="approved",
                ),
                Booking(
                    resource_id=resource.resource_id,
                    requester_id=user.user_id,
                    start_datetime=datetime(2025, 11, 10, 10, 0),
                    end_datetime=datetime(2025, 11, 10, 12, 0),
                    status="approved",
                ),
                Booking(
                    resource_id=resource.resource_id,
                    requester_id=user.user_id,
                    start_datetime=datetime(2025, 11, 10, 12, 0),
                    end_datetime=datetime(2025, 11, 10, 14, 0),
                    status="approved",
                ),
            ]
            db.session.add_all(bookings)
            db.session.commit()

            # All should exist without conflict
            assert (
                Booking.query.filter_by(resource_id=resource.resource_id, status="approved").count()
                == 3
            )
