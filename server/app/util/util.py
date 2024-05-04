from datetime import timedelta
from flask_socketio import SocketIO, emit, join_room, leave_room

def send_notification(recipient_id, notification):
    emit("notification", notification, room="notification-to-" + recipient_id)
    pass
