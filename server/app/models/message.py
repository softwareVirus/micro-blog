from mongoengine import Document, fields
from app.models.user import User
from datetime import datetime


class Message(Document):
    """
    Represents a single message within a conversation.
    """

    sender = fields.ReferenceField(User, required=True)
    recipient = fields.ReferenceField(User, required=True)
    content = fields.StringField(required=True)
    timestamp = fields.DateTimeField(required=True)

    def to_dict(self):
        """
        Convert the Message instance to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Message instance.
        """
        return {
            "id": str(self.id),
            "sender": str(self.sender.id),
            "recipient": str(self.recipient.id),
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }
