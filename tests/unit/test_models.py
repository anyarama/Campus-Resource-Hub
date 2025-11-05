"""
Unit Tests for Models - Campus Resource Hub
Tests CRUD operations and relationships for all models.

Per .clinerules: TDD approach with comprehensive model testing.
"""

import pytest
from datetime import datetime, timedelta
from src.models import db, User, Resource, Booking, Message, Review


class TestUserModel:
    """Test User model CRUD and relationships."""

    def test_create_user(self, app):
        """Test user creation with password hashing."""
        with app.app_context():
            user = User(
                name="Test Student",
                email="test@example.com",
                password="securepass123",
                role="student",
            )
            db.session.add(user)
            db.session.commit()

            assert user.user_id is not None
            assert user.name == "Test Student"
            assert user.email == "test@example.com"
            assert user.role == "student"
            assert user.password_hash != "securepass123"  # Should be hashed

    def test_password_hashing(self, app):
        """Test password hashing and verification."""
        with app.app_context():
            user = User(name="Test", email="test@example.com", password="mypassword")

            assert user.check_password("mypassword") is True
            assert user.check_password("wrongpassword") is False

    def test_user_roles(self, app):
        """Test role helper methods."""
        with app.app_context():
            student = User(
                name="Student", email="student@test.com", password="pass", role="student"
            )
            staff = User(name="Staff", email="staff@test.com", password="pass", role="staff")
            admin = User(name="Admin", email="admin@test.com", password="pass", role="admin")

            assert student.is_student() is True
            assert student.can_approve_bookings() is False

            assert staff.is_staff() is True
            assert staff.can_approve_bookings() is True

            assert admin.is_admin() is True
            assert admin.can_moderate_content() is True

    def test_user_relationships(self, app):
        """Test user relationships to resources and bookings."""
        with app.app_context():
            user = User(name="Owner", email="owner@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            # Create resource owned by user
            resource = Resource(owner_id=user.user_id, title="Test Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            assert user.resources.count() == 1
            assert user.resources.first().title == "Test Room"


class TestResourceModel:
    """Test Resource model CRUD and methods."""

    def test_create_resource(self, app):
        """Test resource creation."""
        with app.app_context():
            user = User(name="Owner", email="owner@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(
                owner_id=user.user_id,
                title="Study Room A",
                category="study_room",
                description="Quiet study room",
                location="Library 2nd Floor",
                capacity=4,
            )
            db.session.add(resource)
            db.session.commit()

            assert resource.resource_id is not None
            assert resource.title == "Study Room A"
            assert resource.status == "draft"  # Default status

    def test_resource_images(self, app):
        """Test JSON image storage and retrieval."""
        with app.app_context():
            user = User(name="Owner", email="owner@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            resource.set_images(["image1.jpg", "image2.jpg"])
            db.session.add(resource)
            db.session.commit()

            retrieved = Resource.query.get(resource.resource_id)
            assert retrieved.get_images() == ["image1.jpg", "image2.jpg"]

    def test_resource_availability_rules(self, app):
        """Test JSON availability rules storage."""
        with app.app_context():
            user = User(name="Owner", email="owner@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            rules = {"requires_approval": True, "max_booking_hours": 4}
            resource.set_availability_rules(rules)
            db.session.add(resource)
            db.session.commit()

            retrieved = Resource.query.get(resource.resource_id)
            assert retrieved.get_availability_rules() == rules
            assert retrieved.requires_approval() is True

    def test_resource_status_lifecycle(self, app):
        """Test resource status transitions."""
        with app.app_context():
            user = User(name="Owner", email="owner@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            assert resource.is_draft() is True

            resource.publish()
            assert resource.is_published() is True
            assert resource.status == "published"

            resource.archive()
            assert resource.is_archived() is True


class TestBookingModel:
    """Test Booking model CRUD and conflict detection."""

    def test_create_booking(self, app):
        """Test booking creation."""
        with app.app_context():
            # Create user and resource
            user = User(name="User", email="user@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            # Create booking
            start = datetime.utcnow() + timedelta(days=1)
            end = start + timedelta(hours=2)
            booking = Booking(
                resource_id=resource.resource_id,
                requester_id=user.user_id,
                start_datetime=start,
                end_datetime=end,
            )
            db.session.add(booking)
            db.session.commit()

            assert booking.booking_id is not None
            assert booking.status == "pending"
            assert booking.get_duration_hours() == 2.0

    def test_booking_validation(self, app):
        """Test end_datetime must be after start_datetime."""
        with app.app_context():
            start = datetime.utcnow()
            end = start - timedelta(hours=1)  # Invalid: end before start

            with pytest.raises(ValueError, match="end_datetime must be after start_datetime"):
                Booking(resource_id=1, requester_id=1, start_datetime=start, end_datetime=end)

    def test_booking_status_transitions(self, app):
        """Test booking status workflow."""
        with app.app_context():
            user = User(name="User", email="user@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            start = datetime.utcnow() + timedelta(days=1)
            end = start + timedelta(hours=2)
            booking = Booking(
                resource_id=resource.resource_id,
                requester_id=user.user_id,
                start_datetime=start,
                end_datetime=end,
            )
            db.session.add(booking)
            db.session.commit()

            assert booking.is_pending() is True

            booking.approve()
            assert booking.is_approved() is True

            booking.complete()
            assert booking.is_completed() is True

    def test_booking_cancel(self, app):
        """Test booking cancellation."""
        with app.app_context():
            user = User(name="User", email="user@test.com", password="pass")
            db.session.add(user)
            db.session.commit()

            resource = Resource(owner_id=user.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            start = datetime.utcnow() + timedelta(days=1)
            end = start + timedelta(hours=2)
            booking = Booking(
                resource_id=resource.resource_id,
                requester_id=user.user_id,
                start_datetime=start,
                end_datetime=end,
            )
            booking.approve()
            db.session.add(booking)
            db.session.commit()

            booking.cancel()
            assert booking.is_cancelled() is True


class TestMessageModel:
    """Test Message model CRUD and validation."""

    def test_create_message(self, app):
        """Test message creation."""
        with app.app_context():
            sender = User(name="Sender", email="sender@test.com", password="pass")
            receiver = User(name="Receiver", email="receiver@test.com", password="pass")
            db.session.add_all([sender, receiver])
            db.session.commit()

            message = Message(
                sender_id=sender.user_id,
                receiver_id=receiver.user_id,
                content="Hello, is this room available?",
            )
            db.session.add(message)
            db.session.commit()

            assert message.message_id is not None
            assert message.content == "Hello, is this room available?"
            assert message.is_read is False

    def test_message_validation_same_user(self, app):
        """Test cannot send message to yourself."""
        with pytest.raises(ValueError, match="Cannot send message to yourself"):
            Message(sender_id=1, receiver_id=1, content="Test")

    def test_message_validation_empty_content(self, app):
        """Test cannot send empty message."""
        with pytest.raises(ValueError, match="Message content cannot be empty"):
            Message(sender_id=1, receiver_id=2, content="   ")

    def test_message_mark_as_read(self, app):
        """Test marking message as read."""
        with app.app_context():
            sender = User(name="Sender", email="sender@test.com", password="pass")
            receiver = User(name="Receiver", email="receiver@test.com", password="pass")
            db.session.add_all([sender, receiver])
            db.session.commit()

            message = Message(
                sender_id=sender.user_id, receiver_id=receiver.user_id, content="Test"
            )
            db.session.add(message)
            db.session.commit()

            assert message.is_read is False
            message.mark_as_read()
            assert message.is_read is True


class TestReviewModel:
    """Test Review model CRUD and constraints."""

    def test_create_review(self, app):
        """Test review creation."""
        with app.app_context():
            owner = User(name="Owner", email="owner@test.com", password="pass")
            reviewer = User(name="Reviewer", email="reviewer@test.com", password="pass")
            db.session.add_all([owner, reviewer])
            db.session.commit()

            resource = Resource(owner_id=owner.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            review = Review(
                resource_id=resource.resource_id,
                reviewer_id=reviewer.user_id,
                rating=4,
                comment="Great study room!",
            )
            db.session.add(review)
            db.session.commit()

            assert review.review_id is not None
            assert review.rating == 4
            assert review.is_visible() is True

    def test_review_rating_validation(self, app):
        """Test rating must be 1-5."""
        with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
            Review(resource_id=1, reviewer_id=1, rating=0)

        with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
            Review(resource_id=1, reviewer_id=1, rating=6)

    def test_review_moderation(self, app):
        """Test admin can hide/unhide reviews."""
        with app.app_context():
            owner = User(name="Owner", email="owner@test.com", password="pass")
            reviewer = User(name="Reviewer", email="reviewer@test.com", password="pass")
            admin = User(name="Admin", email="admin@test.com", password="pass", role="admin")
            db.session.add_all([owner, reviewer, admin])
            db.session.commit()

            resource = Resource(owner_id=owner.user_id, title="Room", category="study_room")
            db.session.add(resource)
            db.session.commit()

            review = Review(
                resource_id=resource.resource_id,
                reviewer_id=reviewer.user_id,
                rating=1,
                comment="Bad",
            )
            db.session.add(review)
            db.session.commit()

            review.hide(admin.user_id, "Inappropriate language")
            assert review.is_visible() is False
            assert review.hidden_reason == "Inappropriate language"

            review.unhide()
            assert review.is_visible() is True

    def test_review_star_display(self, app):
        """Test star rating display."""
        review = Review(resource_id=1, reviewer_id=1, rating=3)
        assert review.get_star_display() == "★★★☆☆"
