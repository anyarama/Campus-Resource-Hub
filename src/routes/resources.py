"""
Campus Resource Hub - Resources Routes (Phase 5: Full CRUD)
AiDD 2025 Capstone Project

Flask blueprint for complete resource management with image uploads.
Implements create, read, update, delete operations.

AI Contribution: Cline generated CRUD route structure
Reviewed by developer on 2025-11-05
"""

from datetime import datetime, date, time, timedelta
from typing import Optional
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.datastructures import ImmutableMultiDict

from src.security.rbac import require_admin
from src.services.resource_service import ResourceService, ResourceServiceError
from src.repositories.resource_repo import ResourceRepository
from src.repositories.review_repo import ReviewRepository
from src.repositories.booking_repo import BookingRepository


# Create resources blueprint
resources_bp = Blueprint("resources", __name__)


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _parse_date(value: str) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _date_range_to_datetimes(start_date: Optional[date], end_date: Optional[date]) -> tuple[Optional[datetime], Optional[datetime]]:
    """
    Convert inclusive start/end dates into datetime boundaries covering full days.
    """
    if not start_date and not end_date:
        return None, None

    start = start_date or end_date
    end = end_date or start_date

    if not start or not end:
        return None, None

    if end < start:
        start, end = end, start

    start_dt = datetime.combine(start, time.min)
    end_dt = datetime.combine(end, time.max)
    return start_dt, end_dt


def _build_availability_calendar(resource_id: int, days: int = 14) -> list[dict[str, object]]:
    """
    Build a lightweight availability calendar for the right rail.

    Marks the next N days as 'booked' if an approved booking overlaps that date.
    """
    today = date.today()
    approved_bookings = BookingRepository.get_by_resource(resource_id, status="approved")
    calendar = []

    for offset in range(days):
        day = today + timedelta(days=offset)
        is_booked = any(
            booking.start_datetime.date() <= day <= booking.end_datetime.date()
            for booking in approved_bookings
        )
        calendar.append(
            {
                "date": day,
                "status": "booked" if is_booked else "available",
            }
        )

    return calendar


def _extract_availability_rules(form: ImmutableMultiDict) -> dict:
    """
    Normalize availability/rules inputs from the multi-step form.
    """
    days = [day for day in form.getlist("availability_days") if day]
    start_time = form.get("availability_start")
    end_time = form.get("availability_end")
    notes = form.get("availability_notes")
    requires_approval = form.get("requires_approval") == "on"

    rules: dict[str, object] = {}

    if days:
        rules["days"] = days

    if start_time or end_time:
        rules["hours"] = {"start": start_time or None, "end": end_time or None}

    if notes:
        rules["notes"] = notes.strip()

    if requires_approval:
        rules["requires_approval"] = True

    return rules


def _capture_form_state(form: ImmutableMultiDict) -> dict:
    """
    Convert ImmutableMultiDict into a dict that preserves multi-value fields.
    """
    state: dict[str, object] = {}
    for key in form.keys():
        values = form.getlist(key)
        if len(values) == 1:
            state[key] = values[0]
        else:
            state[key] = values
    return state


