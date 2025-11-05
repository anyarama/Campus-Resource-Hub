"""
Models Package - Campus Resource Hub
Centralizes all database models and db instance.

Per .clinerules architecture: This module imports all models to ensure
SQLAlchemy properly registers relationships and creates all tables.

Usage:
    from src.models import db, User, Resource, Booking, Message, Review
    
    # In app factory:
    db.init_app(app)
"""

# Import db instance from app
from src.app import db

# Import all model classes
from src.models.user import User
from src.models.resource import Resource
from src.models.booking import Booking
from src.models.message import Message, MessageThread
from src.models.review import Review, ReviewAggregate

# Export all models for easy importing
__all__ = [
    "db",
    "User",
    "Resource",
    "Booking",
    "Message",
    "MessageThread",
    "Review",
    "ReviewAggregate",
]
