from mongoengine import Document, StringField, ReferenceField, DateTimeField, CASCADE
import datetime


class Comment(Document):
    """
    MongoDB Document model representing a comment.

    Attributes
    ----------
    content : StringField
        Content of the comment (max length: 1000 characters), required.
    author : ReferenceField
        Reference to the User who authored the comment, with cascading delete rule.
    parent_comment : ReferenceField
        Reference to the parent Comment, if this comment is a reply to another comment.
    created_at : DateTimeField
        Timestamp representing the comment's creation date (default: current UTC time).

    Methods
    -------
    to_dict()
        Convert the Comment instance to a dictionary.

    Examples
    --------
    Creating a new comment instance:

    >>> new_comment = Comment(
    ...     content="This is a comment.",
    ...     author=some_user_instance,
    ... )
    >>> new_comment.save()
    """

    content = StringField(max_length=1000, required=True)
    author = ReferenceField("User", reverse_delete_rule=CASCADE)
    parent_comment = ReferenceField("Comment")
    created_at = DateTimeField(default=datetime.datetime.utcnow())

    def to_dict(self):
        """
        Convert the Comment instance to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Comment instance.
        """
        return {
            "id": str(self.id),
            "content": self.content,
            "author": str(self.author.id),
            "parent_comment": str(self.parent_comment.id) if self.parent_comment else None,
            "created_at": self.created_at.isoformat(),
        }
