"""
Repositories Package - Campus Resource Hub
Data Access Layer (DAL) for all models.

Per .clinerules: All database operations encapsulated here.
"""

from src.repositories.user_repo import UserRepository
from src.repositories.resource_repo import ResourceRepository
from src.repositories.booking_repo import BookingRepository
from src.repositories.message_repo import MessageRepository
from src.repositories.review_repo import ReviewRepository

__all__ = [
    "UserRepository",
    "ResourceRepository",
    "BookingRepository",
    "MessageRepository",
    "ReviewRepository",
]
