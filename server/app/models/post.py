from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
    DateTimeField,
    CASCADE,
)
import datetime


class Post(Document):
    """
    MongoDB Document model representing a post.

    Attributes
    ----------
    title : StringField
        Title of the post (max length: 200 characters), required.
    content : StringField
        Content of the post (max length: 2000 characters), required.
    tags : ListField
        List of tags associated with the post.
    author : ReferenceField
        Reference to the User who authored the post, with cascading delete rule.
    created_at : DateTimeField
        Timestamp representing the post's creation date (default: current UTC time).
    updated_at : DateTimeField
        Timestamp representing the post's last update date (default: current UTC time).
    votes : ListField
        List of references to Users who voted for the post.
    comments : ListField
        List of references to Comments associated with the post.

    Methods
    -------
    to_dict()
        Convert the Post instance to a dictionary.

    Examples
    --------
    Creating a new post instance:

    >>> new_post = Post(
    ...     title="Sample Post",
    ...     content="This is the content of the post.",
    ...     tags=["tag1", "tag2"],
    ...     author=some_user_instance,
    ... )
    >>> new_post.save()
    """

    title = StringField(max_length=200, required=True)
    content = StringField(max_length=2000, required=True)
    author = ReferenceField("User", reverse_delete_rule=CASCADE)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())
    votes = ListField(ReferenceField("User"))
    comments = ListField(ReferenceField("Comment"))

    def to_dict(self):
        """
        Convert the Post instance to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Post instance.
        """
        # Select_related to populate the author field

        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "author": self.author.to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "votes": [str(user.id) for user in self.votes],
            "comments": [comment.to_dict() for comment in self.comments],
        }
