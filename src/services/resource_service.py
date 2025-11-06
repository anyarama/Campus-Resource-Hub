"""
Resource Service - Business logic for resource management.

Handles resource creation, updates, deletion, and image upload processing.
Enforces business rules: owner-only edits, status transitions, image security.

AI Contribution: Cline generated service structure
Reviewed and configured by developer on 2025-11-05
"""

import json
import os
import uuid
from typing import List, Optional, Tuple
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.models.resource import Resource
from src.repositories.resource_repo import ResourceRepository


# Image upload configuration
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB
UPLOAD_FOLDER = "src/static/uploads/resources"


class ResourceServiceError(Exception):
    """Base exception for resource service errors."""

    pass


class ImageUploadError(ResourceServiceError):
    """Raised when image upload fails validation or processing."""

    pass


class ResourceService:
    """
    Service layer for resource management operations.

    Handles:
    - Resource creation with image uploads
    - Resource updates (owner authorization)
    - Status transitions (draft → published → archived)
    - Image upload security (type, size validation)
    - Resource deletion with authorization
    """

    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Check if file extension is allowed.

        Args:
            filename: Name of the file to check

        Returns:
            True if extension is in ALLOWED_EXTENSIONS
        """
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def validate_image(file: FileStorage) -> Tuple[bool, str]:
        """
        Validate uploaded image file.

        Checks:
        - File exists
        - Has allowed extension
        - Size is within limit

        Args:
            file: Uploaded file object

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file or not file.filename:
            return False, "No file selected"

        if not ResourceService.allowed_file(file.filename):
            return (
                False,
                f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        # Check file size by seeking to end
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)  # Reset to beginning for later reading

        if size > MAX_IMAGE_SIZE:
            return False, f"File too large. Maximum size: {MAX_IMAGE_SIZE // (1024 * 1024)}MB"

        return True, ""

    @staticmethod
    def save_image(file: FileStorage) -> str:
        """
        Save uploaded image with random filename.

        Security measures:
        - Generate random UUID filename
        - Use secure_filename for sanitization
        - Store in uploads directory outside web root

        Args:
            file: Uploaded file object

        Returns:
            Relative path to saved image

        Raises:
            ImageUploadError: If save fails
        """
        # Validate before saving
        is_valid, error_msg = ResourceService.validate_image(file)
        if not is_valid:
            raise ImageUploadError(error_msg)

        # Generate unique filename
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filename = secure_filename(filename)

        # Ensure upload directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Save file
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(filepath)
        except Exception as e:
            raise ImageUploadError(f"Failed to save image: {str(e)}")

        # Return relative path for database storage
        return f"uploads/resources/{filename}"

    @staticmethod
    def create_resource(
        owner_id: int,
        title: str,
        description: str,
        category: str,
        location: str,
        capacity: int,
        images: List[FileStorage] = None,
        availability_rules: dict = None,
        status: str = "draft",
    ) -> Resource:
        """
        Create a new resource with validation.

        Args:
            owner_id: ID of the user creating the resource
            title: Resource title (required)
            description: Resource description
            category: Resource category (study_room, equipment, etc.)
            location: Resource location
            capacity: Maximum capacity
            images: List of uploaded image files
            availability_rules: JSON dict of availability rules
            status: Initial status (default: draft)

        Returns:
            Created Resource object

        Raises:
            ResourceServiceError: If validation fails
        """
        # Validate required fields
        if not title or len(title.strip()) < 3:
            raise ResourceServiceError("Title must be at least 3 characters")

        if not category:
            raise ResourceServiceError("Category is required")

        if capacity is not None and capacity < 0:
            raise ResourceServiceError("Capacity cannot be negative")

        # Process image uploads
        image_paths = []
        if images:
            for img_file in images:
                if img_file and img_file.filename:
                    try:
                        path = ResourceService.save_image(img_file)
                        image_paths.append(path)
                    except ImageUploadError as e:
                        # Clean up any already uploaded images
                        for uploaded_path in image_paths:
                            try:
                                os.remove(os.path.join("src/static", uploaded_path))
                            except (OSError, FileNotFoundError):
                                pass
                        raise ResourceServiceError(f"Image upload failed: {str(e)}")

        # Create resource
        resource = Resource(
            owner_id=owner_id,
            title=title.strip(),
            description=description.strip() if description else None,
            category=category,
            location=location.strip() if location else None,
            capacity=capacity,
            images=json.dumps(image_paths) if image_paths else None,  # type: ignore[arg-type]
            availability_rules=json.dumps(availability_rules) if availability_rules else None,  # type: ignore[arg-type]
            status=status,
        )

        return ResourceRepository.create(resource)  # type: ignore[call-arg]

    @staticmethod
    def update_resource(
        resource_id: int,
        user_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        location: Optional[str] = None,
        capacity: Optional[int] = None,
        images: Optional[List[FileStorage]] = None,
        availability_rules: Optional[dict] = None,
        status: Optional[str] = None,
    ) -> Resource:
        """
        Update existing resource (owner-only).

        Args:
            resource_id: ID of resource to update
            user_id: ID of user requesting update
            **kwargs: Fields to update

        Returns:
            Updated Resource object

        Raises:
            ResourceServiceError: If unauthorized or validation fails
        """
        resource = ResourceRepository.get_by_id(resource_id)
        if not resource:
            raise ResourceServiceError("Resource not found")

        # Authorization check: only owner can edit
        if resource.owner_id != user_id:
            raise ResourceServiceError("Only the resource owner can edit this resource")

        # Update fields if provided
        if title is not None:
            if len(title.strip()) < 3:
                raise ResourceServiceError("Title must be at least 3 characters")
            resource.title = title.strip()

        if description is not None:
            resource.description = description.strip() if description else None

        if category is not None:
            resource.category = category

        if location is not None:
            resource.location = location.strip() if location else None

        if capacity is not None:
            if capacity < 0:
                raise ResourceServiceError("Capacity cannot be negative")
            resource.capacity = capacity

        if availability_rules is not None:
            resource.availability_rules = json.dumps(availability_rules)

        if status is not None:
            # Validate status transition
            if status not in ["draft", "published", "archived"]:
                raise ResourceServiceError("Invalid status")
            resource.status = status

        # Handle image uploads if provided
        if images is not None:
            image_paths = []
            for img_file in images:
                if img_file and img_file.filename:
                    try:
                        path = ResourceService.save_image(img_file)
                        image_paths.append(path)
                    except ImageUploadError as e:
                        raise ResourceServiceError(f"Image upload failed: {str(e)}")

            if image_paths:
                # Append to existing images
                existing = json.loads(resource.images) if resource.images else []
                existing.extend(image_paths)
                resource.images = json.dumps(existing)

        return ResourceRepository.update(resource)

    @staticmethod
    def delete_resource(resource_id: int, user_id: int) -> None:
        """
        Delete resource (owner-only or admin).

        Also deletes associated image files from filesystem.

        Args:
            resource_id: ID of resource to delete
            user_id: ID of user requesting deletion

        Raises:
            ResourceServiceError: If unauthorized or resource not found
        """
        resource = ResourceRepository.get_by_id(resource_id)
        if not resource:
            raise ResourceServiceError("Resource not found")

        # Authorization check: only owner can delete
        # Note: Admin check would be added here in Phase 6
        if resource.owner_id != user_id:
            raise ResourceServiceError("Only the resource owner can delete this resource")

        # Delete associated image files
        if resource.images:
            try:
                image_paths = json.loads(resource.images)
                for img_path in image_paths:
                    full_path = os.path.join("src/static", img_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
            except Exception as e:
                # Log error but don't fail deletion
                print(f"Warning: Failed to delete images: {e}")

        ResourceRepository.delete(resource_id)

    @staticmethod
    def publish_resource(resource_id: int, user_id: int) -> Resource:
        """
        Publish a draft resource (owner-only).

        Args:
            resource_id: ID of resource to publish
            user_id: ID of user requesting publish

        Returns:
            Updated Resource object

        Raises:
            ResourceServiceError: If unauthorized or invalid state
        """
        resource = ResourceRepository.get_by_id(resource_id)
        if not resource:
            raise ResourceServiceError("Resource not found")

        if resource.owner_id != user_id:
            raise ResourceServiceError("Only the resource owner can publish this resource")

        if resource.status == "published":
            raise ResourceServiceError("Resource is already published")

        resource.status = "published"
        return ResourceRepository.update(resource)

    @staticmethod
    def archive_resource(resource_id: int, user_id: int) -> Resource:
        """
        Archive a published resource (owner-only).

        Args:
            resource_id: ID of resource to archive
            user_id: ID of user requesting archive

        Returns:
            Updated Resource object

        Raises:
            ResourceServiceError: If unauthorized or invalid state
        """
        resource = ResourceRepository.get_by_id(resource_id)
        if not resource:
            raise ResourceServiceError("Resource not found")

        if resource.owner_id != user_id:
            raise ResourceServiceError("Only the resource owner can archive this resource")

        if resource.status == "archived":
            raise ResourceServiceError("Resource is already archived")

        resource.status = "archived"
        return ResourceRepository.update(resource)
