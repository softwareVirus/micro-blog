# Import the necessary modules
from datetime import datetime
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_jwt_extended import current_user, jwt_required
from app.models.message import Message
from app.models.user import User
from bson.objectid import ObjectId
from app.models.notification import Notification
from .util.util import send_notification

active_users = {}

socketio = SocketIO()


# Event handler for new socket connections
@socketio.on("connect")
@jwt_required()
def handle_connect():
    # Retrieve user details from request parameters
    user_id = str(current_user.id)
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")

    # Add user to active users dictionary
    active_users[user_id] = {
        "user_socket_id": user_id,
        "user_db_id": None,
        "first_name": first_name,
        "last_name": last_name,
        "status": "online",
    }


# Event handler for socket disconnections
@socketio.on("disconnect")
def handle_disconnect():
    user_id = request.sid
    if user_id in active_users:
        del active_users[user_id]


# Event handler for joining private chat room
@socketio.on("join_private_chat")
@jwt_required()
def handle_join_private_chat(data):
    current_user_id = str(current_user.id)
    join_room(current_user_id)


@socketio.on("join_notification")
@jwt_required()
def handle_join_notification(data):
    current_user_id = str(current_user.id)
    join_room("notification-to-" + current_user_id)


# Event handler for leaving private chat room
@socketio.on("leave_private_chat")
@jwt_required()
def handle_leave_private_chat(data):
    recipient_id = data.get("recipient_id")
    leave_room(recipient_id)
    if recipient_id in active_users:
        del active_users[recipient_id]


# Event handler for private messages
@socketio.on("private_message")
@jwt_required()
def handle_private_message(data):
    recipient_id = data.get("recipient_id")
    message_content = data.get("message")

    # Save the message to the database
    sender_id = str(current_user.id)
    message = Message(
        sender=sender_id,
        recipient=recipient_id,
        content=message_content,
        timestamp=datetime.utcnow(),  # You may adjust the timestamp as per your requirements
    )
    recipient_user = User.objects.get(id=recipient_id)
    current_user.update(add_to_set__conversations=recipient_user)
    recipient_user.update(add_to_set__conversations=current_user)
    current_user.save()
    recipient_user.save()
    message.save()

    new_notification = Notification.add_notification(
        sender=current_user,
        recepient=recipient_user,
        type="message",
        message=f"You have received a new message from {current_user.first_name}.",
    )
    emit("private_message", message.to_dict(), room=recipient_id)
    send_notification(recipient_id, new_notification.to_dict())


# Function to emit user status update to all clients
@socketio.on("user_status")
@jwt_required()
def handle_user_status(data):
    sender_id = request.sid
    recipient_ids = data["recipient_ids"]
    users = {}

    for recipient_id in recipient_ids:

        if active_users.get(recipient_id) is not None:
            users[recipient_id] = {
                "recipient_id": recipient_id,
                "status": active_users.get(recipient_id, {"status": "offline"})[
                    "status"
                ],
            }
    emit("user_status", users, room=sender_id)