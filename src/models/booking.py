"""
Booking Model - Campus Resource Hub
Defines booking requests and approvals for resources.

Per docs/ERD.md specifications and .clinerules architecture.
"""

from datetime import datetime
from typing import Dict

from src.app import db


class Booking(db.Model):
    """
    Booking model for resource reservation requests.

    Status Workflow:
        - pending: Initial state when user requests booking
        - approved: Booking approved by resource owner/staff/admin
        - rejected: Booking denied by resource owner/staff/admin
        - cancelled: Booking cancelled by requester or admin
        - completed: Booking finished (auto-updated after end_datetime)

    Conflict Detection:
        Two bookings conflict if:
        (new.start < existing.end) AND (new.end > existing.start)

        Only 'approved' bookings count for conflict detection.
        Pending/rejected/cancelled bookings do not block time slots.

    Relationships:
        - resource: The resource being booked
        - requester: User who made the booking request
        - reviews: Optional review after booking completion
    """

    __tablename__ = "bookings"

    # Primary Key
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resources.resource_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    requester_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,  # Allow NULL if user deleted (preserve history)
        index=True,
    )

    # Booking Time Range
    start_datetime = db.Column(db.DateTime, nullable=False, index=True)
    end_datetime = db.Column(db.DateTime, nullable=False, index=True)

    # Booking Status
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    resource = db.relationship("Resource", back_populates="bookings", foreign_keys=[resource_id])

    requester = db.relationship("User", back_populates="bookings", foreign_keys=[requester_id])

    # Note: Review relationship added in Review model (one-to-one)

    # Constraints
    __table_args__ = (
        db.CheckConstraint(
            status.in_(["pending", "approved", "rejected", "cancelled", "completed"]),
            name="check_valid_booking_status",
        ),
        db.CheckConstraint("end_datetime > start_datetime", name="check_end_after_start"),
        # Composite index for efficient conflict detection queries
        db.Index("idx_bookings_resource_datetime", "resource_id", "start_datetime", "end_datetime"),
    )

    def __init__(
        self,
        resource_id: int,
        requester_id: int,
        start_datetime: datetime,
        end_datetime: datetime,
        status: str = "pending",
    ):
        """
        Initialize a new Booking.

        Args:
            resource_id: ID of resource being booked
            requester_id: ID of user making the booking
            start_datetime: Start time of booking
            end_datetime: End time of booking
            status: Initial booking status (default: pending)

        Raises:
            ValueError: If end_datetime is not after start_datetime
        """
        if end_datetime <= start_datetime:
            raise ValueError("end_datetime must be after start_datetime")

        self.resource_id = resource_id
        self.requester_id = requester_id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.status = status

    def is_pending(self) -> bool:
        """Check if booking is pending approval."""
        return self.status == "pending"

    def is_approved(self) -> bool:
        """Check if booking is approved."""
        return self.status == "approved"

    def is_rejected(self) -> bool:
        """Check if booking is rejected."""
        return self.status == "rejected"

    def is_cancelled(self) -> bool:
        """Check if booking is cancelled."""
        return self.status == "cancelled"

    def is_completed(self) -> bool:
        """Check if booking is completed."""
        return self.status == "completed"

    def can_be_approved(self) -> bool:
        """Check if booking can be approved (must be pending)."""
        return self.status == "pending"

    def can_be_cancelled(self) -> bool:
        """Check if booking can be cancelled (pending or approved only)."""
        return self.status in ["pending", "approved"]

    def approve(self) -> None:
        """
        Approve the booking.

        Raises:
            ValueError: If booking is not in pending status
        """
        if not self.can_be_approved():
            raise ValueError(f"Cannot approve booking with status: {self.status}")

        self.status = "approved"
        self.updated_at = datetime.utcnow()

    def reject(self) -> None:
        """
        Reject the booking.

        Raises:
            ValueError: If booking is not in pending status
        """
        if not self.can_be_approved():
            raise ValueError(f"Cannot reject booking with status: {self.status}")

        self.status = "rejected"
        self.updated_at = datetime.utcnow()

    def cancel(self) -> None:
        """
        Cancel the booking.

        Raises:
            ValueError: If booking cannot be cancelled
        """
        if not self.can_be_cancelled():
            raise ValueError(f"Cannot cancel booking with status: {self.status}")

        self.status = "cancelled"
        self.updated_at = datetime.utcnow()

    def complete(self) -> None:
        """
        Mark booking as completed.

        This is typically called automatically after end_datetime passes.
        Only approved bookings can be completed.

        Raises:
            ValueError: If booking is not approved
        """
        if not self.is_approved():
            raise ValueError(f"Cannot complete booking with status: {self.status}")

        self.status = "completed"
        self.updated_at = datetime.utcnow()

    def get_duration_hours(self) -> float:
        """
        Calculate booking duration in hours.

        Returns:
            Duration in hours (decimal)
        """
        delta = self.end_datetime - self.start_datetime
        return delta.total_seconds() / 3600

    def is_in_past(self) -> bool:
        """Check if booking end time has passed."""
        return self.end_datetime < datetime.utcnow()

    def is_in_future(self) -> bool:
        """Check if booking start time is in the future."""
        return self.start_datetime > datetime.utcnow()

    def is_active(self) -> bool:
        """Check if booking is currently active (between start and end)."""
        now = datetime.utcnow()
        return self.start_datetime <= now <= self.end_datetime

    def overlaps_with(self, start: datetime, end: datetime) -> bool:
        """
        Check if this booking overlaps with a given time range.

        Overlap condition: (start < self.end) AND (end > self.start)

        Args:
            start: Start datetime to check
            end: End datetime to check

        Returns:
            True if there is overlap, False otherwise
        """
        return (start < self.end_datetime) and (end > self.start_datetime)

    def __repr__(self) -> str:
        """String representation of Booking."""
        return (
            f"<Booking {self.booking_id}: "
            f"Resource={self.resource_id} "
            f"Status={self.status} "
            f"{self.start_datetime} to {self.end_datetime}>"
        )

    def to_dict(self, include_relations: bool = False) -> Dict:
        """
        Convert booking to dictionary (for JSON responses).

        Args:
            include_relations: Whether to include related resource/user info

        Returns:
            Dictionary representation of booking
        """
        data = {
            "booking_id": self.booking_id,
            "resource_id": self.resource_id,
            "requester_id": self.requester_id,
            "start_datetime": self.start_datetime.isoformat() if self.start_datetime else None,
            "end_datetime": self.end_datetime.isoformat() if self.end_datetime else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "duration_hours": self.get_duration_hours(),
            "is_active": self.is_active(),
            "is_in_past": self.is_in_past(),
            "is_in_future": self.is_in_future(),
        }

        if include_relations:
            if self.resource:
                data["resource_title"] = self.resource.title
                data["resource_category"] = self.resource.category
                data["resource_location"] = self.resource.location

            if self.requester:
                data["requester_name"] = self.requester.name
                data["requester_email"] = self.requester.email

        return data
