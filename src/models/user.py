"""
User Model - Campus Resource Hub
Defines the User entity for authentication and RBAC.

Per docs/ERD.md specifications and .clinerules architecture.
"""

from datetime import datetime
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src.app import db


class User(UserMixin, db.Model):
    """
    User model for authentication and role-based access control.

    Roles:
        - student: Basic user, can book resources and create listings
        - staff: Enhanced permissions, can approve restricted resources
        - admin: Full system access, moderation, analytics

    Relationships:
        - resources: Resources owned by this user
        - bookings: Booking requests made by this user
        - sent_messages: Messages sent by this user
        - received_messages: Messages received by this user
        - reviews: Reviews written by this user
        - admin_logs: Admin actions performed by this user
    """

    __tablename__ = "users"

    # Primary Key
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Basic Information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Role and Profile
    role = db.Column(db.String(20), nullable=False, default="student", index=True)
    profile_image = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(100), nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Account Status (for suspension)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    suspended_at = db.Column(db.DateTime, nullable=True)

    # Relationships (defined with lazy='dynamic' for query efficiency)
    resources = db.relationship(
        "Resource", back_populates="owner", lazy="dynamic", foreign_keys="Resource.owner_id"
    )

    bookings = db.relationship(
        "Booking", back_populates="requester", lazy="dynamic", foreign_keys="Booking.requester_id"
    )

    sent_messages = db.relationship(
        "Message", back_populates="sender", lazy="dynamic", foreign_keys="Message.sender_id"
    )

    received_messages = db.relationship(
        "Message", back_populates="receiver", lazy="dynamic", foreign_keys="Message.receiver_id"
    )

    reviews = db.relationship(
        "Review", back_populates="reviewer", lazy="dynamic", foreign_keys="Review.reviewer_id"
    )

    # Note: admin_logs relationship will be added when AdminLog model is created (Phase 4)
    # admin_logs = db.relationship(
    #     "AdminLog", back_populates="admin", lazy="dynamic", foreign_keys="AdminLog.admin_id"
    # )

    # Constraints
    __table_args__ = (
        db.CheckConstraint(role.in_(["student", "staff", "admin"]), name="check_valid_role"),
    )

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "student",
        department: Optional[str] = None,
        profile_image: Optional[str] = None,
    ):
        """
        Initialize a new User.

        Args:
            name: User's full name
            email: Unique email address
            password: Plain text password (will be hashed)
            role: User role (student/staff/admin)
            department: Department affiliation
            profile_image: Path to profile image
        """
        self.name = name
        self.email = email.lower()  # Normalize email
        self.set_password(password)
        self.role = role
        self.department = department
        self.profile_image = profile_image

    def set_password(self, password: str) -> None:
        """
        Hash and store password using bcrypt.

        Per .clinerules security: passwords NEVER stored in plaintext.
        Uses bcrypt with 12 rounds (secure default).

        Args:
            password: Plain text password to hash
        """
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        """
        Verify password against stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def is_student(self) -> bool:
        """Check if user has student role."""
        return self.role == "student"

    def is_staff(self) -> bool:
        """Check if user has staff role."""
        return self.role == "staff"

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == "admin"

    def can_approve_bookings(self) -> bool:
        """Check if user can approve booking requests."""
        return self.role in ["staff", "admin"]

    def can_moderate_content(self) -> bool:
        """Check if user can moderate reviews/resources."""
        return self.role == "admin"

    def suspend(self) -> None:
        """Suspend user account (admin action)."""
        self.is_active = False
        self.suspended_at = datetime.utcnow()

    def reactivate(self) -> None:
        """Reactivate suspended user account."""
        self.is_active = True
        self.suspended_at = None

    # Flask-Login required methods
    def get_id(self) -> str:
        """Return user ID as string for Flask-Login."""
        return str(self.user_id)

    @property
    def is_authenticated(self) -> bool:
        """Return True if user is authenticated."""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Return False as user is not anonymous."""
        return False

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User {self.user_id}: {self.email} ({self.role})>"

    def to_dict(self) -> dict:
        """
        Convert user to dictionary (for JSON responses).

        Note: Does NOT include password_hash for security.
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "department": self.department,
            "profile_image": self.profile_image,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active,
        }
