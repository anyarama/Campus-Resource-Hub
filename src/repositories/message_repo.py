"""
Message Repository - Campus Resource Hub
Data Access Layer for Message model.
"""

from typing import List, Optional, Dict
from src.models import db, Message


class MessageRepository:
    """Repository for Message model CRUD operations."""

    @staticmethod
    def create(
        sender_id: int, receiver_id: int, content: str, thread_id: Optional[int] = None
    ) -> Message:
        """Create a new message."""
        message = Message(
            sender_id=sender_id, receiver_id=receiver_id, content=content, thread_id=thread_id
        )
        db.session.add(message)
        db.session.commit()
        return message

    @staticmethod
    def get_by_id(message_id: int) -> Optional[Message]:
        """Get message by ID."""
        return Message.query.get(message_id)

    @staticmethod
    def get_conversation(user1_id: int, user2_id: int) -> List[Message]:
        """Get all messages between two users."""
        return (
            Message.query.filter(
                db.or_(
                    db.and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
                    db.and_(Message.sender_id == user2_id, Message.receiver_id == user1_id),
                )
            )
            .order_by(Message.timestamp.asc())
            .all()
        )

    @staticmethod
    def get_inbox(user_id: int, page: int = 1, per_page: int = 50) -> Dict:
        """Get user's received messages with pagination."""
        paginated = (
            Message.query.filter_by(receiver_id=user_id)
            .order_by(Message.timestamp.desc())
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
    def get_sent(user_id: int, page: int = 1, per_page: int = 50) -> Dict:
        """Get user's sent messages with pagination."""
        paginated = (
            Message.query.filter_by(sender_id=user_id)
            .order_by(Message.timestamp.desc())
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
    def mark_as_read(message_id: int) -> Optional[Message]:
        """Mark message as read."""
        message = Message.query.get(message_id)
        if not message:
            return None

        message.mark_as_read()
        db.session.commit()
        return message

    @staticmethod
    def delete(message_id: int) -> bool:
        """Delete message."""
        message = Message.query.get(message_id)
        if not message:
            return False

        db.session.delete(message)
        db.session.commit()
        return True

    @staticmethod
    def count_unread(user_id: int) -> int:
        """Count unread messages for user."""
        return Message.query.filter_by(receiver_id=user_id, is_read=False).count()