@resources_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Protected dashboard route.

    Requires authentication. Accessible by all authenticated users.
    """
    return render_template("resources/dashboard.html", user=current_user)


@resources_bp.route("/admin/ping")
@login_required
@require_admin
def admin_ping():
    """
    Admin-only test route (smoke test for RBAC).

    Requires authentication AND admin role.
    """
    return (
        jsonify(
            {
                "message": "Admin access confirmed",
                "user": current_user.name,
                "role": current_user.role,
            }
        ),
        200,
    )


# ============================================================================
# Resource CRUD Routes (Phase 5)
# ============================================================================


CATEGORY_FILTERS = [
    {"value": "study_room", "label": "Study Room"},
    {"value": "equipment", "label": "Equipment"},
    {"value": "lab", "label": "Lab / Workshop"},
    {"value": "space", "label": "Event Space"},
    {"value": "tutoring", "label": "Tutoring / Mentoring"},
]

STATUS_FILTERS = [
    {"value": "published", "label": "Published"},
    {"value": "draft", "label": "Draft"},
    {"value": "archived", "label": "Archived"},
]


@resources_bp.route("/resources")
def index():
    """
    List all published resources (public route).

    Filters: category, location, search query
    Pagination: 20 items per page
    """
    # Get query parameters
    search_term = request.args.get("q")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Multi-select filters fall back to legacy single-value params for backward compatibility
    selected_categories = request.args.getlist("category")
    if not selected_categories and request.args.get("category"):
        selected_categories = [request.args.get("category")]  # type: ignore[list-item]

    selected_locations = request.args.getlist("location")
    if not selected_locations and request.args.get("location"):
        selected_locations = [request.args.get("location")]  # type: ignore[list-item]

    allow_status_filter = current_user.is_authenticated and current_user.role in ["staff", "admin"]
    selected_statuses = request.args.getlist("status") if allow_status_filter else []
    if not selected_statuses:
        selected_statuses = ["published"]

    capacity_min = request.args.get("capacity_min", type=int)
    capacity_max = request.args.get("capacity_max", type=int)

    date_from_raw = request.args.get("date_from")
    date_to_raw = request.args.get("date_to")
    date_from = _parse_date(date_from_raw) if date_from_raw else None
    date_to = _parse_date(date_to_raw) if date_to_raw else None
    availability_start, availability_end = _date_range_to_datetimes(date_from, date_to)

    sort = request.args.get("sort", "created_desc")

    resources = ResourceRepository.search(
        query_str=search_term,
        status="published",
        categories=selected_categories or None,
        locations=selected_locations or None,
        statuses=selected_statuses or None,
        capacity_min=capacity_min,
        capacity_max=capacity_max,
        availability_start=availability_start,
        availability_end=availability_end,
        sort=sort,
    )

    # Simple pagination (in-memory for now)
    total = len(resources)
    start = (page - 1) * per_page
    end = start + per_page
    resources_page = resources[start:end]

    return render_template(
        "resources/list.html",
        resources=resources_page,
        search_term=search_term,
        page=page,
        total=total,
        per_page=per_page,
        category_filters=CATEGORY_FILTERS,
        status_filters=STATUS_FILTERS,
        location_facets=ResourceRepository.get_location_facets(),
        filter_state={
            "categories": selected_categories,
            "locations": selected_locations,
            "statuses": selected_statuses,
            "capacity_min": capacity_min,
            "capacity_max": capacity_max,
            "date_from": date_from_raw,
            "date_to": date_to_raw,
            "sort": sort,
        },
    )


@resources_bp.route("/resources/<int:resource_id>")
def detail(resource_id):
    """
    Resource detail page (public for published resources).

    Shows full resource information, images, availability, and reviews.
    """
    resource = ResourceRepository.get_by_id(resource_id)

    if not resource:
        flash("Resource not found", "error")
        return redirect(url_for("resources.index"))

    images = resource.get_images()
    availability_rules = resource.get_availability_rules()

    include_hidden_reviews = current_user.is_authenticated and current_user.role == "admin"
    reviews = ReviewRepository.get_by_resource(resource_id, include_hidden=include_hidden_reviews)
    visible_reviews = [r for r in reviews if not r.is_hidden]
    avg_rating = (
        round(sum(r.rating for r in visible_reviews) / len(visible_reviews), 1)
        if visible_reviews
        else None
    )
    review_count = len(visible_reviews)

    user_review = None
    can_review = False
    if current_user.is_authenticated:
        user_review = ReviewRepository.get_by_resource_and_reviewer(
            resource_id=resource_id, reviewer_id=current_user.user_id
        )
        completed_bookings = BookingRepository.get_by_requester(current_user.user_id)
        can_review = any(
            booking.resource_id == resource_id and booking.status == "completed"
            for booking in completed_bookings
        )

    availability_calendar = _build_availability_calendar(resource_id)
    next_available = next(
        (day["date"] for day in availability_calendar if day["status"] == "available"), None
    )

    return render_template(
        "resources/detail.html",
        resource=resource,
        images=images,
        availability=availability_rules,
        reviews=reviews,
        review_count=review_count,
        average_rating=avg_rating,
        user_review=user_review,
        can_review=can_review and user_review is None,
        show_moderation=include_hidden_reviews,
        availability_calendar=availability_calendar,
        next_available_date=next_available,
        category_filters=CATEGORY_FILTERS,
    )


@resources_bp.route("/resources/<int:resource_id>/availability")
def availability(resource_id):
    """
    Return booking availability for a given resource and day.
    """
    resource = ResourceRepository.get_by_id(resource_id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    # Only expose unpublished resources to owners/admin/staff
    if not resource.is_published():
        allowed = False
        if current_user.is_authenticated:
            if current_user.user_id == resource.owner_id or current_user.role in ["admin", "staff"]:
                allowed = True
        if not allowed:
            return jsonify({"error": "Resource unavailable"}), 403

    date_param = request.args.get("date")
    day = _parse_date(date_param) if date_param else date.today()
    if not day:
        return jsonify({"error": "Invalid date"}), 400

    bookings = BookingRepository.get_for_day(resource_id, day, statuses=["approved"])
    availability_rules = resource.get_availability_rules()

    return jsonify(
        {
            "resource_id": resource_id,
            "date": day.isoformat(),
            "requires_approval": availability_rules.get("requires_approval", False)
            if availability_rules
            else False,
            "bookings": [
                {
                    "booking_id": booking.booking_id,
                    "start": booking.start_datetime.isoformat(),
                    "end": booking.end_datetime.isoformat(),
                    "status": booking.status,
                }
                for booking in bookings
            ],
        }
    )


@resources_bp.route("/resources/create", methods=["GET", "POST"])
@login_required
def create():
    """
    Create new resource form.

    GET: Display creation form
    POST: Process form submission with image uploads
    """
    if request.method == "GET":
        return render_template(
            "resources/create.html",
            category_filters=CATEGORY_FILTERS,
            form_data={},
            form_errors={},
            images=[],
            resource=None,
        )

    # Process POST request
    form_state = _capture_form_state(request.form)
    availability_rules = _extract_availability_rules(request.form)
    capacity_raw = request.form.get("capacity", "").strip()
    capacity_value: Optional[int] = None
    if capacity_raw:
        try:
            capacity_value = int(capacity_raw)
        except ValueError:
            capacity_value = None

    try:
        # Get form data
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category")
        location = request.form.get("location", "").strip()
        status = request.form.get("status", "draft")

        # Get uploaded images (multiple files)
        images = request.files.getlist("images")

        # Create resource using service layer
        resource = ResourceService.create_resource(
            owner_id=current_user.user_id,
            title=title,
            description=description,
            category=category,
            location=location,
            capacity=capacity_value,
            images=images if images else None,
            availability_rules=availability_rules or None,
            status=status,
        )

        flash(f"Resource '{resource.title}' created successfully!", "success")
        return redirect(url_for("resources.detail", resource_id=resource.resource_id))

    except ResourceServiceError as e:
        flash(str(e), "error")
        return (
            render_template(
                "resources/create.html",
                category_filters=CATEGORY_FILTERS,
                form_data=form_state,
                form_errors={"__all__": str(e)},
                images=[],
                resource=None,
            ),
            400,
        )


@resources_bp.route("/resources/<int:resource_id>/edit", methods=["GET", "POST"])
@login_required
def edit(resource_id):
    """
    Edit existing resource (owner-only).

    GET: Display edit form with current values
    POST: Process updates
    """
    resource = ResourceRepository.get_by_id(resource_id)

    if not resource:
        flash("Resource not found", "error")
        return redirect(url_for("resources.index"))

    # Authorization: only owner can edit
    if resource.owner_id != current_user.user_id:
        flash("You can only edit your own resources", "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    if request.method == "GET":
        images = resource.get_images()
        availability_rules = resource.get_availability_rules()
        hours_config = availability_rules.get("hours") or {}
        default_form_state = {
            "title": resource.title,
            "description": resource.description or "",
            "category": resource.category,
            "location": resource.location or "",
            "capacity": str(resource.capacity or ""),
            "status": resource.status,
            "availability_days": availability_rules.get("days", []),
            "availability_start": hours_config.get("start", ""),
            "availability_end": hours_config.get("end", ""),
            "availability_notes": availability_rules.get("notes", ""),
            "requires_approval": availability_rules.get("requires_approval"),
        }

        return render_template(
            "resources/edit.html",
            resource=resource,
            images=images,
            category_filters=CATEGORY_FILTERS,
            form_data=default_form_state,
            form_errors={},
        )

    # Process POST request
    form_state = _capture_form_state(request.form)
    availability_rules = _extract_availability_rules(request.form)

    try:
        # Get form data (only update provided fields)
        updates = {}
        if "title" in request.form:
            updates["title"] = request.form["title"].strip()
        if "description" in request.form:
            updates["description"] = request.form["description"].strip()
        if "category" in request.form:
            updates["category"] = request.form["category"]
        if "location" in request.form:
            updates["location"] = request.form["location"].strip()
        if "capacity" in request.form:
            capacity_raw = request.form["capacity"].strip()
            if capacity_raw:
                updates["capacity"] = int(capacity_raw)
            else:
                updates["capacity"] = None
        if "status" in request.form:
            updates["status"] = request.form["status"]
        if availability_rules:
            updates["availability_rules"] = availability_rules

        # Handle image uploads
        images = request.files.getlist("images")
        if images and any(img.filename for img in images):
            updates["images"] = images

        # Update resource
        resource = ResourceService.update_resource(
            resource_id=resource_id, user_id=current_user.user_id, **updates
        )

        flash(f"Resource '{resource.title}' updated successfully!", "success")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    except (ResourceServiceError, ValueError) as e:
        flash(str(e), "error")
        return (
            render_template(
                "resources/edit.html",
                resource=resource,
                images=resource.get_images(),
                category_filters=CATEGORY_FILTERS,
                form_data=form_state,
                form_errors={"__all__": str(e)},
            ),
            400,
        )


@resources_bp.route("/resources/<int:resource_id>/delete", methods=["POST"])
@login_required
def delete(resource_id):
    """
    Delete resource (owner-only).

    POST-only route for CSRF protection.
    """
    try:
        ResourceService.delete_resource(resource_id, current_user.user_id)
        flash("Resource deleted successfully", "success")
        return redirect(url_for("resources.my_resources"))

    except ResourceServiceError as e:
        flash(str(e), "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))


@resources_bp.route("/resources/<int:resource_id>/publish", methods=["POST"])
@login_required
def publish(resource_id):
    """
    Publish a draft resource (owner-only).
    """
    try:
        resource = ResourceService.publish_resource(resource_id, current_user.user_id)
        flash(f"Resource '{resource.title}' published successfully!", "success")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    except ResourceServiceError as e:
        flash(str(e), "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))


@resources_bp.route("/resources/<int:resource_id>/archive", methods=["POST"])
@login_required
def archive(resource_id):
    """
    Archive a published resource (owner-only).
    """
    try:
        resource = ResourceService.archive_resource(resource_id, current_user.user_id)
        flash(f"Resource '{resource.title}' archived", "info")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    except ResourceServiceError as e:
        flash(str(e), "error")
        return redirect(url_for("resources.detail", resource_id=resource_id))


@resources_bp.route("/my-resources")
@login_required
def my_resources():
    """
    List current user's resources (all statuses).

    Shows draft, published, and archived resources.
    """
    resources = ResourceRepository.get_by_owner(current_user.user_id)

    return render_template("resources/my_resources.html", resources=resources)
