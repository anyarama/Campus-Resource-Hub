"""
Resource Repository - Campus Resource Hub
Data Access Layer for Resource model.

Per .clinerules: All database operations encapsulated in repositories.
"""

from typing import List, Optional, Dict, Sequence, Union, Any
from sqlalchemy import or_, func
from datetime import datetime
from src.models import db, Resource, Booking


class ResourceRepository:
    """Repository for Resource model CRUD operations."""

    @staticmethod
    def create(
        owner_id: Optional[int] = None,
        title: Optional[str] = None,
        category: Optional[str] = None,
        resource: Optional[Resource] = None,
        **kwargs: Any,
    ) -> Resource:
        """
        Create a new resource.

        Accepts either a fully-instantiated Resource model (via positional argument or explicit
        `resource=` kwarg) or the primitive fields used to build one.
        """
        resource_model: Optional[Resource] = None

        if resource is not None:
            resource_model = resource
        elif isinstance(owner_id, Resource):
            resource_model = owner_id
        else:
            if owner_id is None or title is None or category is None:
                raise ValueError(
                    "owner_id, title, and category are required when creating a resource"
                )
            resource_model = Resource(
                owner_id=owner_id,
                title=title,
                category=category,
                description=kwargs.get("description"),
                location=kwargs.get("location"),
                capacity=kwargs.get("capacity"),
                images=kwargs.get("images", []),
                availability_rules=kwargs.get("availability_rules", {}),
                status=kwargs.get("status", "draft"),
            )
        db.session.add(resource_model)
        db.session.commit()
        return resource_model

    @staticmethod
    def get_by_id(resource_id: int) -> Optional[Resource]:
        """Get resource by ID."""
        return Resource.query.get(resource_id)

    @staticmethod
    def get_all(
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None,
        category: Optional[str] = None,
        owner_id: Optional[int] = None,
    ) -> Dict:
        """Get all resources with pagination and filters."""
        query = Resource.query

        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)
        if owner_id:
            query = query.filter_by(owner_id=owner_id)

        query = query.order_by(Resource.created_at.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": paginated.items,
            "total": paginated.total,
            "page": paginated.page,
            "per_page": paginated.per_page,
            "pages": paginated.pages,
        }

    @staticmethod
    def search(
        query_str: Optional[str] = None,
        page: int = 1,
        per_page: int = 50,
        category: Optional[str] = None,
        location: Optional[str] = None,
        status: Optional[str] = None,
        categories: Optional[Sequence[str]] = None,
        locations: Optional[Sequence[str]] = None,
        statuses: Optional[Sequence[str]] = None,
        capacity_min: Optional[int] = None,
        capacity_max: Optional[int] = None,
        availability_start: Optional[datetime] = None,
        availability_end: Optional[datetime] = None,
        sort: Optional[str] = None,
    ) -> List[Resource]:
        """
        Search resources by title, description, or location.

        Note: Returns list for backward compatibility with routes/resources.py
        """
        query = Resource.query

        # Apply status filter (default to published if not specified)
        if statuses:
            query = query.filter(Resource.status.in_(statuses))
        elif status:
            query = query.filter_by(status=status)
        else:
            query = query.filter(Resource.status == "published")

        # Apply search filter if query string provided
        if query_str:
            search_filter = or_(
                Resource.title.ilike(f"%{query_str}%"),
                Resource.description.ilike(f"%{query_str}%"),
                Resource.location.ilike(f"%{query_str}%"),
            )
            query = query.filter(search_filter)

        # Apply category filter (single or multiple)
        if categories:
            query = query.filter(Resource.category.in_(categories))
        elif category:
            query = query.filter_by(category=category)

        # Apply location filter (single or multiple, partial match)
        if locations:
            location_filters = [Resource.location.ilike(f"%{loc}%") for loc in locations if loc]
            if location_filters:
                query = query.filter(or_(*location_filters))
        elif location:
            query = query.filter(Resource.location.ilike(f"%{location}%"))

        # Capacity range filters
        if capacity_min is not None:
            query = query.filter(Resource.capacity >= capacity_min)
        if capacity_max is not None:
            query = query.filter(Resource.capacity <= capacity_max)

        # Availability window filter (exclude resources with approved bookings overlapping window)
        if availability_start or availability_end:
            start = availability_start or availability_end
            end = availability_end or availability_start
            if start and end and end < start:
                start, end = end, start

            if start and end:
                conflicts = (
                    db.session.query(Booking.resource_id)
                    .filter(Booking.status == "approved")
                    .filter(Booking.start_datetime < end)
                    .filter(Booking.end_datetime > start)
                )
                query = query.filter(~Resource.resource_id.in_(conflicts))

        # Base ordering (defaults to newest first)
        if sort == "created_asc":
            query = query.order_by(Resource.created_at.asc())
        elif sort == "title_asc":
            query = query.order_by(Resource.title.asc())
        elif sort == "title_desc":
            query = query.order_by(Resource.title.desc())
        else:
            query = query.order_by(Resource.created_at.desc())

        results = query.all()

        # Derived sorting (rating/popularity) happens in Python since it depends on relationships
        if sort == "rating_desc":
            results.sort(
                key=lambda r: (r.get_average_rating() or 0, r.get_review_count()), reverse=True
            )
        elif sort == "popular":
            results.sort(key=lambda r: r.get_booking_count(), reverse=True)

        return results

    @staticmethod
    def update(resource_or_id: Union[Resource, int], **kwargs: Any) -> Optional[Resource]:
        """Update resource fields."""
        resource = (
            resource_or_id
            if isinstance(resource_or_id, Resource)
            else Resource.query.get(resource_or_id)
        )
        if not resource:
            return None

        allowed_fields = ["title", "description", "category", "location", "capacity", "status"]
        for field in allowed_fields:
            if field in kwargs:
                setattr(resource, field, kwargs[field])

        if "images" in kwargs:
            resource.set_images(kwargs["images"])
        if "availability_rules" in kwargs:
            resource.set_availability_rules(kwargs["availability_rules"])

        resource.updated_at = datetime.utcnow()
        db.session.commit()
        return resource

    @staticmethod
    def delete(resource_id: int) -> bool:
        """Delete resource by ID."""
        resource = Resource.query.get(resource_id)
        if not resource:
            return False

        db.session.delete(resource)
        db.session.commit()
        return True

    @staticmethod
    def get_by_category(category: str, status: str = "published") -> List[Resource]:
        """Get all resources in a category."""
        return Resource.query.filter_by(category=category, status=status).all()

    @staticmethod
    def get_by_owner(owner_id: int) -> List[Resource]:
        """Get all resources owned by user."""
        return Resource.query.filter_by(owner_id=owner_id).all()

    @staticmethod
    def count() -> int:
        """Get total number of resources."""
        return Resource.query.count()

    @staticmethod
    def count_by_status(status: str) -> int:
        """Get count of resources by status."""
        return Resource.query.filter_by(status=status).count()

    @staticmethod
    def get_location_facets(status: Optional[str] = "published") -> List[Dict[str, object]]:
        """
        Return distinct locations with counts for filter drawer.

        Args:
            status: Filter resources by status (default: published)
        """
        query = (
            db.session.query(
                Resource.location,
                func.count(Resource.resource_id).label("count"),
            )
            .filter(Resource.location.isnot(None))
            .filter(Resource.location != "")
        )

        if status:
            query = query.filter(Resource.status == status)

        rows = (
            query.group_by(Resource.location)
            .order_by(func.count(Resource.resource_id).desc())
            .all()
        )

        return [
            {
                "label": location,
                "count": count,
            }
            for location, count in rows
        ]
