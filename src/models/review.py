"""
Review Model - Campus Resource Hub
Defines ratings and feedback for resources after booking completion.

Per docs/ERD.md specifications and .clinerules architecture.
"""

from datetime import datetime
from typing import Optional, Dict

from src.app import db


class Review(db.Model):
    """
    Review model for resource ratings and feedback.

    Authorization:
        - Users can only review resources they have completed bookings for
        - One review per user per resource (enforced by UNIQUE constraint)
        - Admin can moderate/remove inappropriate reviews

    Rating Scale:
        1 = Poor
        2 = Fair
        3 = Good
        4 = Very Good
        5 = Excellent

    Use Cases:
        - Post-booking feedback
        - Quality assurance for resource owners
        - Help other users make informed booking decisions
        - Identify highly-rated resources for featured listings

    Relationships:
        - resource: The resource being reviewed
        - reviewer: User who wrote the review
        - booking: Optional link to completed booking that enabled review
    """

    __tablename__ = "reviews"

    # Primary Key
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resources.resource_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reviewer_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Optional: Link to booking that enabled this review
    booking_id = db.Column(
        db.Integer, db.ForeignKey("bookings.booking_id", ondelete="SET NULL"), nullable=True
    )

    # Review Content
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    # Timestamp
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Moderation (for admin oversight)
    is_hidden = db.Column(db.Boolean, default=False, nullable=False)
    hidden_reason = db.Column(db.String(200), nullable=True)
    hidden_at = db.Column(db.DateTime, nullable=True)
    hidden_by = db.Column(
        db.Integer, db.ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    resource = db.relationship("Resource", back_populates="reviews", foreign_keys=[resource_id])

    reviewer = db.relationship("User", back_populates="reviews", foreign_keys=[reviewer_id])

    booking = db.relationship("Booking", foreign_keys=[booking_id])

    moderator = db.relationship("User", foreign_keys=[hidden_by])

    # Constraints
    __table_args__ = (
        db.CheckConstraint("rating BETWEEN 1 AND 5", name="check_rating_range"),
        db.UniqueConstraint("resource_id", "reviewer_id", name="unique_review_per_user_resource"),
        db.Index("idx_reviews_resource_reviewer", "resource_id", "reviewer_id"),
    )

    def __init__(
        self,
        resource_id: int,
        reviewer_id: int,
        rating: int,
        comment: Optional[str] = None,
        booking_id: Optional[int] = None,
    ):
        """
        Initialize a new Review.

        Args:
            resource_id: ID of resource being reviewed
            reviewer_id: ID of user writing the review
            rating: Star rating (1-5)
            comment: Optional written feedback
            booking_id: Optional ID of completed booking

        Raises:
            ValueError: If rating is not between 1 and 5
        """
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.resource_id = resource_id
        self.reviewer_id = reviewer_id
        self.rating = rating
        self.comment = comment.strip() if comment else None
        self.booking_id = booking_id

    def is_visible(self) -> bool:
        """Check if review is visible to users (not hidden by admin)."""
        return not self.is_hidden

    def hide(self, admin_id: int, reason: str) -> None:
        """
        Hide review from public view (admin moderation).

        Args:
            admin_id: ID of admin hiding the review
            reason: Reason for hiding (e.g., "Inappropriate language")
        """
        self.is_hidden = True
        self.hidden_reason = reason
        self.hidden_at = datetime.utcnow()
        self.hidden_by = admin_id

    def unhide(self) -> None:
        """Restore hidden review to public view."""
        self.is_hidden = False
        self.hidden_reason = None
        self.hidden_at = None
        self.hidden_by = None

    def get_star_display(self) -> str:
        """
        Get visual star representation of rating.

        Returns:
            String like "★★★★☆" for 4-star rating
        """
        filled = "★" * self.rating
        empty = "☆" * (5 - self.rating)
        return filled + empty

    def has_comment(self) -> bool:
        """Check if review includes written comment."""
        return bool(self.comment and self.comment.strip())

    def get_age_days(self) -> int:
        """
        Calculate how many days ago review was posted.

        Returns:
            Age in days
        """
        delta = datetime.utcnow() - self.timestamp
        return delta.days

    def is_recent(self, days: int = 7) -> bool:
        """
        Check if review was posted within the last N days.

        Args:
            days: Time threshold in days

        Returns:
            True if review is recent, False otherwise
        """
        return self.get_age_days() < days

    def can_be_edited_by(self, user_id: int) -> bool:
        """
        Check if user can edit this review.

        Only reviewer can edit within 24 hours of posting.

        Args:
            user_id: ID of user attempting to edit

        Returns:
            True if user can edit, False otherwise
        """
        if user_id != self.reviewer_id:
            return False

        # Allow editing within 24 hours
        hours_since_posting = (datetime.utcnow() - self.timestamp).total_seconds() / 3600
        return hours_since_posting < 24

    def update_rating(self, new_rating: int) -> None:
        """
        Update review rating.

        Args:
            new_rating: New star rating (1-5)

        Raises:
            ValueError: If rating is not between 1 and 5
        """
        if not (1 <= new_rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.rating = new_rating

    def update_comment(self, new_comment: Optional[str]) -> None:
        """Update review comment."""
        self.comment = new_comment.strip() if new_comment else None

    def __repr__(self) -> str:
        """String representation of Review."""
        stars = self.get_star_display()
        return (
            f"<Review {self.review_id}: "
            f"Resource={self.resource_id} "
            f"Reviewer={self.reviewer_id} "
            f"{stars}>"
        )

    def to_dict(self, include_relations: bool = False) -> Dict:
        """
        Convert review to dictionary (for JSON responses).

        Args:
            include_relations: Whether to include related resource/user info

        Returns:
            Dictionary representation of review
        """
        data = {
            "review_id": self.review_id,
            "resource_id": self.resource_id,
            "reviewer_id": self.reviewer_id,
            "rating": self.rating,
            "comment": self.comment,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "is_hidden": self.is_hidden,
            "age_days": self.get_age_days(),
            "is_recent": self.is_recent(),
            "star_display": self.get_star_display(),
        }

        if include_relations:
            if self.resource:
                data["resource_title"] = self.resource.title
                data["resource_category"] = self.resource.category

            if self.reviewer:
                data["reviewer_name"] = self.reviewer.name
                data["reviewer_profile_image"] = self.reviewer.profile_image

        # Only include moderation info if review is hidden
        if self.is_hidden:
            data["hidden_reason"] = self.hidden_reason
            data["hidden_at"] = self.hidden_at.isoformat() if self.hidden_at else None

        return data


class ReviewAggregate:
    """
    Helper class for calculating review statistics.

    This is not a model, but a utility class for working with
    aggregated review data for resources.
    """

    def __init__(self, reviews: list):
        """
        Initialize review aggregate.

        Args:
            reviews: List of Review objects
        """
        self.reviews = reviews
        self.visible_reviews = [r for r in reviews if r.is_visible()]

    def get_average_rating(self) -> Optional[float]:
        """Calculate average rating from visible reviews."""
        if not self.visible_reviews:
            return None

        total = sum(r.rating for r in self.visible_reviews)
        return round(total / len(self.visible_reviews), 1)

    def get_total_count(self) -> int:
        """Get total number of visible reviews."""
        return len(self.visible_reviews)

    def get_rating_distribution(self) -> Dict[int, int]:
        """
        Get count of reviews for each rating level.

        Returns:
            Dict like {5: 10, 4: 5, 3: 2, 2: 1, 1: 0}
        """
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for review in self.visible_reviews:
            distribution[review.rating] += 1
        return distribution

    def get_rating_percentages(self) -> Dict[int, float]:
        """
        Get percentage of reviews for each rating level.

        Returns:
            Dict like {5: 50.0, 4: 25.0, 3: 10.0, 2: 5.0, 1: 0.0}
        """
        distribution = self.get_rating_distribution()
        total = self.get_total_count()

        if total == 0:
            return {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0}

        return {rating: round((count / total) * 100, 1) for rating, count in distribution.items()}

    def has_reviews(self) -> bool:
        """Check if there are any visible reviews."""
        return len(self.visible_reviews) > 0

    def __repr__(self) -> str:
        """String representation of ReviewAggregate."""
        avg = self.get_average_rating()
        count = self.get_total_count()
        return f"<ReviewAggregate: {count} reviews, avg={avg}>"
