"""
Campus Resource Hub - Bookings Routes (Phase 6)
AiDD 2025 Capstone Project

Flask blueprint for booking management: create, view, approve, reject, cancel.
Implements conflict detection and approval workflows.

AI Contribution: Cline generated booking route structure
Reviewed by developer on 2025-11-05
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from src.repositories.booking_repo import BookingRepository
from src.repositories.resource_repo import ResourceRepository
from src.services.booking_service import BookingService
from src.security.rbac import require_staff


# Create bookings blueprint
bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")


@bookings_bp.route("/new")
@login_required
def new():
    """
    Display booking creation form.

    Query params:
        resource_id: ID of resource to book (required)
    """
    resource_id = request.args.get("resource_id", type=int)

    if not resource_id:
        flash("Resource ID is required to create a booking", "error")
        return redirect(url_for("resources.index"))

    resource = ResourceRepository.get_by_id(resource_id)

    if not resource:
        flash("Resource not found", "error")
        return redirect(url_for("resources.index"))

    if resource.status != "published":
        flash("This resource is not available for booking", "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    return render_template("bookings/new.html", resource=resource)


@bookings_bp.route("", methods=["POST"])
@login_required
def create():
    """
    Create a new booking with conflict detection.

    POST data:
        resource_id: ID of resource
        start_date: Date (YYYY-MM-DD)
        start_time: Time (HH:MM)
        end_date: Date (YYYY-MM-DD)
        end_time: Time (HH:MM)
        notes: Optional booking notes
    """
    try:
        # Get form data
        resource_id = request.form.get("resource_id", type=int)
        start_date = request.form.get("start_date")
        start_time = request.form.get("start_time")
        end_date = request.form.get("end_date")
        end_time = request.form.get("end_time")
        # Validate resource exists
        resource = ResourceRepository.get_by_id(resource_id)
        if not resource:
            flash("Resource not found", "error")
            return redirect(url_for("resources.index"))

        # Parse datetimes
        start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")

        # Validation: end must be after start
        if end_datetime <= start_datetime:
            flash("End time must be after start time", "error")
            return redirect(url_for("bookings.new", resource_id=resource_id))

        # Validation: can't book in the past
        if start_datetime < datetime.now():
            flash("Cannot book resources in the past", "error")
            return redirect(url_for("bookings.new", resource_id=resource_id))

        # Check for booking conflicts
        conflicts = BookingService.check_booking_conflicts(
            resource_id=resource_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            exclude_booking_id=None,
        )

        if conflicts:
            flash(f"Time slot unavailable - {len(conflicts)} conflicting booking(s) found", "error")
            return redirect(url_for("bookings.new", resource_id=resource_id))

        # Determine initial status (auto-approve for now, can add approval logic later)
        # Future: Check resource.requires_approval flag
        initial_status = "approved"

        # Create booking
        booking = BookingRepository.create(
            resource_id=resource_id,
            requester_id=current_user.user_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            status=initial_status,
        )

        if initial_status == "approved":
            flash(f"Booking confirmed for {resource.title}!", "success")
        else:
            flash(f"Booking request submitted for {resource.title}. Awaiting approval.", "info")

        return redirect(url_for("bookings.detail", booking_id=booking.booking_id))

    except ValueError as e:
        flash(f"Invalid date/time format: {e}", "error")
        return redirect(url_for("bookings.new", resource_id=resource_id))
    except Exception as e:
        flash(f"Booking creation failed: {e}", "error")
        return redirect(url_for("bookings.new", resource_id=resource_id))


@bookings_bp.route("/<int:booking_id>")
@login_required
def detail(booking_id):
    """
    View booking details.

    Accessible by:
    - Booking requester
    - Resource owner
    - Staff/Admin
    """
    booking = BookingRepository.get_by_id(booking_id)

    if not booking:
        flash("Booking not found", "error")
        return redirect(url_for("bookings.my_bookings"))

    # Authorization check
    is_requester = booking.requester_id == current_user.user_id
    is_resource_owner = booking.resource.owner_id == current_user.user_id
    is_staff_or_admin = current_user.role in ["staff", "admin"]

    if not (is_requester or is_resource_owner or is_staff_or_admin):
        flash("You don't have permission to view this booking", "error")
        return redirect(url_for("bookings.my_bookings"))

    return render_template(
        "bookings/detail.html",
        booking=booking,
        resource=booking.resource,
        requester=booking.requester,
        resource_owner=booking.resource.owner,
    )


@bookings_bp.route("/<int:booking_id>/approve", methods=["POST"])
@login_required
@require_staff
def approve(booking_id):
    """
    Approve a pending booking (staff/admin only).
    """
    booking = BookingRepository.get_by_id(booking_id)

    if not booking:
        flash("Booking not found", "error")
        return redirect(url_for("bookings.my_bookings"))

    if booking.status != "pending":
        flash(f"Cannot approve booking with status: {booking.status}", "error")
        return redirect(url_for("bookings.detail", booking_id=booking_id))

    # Check for conflicts again (in case new bookings were made)
    conflicts = BookingService.check_booking_conflicts(
        resource_id=booking.resource_id,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime,
        exclude_booking_id=booking_id,
    )

    if conflicts:
        flash(f"Cannot approve - {len(conflicts)} conflicting booking(s) exist", "error")
        return redirect(url_for("bookings.detail", booking_id=booking_id))

    # Approve booking
    booking = BookingRepository.update_status(booking_id, "approved")

    flash("Booking approved successfully", "success")
    return redirect(url_for("bookings.detail", booking_id=booking_id))


@bookings_bp.route("/<int:booking_id>/reject", methods=["POST"])
@login_required
@require_staff
def reject(booking_id):
    """
    Reject a pending booking (staff/admin only).
    """
    booking = BookingRepository.get_by_id(booking_id)

    if not booking:
        flash("Booking not found", "error")
        return redirect(url_for("bookings.my_bookings"))

    if booking.status != "pending":
        flash(f"Cannot reject booking with status: {booking.status}", "error")
        return redirect(url_for("bookings.detail", booking_id=booking_id))

    # Reject booking
    booking = BookingRepository.update_status(booking_id, "rejected")

    flash("Booking rejected", "info")
    return redirect(url_for("bookings.detail", booking_id=booking_id))


@bookings_bp.route("/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel(booking_id):
    """
    Cancel a booking (requester or admin).
    """
    booking = BookingRepository.get_by_id(booking_id)

    if not booking:
        flash("Booking not found", "error")
        return redirect(url_for("bookings.my_bookings"))

    # Authorization: requester or admin can cancel
    if booking.requester_id != current_user.user_id and current_user.role != "admin":
        flash("You can only cancel your own bookings", "error")
        return redirect(url_for("bookings.detail", booking_id=booking_id))

    # Can only cancel pending or approved bookings
    if booking.status not in ["pending", "approved"]:
        flash(f"Cannot cancel booking with status: {booking.status}", "error")
        return redirect(url_for("bookings.detail", booking_id=booking_id))

    # Cancel booking
    booking = BookingRepository.update_status(booking_id, "cancelled")

    flash("Booking cancelled", "info")
    return redirect(url_for("bookings.my_bookings"))


@bookings_bp.route("/<int:booking_id>/complete", methods=["POST"])
@login_required
def complete(booking_id):
    """
    Mark booking as completed (admin or system).

    This enables review submission for the booking.
    """
    booking = BookingRepository.get_by_id(booking_id)

    if not booking:
        flash("Booking not found", "error")
        return redirect(url_for("bookings.my_bookings"))

    # Only admin can manually complete bookings
    if current_user.role != "admin":
        flash("Only admins can complete bookings", "error")
        return redirect(url_for("bookings.detail", booking_id=booking_id))

    # Can only complete approved bookings
    if booking.status != "approved":
        flash(f"Cannot complete booking with status: {booking.status}", "error")
        return redirect(url_for("bookings.detail", booking_id=booking_id))

    # Complete booking
    booking = BookingRepository.update_status(booking_id, "completed")

    flash("Booking marked as completed", "success")
    return redirect(url_for("bookings.detail", booking_id=booking_id))


@bookings_bp.route("/my-bookings")
@login_required
def my_bookings():
    """
    User's booking dashboard showing all their bookings.

    Tabs: Upcoming, Past, Cancelled
    """
    # Get all user's bookings
    user_bookings = BookingRepository.get_by_requester(current_user.user_id)

    # Categorize bookings
    now = datetime.now()
    upcoming = []
    past = []
    cancelled = []

    for booking in user_bookings:
        if booking.status == "cancelled":
            cancelled.append(booking)
        elif booking.end_datetime < now:
            past.append(booking)
        else:
            upcoming.append(booking)

    # Sort by date
    upcoming.sort(key=lambda b: b.start_datetime)
    past.sort(key=lambda b: b.start_datetime, reverse=True)
    cancelled.sort(key=lambda b: b.created_at, reverse=True)

    return render_template(
        "bookings/my_bookings.html", upcoming=upcoming, past=past, cancelled=cancelled
    )
