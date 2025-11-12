"""
Campus Resource Hub — UI Kit routes

Provides a locked-down visual gallery so designers/devs can verify
component states without affecting production traffic.
"""

from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import login_required

from src.security.rbac import require_admin

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/ui-kit")
@login_required
@require_admin
def ui_kit():
    """Render the design system gallery for visual QA."""

    button_variants = [
        {"label": "Primary", "class": "ui-button--primary"},
        {"label": "Secondary", "class": "ui-button--secondary"},
        {"label": "Ghost", "class": "ui-button--ghost"},
        {"label": "Destructive", "class": "ui-button--danger"},
        {"label": "Disabled", "class": "ui-button--primary", "disabled": True},
        {"label": "Loading", "class": "ui-button--primary", "loading": True},
    ]

    badge_variants = [
        {"label": "Default", "class": "badge"},
        {"label": "Info", "class": "badge badge--info"},
        {"label": "Success", "class": "badge badge--success"},
        {"label": "Warning", "class": "badge badge--warning"},
        {"label": "Danger", "class": "badge badge--danger"},
    ]

    alert_variants = [
        {"title": "Heads up", "body": "Use alerts for inline status messaging.", "class": "alert alert--info"},
        {"title": "Success", "body": "The booking workflow completed.", "class": "alert alert--success"},
        {"title": "Warning", "body": "Capacity is nearing the configured quota.", "class": "alert alert--warning"},
        {"title": "Error", "body": "We could not complete that action.", "class": "alert alert--danger"},
    ]

    form_examples = [
        {"label": "Default", "value": "Readable label and helper text", "state": "default"},
        {"label": "Success", "value": "Looks good!", "state": "success", "helper": "Checks passed"},
        {"label": "Error", "value": "Needs attention", "state": "error", "helper": "This field is required"},
        {"label": "Disabled", "value": "Field disabled", "state": "disabled"},
    ]

    table_rows = [
        {"resource": "Innovation Lab", "owner": "Clara Patel", "status": "Published", "inventory": "12 assets"},
        {"resource": "Studio B", "owner": "Diego Alvarez", "status": "Draft", "inventory": "3 assets"},
        {"resource": "AI Pod", "owner": "Sage Powell", "status": "Archived", "inventory": "6 assets"},
    ]

    return render_template(
        "ui/ui_kit.html",
        button_variants=button_variants,
        badge_variants=badge_variants,
        alert_variants=alert_variants,
        form_examples=form_examples,
        table_rows=table_rows,
    )
