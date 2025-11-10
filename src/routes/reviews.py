"""
Campus Resource Hub - Reviews Routes (Phase 6)
AiDD 2025 Capstone Project

Flask blueprint for review management: create, view, edit, delete, moderate.
Users can only review resources after completing a booking.

AI Contribution: Cline generated review route structure
Reviewed by developer on 2025-11-05
"""

from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from src.repositories.review_repo import ReviewRepository
from src.repositories.booking_repo import BookingRepository
from src.repositories.resource_repo import ResourceRepository
from src.security.rbac import require_admin


# Create reviews blueprint
reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/resources/<int:resource_id>/reviews", methods=["POST"])
@login_required
def create(resource_id):
    """
    Submit a review for a resource.

    Authorization: User must have a completed booking for this resource.
    Constraint: One review per user per resource.

    POST data:
        rating: Integer 1-5 (required)
        comment: Text feedback (optional)
        booking_id: Associated booking ID (optional but recommended)
    """
    # Check resource exists
    resource = ResourceRepository.get_by_id(resource_id)
    if not resource:
        flash("Resource not found", "error")
        return redirect(url_for("resources.index"))

    # Get form data
    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment", "").strip()
    booking_id = request.form.get("booking_id", type=int)

    # Validate rating
    if not rating or rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5 stars", "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    # Authorization: Check user has completed booking for this resource
    completed_bookings = BookingRepository.get_by_requester(current_user.user_id)
    has_completed_booking = any(
        b.resource_id == resource_id and b.status == "completed" for b in completed_bookings
    )

    if not has_completed_booking:
        flash("You can only review resources after completing a booking", "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    # Check if user already reviewed this resource
    existing_review = ReviewRepository.get_by_resource_and_reviewer(
        resource_id=resource_id, reviewer_id=current_user.user_id
    )

    if existing_review:
        flash(
            "You have already reviewed this resource. Edit your existing review instead.", "warning"
        )
        return redirect(url_for("resources.detail", resource_id=resource_id))

    # Create review
    try:
        ReviewRepository.create(
            resource_id=resource_id,
            reviewer_id=current_user.user_id,
            booking_id=booking_id,
            rating=rating,
            comment=comment if comment else None,
        )

        flash("Thank you for your review!", "success")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    except Exception as e:
        flash(f"Failed to submit review: {e}", "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))


@reviews_bp.route("/reviews/<int:review_id>", methods=["PUT", "PATCH"])
@login_required
def update(review_id):
    """
    Update an existing review (owner only).

    PUT/PATCH data:
        rating: Integer 1-5 (optional)
        comment: Text feedback (optional)
    """
    review = ReviewRepository.get_by_id(review_id)

    if not review:
        flash("Review not found", "error")
        return redirect(url_for("resources.index"))

    # Authorization: only review owner can edit
    if review.reviewer_id != current_user.user_id:
        flash("You can only edit your own reviews", "error")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))

    # Get update data
    rating = request.form.get("rating", type=int)
    comment = request.form.get("comment")

    updates = {}
    if rating and 1 <= rating <= 5:
        updates["rating"] = rating
    if comment is not None:  # Allow empty string to clear comment
        updates["comment"] = comment.strip() if comment.strip() else None

    if not updates:
        flash("No changes provided", "warning")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))

    try:
        review = ReviewRepository.update(review_id, **updates)
        flash("Review updated successfully", "success")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))

    except Exception as e:
        flash(f"Failed to update review: {e}", "error")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))


@reviews_bp.route("/reviews/<int:review_id>/delete", methods=["POST", "DELETE"])
@login_required
def delete(review_id):
    """
    Delete a review (owner only).

    Note: This is a hard delete. Consider soft delete in production.
    """
    review = ReviewRepository.get_by_id(review_id)

    if not review:
        flash("Review not found", "error")
        return redirect(url_for("resources.index"))

    # Authorization: only review owner can delete
    if review.reviewer_id != current_user.user_id:
        flash("You can only delete your own reviews", "error")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))

    resource_id = review.resource_id

    try:
        ReviewRepository.delete(review_id)
        flash("Review deleted", "info")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    except Exception as e:
        flash(f"Failed to delete review: {e}", "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))


@reviews_bp.route("/reviews/<int:review_id>/hide", methods=["POST"])
@login_required
@require_admin
def hide(review_id):
    """
    Hide a review (admin moderation).

    Hidden reviews are not shown to public but remain in database.

    POST data:
        reason: Reason for hiding (optional)
    """
    review = ReviewRepository.get_by_id(review_id)

    if not review:
        flash("Review not found", "error")
        return redirect(url_for("resources.index"))

    if review.is_hidden:
        flash("Review is already hidden", "warning")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))

    reason = request.form.get("reason", "").strip()

    try:
        review = ReviewRepository.hide(
            review_id=review_id, admin_id=current_user.user_id, reason=reason if reason else None
        )

        flash("Review hidden successfully", "success")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))

    except Exception as e:
        flash(f"Failed to hide review: {e}", "error")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))


@reviews_bp.route("/reviews/<int:review_id>/unhide", methods=["POST"])
@login_required
@require_admin
def unhide(review_id):
    """
    Unhide a previously hidden review (admin moderation).
    """
    review = ReviewRepository.get_by_id(review_id)

    if not review:
        flash("Review not found", "error")
        return redirect(url_for("resources.index"))

    if not review.is_hidden:
        flash("Review is not hidden", "warning")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))

    try:
        review = ReviewRepository.unhide(review_id)
        flash("Review unhidden successfully", "success")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))

    except Exception as e:
        flash(f"Failed to unhide review: {e}", "error")
        return redirect(url_for("resources.detail", resource_id=review.resource_id))


@reviews_bp.route("/resources/<int:resource_id>/reviews")
def list_reviews(resource_id):
    """
    List all visible reviews for a resource (public route).

    Returns JSON for AJAX or renders template.
    """
    resource = ResourceRepository.get_by_id(resource_id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    # Get visible reviews (not hidden)
    reviews = ReviewRepository.get_by_resource(resource_id, include_hidden=False)

    # Calculate aggregate rating
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        review_count = len(reviews)
    else:
        avg_rating = None
        review_count = 0

    # If JSON request, return JSON
    if request.accept_mimetypes.best == "application/json":
        return jsonify(
            {
                "resource_id": resource_id,
                "average_rating": round(avg_rating, 1) if avg_rating else None,
                "review_count": review_count,
                "reviews": [
                    {
                        "review_id": r.review_id,
                        "reviewer_name": r.reviewer.name,
                        "rating": r.rating,
                        "comment": r.comment,
                        "timestamp": r.timestamp.isoformat() if r.timestamp else None,
                    }
                    for r in reviews
                ],
            }
        )

    # Otherwise render template (or return to resource detail)
    return redirect(url_for("resources.detail", resource_id=resource_id))


@reviews_bp.route("/resources/<int:resource_id>/rating")
def get_rating(resource_id):
    """
    Get aggregate rating for a resource (API endpoint).

    Returns JSON with average rating and count.
    """
    reviews = ReviewRepository.get_by_resource(resource_id, include_hidden=False)

    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        review_count = len(reviews)
    else:
        avg_rating = None
        review_count = 0

    return jsonify(
        {
            "resource_id": resource_id,
            "average_rating": round(avg_rating, 1) if avg_rating else None,
            "review_count": review_count,
            "top_rated": avg_rating >= 4.5 if avg_rating else False,
        }
    )
