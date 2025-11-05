"""
User Repository - Campus Resource Hub
Data Access Layer for User model.

Per .clinerules: All database operations encapsulated in repositories.
No SQL queries should exist outside this layer.
"""

from typing import List, Optional, Dict
from sqlalchemy import or_
from src.models import db, User


class UserRepository:
    """
    Repository for User model CRUD operations.

    Provides typed, tested database operations for user management.
    """

    @staticmethod
    def create(
        name: str,
        email: str,
        password: str,
        role: str = "student",
        department: Optional[str] = None,
        profile_image: Optional[str] = None,
    ) -> User:
        """
        Create a new user.

        Args:
            name: Full name
            email: Email address (must be unique)
            password: Plain text password (will be hashed)
            role: User role (student/staff/admin)
            department: Department affiliation
            profile_image: Path to profile image

        Returns:
            Created User instance
        """
        user = User(
            name=name,
            email=email.lower(),
            password=password,
            role=role,
            department=department,
            profile_image=profile_image,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """Get user by ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get user by email address."""
        return User.query.filter_by(email=email.lower()).first()

    @staticmethod
    def get_all(page: int = 1, per_page: int = 50, role: Optional[str] = None) -> Dict:
        """
        Get all users with pagination.

        Args:
            page: Page number (1-indexed)
            per_page: Items per page
            role: Optional role filter

        Returns:
            Dict with 'items', 'total', 'page', 'per_page', 'pages'
        """
        query = User.query

        if role:
            query = query.filter_by(role=role)

        query = query.order_by(User.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": paginated.items,
            "total": paginated.total,
            "page": paginated.page,
            "per_page": paginated.per_page,
            "pages": paginated.pages,
        }

    @staticmethod
    def search(query: str, page: int = 1, per_page: int = 50) -> Dict:
        """
        Search users by name or email.

        Args:
            query: Search query string
            page: Page number
            per_page: Items per page

        Returns:
            Paginated search results
        """
        search_filter = or_(User.name.ilike(f"%{query}%"), User.email.ilike(f"%{query}%"))

        paginated = (
            User.query.filter(search_filter)
            .order_by(User.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            "items": paginated.items,
            "total": paginated.total,
            "page": paginated.page,
            "per_page": paginated.per_page,
            "pages": paginated.pages,
        }

    @staticmethod
    def update(user_id: int, **kwargs) -> Optional[User]:
        """
        Update user fields.

        Args:
            user_id: User ID to update
            **kwargs: Fields to update

        Returns:
            Updated User instance or None if not found
        """
        user = User.query.get(user_id)
        if not user:
            return None

        # Allow updating specific fields
        allowed_fields = ["name", "email", "department", "profile_image", "role"]
        for field in allowed_fields:
            if field in kwargs:
                setattr(user, field, kwargs[field])

        db.session.commit()
        return user

    @staticmethod
    def delete(user_id: int) -> bool:
        """
        Delete user by ID.

        Args:
            user_id: User ID to delete

        Returns:
            True if deleted, False if not found
        """
        user = User.query.get(user_id)
        if not user:
            return False

        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def suspend(user_id: int) -> Optional[User]:
        """Suspend user account."""
        user = User.query.get(user_id)
        if not user:
            return None

        user.suspend()
        db.session.commit()
        return user

    @staticmethod
    def reactivate(user_id: int) -> Optional[User]:
        """Reactivate suspended user account."""
        user = User.query.get(user_id)
        if not user:
            return None

        user.reactivate()
        db.session.commit()
        return user

    @staticmethod
    def get_by_role(role: str) -> List[User]:
        """Get all users with specific role."""
        return User.query.filter_by(role=role).all()

    @staticmethod
    def count() -> int:
        """Get total number of users."""
        return User.query.count()

    @staticmethod
    def count_by_role(role: str) -> int:
        """Get count of users with specific role."""
        return User.query.filter_by(role=role).count()
