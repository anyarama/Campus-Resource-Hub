"""
Campus Resource Hub - Resources Routes (Phase 5: Full CRUD)
AiDD 2025 Capstone Project

Flask blueprint for complete resource management with image uploads.
Implements create, read, update, delete operations.

AI Contribution: Cline generated CRUD route structure
Reviewed by developer on 2025-11-05
"""

import json
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from src.security.rbac import require_admin
from src.services.resource_service import ResourceService, ResourceServiceError
from src.repositories.resource_repo import ResourceRepository


# Create resources blueprint
resources_bp = Blueprint("resources", __name__)


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
    return jsonify({
        "message": "Admin access confirmed",
        "user": current_user.name,
        "role": current_user.role,
    }), 200


# ============================================================================
# Resource CRUD Routes (Phase 5)
# ============================================================================


@resources_bp.route("/resources")
def index():
    """
    List all published resources (public route).

    Filters: category, location, search query
    Pagination: 20 items per page
    """
    # Get query parameters
    category = request.args.get("category")
    location = request.args.get("location")
    search_term = request.args.get("q")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Fetch resources (published only for public view)
    resources = ResourceRepository.search(
        query_str=search_term,
        category=category,
        location=location,
        status="published"
    )

    # Simple pagination (in-memory for now)
    total = len(resources)
    start = (page - 1) * per_page
    end = start + per_page
    resources_page = resources[start:end]

    return render_template(
        "resources/list.html",
        resources=resources_page,
        category=category,
        location=location,
        search_term=search_term,
        page=page,
        total=total,
        per_page=per_page
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

    # Parse images from JSON
    images = []
    if resource.images:
        try:
            images = json.loads(resource.images)
        except:
            images = []

    # Parse availability rules
    availability = {}
    if resource.availability_rules:
        try:
            availability = json.loads(resource.availability_rules)
        except:
            availability = {}

    return render_template(
        "resources/detail.html",
        resource=resource,
        images=images,
        availability=availability
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
        return render_template("resources/create.html")

    # Process POST request
    try:
        # Get form data
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category")
        location = request.form.get("location", "").strip()
        capacity = request.form.get("capacity", type=int)
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
            capacity=capacity,
            images=images if images else None,
            status=status
        )

        flash(f"Resource '{resource.title}' created successfully!", "success")
        return redirect(url_for("resources.detail", resource_id=resource.resource_id))

    except ResourceServiceError as e:
        flash(str(e), "error")
        return redirect(url_for("resources.create"))


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
        # Parse images for display
        images = []
        if resource.images:
            try:
                images = json.loads(resource.images)
            except:
                images = []

        return render_template("resources/edit.html", resource=resource, images=images)

    # Process POST request
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
            updates["capacity"] = int(request.form["capacity"])
        if "status" in request.form:
            updates["status"] = request.form["status"]

        # Handle image uploads
        images = request.files.getlist("images")
        if images and any(img.filename for img in images):
            updates["images"] = images

        # Update resource
        resource = ResourceService.update_resource(
            resource_id=resource_id,
            user_id=current_user.user_id,
            **updates
        )

        flash(f"Resource '{resource.title}' updated successfully!", "success")
        return redirect(url_for("resources.detail", resource_id=resource_id))

    except ResourceServiceError as e:
        flash(str(e), "error")
        return redirect(url_for("resources.edit", resource_id=resource_id))


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
