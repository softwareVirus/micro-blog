from mongoengine import Document, StringField


class Tag(Document):
    """
    MongoDB Document model representing a tag.

    Attributes
    ----------
    tag : StringField
        Tag name, must be unique.
    """

    tag = StringField(unique=True)

    def to_dict(self):
        """
        Convert the Tag instance to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Tag instance.
        """
        return {
            "id": str(self.id),
            "tag": self.tag,
        }
