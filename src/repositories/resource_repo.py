"""
Resource Repository - Campus Resource Hub
Data Access Layer for Resource model.

Per .clinerules: All database operations encapsulated in repositories.
"""

from typing import List, Optional, Dict
from sqlalchemy import or_
from datetime import datetime
from src.models import db, Resource


class ResourceRepository:
    """Repository for Resource model CRUD operations."""

    @staticmethod
    def create(owner_id: int, title: str, category: str, **kwargs) -> Resource:
        """Create a new resource."""
        resource = Resource(
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
        db.session.add(resource)
        db.session.commit()
        return resource

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
        query_str: str, page: int = 1, per_page: int = 50, category: Optional[str] = None
    ) -> Dict:
        """Search resources by title, description, or location."""
        search_filter = or_(
            Resource.title.ilike(f"%{query_str}%"),
            Resource.description.ilike(f"%{query_str}%"),
            Resource.location.ilike(f"%{query_str}%"),
        )

        query = Resource.query.filter(search_filter, Resource.status == "published")

        if category:
            query = query.filter_by(category=category)

        paginated = query.order_by(Resource.created_at.desc()).paginate(
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
    def update(resource_id: int, **kwargs) -> Optional[Resource]:
        """Update resource fields."""
        resource = Resource.query.get(resource_id)
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
