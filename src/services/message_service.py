"""
Message Service - Campus Resource Hub
Business logic for messaging system with thread management.

AI Contribution: Cline generated messaging service structure
Reviewed by developer on 2025-11-06
"""

from typing import List, Dict, Optional, Tuple

from src.models import Message
from src.repositories.message_repo import MessageRepository
from src.repositories.user_repo import UserRepository


class MessageServiceError(Exception):
    """Custom exception for message service errors."""

    pass


class MessageService:
    """
    Service layer for messaging operations.

    Handles:
    - Thread-based conversation management
    - Message sending with validation
    - Inbox organization (grouped by conversations)
    - Unread message tracking
    """

    @staticmethod
    def send_message(
        sender_id: int, receiver_id: int, content: str, thread_id: Optional[int] = None
    ) -> Message:
        """
        Send a message from one user to another.

        Args:
            sender_id: ID of sender
            receiver_id: ID of receiver
            content: Message content (plain text)
            thread_id: Optional thread_id for replies

        Returns:
            Created Message object

        Raises:
            MessageServiceError: If validation fails
        """
        # Validate users exist
        sender = UserRepository.get_by_id(sender_id)
        receiver = UserRepository.get_by_id(receiver_id)

        if not sender:
            raise MessageServiceError("Sender not found")
        if not receiver:
            raise MessageServiceError("Receiver not found")

        # Validate sender is active
        if not sender.is_active:
            raise MessageServiceError("Your account is suspended")

        # Validate content
        if not content or not content.strip():
            raise MessageServiceError("Message content cannot be empty")

        if len(content) > 10000:
            raise MessageServiceError("Message too long (max 10,000 characters)")

        # Validate not messaging self
        if sender_id == receiver_id:
            raise MessageServiceError("Cannot send message to yourself")

        # Create message
        try:
            message = MessageRepository.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=content.strip(),
                thread_id=thread_id,
            )
            return message
        except Exception as e:
            raise MessageServiceError(f"Failed to send message: {str(e)}")

    @staticmethod
    def get_conversation(user_id: int, other_user_id: int) -> List[Message]:
        """
        Get full conversation between two users.

        Args:
            user_id: Current user ID
            other_user_id: Other user ID

        Returns:
            List of messages ordered by timestamp (oldest first)

        Raises:
            MessageServiceError: If users not found
        """
        # Validate users exist
        user = UserRepository.get_by_id(user_id)
        other_user = UserRepository.get_by_id(other_user_id)

        if not user:
            raise MessageServiceError("User not found")
        if not other_user:
            raise MessageServiceError("Recipient not found")

        # Get conversation
        messages = MessageRepository.get_conversation(user_id, other_user_id)

        # Mark received messages as read
        for msg in messages:
            if msg.receiver_id == user_id and not msg.is_read:
                MessageRepository.mark_as_read(msg.message_id)

        return messages

    @staticmethod
    def get_conversations(user_id: int) -> List[Dict]:
        """
        Get all conversations for a user, grouped by participants.

        Returns list of conversation summaries ordered by last message time.

        Args:
            user_id: Current user ID

        Returns:
            List of dicts with conversation info:
            {
                'other_user': User object,
                'last_message': Message object,
                'unread_count': int,
                'message_count': int
            }
        """
        # Get all messages involving user
        from src.models import db

        all_messages = (
            Message.query.filter(
                db.or_(Message.sender_id == user_id, Message.receiver_id == user_id)
            )
            .order_by(Message.timestamp.desc())
            .all()
        )

        # Group by conversation partner
        conversations = {}

        for msg in all_messages:
            # Determine the other user
            other_user_id = msg.get_other_user_id(user_id)
            if other_user_id is None:
                continue

            # Initialize conversation if not exists
            if other_user_id not in conversations:
                conversations[other_user_id] = {
                    "messages": [],
                    "last_message": msg,
                    "unread_count": 0,
                }

            # Add message to conversation
            conversations[other_user_id]["messages"].append(msg)

            # Count unread (received by current user)
            if msg.receiver_id == user_id and not msg.is_read:
                conversations[other_user_id]["unread_count"] += 1

        # Build result list with user info
        result = []
        for other_user_id, conv_data in conversations.items():
            other_user = UserRepository.get_by_id(other_user_id)
            if other_user:
                result.append(
                    {
                        "other_user": other_user,
                        "last_message": conv_data["last_message"],
                        "unread_count": conv_data["unread_count"],
                        "message_count": len(conv_data["messages"]),
                    }
                )

        # Sort by last message timestamp (most recent first)
        result.sort(key=lambda x: x["last_message"].timestamp, reverse=True)

        return result

    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """
        Get total unread message count for user.

        Args:
            user_id: User ID

        Returns:
            Number of unread messages
        """
        return MessageRepository.count_unread(user_id)

    @staticmethod
    def mark_conversation_read(user_id: int, other_user_id: int) -> None:
        """
        Mark all messages from another user as read.

        Args:
            user_id: Current user ID
            other_user_id: Other user ID
        """
        messages = MessageRepository.get_conversation(user_id, other_user_id)

        for msg in messages:
            if msg.receiver_id == user_id and not msg.is_read:
                MessageRepository.mark_as_read(msg.message_id)

    @staticmethod
    def can_message_user(sender_id: int, receiver_id: int) -> Tuple[bool, Optional[str]]:
        """
        Check if sender can message receiver.

        Args:
            sender_id: ID of sender
            receiver_id: ID of receiver

        Returns:
            Tuple of (can_message: bool, error_message: Optional[str])
        """
        # Check sender exists and is active
        sender = UserRepository.get_by_id(sender_id)
        if not sender:
            return False, "Sender not found"
        if not sender.is_active:
            return False, "Your account is suspended"

        # Check receiver exists
        receiver = UserRepository.get_by_id(receiver_id)
        if not receiver:
            return False, "Recipient not found"

        # Cannot message self
        if sender_id == receiver_id:
            return False, "Cannot message yourself"

        return True, None

    @staticmethod
    def delete_message(message_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Delete a message (only by sender).

        Args:
            message_id: Message ID to delete
            user_id: User attempting deletion

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        message = MessageRepository.get_by_id(message_id)

        if not message:
            return False, "Message not found"

        # Only sender can delete
        if message.sender_id != user_id:
            return False, "You can only delete messages you sent"

        success = MessageRepository.delete(message_id)
        if success:
            return True, None
        return False, "Failed to delete message"

    @staticmethod
    def get_message_stats(user_id: int) -> Dict:
        """
        Get messaging statistics for user.

        Args:
            user_id: User ID

        Returns:
            Dict with stats: {
                'total_sent': int,
                'total_received': int,
                'unread': int,
                'conversations': int
            }
        """
        from src.models import db

        sent_count = Message.query.filter_by(sender_id=user_id).count()
        received_count = Message.query.filter_by(receiver_id=user_id).count()
        unread_count = MessageRepository.count_unread(user_id)

        # Count unique conversation partners
        messages = Message.query.filter(
            db.or_(Message.sender_id == user_id, Message.receiver_id == user_id)
        ).all()

        partners = set()
        for msg in messages:
            other_id = msg.get_other_user_id(user_id)
            if other_id:
                partners.add(other_id)

        return {
            "total_sent": sent_count,
            "total_received": received_count,
            "unread": unread_count,
            "conversations": len(partners),
        }
