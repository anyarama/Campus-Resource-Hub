"""
Campus Resource Hub - AI Concierge Routes
AiDD 2025 Capstone Project - Phase 9

Natural language query interface for resource discovery.

AI Contribution: Cline generated route structure and CSRF protection
Reviewed and extended by developer on 2025-11-06
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user
from src.services.ai_concierge_service import AIConciergeService, AIConciergeError


# Create concierge blueprint
concierge_bp = Blueprint("concierge", __name__, url_prefix="/concierge")


@concierge_bp.route("/")
def index():
    """
    AI Concierge main interface.

    GET /concierge

    Shows a conversational search interface with example queries.

    Security: Public access (no login required)

    Returns:
        HTML: Concierge search interface
    """
    # Get example queries
    examples = AIConciergeService.get_example_queries()

    return render_template(
        "concierge/index.html", examples=examples, page_title="AI Resource Concierge"
    )


@concierge_bp.route("/query", methods=["POST"])
def query():
    """
    Process a natural language query.

    POST /concierge/query

    Request Body (JSON):
        {
            "query": "Find a study room for 4 people"
        }

    OR Form Data:
        query=Find+a+study+room+for+4+people

    Security:
        - CSRF protection (if using forms)
        - Input validation (max 500 chars)
        - Rate limiting (10 queries/min per user - future)

    Returns:
        JSON: Search results with conversational response
        {
            "success": bool,
            "message": str,
            "results": [...],
            "total_count": int,
            "params": {...}
        }
    """
    try:
        # Get query from JSON or form data
        if request.is_json:
            data = request.get_json()
            query_text = data.get("query", "").strip()
        else:
            query_text = request.form.get("query", "").strip()

        # Validate input
        if not query_text:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Please enter a search query.",
                        "error": "empty_query",
                    }
                ),
                400,
            )

        if len(query_text) > 500:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Query too long. Please keep it under 500 characters.",
                        "error": "query_too_long",
                    }
                ),
                400,
            )

        # Get user ID if logged in
        user_id = current_user.user_id if current_user.is_authenticated else None

        # Process query through AI service
        result = AIConciergeService.process_query(query_text, user_id=user_id)

        # Convert Resource objects to dictionaries for JSON response
        if result.get("results"):
            result["results"] = [
                {
                    "resource_id": r.resource_id,
                    "title": r.title,
                    "description": r.description[:150] + "..."
                    if len(r.description or "") > 150
                    else r.description,
                    "category": r.category,
                    "location": r.location,
                    "capacity": r.capacity,
                    "images": r.images,
                    "url": url_for("resources.detail", resource_id=r.resource_id, _external=False),
                }
                for r in result["results"]
            ]

        # Return JSON response
        status_code = 200 if result.get("success") else 404 if not result.get("error") else 500

        return jsonify(result), status_code

    except AIConciergeError as e:
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Concierge error: {str(e)}",
                    "error": "service_error",
                }
            ),
            500,
        )

    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"Concierge query error: {e}")

        return (
            jsonify(
                {
                    "success": False,
                    "message": "An unexpected error occurred. Please try again.",
                    "error": "server_error",
                }
            ),
            500,
        )


@concierge_bp.route("/examples")
def examples():
    """
    Get example queries for the UI.

    GET /concierge/examples

    Security: Public access

    Returns:
        JSON: List of example query strings
        {
            "examples": ["query1", "query2", ...]
        }
    """
    try:
        examples = AIConciergeService.get_example_queries()

        return jsonify({"success": True, "examples": examples}), 200

    except Exception as e:
        return (
            jsonify({"success": False, "message": "Could not load examples", "error": str(e)}),
            500,
        )


@concierge_bp.route("/help")
def help():
    """
    Show concierge help and documentation.

    GET /concierge/help

    Security: Public access

    Returns:
        HTML: Help page with query examples and tips
    """
    return render_template("concierge/help.html", page_title="Concierge Help")


# Error handlers for concierge routes
@concierge_bp.errorhandler(404)
def concierge_not_found(e):
    """Handle 404 errors in concierge blueprint."""
    if request.is_json or request.accept_mimetypes.accept_json:
        return (
            jsonify({"success": False, "message": "Endpoint not found", "error": "not_found"}),
            404,
        )

    flash("Page not found", "danger")
    return redirect(url_for("concierge.index"))


@concierge_bp.errorhandler(500)
def concierge_server_error(e):
    """Handle 500 errors in concierge blueprint."""
    if request.is_json or request.accept_mimetypes.accept_json:
        return (
            jsonify(
                {"success": False, "message": "Internal server error", "error": "server_error"}
            ),
            500,
        )

    flash("An error occurred. Please try again.", "danger")
    return redirect(url_for("concierge.index"))
