"""
Booking Repository - Campus Resource Hub
Data Access Layer for Booking model.

Per .clinerules: All database operations encapsulated in repositories.
Includes conflict detection queries.
"""

from typing import List, Optional, Dict
from datetime import datetime
from src.models import db, Booking


class BookingRepository:
    """Repository for Booking model CRUD operations with conflict detection."""

    @staticmethod
    def create(
        resource_id: int,
        requester_id: int,
        start_datetime: datetime,
        end_datetime: datetime,
        status: str = "pending",
    ) -> Booking:
        """Create a new booking."""
        booking = Booking(
            resource_id=resource_id,
            requester_id=requester_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            status=status,
        )
        db.session.add(booking)
        db.session.commit()
        return booking

    @staticmethod
    def get_by_id(booking_id: int) -> Optional[Booking]:
        """Get booking by ID."""
        return Booking.query.get(booking_id)

    @staticmethod
    def get_all(
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None,
        resource_id: Optional[int] = None,
        requester_id: Optional[int] = None,
    ) -> Dict:
        """Get all bookings with pagination and filters."""
        query = Booking.query

        if status:
            query = query.filter_by(status=status)
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        if requester_id:
            query = query.filter_by(requester_id=requester_id)

        query = query.order_by(Booking.start_datetime.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": paginated.items,
            "total": paginated.total,
            "page": paginated.page,
            "per_page": paginated.per_page,
            "pages": paginated.pages,
        }

    @staticmethod
    def find_conflicts(
        resource_id: int,
        start_datetime: datetime,
        end_datetime: datetime,
        exclude_booking_id: Optional[int] = None,
    ) -> List[Booking]:
        """
        Find conflicting approved bookings for a resource and time range.

        Conflict condition: (new.start < existing.end) AND (new.end > existing.start)
        Only approved bookings count as conflicts.

        Args:
            resource_id: Resource to check
            start_datetime: Proposed start time
            end_datetime: Proposed end time
            exclude_booking_id: Optional booking ID to exclude (for updates)

        Returns:
            List of conflicting bookings
        """
        query = Booking.query.filter(
            Booking.resource_id == resource_id,
            Booking.status == "approved",
            Booking.start_datetime < end_datetime,
            Booking.end_datetime > start_datetime,
        )

        if exclude_booking_id:
            query = query.filter(Booking.booking_id != exclude_booking_id)

        return query.all()

    @staticmethod
    def has_conflict(
        resource_id: int,
        start_datetime: datetime,
        end_datetime: datetime,
        exclude_booking_id: Optional[int] = None,
    ) -> bool:
        """
        Check if there are any conflicting bookings.

        Returns:
            True if conflicts exist, False otherwise
        """
        conflicts = BookingRepository.find_conflicts(
            resource_id, start_datetime, end_datetime, exclude_booking_id
        )
        return len(conflicts) > 0

    @staticmethod
    def update(booking_id: int, **kwargs) -> Optional[Booking]:
        """Update booking fields."""
        booking = Booking.query.get(booking_id)
        if not booking:
            return None

        allowed_fields = ["status", "start_datetime", "end_datetime"]
        for field in allowed_fields:
            if field in kwargs:
                setattr(booking, field, kwargs[field])

        booking.updated_at = datetime.utcnow()
        db.session.commit()
        return booking

    @staticmethod
    def delete(booking_id: int) -> bool:
        """Delete booking by ID."""
        booking = Booking.query.get(booking_id)
        if not booking:
            return False

        db.session.delete(booking)
        db.session.commit()
        return True

    @staticmethod
    def approve(booking_id: int) -> Optional[Booking]:
        """Approve a pending booking."""
        booking = Booking.query.get(booking_id)
        if not booking:
            return None

        booking.approve()
        db.session.commit()
        return booking

    @staticmethod
    def reject(booking_id: int) -> Optional[Booking]:
        """Reject a pending booking."""
        booking = Booking.query.get(booking_id)
        if not booking:
            return None

        booking.reject()
        db.session.commit()
        return booking

    @staticmethod
    def cancel(booking_id: int) -> Optional[Booking]:
        """Cancel a booking."""
        booking = Booking.query.get(booking_id)
        if not booking:
            return None

        booking.cancel()
        db.session.commit()
        return booking

    @staticmethod
    def complete(booking_id: int) -> Optional[Booking]:
        """Mark booking as completed."""
        booking = Booking.query.get(booking_id)
        if not booking:
            return None

        booking.complete()
        db.session.commit()
        return booking

    @staticmethod
    def get_by_resource(resource_id: int, status: Optional[str] = None) -> List[Booking]:
        """Get all bookings for a resource."""
        query = Booking.query.filter_by(resource_id=resource_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Booking.start_datetime.desc()).all()

    @staticmethod
    def get_by_requester(requester_id: int, status: Optional[str] = None) -> List[Booking]:
        """Get all bookings by a user."""
        query = Booking.query.filter_by(requester_id=requester_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Booking.start_datetime.desc()).all()

    @staticmethod
    def get_pending_approvals(resource_id: Optional[int] = None) -> List[Booking]:
        """Get all pending bookings awaiting approval."""
        query = Booking.query.filter_by(status="pending")
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        return query.order_by(Booking.created_at.asc()).all()

    @staticmethod
    def get_upcoming(requester_id: Optional[int] = None, limit: int = 10) -> List[Booking]:
        """Get upcoming approved bookings."""
        query = Booking.query.filter(
            Booking.status == "approved", Booking.start_datetime > datetime.utcnow()
        )
        if requester_id:
            query = query.filter_by(requester_id=requester_id)

        return query.order_by(Booking.start_datetime.asc()).limit(limit).all()

    @staticmethod
    def count() -> int:
        """Get total number of bookings."""
        return Booking.query.count()

    @staticmethod
    def count_by_status(status: str) -> int:
        """Get count of bookings by status."""
        return Booking.query.filter_by(status=status).count()
