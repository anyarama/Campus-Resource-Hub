"""
Campus Resource Hub - Admin Service
AiDD 2025 Capstone Project

Business logic for admin dashboard and platform management operations.

AI Contribution: Cline generated admin service structure
Reviewed and extended by developer on 2025-11-06
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_, or_
from src.app import db
from src.models.user import User
from src.models.resource import Resource
from src.models.booking import Booking
from src.models.message import Message
from src.models.review import Review
from src.repositories.user_repo import UserRepository
from src.repositories.resource_repo import ResourceRepository
from src.repositories.booking_repo import BookingRepository
from src.repositories.message_repo import MessageRepository
from src.repositories.review_repo import ReviewRepository


class AdminServiceError(Exception):
    """Raised when admin service operations fail."""
    pass


class AdminService:
    """
    Service layer for admin dashboard and platform management.
    
    Provides methods for:
    - Platform statistics and analytics
    - User management (suspend, activate, delete)
    - Content moderation
    - Activity monitoring
    """
    
    @staticmethod
    def get_platform_stats() -> Dict[str, Any]:
        """
        Get comprehensive platform statistics.
        
        Returns:
            Dict containing platform-wide metrics:
            - total_users, active_users, suspended_users
            - total_resources, published_resources
            - total_bookings, pending_bookings, completed_bookings
            - total_messages, total_reviews
            - hidden_reviews
        
        Example:
            >>> stats = AdminService.get_platform_stats()
            >>> print(f"Total users: {stats['total_users']}")
        """
        try:
            # User statistics
            total_users = db.session.query(func.count(User.user_id)).scalar() or 0
            active_users = db.session.query(func.count(User.user_id)).filter(
                User.is_active == True
            ).scalar() or 0
            suspended_users = db.session.query(func.count(User.user_id)).filter(
                User.is_active == False
            ).scalar() or 0
            
            # Role distribution
            admins = db.session.query(func.count(User.user_id)).filter(
                User.role == 'admin'
            ).scalar() or 0
            staff = db.session.query(func.count(User.user_id)).filter(
                User.role == 'staff'
            ).scalar() or 0
            students = db.session.query(func.count(User.user_id)).filter(
                User.role == 'student'
            ).scalar() or 0
            
            # Resource statistics
            total_resources = db.session.query(func.count(Resource.resource_id)).scalar() or 0
            published_resources = db.session.query(func.count(Resource.resource_id)).filter(
                Resource.status == 'published'
            ).scalar() or 0
            draft_resources = db.session.query(func.count(Resource.resource_id)).filter(
                Resource.status == 'draft'
            ).scalar() or 0
            archived_resources = db.session.query(func.count(Resource.resource_id)).filter(
                Resource.status == 'archived'
            ).scalar() or 0
            
            # Booking statistics
            total_bookings = db.session.query(func.count(Booking.booking_id)).scalar() or 0
            pending_bookings = db.session.query(func.count(Booking.booking_id)).filter(
                Booking.status == 'pending'
            ).scalar() or 0
            approved_bookings = db.session.query(func.count(Booking.booking_id)).filter(
                Booking.status == 'approved'
            ).scalar() or 0
            completed_bookings = db.session.query(func.count(Booking.booking_id)).filter(
                Booking.status == 'completed'
            ).scalar() or 0
            cancelled_bookings = db.session.query(func.count(Booking.booking_id)).filter(
                or_(Booking.status == 'cancelled', Booking.status == 'rejected')
            ).scalar() or 0
            
            # Message statistics
            total_messages = db.session.query(func.count(Message.message_id)).scalar() or 0
            unread_messages = db.session.query(func.count(Message.message_id)).filter(
                Message.is_read == False
            ).scalar() or 0
            
            # Review statistics
            total_reviews = db.session.query(func.count(Review.review_id)).scalar() or 0
            hidden_reviews = db.session.query(func.count(Review.review_id)).filter(
                Review.is_hidden == True
            ).scalar() or 0
            
            return {
                # User stats
                'total_users': total_users,
                'active_users': active_users,
                'suspended_users': suspended_users,
                'admins': admins,
                'staff': staff,
                'students': students,
                
                # Resource stats
                'total_resources': total_resources,
                'published_resources': published_resources,
                'archived_resources': archived_resources,
                'draft_resources': draft_resources,
                'archived_resources': archived_resources,
                
                # Booking stats
                'total_bookings': total_bookings,
                'pending_bookings': pending_bookings,
                'approved_bookings': approved_bookings,
                'completed_bookings': completed_bookings,
                'cancelled_bookings': cancelled_bookings,
                
                # Message stats
                'total_messages': total_messages,
                'unread_messages': unread_messages,
                
                # Review stats
                'total_reviews': total_reviews,
                'hidden_reviews': hidden_reviews,
            }
            
        except Exception as e:
            raise AdminServiceError(f"Failed to get platform stats: {e}")
    
    @staticmethod
    def get_recent_activity(limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get recent platform activity across all entities.
        
        Args:
            limit: Maximum items per category (default 20)
        
        Returns:
            Dict with lists of recent users, resources, bookings, messages, reviews
        
        Example:
            >>> activity = AdminService.get_recent_activity(limit=10)
            >>> print(f"Recent users: {len(activity['users'])}")
        """
        try:
            # Recent users
            recent_users = db.session.query(User).order_by(
                User.created_at.desc()
            ).limit(limit).all()
            
            # Recent resources
            recent_resources = db.session.query(Resource).order_by(
                Resource.created_at.desc()
            ).limit(limit).all()
            
            # Recent bookings
            recent_bookings = db.session.query(Booking).order_by(
                Booking.created_at.desc()
            ).limit(limit).all()
            
            # Recent messages
            recent_messages = db.session.query(Message).order_by(
                Message.timestamp.desc()
            ).limit(limit).all()
            
            # Recent reviews
            recent_reviews = db.session.query(Review).order_by(
                Review.timestamp.desc()
            ).limit(limit).all()
            
            return {
                'users': [
                    {
                        'user_id': u.user_id,
                        'name': u.name,
                        'email': u.email,
                        'role': u.role,
                        'created_at': u.created_at,
                        'is_active': u.is_active
                    } for u in recent_users
                ],
                'resources': [
                    {
                        'resource_id': r.resource_id,
                        'title': r.title,
                        'category': r.category,
                        'status': r.status,
                        'created_at': r.created_at,
                        'owner_name': r.owner.name if r.owner else 'Unknown'
                    } for r in recent_resources
                ],
                'bookings': [
                    {
                        'booking_id': b.booking_id,
                        'resource_title': b.resource.title if b.resource else 'Unknown',
                        'requester_name': b.requester.name if b.requester else 'Unknown',
                        'status': b.status,
                        'created_at': b.created_at
                    } for b in recent_bookings
                ],
                'messages': [
                    {
                        'message_id': m.message_id,
                        'sender_name': m.sender.name if m.sender else 'Unknown',
                        'receiver_name': m.receiver.name if m.receiver else 'Unknown',
                        'timestamp': m.timestamp,
                        'is_read': m.is_read
                    } for m in recent_messages
                ],
                'reviews': [
                    {
                        'review_id': r.review_id,
                        'resource_title': r.resource.title if r.resource else 'Unknown',
                        'reviewer_name': r.reviewer.name if r.reviewer else 'Unknown',
                        'rating': r.rating,
                        'timestamp': r.timestamp,
                        'is_hidden': r.is_hidden
                    } for r in recent_reviews
                ]
            }
            
        except Exception as e:
            raise AdminServiceError(f"Failed to get recent activity: {e}")
    
    @staticmethod
    def get_user_activity_summary(user_id: int) -> Dict[str, Any]:
        """
        Get summary of a user's platform activity.
        
        Args:
            user_id: ID of user to analyze
        
        Returns:
            Dict with user's activity metrics
        
        Raises:
            AdminServiceError: If user not found or query fails
        """
        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                raise AdminServiceError(f"User {user_id} not found")
            
            # Count user's resources
            resources_count = db.session.query(func.count(Resource.resource_id)).filter(
                Resource.owner_id == user_id
            ).scalar() or 0
            
            # Count user's bookings
            bookings_count = db.session.query(func.count(Booking.booking_id)).filter(
                Booking.requester_id == user_id
            ).scalar() or 0
            
            # Count messages sent
            messages_sent = db.session.query(func.count(Message.message_id)).filter(
                Message.sender_id == user_id
            ).scalar() or 0
            
            # Count messages received
            messages_received = db.session.query(func.count(Message.message_id)).filter(
                Message.receiver_id == user_id
            ).scalar() or 0
            
            # Count reviews written
            reviews_written = db.session.query(func.count(Review.review_id)).filter(
                Review.reviewer_id == user_id
            ).scalar() or 0
            
            return {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at,
                'resources_owned': resources_count,
                'bookings_made': bookings_count,
                'messages_sent': messages_sent,
                'messages_received': messages_received,
                'reviews_written': reviews_written
            }
            
        except AdminServiceError:
            raise
        except Exception as e:
            raise AdminServiceError(f"Failed to get user activity: {e}")
    
    @staticmethod
    def suspend_user(user_id: int, admin_id: int) -> bool:
        """
        Suspend a user account.
        
        Args:
            user_id: ID of user to suspend
            admin_id: ID of admin performing the action
        
        Returns:
            True if successful
        
        Raises:
            AdminServiceError: If operation fails or user cannot be suspended
        
        Security:
            - Cannot suspend admin accounts
            - Cannot suspend self
        """
        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                raise AdminServiceError(f"User {user_id} not found")
            
            # Prevent suspending admins
            if user.role == 'admin':
                raise AdminServiceError("Cannot suspend admin accounts")
            
            # Prevent self-suspension
            if user_id == admin_id:
                raise AdminServiceError("Cannot suspend your own account")
            
            # Set user as inactive
            user.is_active = False
            user.suspended_at = datetime.utcnow()
            db.session.commit()
            
            return True
            
        except AdminServiceError:
            raise
        except Exception as e:
            db.session.rollback()
            raise AdminServiceError(f"Failed to suspend user: {e}")
    
    @staticmethod
    def activate_user(user_id: int) -> bool:
        """
        Activate a suspended user account.
        
        Args:
            user_id: ID of user to activate
        
        Returns:
            True if successful
        
        Raises:
            AdminServiceError: If operation fails
        """
        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                raise AdminServiceError(f"User {user_id} not found")
            
            # Set user as active
            user.is_active = True
            user.suspended_at = None
            db.session.commit()
            
            return True
            
        except AdminServiceError:
            raise
        except Exception as e:
            db.session.rollback()
            raise AdminServiceError(f"Failed to activate user: {e}")
    
    @staticmethod
    def delete_user(user_id: int, admin_id: int) -> bool:
        """
        Permanently delete a user account and all associated data.
        
        WARNING: This is a destructive operation. All user data will be lost.
        
        Args:
            user_id: ID of user to delete
            admin_id: ID of admin performing the action
        
        Returns:
            True if successful
        
        Raises:
            AdminServiceError: If operation fails or user cannot be deleted
        
        Security:
            - Cannot delete admin accounts
            - Cannot delete self
            - Cascading deletion of user's resources, bookings, messages, reviews
        """
        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                raise AdminServiceError(f"User {user_id} not found")
            
            # Prevent deleting admins
            if user.role == 'admin':
                raise AdminServiceError("Cannot delete admin accounts")
            
            # Prevent self-deletion
            if user_id == admin_id:
                raise AdminServiceError("Cannot delete your own account")
            
            # Delete user (cascade will handle related records)
            db.session.delete(user)
            db.session.commit()
            
            return True
            
        except AdminServiceError:
            raise
        except Exception as e:
            db.session.rollback()
            raise AdminServiceError(f"Failed to delete user: {e}")
    
    @staticmethod
    def get_popular_resources(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most popular resources by booking count.
        
        Args:
            limit: Maximum number of results (default 10)
        
        Returns:
            List of dicts with resource info and booking count
        """
        try:
            # Query resources with booking count
            results = db.session.query(
                Resource,
                func.count(Booking.booking_id).label('booking_count')
            ).outerjoin(Booking).filter(
                Resource.status == 'published'
            ).group_by(Resource.resource_id).order_by(
                func.count(Booking.booking_id).desc()
            ).limit(limit).all()
            
            return [
                {
                    'resource_id': r.resource_id,
                    'title': r.title,
                    'category': r.category,
                    'owner_name': r.owner.name if r.owner else 'Unknown',
                    'booking_count': count
                }
                for r, count in results
            ]
            
        except Exception as e:
            raise AdminServiceError(f"Failed to get popular resources: {e}")
    
    @staticmethod
    def get_booking_trends(days: int = 30) -> Dict[str, Any]:
        """
        Get booking trends over specified time period.
        
        Args:
            days: Number of days to analyze (default 30)
        
        Returns:
            Dict with trend data
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Bookings by status in period
            trends = db.session.query(
                Booking.status,
                func.count(Booking.booking_id)
            ).filter(
                Booking.created_at >= cutoff_date
            ).group_by(Booking.status).all()
            
            # Total bookings in period
            total_in_period = db.session.query(func.count(Booking.booking_id)).filter(
                Booking.created_at >= cutoff_date
            ).scalar() or 0
            
            return {
                'period_days': days,
                'total_bookings': total_in_period,
                'by_status': {status: count for status, count in trends}
            }
            
        except Exception as e:
            raise AdminServiceError(f"Failed to get booking trends: {e}")

    @staticmethod
    def get_approvals_queue(limit: int = 10) -> List[Dict[str, Any]]:
        """Return pending bookings requiring admin approval."""
        try:
            rows = (
                db.session.query(Booking, Resource, User)
                    .join(Resource, Booking.resource_id == Resource.resource_id)
                    .join(User, Booking.requester_id == User.user_id)
                    .filter(Booking.status == 'pending')
                    .order_by(Booking.created_at.asc())
                    .limit(limit)
                    .all()
            )

            approvals = []
            for booking, resource, requester in rows:
                approvals.append(
                    {
                        'booking_id': booking.booking_id,
                        'resource_title': resource.title,
                        'resource_category': resource.category,
                        'requester_name': requester.name,
                        'requester_email': requester.email,
                        'start_datetime': booking.start_datetime,
                        'end_datetime': booking.end_datetime,
                        'created_at': booking.created_at,
                    }
                )
            return approvals
        except Exception as e:
            raise AdminServiceError(f"Failed to load approvals queue: {e}")

    @staticmethod
    def process_booking_approvals(booking_ids: List[int], action: str, admin_id: int) -> Dict[str, int]:
        """
        Bulk approve or reject bookings.
        Returns counts of processed and skipped bookings.
        """
        if not booking_ids:
            raise AdminServiceError("No bookings selected")
        if action not in {'approve', 'reject'}:
            raise AdminServiceError("Invalid action")

        try:
            bookings = Booking.query.filter(Booking.booking_id.in_(booking_ids)).all()
            processed = 0
            skipped = 0

            for booking in bookings:
                if booking.status != 'pending':
                    skipped += 1
                    continue

                if action == 'approve':
                    booking.approve()
                else:
                    booking.reject()
                processed += 1

            db.session.commit()
            return {'processed': processed, 'skipped': skipped, 'total': len(booking_ids)}
        except Exception as e:
            db.session.rollback()
            raise AdminServiceError(f"Failed to update approvals: {e}")

    @staticmethod
    def get_flagged_reviews(limit: int = 5) -> List[Dict[str, Any]]:
        """Return recently flagged/hidden reviews."""
        try:
            reviews = (
                Review.query.filter(Review.is_hidden == True)
                .order_by(Review.hidden_at.desc())
                .limit(limit)
                .all()
            )

            flagged = []
            for review in reviews:
                flagged.append(
                    {
                        'review_id': review.review_id,
                        'resource_title': review.resource.title if review.resource else 'Unknown resource',
                        'reviewer_name': review.reviewer.name if review.reviewer else 'Unknown user',
                        'rating': review.rating,
                        'comment': review.comment,
                        'hidden_reason': review.hidden_reason,
                        'hidden_at': review.hidden_at,
                        'resource_id': review.resource_id,
                    }
                )
            return flagged
        except Exception as e:
            raise AdminServiceError(f"Failed to load flagged reviews: {e}")

    @staticmethod
    def get_bookings_per_day(days: int = 14) -> Dict[str, Any]:
        """Return bookings per day over the provided window."""
        try:
            days = max(1, days)
            today = date.today()
            start_day = today - timedelta(days=days - 1)
            start_dt = datetime.combine(start_day, datetime.min.time())

            day_field = func.date(Booking.start_datetime)
            rows = (
                db.session.query(day_field.label('day'), func.count(Booking.booking_id))
                .filter(Booking.start_datetime >= start_dt)
                .group_by(day_field)
                .order_by(day_field)
                .all()
            )

            counts_map = {}
            for day_value, count in rows:
                if isinstance(day_value, str):
                    parsed_day = datetime.strptime(day_value, "%Y-%m-%d").date()
                elif isinstance(day_value, datetime):
                    parsed_day = day_value.date()
                else:
                    parsed_day = day_value
                counts_map[parsed_day] = count
            labels = []
            data = []
            for i in range(days):
                current_day = start_day + timedelta(days=i)
                labels.append(current_day.strftime('%b %d'))
                data.append(counts_map.get(current_day, 0))

            return {
                'labels': labels,
                'datasets': [
                    {
                        'label': 'Bookings per day',
                        'data': data,
                    }
                ],
            }
        except Exception as e:
            raise AdminServiceError(f"Failed to build booking timeline: {e}")

    @staticmethod
    def get_category_popularity(days: Optional[int] = None, limit: int = 6) -> Dict[str, Any]:
        """Return booking counts grouped by resource category."""
        try:
            query = (
                db.session.query(Resource.category, func.count(Booking.booking_id).label('count'))
                .join(Booking, Booking.resource_id == Resource.resource_id)
                .filter(Booking.status.in_(['approved', 'completed']))
            )

            if days:
                cutoff = datetime.utcnow() - timedelta(days=days)
                query = query.filter(Booking.created_at >= cutoff)

            rows = (
                query.group_by(Resource.category)
                .order_by(func.count(Booking.booking_id).desc())
                .limit(limit)
                .all()
            )

            if not rows:
                # Fallback to resource counts
                rows = (
                    db.session.query(Resource.category, func.count(Resource.resource_id))
                    .filter(Resource.status == 'published')
                    .group_by(Resource.category)
                    .order_by(func.count(Resource.resource_id).desc())
                    .limit(limit)
                    .all()
                )

            labels = []
            data = []
            for category, count in rows:
                labels.append((category or 'Uncategorized').replace('_', ' ').title())
                data.append(count)

            return {'labels': labels, 'datasets': [{'label': 'Bookings', 'data': data}]}
        except Exception as e:
            raise AdminServiceError(f"Failed to build category popularity: {e}")

    @staticmethod
    def get_utilization_summary() -> Dict[str, Any]:
        """Estimate resource utilization for analytics."""
        try:
            total_resources = db.session.query(func.count(Resource.resource_id)).scalar() or 0
            archived_resources = db.session.query(func.count(Resource.resource_id)).filter(
                Resource.status == 'archived'
            ).scalar() or 0
            booked_resources = (
                db.session.query(func.count(func.distinct(Booking.resource_id)))
                .filter(Booking.status.in_(['approved', 'completed']))
                .scalar()
                or 0
            )
            available_resources = max(total_resources - archived_resources - booked_resources, 0)

            return {
                'labels': ['Booked', 'Available', 'Archived'],
                'data': [booked_resources, available_resources, archived_resources],
            }
        except Exception as e:
            raise AdminServiceError(f"Failed to calculate utilization: {e}")

    @staticmethod
    def get_analytics_snapshot(period_days: int = 30) -> Dict[str, Any]:
        """Bundle analytics datasets for the analytics page."""
        try:
            bookings = AdminService.get_bookings_per_day(days=period_days)
            categories = AdminService.get_category_popularity(days=period_days)
            utilization = AdminService.get_utilization_summary()
            return {
                'period': period_days,
                'bookingsPerDay': bookings,
                'popularCategories': categories,
                'utilization': utilization,
            }
        except Exception as e:
            raise AdminServiceError(f"Failed to assemble analytics snapshot: {e}")

    @staticmethod
    def bulk_update_users(user_ids: List[int], action: str, admin_id: int) -> Dict[str, int]:
        """Suspend or activate many users at once."""
        if not user_ids:
            raise AdminServiceError("No users selected")
        if action not in {'suspend', 'activate'}:
            raise AdminServiceError("Invalid action")

        try:
            users = User.query.filter(User.user_id.in_(user_ids)).all()
            updated = 0
            skipped = 0

            for user in users:
                if user.role == 'admin' or user.user_id == admin_id:
                    skipped += 1
                    continue

                if action == 'suspend':
                    user.is_active = False
                    user.suspended_at = datetime.utcnow()
                else:
                    user.is_active = True
                    user.suspended_at = None
                updated += 1

            db.session.commit()
            return {'updated': updated, 'skipped': skipped, 'total': len(user_ids)}
        except Exception as e:
            db.session.rollback()
            raise AdminServiceError(f"Failed to update users: {e}")
