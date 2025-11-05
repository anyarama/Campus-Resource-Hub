"""
Booking Service - Campus Resource Hub
Business logic layer for booking operations.

Per .clinerules: Services orchestrate business logic and call repositories.
Implements conflict detection and status transition enforcement.
"""

from typing import Optional, Dict, List
from datetime import datetime
from src.repositories import BookingRepository
from src.models import Booking


class BookingConflictError(Exception):
    """Raised when a booking conflicts with existing approved bookings."""

    pass


class BookingStatusError(Exception):
    """Raised when an invalid status transition is attempted."""

    pass


class BookingService:
    """
    Service for booking operations with conflict detection.

    Enforces business rules:
    - No overlapping approved bookings for same resource
    - Status transitions follow workflow rules
    - Only certain roles can approve bookings
    """

    @staticmethod
    def is_conflicting(
        resource_id: int,
        start_datetime: datetime,
        end_datetime: datetime,
        exclude_booking_id: Optional[int] = None,
    ) -> bool:
        """
        Check if a booking would conflict with existing approved bookings.

        Args:
            resource_id: Resource to check
            start_datetime: Proposed start time
            end_datetime: Proposed end time
            exclude_booking_id: Optional booking ID to exclude (for updates)

        Returns:
            True if conflicts exist, False otherwise
        """
        return BookingRepository.has_conflict(
            resource_id, start_datetime, end_datetime, exclude_booking_id
        )

    @staticmethod
    def create_booking(
        resource_id: int,
        requester_id: int,
        start_datetime: datetime,
        end_datetime: datetime,
        check_conflicts: bool = True,
    ) -> Booking:
        """
        Create a new booking with conflict detection.

        Args:
            resource_id: Resource to book
            requester_id: User making the booking
            start_datetime: Start time
            end_datetime: End time
            check_conflicts: Whether to check for conflicts (default True)

        Returns:
            Created Booking instance

        Raises:
            BookingConflictError: If booking conflicts with approved bookings
            ValueError: If end_datetime is not after start_datetime
        """
        # Validate time range
        if end_datetime <= start_datetime:
            raise ValueError("end_datetime must be after start_datetime")

        # Check for conflicts if requested
        if check_conflicts:
            conflicts = BookingRepository.find_conflicts(resource_id, start_datetime, end_datetime)
            if conflicts:
                conflict_times = [f"{c.start_datetime} to {c.end_datetime}" for c in conflicts]
                raise BookingConflictError(
                    f"Booking conflicts with existing approved bookings: {', '.join(conflict_times)}"
                )

        # Create booking with pending status
        return BookingRepository.create(
            resource_id=resource_id,
            requester_id=requester_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            status="pending",
        )

    @staticmethod
    def approve_booking(booking_id: int, check_conflicts: bool = True) -> Booking:
        """
        Approve a pending booking.

        Args:
            booking_id: Booking ID to approve
            check_conflicts: Whether to check for conflicts before approving

        Returns:
            Approved Booking instance

        Raises:
            BookingStatusError: If booking is not pending
            BookingConflictError: If approval would create conflict
            ValueError: If booking not found
        """
        booking = BookingRepository.get_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found")

        if not booking.can_be_approved():
            raise BookingStatusError(f"Cannot approve booking with status: {booking.status}")

        # Check if approving would create a conflict
        if check_conflicts:
            conflicts = BookingRepository.find_conflicts(
                booking.resource_id,
                booking.start_datetime,
                booking.end_datetime,
                exclude_booking_id=booking_id,
            )
            if conflicts:
                raise BookingConflictError(
                    f"Approving this booking would conflict with {len(conflicts)} existing booking(s)"
                )

        return BookingRepository.approve(booking_id)

    @staticmethod
    def deny_booking(booking_id: int) -> Booking:
        """
        Deny/reject a pending booking.

        Args:
            booking_id: Booking ID to deny

        Returns:
            Rejected Booking instance

        Raises:
            BookingStatusError: If booking is not pending
            ValueError: If booking not found
        """
        booking = BookingRepository.get_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found")

        if not booking.can_be_approved():
            raise BookingStatusError(f"Cannot reject booking with status: {booking.status}")

        return BookingRepository.reject(booking_id)

    @staticmethod
    def cancel_booking(booking_id: int) -> Booking:
        """
        Cancel a booking (pending or approved only).

        Args:
            booking_id: Booking ID to cancel

        Returns:
            Cancelled Booking instance

        Raises:
            BookingStatusError: If booking cannot be cancelled
            ValueError: If booking not found
        """
        booking = BookingRepository.get_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found")

        if not booking.can_be_cancelled():
            raise BookingStatusError(f"Cannot cancel booking with status: {booking.status}")

        return BookingRepository.cancel(booking_id)

    @staticmethod
    def complete_booking(booking_id: int) -> Booking:
        """
        Mark booking as completed (approved bookings only).

        Args:
            booking_id: Booking ID to complete

        Returns:
            Completed Booking instance

        Raises:
            BookingStatusError: If booking is not approved
            ValueError: If booking not found
        """
        booking = BookingRepository.get_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found")

        if not booking.is_approved():
            raise BookingStatusError(
                f"Cannot complete booking with status: {booking.status}. Must be approved first."
            )

        return BookingRepository.complete(booking_id)

    @staticmethod
    def get_booking(booking_id: int) -> Optional[Booking]:
        """Get booking by ID."""
        return BookingRepository.get_by_id(booking_id)

    @staticmethod
    def get_user_bookings(user_id: int, status: Optional[str] = None) -> List[Booking]:
        """Get all bookings for a user."""
        return BookingRepository.get_by_requester(user_id, status=status)

    @staticmethod
    def get_resource_bookings(resource_id: int, status: Optional[str] = None) -> List[Booking]:
        """Get all bookings for a resource."""
        return BookingRepository.get_by_resource(resource_id, status=status)

    @staticmethod
    def get_pending_approvals(resource_id: Optional[int] = None) -> List[Booking]:
        """Get pending bookings awaiting approval."""
        return BookingRepository.get_pending_approvals(resource_id=resource_id)

    @staticmethod
    def get_upcoming_bookings(user_id: Optional[int] = None, limit: int = 10) -> List[Booking]:
        """Get upcoming approved bookings."""
        return BookingRepository.get_upcoming(requester_id=user_id, limit=limit)

    @staticmethod
    def get_booking_statistics() -> Dict[str, int]:
        """
        Get booking statistics.

        Returns:
            Dict with counts by status
        """
        return {
            "total": BookingRepository.count(),
            "pending": BookingRepository.count_by_status("pending"),
            "approved": BookingRepository.count_by_status("approved"),
            "rejected": BookingRepository.count_by_status("rejected"),
            "cancelled": BookingRepository.count_by_status("cancelled"),
            "completed": BookingRepository.count_by_status("completed"),
        }
