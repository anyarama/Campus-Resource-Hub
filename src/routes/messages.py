"""
Campus Resource Hub - Messages Routes
Flask blueprint for messaging system.

AI Contribution: Cline generated messaging routes structure
Reviewed by developer on 2025-11-06
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

from src.services.message_service import MessageService, MessageServiceError
from src.repositories.user_repo import UserRepository


# Create messages blueprint
messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/messages")
@login_required
def inbox():
    """
    Display messaging workspace with conversation list + active thread.
    """
    try:
        selected_user_id = request.args.get("user_id", type=int)

        conversations = MessageService.get_conversations(current_user.user_id)
        stats = MessageService.get_message_stats(current_user.user_id)

        # Determine active conversation partner
        active_user = None
        if selected_user_id:
            active_user = UserRepository.get_by_id(selected_user_id)

        if active_user and active_user.user_id == current_user.user_id:
            active_user = None

        if not active_user and conversations:
            active_user = conversations[0]["other_user"]

        active_messages = []
        if active_user and active_user.user_id != current_user.user_id:
            try:
                active_messages = MessageService.get_conversation(
                    current_user.user_id, active_user.user_id
                )
            except MessageServiceError as conv_error:
                flash(str(conv_error), "error")
                active_user = None

        return render_template(
            "messages/inbox.html",
            conversations=conversations,
            stats=stats,
            active_user=active_user,
            active_messages=active_messages,
            selected_user_id=active_user.user_id if active_user else None,
        )
    except Exception as e:
        flash(f"Error loading messages: {str(e)}", "error")
        return redirect(url_for("resources.dashboard"))


@messages_bp.route("/messages/conversation/<int:user_id>")
@login_required
def conversation(user_id):
    """
    Display conversation with a specific user.

    Args:
        user_id: ID of the other user in conversation
    """
    try:
        # Get the other user
        other_user = UserRepository.get_by_id(user_id)
        if not other_user:
            flash("User not found", "error")
            return redirect(url_for("messages.inbox"))

        # Check if can message this user
        can_message, error = MessageService.can_message_user(current_user.user_id, user_id)
        if not can_message:
            flash(error, "error")
            return redirect(url_for("messages.inbox"))

        # Get conversation messages (also marks as read)
        MessageService.get_conversation(current_user.user_id, user_id)

        return redirect(url_for("messages.inbox", user_id=other_user.user_id))
    except MessageServiceError as e:
        flash(str(e), "error")
        return redirect(url_for("messages.inbox"))
    except Exception as e:
        flash(f"Error loading conversation: {str(e)}", "error")
        return redirect(url_for("messages.inbox"))


@messages_bp.route("/messages/compose/<int:user_id>", methods=["GET", "POST"])
@login_required
def compose(user_id):
    """
    Compose a new message to a user.

    GET: Show compose form
    POST: Send message

    Args:
        user_id: ID of recipient
    """
    # Get recipient
    recipient = UserRepository.get_by_id(user_id)
    if not recipient:
        flash("Recipient not found", "error")
        return redirect(url_for("messages.inbox"))

    if request.method == "GET":
        # Show compose form
        return render_template(
            "messages/compose.html",
            recipient=recipient,
        )

    # Process POST - send message
    try:
        content = request.form.get("content", "").strip()

        if not content:
            flash("Message content cannot be empty", "error")
            return redirect(url_for("messages.compose", user_id=user_id))

        # Send message
        MessageService.send_message(
            sender_id=current_user.user_id,
            receiver_id=user_id,
            content=content,
        )

        flash("Message sent successfully!", "success")
        return redirect(url_for("messages.inbox", user_id=user_id))

    except MessageServiceError as e:
        flash(str(e), "error")
        return redirect(url_for("messages.compose", user_id=user_id))


@messages_bp.route("/messages/send", methods=["POST"])
@login_required
def send():
    """
    Send a message (AJAX endpoint or form submission).

    Expects:
        receiver_id: int
        content: str
        thread_id: int (optional)

    Returns:
        JSON response or redirect
    """
    try:
        receiver_id = request.form.get("receiver_id", type=int)
        content = request.form.get("content", "").strip()
        thread_id = request.form.get("thread_id", type=int)

        if not receiver_id:
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Receiver ID required"}), 400
            flash("Recipient not specified", "error")
            return redirect(url_for("messages.inbox"))

        if not content:
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "Message content required"}), 400
            flash("Message content cannot be empty", "error")
            return redirect(url_for("messages.inbox", user_id=receiver_id))

        # Send message
        message = MessageService.send_message(
            sender_id=current_user.user_id,
            receiver_id=receiver_id,
            content=content,
            thread_id=thread_id,
        )

        # Return JSON for AJAX requests
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return (
                jsonify(
                    {
                        "success": True,
                        "message_id": message.message_id,
                        "timestamp": message.timestamp.isoformat(),
                    }
                ),
                200,
            )

        # Regular form submission - redirect to conversation
        flash("Message sent!", "success")
        return redirect(url_for("messages.inbox", user_id=receiver_id))

    except MessageServiceError as e:
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": str(e)}), 400
        flash(str(e), "error")
        return redirect(url_for("messages.inbox"))


@messages_bp.route("/messages/<int:message_id>/delete", methods=["POST"])
@login_required
def delete(message_id):
    """
    Delete a message (sender only).

    Args:
        message_id: ID of message to delete
    """
    try:
        success, error = MessageService.delete_message(message_id, current_user.user_id)

        if success:
            flash("Message deleted", "success")
        else:
            flash(error or "Failed to delete message", "error")

    except Exception as e:
        flash(f"Error: {str(e)}", "error")

    # Redirect back to referrer or inbox
    return redirect(request.referrer or url_for("messages.inbox"))


@messages_bp.route("/messages/mark-read/<int:user_id>", methods=["POST"])
@login_required
def mark_read(user_id):
    """
    Mark all messages from a user as read.

    Args:
        user_id: ID of the other user
    """
    try:
        MessageService.mark_conversation_read(current_user.user_id, user_id)

        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True}), 200

        flash("Messages marked as read", "success")
        return redirect(url_for("messages.inbox", user_id=user_id))

    except Exception as e:
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": str(e)}), 400
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("messages.inbox"))


@messages_bp.route("/messages/unread-count")
@login_required
def unread_count():
    """
    Get unread message count (AJAX endpoint for navbar badge).

    Returns:
        JSON with unread count
    """
    try:
        count = MessageService.get_unread_count(current_user.user_id)
        return jsonify({"unread_count": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@messages_bp.route("/messages/stats")
@login_required
def stats():
    """
    Get messaging statistics for current user.

    Returns:
        JSON with stats
    """
    try:
        stats = MessageService.get_message_stats(current_user.user_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Integration with bookings - message resource owner
@messages_bp.route("/messages/about-resource/<int:resource_id>")
@login_required
def about_resource(resource_id):
    """
    Start a conversation about a specific resource.

    Redirects to compose message to resource owner.

    Args:
        resource_id: ID of resource to inquire about
    """
    from src.repositories.resource_repo import ResourceRepository

    try:
        resource = ResourceRepository.get_by_id(resource_id)

        if not resource:
            flash("Resource not found", "error")
            return redirect(url_for("resources.index"))

        # Check if user is owner
        if resource.owner_id == current_user.user_id:
            flash("You own this resource", "info")
            return redirect(url_for("resources.detail", resource_id=resource_id))

        # Redirect to compose message to owner
        return redirect(url_for("messages.compose", user_id=resource.owner_id))

    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("resources.index"))


@messages_bp.route("/messages/about-booking/<int:booking_id>")
@login_required
def about_booking(booking_id):
    """
    Start a conversation about a specific booking.

    Redirects to compose message to the other party (owner or requester).

    Args:
        booking_id: ID of booking to discuss
    """
    from src.repositories.booking_repo import BookingRepository
    from src.repositories.resource_repo import ResourceRepository

    try:
        booking = BookingRepository.get_by_id(booking_id)

        if not booking:
            flash("Booking not found", "error")
            return redirect(url_for("bookings.my_bookings"))

        # Determine who to message
        if booking.requester_id == current_user.user_id:
            # Current user is requester - message resource owner
            resource = ResourceRepository.get_by_id(booking.resource_id)
            if resource:
                other_user_id = resource.owner_id
            else:
                flash("Resource not found", "error")
                return redirect(url_for("bookings.my_bookings"))
        else:
            # Current user is owner - message requester
            other_user_id = booking.requester_id

        # Check authorization
        if booking.requester_id != current_user.user_id:
            resource = ResourceRepository.get_by_id(booking.resource_id)
            if not resource or resource.owner_id != current_user.user_id:
                flash("Unauthorized", "error")
                return redirect(url_for("bookings.my_bookings"))

        # Redirect to compose or conversation
        return redirect(url_for("messages.inbox", user_id=other_user_id))

    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("bookings.my_bookings"))
