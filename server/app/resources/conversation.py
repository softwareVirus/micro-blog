from flask import request
from flask_restful import Resource
from server.app.models.message import Message
from server.app.models.user import User


class Conversation(Resource):
    def get(self, user_id1, user_id2):
        """
        Retrieve all messages exchanged between two users.

        Parameters
        ----------
        user_id1 : str
            ID of the first user.
        user_id2 : str
            ID of the second user.

        Returns
        -------
        list of dict
            List of messages exchanged between the two users.
        """
        user1 = User.objects.get(id=user_id1)
        user2 = User.objects.get(id=user_id2)

        # Retrieve messages where either user is the sender and the other is the recipient
        messages1_to_2 = Message.objects.filter(sender=user1, recipient=user2)
        messages2_to_1 = Message.objects.filter(sender=user2, recipient=user1)

        # Combine and sort messages by timestamp
        all_messages = list(messages1_to_2) + list(messages2_to_1)
        all_messages.sort(key=lambda x: x.timestamp)

        # Convert messages to dictionary format
        messages_data = [
            {
                "sender": str(message.sender.id),
                "recipient": str(message.recipient.id),
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
            }
            for message in all_messages
        ]

        return messages_data
