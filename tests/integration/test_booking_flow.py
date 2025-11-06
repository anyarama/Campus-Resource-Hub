"""
Integration Tests for Booking Flow
Campus Resource Hub - Phase 6

Tests the complete booking workflow including:
- Creating bookings
- Conflict detection
- Approval workflow
- Cancellation
- Status transitions
"""

import pytest
from datetime import datetime, timedelta
from src.models.booking import Booking
from src.models.resource import Resource
from src.models.user import User
from src.repositories.booking_repo import BookingRepository
from src.repositories.resource_repo import ResourceRepository
from src.repositories.user_repo import UserRepository


class TestBookingFlow:
    """Integration tests for booking workflow"""

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
                title="Test Conference Room",
                description="Test room for bookings",
                category="Meeting Room",
                location="Building A, Room 101",
                capacity=10,
                status="published"
            )
            
            db.session.commit()
            yield
            db.session.rollback()

    def test_create_booking_success(self, client, app):
        """Test successful booking creation"""
        with app.app_context():
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Create booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)
            
            response = client.post('/bookings', data={
                'resource_id': self.resource.resource_id,
                'start_date': start.strftime('%Y-%m-%d'),
                'start_time': start.strftime('%H:%M'),
                'end_date': end.strftime('%Y-%m-%d'),
                'end_time': end.strftime('%H:%M'),
                'notes': 'Test booking'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify booking was created
            bookings = BookingRepository.get_by_requester(self.student.user_id)
            assert len(bookings) == 1
            assert bookings[0].status == 'pending'
            assert bookings[0].resource_id == self.resource.resource_id

    def test_booking_conflict_detection(self, client, app):
        """Test that overlapping bookings are prevented"""
        with app.app_context():
            # Create first booking
            start1 = datetime.now() + timedelta(days=1)
            end1 = start1 + timedelta(hours=2)
            
            booking1 = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start1,
                end_datetime=end1,
                status='approved'
            )
            
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
            
            # Try to create overlapping booking
            start2 = start1 + timedelta(minutes=30)  # Overlaps with first booking
            end2 = end1 + timedelta(minutes=30)
            
            response = client.post('/bookings', data={
                'resource_id': self.resource.resource_id,
                'start_date': start2.strftime('%Y-%m-%d'),
                'start_time': start2.strftime('%H:%M'),
                'end_date': end2.strftime('%Y-%m-%d'),
                'end_time': end2.strftime('%H:%M')
            }, follow_redirects=True)
            
            # Should redirect with error message
            assert b'conflicting' in response.data.lower() or b'unavailable' in response.data.lower()
            
            # Verify second booking was not created
            bookings = BookingRepository.get_by_requester(student2.user_id)
            assert len(bookings) == 0

    def test_staff_approve_booking(self, client, app):
        """Test staff can approve pending bookings"""
        with app.app_context():
            # Create pending booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)
            
            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status='pending'
            )
            
            # Login as staff
            client.post('/auth/login', data={
                'email': 'staff@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Approve booking
            response = client.post(f'/bookings/{booking.booking_id}/approve', follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify booking was approved
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == 'approved'

    def test_staff_reject_booking(self, client, app):
        """Test staff can reject pending bookings"""
        with app.app_context():
            # Create pending booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)
            
            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status='pending'
            )
            
            # Login as staff
            client.post('/auth/login', data={
                'email': 'staff@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Reject booking
            response = client.post(f'/bookings/{booking.booking_id}/reject', data={
                'rejection_reason': 'Resource not available'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify booking was rejected
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == 'rejected'
            assert updated_booking.rejection_reason == 'Resource not available'

    def test_user_cancel_booking(self, client, app):
        """Test user can cancel their own booking"""
        with app.app_context():
            # Create approved booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)
            
            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status='approved'
            )
            
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Cancel booking
            response = client.post(f'/bookings/{booking.booking_id}/cancel', follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify booking was cancelled
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == 'cancelled'

    def test_admin_complete_booking(self, client, app):
        """Test admin can mark booking as completed"""
        with app.app_context():
            # Create approved booking
            start = datetime.now() - timedelta(days=1)  # Past booking
            end = start + timedelta(hours=2)
            
            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status='approved'
            )
            
            # Login as admin
            client.post('/auth/login', data={
                'email': 'admin@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Mark as complete
            response = client.post(f'/bookings/{booking.booking_id}/complete', follow_redirects=True)
            
            assert response.status_code == 200
            
            # Verify booking was completed
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == 'completed'

    def test_unauthorized_approval_denied(self, client, app):
        """Test that students cannot approve bookings"""
        with app.app_context():
            # Create pending booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)
            
            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status='pending'
            )
            
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Try to approve booking (should fail)
            response = client.post(f'/bookings/{booking.booking_id}/approve', follow_redirects=True)
            
            # Should be denied (403 or redirect with error)
            assert response.status_code in [200, 403]
            
            # Verify booking is still pending
            updated_booking = BookingRepository.get_by_id(booking.booking_id)
            assert updated_booking.status == 'pending'

    def test_view_my_bookings(self, client, app):
        """Test user can view their bookings dashboard"""
        with app.app_context():
            # Create multiple bookings with different statuses
            now = datetime.now()
            
            # Pending booking
            BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=now + timedelta(days=1),
                end_datetime=now + timedelta(days=1, hours=2),
                status='pending'
            )
            
            # Approved booking
            BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=now + timedelta(days=2),
                end_datetime=now + timedelta(days=2, hours=2),
                status='approved'
            )
            
            # Completed booking
            BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=now - timedelta(days=1),
                end_datetime=now - timedelta(days=1) + timedelta(hours=2),
                status='completed'
            )
            
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # View my bookings
            response = client.get('/my-bookings')
            
            assert response.status_code == 200
            assert b'My Bookings' in response.data
            assert b'Pending' in response.data
            assert b'Upcoming' in response.data or b'Approved' in response.data
            assert b'Past' in response.data or b'Completed' in response.data

    def test_booking_detail_view(self, client, app):
        """Test viewing booking details"""
        with app.app_context():
            # Create booking
            start = datetime.now() + timedelta(days=1)
            end = start + timedelta(hours=2)
            
            booking = BookingRepository.create(
                resource_id=self.resource.resource_id,
                requester_id=self.student.user_id,
                start_datetime=start,
                end_datetime=end,
                status='pending',
                notes='Test notes'
            )
            
            # Login as student
            client.post('/auth/login', data={
                'email': 'student@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # View booking detail
            response = client.get(f'/bookings/{booking.booking_id}')
            
            assert response.status_code == 200
            assert b'Booking Details' in response.data
            assert b'Test Conference Room' in response.data
            assert b'Test notes' in response.data
