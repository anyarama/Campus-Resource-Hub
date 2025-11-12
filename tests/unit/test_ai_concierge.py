"""
Unit tests for the AI Concierge service.

Validates natural-language parsing and resource search grounding.
"""

import pytest

from src.app import db
from src.models import Resource, User
from src.services.ai_concierge_service import AIConciergeService, QueryParser


@pytest.fixture(scope="function")
def concierge_fixtures(app):
    """Seed a small catalog for concierge searches."""
    with app.app_context():
        user = User(
            name="Concierge Owner",
            email="concierge-owner@example.com",
            password="TestPassword123!",
            role="staff",
        )
        db.session.add(user)
        db.session.commit()

        published_room = Resource(
            owner_id=user.user_id,
            title="Quiet Study Room – Library",
            description="Acoustic dampening, whiteboard, HDMI display.",
            category="Study Room",
            location="Hodge Hall",
            capacity=6,
            status="published",
        )
        unpublished_room = Resource(
            owner_id=user.user_id,
            title="Draft Conference Room",
            description="Not visible to students.",
            category="Conference Room",
            location="Hodge Hall",
            capacity=20,
            status="draft",
        )
        projector = Resource(
            owner_id=user.user_id,
            title="4K Projector Kit",
            description="Includes HDMI adapters and rolling stand.",
            category="Equipment",
            location="Tech Checkout Desk",
            capacity=None,
            status="published",
        )

        db.session.add_all([published_room, unpublished_room, projector])
        db.session.commit()

        yield {
            "owner": user,
            "published_room": published_room,
            "projector": projector,
        }


class TestQueryParser:
    """Ensure the rule-based parser extracts expected parameters."""

    def test_extracts_category_capacity_and_time(self):
        params = QueryParser.parse_query(
            "Find a study room for 4 people in Hodge Hall tomorrow afternoon"
        )
        assert params["category"] == "Study Room"
        assert params["capacity"] == 4
        assert params["date"] == "tomorrow"
        assert params["time"] == "afternoon"
        assert params["location"] == "Hodge Hall"
        assert params["intent"] == "search"


class TestAIConciergeService:
    """Exercise the concierge service end-to-end."""

    def test_returns_matching_resources(self, app, concierge_fixtures):
        with app.app_context():
            result = AIConciergeService.process_query(
                "Find a study room for 4 people tomorrow afternoon"
            )
            assert result["success"] is True
            assert result["total_count"] == 1
            first_result = result["results"][0]
            assert first_result.title == concierge_fixtures["published_room"].title
            # Ensure unpublished resources were filtered out
            assert all(resource.status == "published" for resource in result["results"])

    def test_no_results_response_includes_suggestions(self, app, concierge_fixtures):
        with app.app_context():
            result = AIConciergeService.process_query("Find a lab for 100 people next week")
            assert result["success"] is False
            assert result["total_count"] == 0
            assert result["suggestions"]  # fallback guidance is provided

    def test_help_intent_returns_help_block(self, app, concierge_fixtures):
        with app.app_context():
            result = AIConciergeService.process_query("How does this concierge work?")
            assert result["success"] is True
            assert result.get("is_help") is True
