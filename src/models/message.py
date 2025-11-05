"""
Message Model - Campus Resource Hub
Enables communication between users (requester ↔ resource owner).

Per docs/ERD.md specifications and .clinerules architecture.
"""

from datetime import datetime
from typing import Optional, Dict

from src.app import db


class Message(db.Model):
    """
    Message model for user-to-user communication.

    Threading:
        Messages are grouped by thread_id to form conversations.
        First message in a conversation generates a new thread_id,
        subsequent replies use the same thread_id.

    Use Cases:
        - Booking inquiries (requester → resource owner)
        - Booking clarifications (owner → requester)
        - Follow-up questions after booking
        - General resource questions

    Security:
        - Content sanitized via Jinja auto-escaping (XSS protection)
        - Plain text only (no HTML allowed)
        - Users cannot message themselves

    Relationships:
        - sender: User who sent the message
        - receiver: User who received the message
    """

    __tablename__ = "messages"

    # Primary Key
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Threading
    thread_id = db.Column(db.Integer, nullable=True, index=True)

    # Foreign Keys
    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    receiver_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Message Content
    content = db.Column(db.Text, nullable=False)

    # Timestamp
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Message Status (for future feature: read receipts)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    sender = db.relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])

    receiver = db.relationship(
        "User", back_populates="received_messages", foreign_keys=[receiver_id]
    )

    # Constraints
    __table_args__ = (
        db.CheckConstraint("sender_id != receiver_id", name="check_different_users"),
        db.CheckConstraint("length(trim(content)) > 0", name="check_content_not_empty"),
    )

    def __init__(
        self, sender_id: int, receiver_id: int, content: str, thread_id: Optional[int] = None
    ):
        """
        Initialize a new Message.

        Args:
            sender_id: ID of user sending the message
            receiver_id: ID of user receiving the message
            content: Message body (plain text)
            thread_id: Optional thread ID for grouping messages

        Raises:
            ValueError: If sender and receiver are the same
            ValueError: If content is empty or whitespace only
        """
        if sender_id == receiver_id:
            raise ValueError("Cannot send message to yourself")

        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")

        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content.strip()
        self.thread_id = thread_id

    def mark_as_read(self) -> None:
        """Mark message as read by receiver."""
        self.is_read = True

    def is_sent_by(self, user_id: int) -> bool:
        """Check if message was sent by given user."""
        return self.sender_id == user_id

    def is_received_by(self, user_id: int) -> bool:
        """Check if message was received by given user."""
        return self.receiver_id == user_id

    def involves_user(self, user_id: int) -> bool:
        """Check if user is sender or receiver of this message."""
        return user_id in [self.sender_id, self.receiver_id]

    def get_other_user_id(self, user_id: int) -> Optional[int]:
        """
        Get the other user ID in the conversation.

        Args:
            user_id: ID of one user in the conversation

        Returns:
            ID of the other user, or None if user_id is not involved
        """
        if self.sender_id == user_id:
            return self.receiver_id
        elif self.receiver_id == user_id:
            return self.sender_id
        return None

    def get_age_minutes(self) -> float:
        """
        Calculate how many minutes ago message was sent.

        Returns:
            Age in minutes (decimal)
        """
        delta = datetime.utcnow() - self.timestamp
        return delta.total_seconds() / 60

    def is_recent(self, minutes: int = 5) -> bool:
        """
        Check if message was sent within the last N minutes.

        Args:
            minutes: Time threshold in minutes

        Returns:
            True if message is recent, False otherwise
        """
        return self.get_age_minutes() < minutes

    def get_preview(self, max_length: int = 50) -> str:
        """
        Get truncated message preview for list views.

        Args:
            max_length: Maximum length of preview

        Returns:
            Truncated content with ellipsis if needed
        """
        if len(self.content) <= max_length:
            return self.content
        return self.content[: max_length - 3] + "..."

    def __repr__(self) -> str:
        """String representation of Message."""
        preview = self.get_preview(30)
        return (
            f"<Message {self.message_id}: "
            f"From={self.sender_id} To={self.receiver_id} "
            f'Thread={self.thread_id} "{preview}">'
        )

    def to_dict(self, include_relations: bool = False) -> Dict:
        """
        Convert message to dictionary (for JSON responses).

        Args:
            include_relations: Whether to include related user info

        Returns:
            Dictionary representation of message
        """
        data = {
            "message_id": self.message_id,
            "thread_id": self.thread_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "is_read": self.is_read,
            "age_minutes": self.get_age_minutes(),
            "is_recent": self.is_recent(),
        }

        if include_relations:
            if self.sender:
                data["sender_name"] = self.sender.name
                data["sender_email"] = self.sender.email
                data["sender_profile_image"] = self.sender.profile_image

            if self.receiver:
                data["receiver_name"] = self.receiver.name
                data["receiver_email"] = self.receiver.email
                data["receiver_profile_image"] = self.receiver.profile_image

        return data


class MessageThread:
    """
    Helper class for working with message threads.

    This is not a model, but a utility class for grouping and
    managing messages in a conversation thread.
    """

    def __init__(self, thread_id: int, messages: list):
        """
        Initialize a message thread.

        Args:
            thread_id: Thread identifier
            messages: List of Message objects in this thread
        """
        self.thread_id = thread_id
        self.messages = sorted(messages, key=lambda m: m.timestamp)

    def get_participants(self) -> set:
        """Get set of user IDs participating in this thread."""
        participant_ids = set()
        for msg in self.messages:
            participant_ids.add(msg.sender_id)
            participant_ids.add(msg.receiver_id)
        return participant_ids

    def get_last_message(self) -> Optional["Message"]:
        """Get the most recent message in thread."""
        return self.messages[-1] if self.messages else None

    def get_unread_count(self, user_id: int) -> int:
        """Get number of unread messages for a user in this thread."""
        return sum(1 for msg in self.messages if msg.receiver_id == user_id and not msg.is_read)

    def mark_all_read(self, user_id: int) -> None:
        """Mark all messages for a user as read."""
        for msg in self.messages:
            if msg.receiver_id == user_id and not msg.is_read:
                msg.mark_as_read()

    def __repr__(self) -> str:
        """String representation of MessageThread."""
        return f"<MessageThread {self.thread_id}: {len(self.messages)} messages>"
