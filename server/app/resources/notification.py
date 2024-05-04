from flask_restful import Resource
from app.models.notification import Notification
from flask_jwt_extended import jwt_required, current_user


class NotificationResource(Resource):
    @jwt_required()  # Requires JWT authentication
    def get(self):
        # Retrieve notifications for the current user
        notifications = (
            Notification.objects(recepient=current_user).order_by("-timestamp").all()
        )

        # Convert notifications to dictionary format
        notifications_dict = [notification.to_dict() for notification in notifications]

        return notifications_dict, 200