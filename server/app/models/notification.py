from mongoengine import Document, fields
from app.models.user import User
from datetime import datetime


class Notification(Document):
    """
    Represents a single notification.
    """

    sender = fields.ReferenceField(User, required=True)
    recepient = fields.ReferenceField(User, required=True)
    type = fields.StringField(required=True, choices=["message", "follow", "unfollow"])
    message = fields.StringField(required=True)
    timestamp = fields.DateTimeField(required=True, default=datetime.utcnow())

    @classmethod
    def add_notification(self, recepient, sender, type, message):
        # Find or create UserNotification document for the recipient
        user_notifications = self.objects(recepient=recepient).order_by("-timestamp")

        # Add new notification
        notification = Notification(
            sender=sender, recepient=recepient, type=type, message=message
        )

        # Trim notifications list to maintain max length
        if len(user_notifications) > 20:
            oldest_notification = user_notifications[-1]
            oldest_notification.delete()

        # Save document
        notification.save()
        return notification

    def to_dict(self):
        """
        Convert the Notification instance to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Notification instance.
        """
        return {
            "id": str(self.id),
            "sender": str(self.sender.id),
            "recepient": str(self.recepient.id),
            "type": self.type,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
        }