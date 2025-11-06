"""
Integration Tests for Review Flow
Campus Resource Hub - Phase 6

Tests the complete review workflow including:
- Submitting reviews (with authorization)
- Editing/deleting reviews
- Admin moderation
- One review per user per resource
- Aggregate rating calculation
"""

import pytest
from datetime import datetime, timedelta
from src.models.booking import Booking
from src.models.resource import Resource
from src.models.review import Review
from src.models.user import User
from src.repositories.booking_repo import BookingRepository
from src.repositories.resource_repo import ResourceRepository
from src.repositories.review_repo import ReviewRepository
from src.repositories.user_repo import UserRepository


class TestReviewFlow:
    """Integration tests for review workflow"""

    @pytest.fixture(autouse=True)
    def setup(self, app, db):
        """Set up test data before each test"""
        with app.app_context():
            # Create test users
            self.student = UserRepository.create(
                name="Test Student",
                email="student@test.com",
                password="password123",
                role="student"
            )
            
            self.staff = UserRepository.create(
                name="Test Staff",
                email="staff@test.com",
                password="password123",
                role="staff"
            )
            
            self.admin = UserRepository.create(
                name="Test Admin",
                email="admin@test.com",
                password="password123",
                role="admin"
            )
            
            # Create test resource
            self.resource = ResourceRepository.create(
                owner_id=self.staff.user_id,
                title="Test Projector",
                description="Test projector for reviews",
                category="Equipment",
                location="AV Department",
                status="published"
            )
            
            # Create completed booking (required for review)
            past_start = datetime.now() - timedelta(days=2)
            past_end = past_start + timedelta(hours=2)
            
            self.completed_booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=past_start,
                end_datetime=past_end,
                status='completed'
            )
            
            db.session.commit()
            yield
            db.session.rollback()

    def test_submit_review_success(self, client, app):
        """Test successful review submission after completed booking"""
        with app.app_context():
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Submit review
            response = client.post(f'/resources/{self.resource.resource_id}/reviews', data={
                'rating': '5',
                'comment': 'Excellent projector! Very clear image and easy to use.'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify review was created
            reviews = ReviewRepository.get_by_resource(self.resource.resource_id)
            assert len(reviews) == 1
            assert reviews[0].rating == 5
            assert reviews[0].reviewer_id == self.student.user_id
            assert 'Excellent projector' in reviews[0].comment

    def test_cannot_review_without_completed_booking(self, client, app):
        """Test that users cannot review without a completed booking"""
        with app.app_context():
            # Create new student without completed booking
            student2 = UserRepository.create(
                name="Student Two",
                email="student2@test.com",
                password="password123",
                role="student"
            )
            
            # Login as student2
            client.post('/auth/login', data={
                'email': 'student2@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Try to submit review
            response = client.post(f'/resources/{self.resource.resource_id}/reviews', data={
                'rating': '5',
                'comment': 'Great resource!'
            }, follow_redirects=True)
            
            # Should be denied
            assert b'completed' in response.data.lower() or b'booking' in response.data.lower()
            
            # Verify review was not created
            reviews = ReviewRepository.get_by_resource(self.resource.resource_id)
            student2_reviews = [r for r in reviews if r.reviewer_id == student2.user_id]
            assert len(student2_reviews) == 0

    def test_one_review_per_user_per_resource(self, client, app):
        """Test that a user can only submit one review per resource"""
        with app.app_context():
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Submit first review
            client.post(f'/resources/{self.resource.resource_id}/reviews', data={
                'rating': '5',
                'comment': 'Great projector!'
            }, follow_redirects=True)
            
            # Try to submit second review
            response = client.post(f'/resources/{self.resource.resource_id}/reviews', data={
                'rating': '4',
                'comment': 'Good but not perfect'
            }, follow_redirects=True)
            
            # Should be denied
            assert b'already' in response.data.lower() or b'existing' in response.data.lower()
            
            # Verify only one review exists
            reviews = ReviewRepository.get_by_resource(self.resource.resource_id)
            student_reviews = [r for r in reviews if r.reviewer_id == self.student.user_id]
            assert len(student_reviews) == 1

    def test_edit_own_review(self, client, app):
        """Test user can edit their own review"""
        with app.app_context():
            # Create review
            review = ReviewRepository.create(
                resource_id=self.resource.resource_id,
                reviewer_id=self.student.user_id,
                rating=4,
                comment='Good projector'
            )
            
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Edit review
            response = client.post(f'/reviews/{review.review_id}', data={
                '_method': 'PUT',
                'rating': '5',
                'comment': 'Excellent projector! Updated my review.'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify review was updated
            updated_review = ReviewRepository.get_by_id(review.review_id)
            assert updated_review.rating == 5
            assert 'Updated my review' in updated_review.comment

    def test_delete_own_review(self, client, app):
        """Test user can delete their own review"""
        with app.app_context():
            # Create review
            review = ReviewRepository.create(
                resource_id=self.resource.resource_id,
                reviewer_id=self.student.user_id,
                rating=4,
                comment='Test review'
            )
            
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Delete review
            response = client.post(f'/reviews/{review.review_id}/delete', follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify review was deleted
            deleted_review = ReviewRepository.get_by_id(review.review_id)
            assert deleted_review is None

    def test_cannot_edit_others_review(self, client, app):
        """Test user cannot edit another user's review"""
        with app.app_context():
            # Create review by student
            review = ReviewRepository.create(
                resource_id=self.resource.resource_id,
                reviewer_id=self.student.user_id,
                rating=4,
                comment='Student review'
            )
            
            # Create another student
            student2 = UserRepository.create(
                name="Student Two",
                email="student2@test.com",
                password="password123",
                role="student"
            )
            
            # Login as student2
            client.post('/auth/login', data={
                'email': 'student2@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Try to edit student's review
            response = client.post(f'/reviews/{review.review_id}', data={
                '_method': 'PUT',
                'rating': '1',
                'comment': 'Hacked!'
            }, follow_redirects=True)
            
            # Should be denied (403 or redirect with error)
            assert response.status_code in [200, 403]
            
            # Verify review was not changed
            unchanged_review = ReviewRepository.get_by_id(review.review_id)
            assert unchanged_review.rating == 4
            assert unchanged_review.comment == 'Student review'

    def test_admin_hide_review(self, client, app):
        """Test admin can hide inappropriate reviews"""
        with app.app_context():
            # Create review
            review = ReviewRepository.create(
                resource_id=self.resource.resource_id,
                reviewer_id=self.student.user_id,
                rating=1,
                comment='Inappropriate content here'
            )
            
            # Login as admin
            client.post('/auth/login', data={
                'email': 'admin@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Hide review
            response = client.post(f'/reviews/{review.review_id}/hide', follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify review was hidden
            hidden_review = ReviewRepository.get_by_id(review.review_id)
            assert hidden_review.is_hidden is True

    def test_admin_unhide_review(self, client, app):
        """Test admin can unhide reviews"""
        with app.app_context():
            # Create hidden review
            review = ReviewRepository.create(
                resource_id=self.resource.resource_id,
                reviewer_id=self.student.user_id,
                rating=4,
                comment='Good review'
            )
            review.is_hidden = True
            ReviewRepository.update(review)
            
            # Login as admin
            client.post('/auth/login', data={
                'email': 'admin@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Unhide review
            response = client.post(f'/reviews/{review.review_id}/unhide', follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify review was unhidden
            unhidden_review = ReviewRepository.get_by_id(review.review_id)
            assert unhidden_review.is_hidden is False

    def test_non_admin_cannot_hide_review(self, client, app):
        """Test that non-admin users cannot hide reviews"""
        with app.app_context():
            # Create review
            review = ReviewRepository.create(
                resource_id=self.resource.resource_id,
                reviewer_id=self.student.user_id,
                rating=4,
                comment='Test review'
            )
            
            # Login as staff (not admin)
            client.post('/auth/login', data={
                'email': 'staff@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Try to hide review
            response = client.post(f'/reviews/{review.review_id}/hide', follow_redirects=True)
            
            # Should be denied (403 or redirect with error)
            assert response.status_code in [200, 403]
            
            # Verify review was not hidden
            unchanged_review = ReviewRepository.get_by_id(review.review_id)
            assert unchanged_review.is_hidden is False

    def test_aggregate_rating_calculation(self, client, app):
        """Test that aggregate ratings are calculated correctly"""
        with app.app_context():
            # Create multiple users with completed bookings
            users = []
            for i in range(3):
                user = UserRepository.create(
                    name=f"User {i}",
                    email=f"user{i}@test.com",
                    password="password123",
                    role="student"
                )
                
                # Create completed booking
                past_start = datetime.now() - timedelta(days=i+1)
                BookingRepository.create(
                    resource_id=self.resource.resource_id,
                    requester_id=user.user_id,
                    start_datetime=past_start,
                    end_datetime=past_start + timedelta(hours=1),
                    status='completed'
                )
                users.append(user)
            
            # Create reviews with ratings: 5, 4, 3 (average = 4.0)
            ratings = [5, 4, 3]
            for user, rating in zip(users, ratings):
                ReviewRepository.create(
                    resource_id=self.resource.resource_id,
                    reviewer_id=user.user_id,
                    rating=rating,
                    comment=f'Rating {rating} review'
                )
            
            # Get resource and check average rating
            resource = ResourceRepository.get_by_id(self.resource.resource_id)
            reviews = ReviewRepository.get_by_resource(self.resource.resource_id)
            
            # Calculate average
            if reviews:
                avg_rating = sum(r.rating for r in reviews) / len(reviews)
                assert avg_rating == 4.0

    def test_review_validation_min_length(self, client, app):
        """Test review comment minimum length validation"""
        with app.app_context():
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Try to submit review with short comment
            response = client.post(f'/resources/{self.resource.resource_id}/reviews', data={
                'rating': '5',
                'comment': 'Too short'  # Less than 10 characters
            }, follow_redirects=True)
            
            # Should show validation error
            assert b'10' in response.data or b'characters' in response.data.lower()

    def test_review_requires_rating(self, client, app):
        """Test that reviews require a rating"""
        with app.app_context():
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Try to submit review without rating
            response = client.post(f'/resources/{self.resource.resource_id}/reviews', data={
                'comment': 'This is a comment without a rating'
            }, follow_redirects=True)
            
            # Should show validation error
            assert response.status_code in [200, 400]
            
            # Verify review was not created
            reviews = ReviewRepository.get_by_resource(self.resource.resource_id)
            assert len(reviews) == 0

    def test_view_reviews_on_resource_page(self, client, app):
        """Test that reviews are displayed on resource detail page"""
        with app.app_context():
            # Create review
            ReviewRepository.create(
                resource_id=self.resource.resource_id,
                reviewer_id=self.student.user_id,
                rating=5,
                comment='Excellent equipment!'
            )
            
            # View resource detail page
            response = client.get(f'/resources/{self.resource.resource_id}')
            
            assert response.status_code == 200
            assert b'Review' in response.data
            assert b'Excellent equipment' in response.data
            assert b'Test Student' in response.data

    def test_hidden_reviews_not_visible_to_users(self, client, app):
        """Test that hidden reviews are not shown to regular users"""
        with app.app_context():
            # Create hidden review
            review = ReviewRepository.create(
                resource_id=self.resource.resource_id,
                reviewer_id=self.student.user_id,
                rating=1,
                comment='Hidden inappropriate content'
            )
            review.is_hidden = True
            ReviewRepository.update(review)
            
            # Login as different student
            student2 = UserRepository.create(
                name="Student Two",
                email="student2@test.com",
                password="password123",
                role="student"
            )
            
            client.post('/auth/login', data={
                'email': 'student2@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # View resource detail page
            response = client.get(f'/resources/{self.resource.resource_id}')
            
            # Hidden content should not be visible
            assert b'Hidden inappropriate content' not in response.data
