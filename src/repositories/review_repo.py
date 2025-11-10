"""
Review Repository - Campus Resource Hub
Data Access Layer for Review model.
"""

from typing import List, Optional, Dict
from src.models import db, Review


class ReviewRepository:
    """Repository for Review model CRUD operations."""

    @staticmethod
    def create(
        resource_id: int,
        reviewer_id: int,
        rating: int,
        comment: Optional[str] = None,
        booking_id: Optional[int] = None,
    ) -> Review:
        """Create a new review."""
        review = Review(
            resource_id=resource_id,
            reviewer_id=reviewer_id,
            rating=rating,
            comment=comment,
            booking_id=booking_id,
        )
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def get_by_id(review_id: int) -> Optional[Review]:
        """Get review by ID."""
        return Review.query.get(review_id)

    @staticmethod
    def get_by_resource(resource_id: int, include_hidden: bool = False) -> List[Review]:
        """Get all reviews for a resource."""
        query = Review.query.filter_by(resource_id=resource_id)
        if not include_hidden:
            query = query.filter_by(is_hidden=False)
        return query.order_by(Review.timestamp.desc()).all()

    @staticmethod
    def get_by_reviewer(reviewer_id: int) -> List[Review]:
        """Get all reviews by a user."""
        return (
            Review.query.filter_by(reviewer_id=reviewer_id).order_by(Review.timestamp.desc()).all()
        )

    @staticmethod
    def get_by_resource_and_reviewer(resource_id: int, reviewer_id: int) -> Optional[Review]:
        """Return a single review for a resource by the specified reviewer."""
        return Review.query.filter_by(resource_id=resource_id, reviewer_id=reviewer_id).first()

    @staticmethod
    def get_all(page: int = 1, per_page: int = 50, include_hidden: bool = False) -> Dict:
        """Get all reviews with pagination."""
        query = Review.query
        if not include_hidden:
            query = query.filter_by(is_hidden=False)

        paginated = query.order_by(Review.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return {
            "items": paginated.items,
            "total": paginated.total,
            "page": paginated.page,
            "per_page": paginated.per_page,
            "pages": paginated.pages,
        }

    @staticmethod
    def update(
        review_id: int, rating: Optional[int] = None, comment: Optional[str] = None
    ) -> Optional[Review]:
        """Update review rating and/or comment."""
        review = Review.query.get(review_id)
        if not review:
            return None

        if rating is not None:
            review.update_rating(rating)
        if comment is not None:
            review.update_comment(comment)

        db.session.commit()
        return review

    @staticmethod
    def delete(review_id: int) -> bool:
        """Delete review."""
        review = Review.query.get(review_id)
        if not review:
            return False

        db.session.delete(review)
        db.session.commit()
        return True

    @staticmethod
    def hide(review_id: int, admin_id: int, reason: str) -> Optional[Review]:
        """Hide review (admin moderation)."""
        review = Review.query.get(review_id)
        if not review:
            return None

        review.hide(admin_id, reason)
        db.session.commit()
        return review

    @staticmethod
    def unhide(review_id: int) -> Optional[Review]:
        """Unhide review."""
        review = Review.query.get(review_id)
        if not review:
            return None

        review.unhide()
        db.session.commit()
        return review

    @staticmethod
    def get_average_rating(resource_id: int) -> Optional[float]:
        """Get average rating for a resource."""
        reviews = ReviewRepository.get_by_resource(resource_id, include_hidden=False)
        if not reviews:
            return None

        total = sum(r.rating for r in reviews)
        return round(total / len(reviews), 1)

    @staticmethod
    def count_by_resource(resource_id: int) -> int:
        """Count reviews for a resource."""
        return Review.query.filter_by(resource_id=resource_id, is_hidden=False).count()
