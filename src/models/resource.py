"""
Resource Model - Campus Resource Hub
Defines campus resources available for booking.

Per docs/ERD.md specifications and .clinerules architecture.
"""

from datetime import datetime
from typing import Optional, Dict, List
import json

from src.app import db


class Resource(db.Model):
    """
    Resource model for campus assets available for booking.

    Resource Types:
        - study_room: Study/meeting rooms
        - equipment: Laptops, projectors, cameras, etc.
        - lab: Laboratory spaces and instruments
        - space: Event spaces, auditoriums
        - tutoring: Tutoring time slots

    Lifecycle:
        - draft: Created but not published (owner-only visible)
        - published: Active and searchable
        - archived: Deactivated (admin-only, not bookable)

    Relationships:
        - owner: User who created this resource
        - bookings: All booking requests for this resource
        - reviews: All reviews for this resource
    """

    __tablename__ = "resources"

    # Primary Key
    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Resource Information
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    location = db.Column(db.String(200), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)

    # Images (JSON array of image paths)
    images = db.Column(db.Text, nullable=True)  # Stored as JSON string

    # Availability Rules (JSON object defining when resource is available)
    availability_rules = db.Column(db.Text, nullable=True)  # Stored as JSON string

    # Status
    status = db.Column(db.String(20), nullable=False, default="draft", index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    owner = db.relationship("User", back_populates="resources", foreign_keys=[owner_id])

    bookings = db.relationship(
        "Booking", back_populates="resource", lazy="dynamic", cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review", back_populates="resource", lazy="dynamic", cascade="all, delete-orphan"
    )

    # Constraints
    CATEGORY_CHOICES = ("study_room", "equipment", "lab", "space", "tutoring")
    CATEGORY_ALIASES = {
        "meeting_room": "study_room",
        "conference_room": "study_room",
        "study_room": "study_room",
        "studyspace": "study_room",
        "equipment": "equipment",
        "technology": "equipment",
        "tech": "equipment",
        "lab": "lab",
        "laboratory": "lab",
        "event": "space",
        "event_space": "space",
        "space": "space",
        "tutoring": "tutoring",
    }

    __table_args__ = (
        db.CheckConstraint(
            status.in_(["draft", "published", "archived"]), name="check_valid_status"
        ),
        db.CheckConstraint(category.in_(CATEGORY_CHOICES), name="check_valid_category"),
    )

    def __init__(
        self,
        owner_id: int,
        title: str,
        category: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        capacity: Optional[int] = None,
        images: Optional[List[str]] = None,
        availability_rules: Optional[Dict] = None,
        status: str = "draft",
    ):
        """
        Initialize a new Resource.

        Args:
            owner_id: ID of user who owns this resource
            title: Resource name/title
            category: Resource category
            description: Detailed description
            location: Physical location
            capacity: Maximum number of users
            images: List of image paths
            availability_rules: Dict defining when resource is available
            status: Resource status (draft/published/archived)
        """
        self.owner_id = owner_id
        self.title = title
        self.category = self._normalize_category(category)
        self.description = description
        self.location = location
        self.capacity = capacity
        self.set_images(images or [])
        self.set_availability_rules(availability_rules or {})
        self.status = status

    def set_images(self, images: List[str]) -> None:
        """
        Set resource images as JSON string.

        Args:
            images: List of image file paths
        """
        self.images = json.dumps(images) if images else None

    def get_images(self) -> List[str]:
        """
        Parse and return list of image paths.

        Returns:
            List of image paths, empty list if none
        """
        if not self.images:
            return []
        try:
            return json.loads(self.images)
        except json.JSONDecodeError:
            return []

    def add_image(self, image_path: str) -> None:
        """Add an image to the resource."""
        images = self.get_images()
        if image_path not in images:
            images.append(image_path)
            self.set_images(images)

    def remove_image(self, image_path: str) -> None:
        """Remove an image from the resource."""
        images = self.get_images()
        if image_path in images:
            images.remove(image_path)
            self.set_images(images)

    def set_availability_rules(self, rules: Dict) -> None:
        """
        Set availability rules as JSON string.

        Example rules format:
        {
            "days": ["monday", "tuesday", "wednesday"],
            "hours": {"start": "08:00", "end": "18:00"},
            "requires_approval": True,
            "max_booking_hours": 4
        }

        Args:
            rules: Dictionary of availability rules
        """
        self.availability_rules = json.dumps(rules) if rules else None

    def get_availability_rules(self) -> Dict:
        """
        Parse and return availability rules.

        Returns:
            Dictionary of availability rules, empty dict if none
        """
        if not self.availability_rules:
            return {}
        try:
            return json.loads(self.availability_rules)
        except json.JSONDecodeError:
            return {}

    def requires_approval(self) -> bool:
        """Check if resource requires booking approval."""
        rules = self.get_availability_rules()
        return rules.get("requires_approval", False)

    @classmethod
    def _normalize_category(cls, value: str) -> str:
        """
        Normalize incoming category strings to allowed slugs.

        Args:
            value: Raw category value from forms/tests

        Returns:
            Canonical slug defined in CATEGORY_CHOICES
        """
        if not value:
            return "space"

        slug = value.strip().lower().replace(" ", "_")
        canonical = cls.CATEGORY_ALIASES.get(slug, slug)
        return canonical if canonical in cls.CATEGORY_CHOICES else "space"

    def is_published(self) -> bool:
        """Check if resource is published and visible."""
        return self.status == "published"

    def is_draft(self) -> bool:
        """Check if resource is in draft status."""
        return self.status == "draft"

    def is_archived(self) -> bool:
        """Check if resource is archived."""
        return self.status == "archived"

    def publish(self) -> None:
        """Publish the resource (make it searchable and bookable)."""
        self.status = "published"
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Archive the resource (hide from search, not bookable)."""
        self.status = "archived"
        self.updated_at = datetime.utcnow()

    def unarchive(self) -> None:
        """Restore archived resource to published status."""
        self.status = "published"
        self.updated_at = datetime.utcnow()

    def get_average_rating(self) -> Optional[float]:
        """
        Calculate average rating from reviews.

        Returns:
            Average rating (1-5) or None if no reviews
        """
        reviews_list = self.reviews.all()
        if not reviews_list:
            return None

        total = sum(review.rating for review in reviews_list)
        return round(total / len(reviews_list), 1)

    def get_review_count(self) -> int:
        """Get total number of reviews."""
        return self.reviews.count()

    def get_booking_count(self) -> int:
        """Get total number of bookings (all statuses)."""
        return self.bookings.count()

    def __repr__(self) -> str:
        """String representation of Resource."""
        return f"<Resource {self.resource_id}: {self.title} ({self.category})>"

    def to_dict(self, include_reviews: bool = False) -> Dict:
        """
        Convert resource to dictionary (for JSON responses).

        Args:
            include_reviews: Whether to include review summaries

        Returns:
            Dictionary representation of resource
        """
        data = {
            "resource_id": self.resource_id,
            "owner_id": self.owner_id,
            "owner_name": self.owner.name if self.owner else None,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "location": self.location,
            "capacity": self.capacity,
            "images": self.get_images(),
            "availability_rules": self.get_availability_rules(),
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_reviews:
            data["average_rating"] = self.get_average_rating()
            data["review_count"] = self.get_review_count()
            data["booking_count"] = self.get_booking_count()

        return data
