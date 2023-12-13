from mongoengine import Document, StringField, EmailField, DateTimeField
import datetime

class User(Document):
    """
    MongoDB Document model representing a user.

    Attributes
    ----------
    first_name : StringField
        First name of the user (max length: 200 characters), required.
    last_name : StringField
        Last name of the user (max length: 200 characters), required.
    email : EmailField
        Email of the user, unique and required.
    hashed_password : StringField
        Hashed password of the user, required.
    salt : StringField
        Salt used in password hashing, required.
    created_at : DateTimeField
        Timestamp representing the user's creation date (default: current UTC time).
    updated_at : DateTimeField
        Timestamp representing the user's last update date (default: current UTC time).

    Methods
    -------
    None

    Examples
    --------
    Creating a new user instance:

    >>> new_user = User(
    ...     first_name="John",
    ...     last_name="Doe",
    ...     email="john.doe@example.com",
    ...     hashed_password="hashed_password",
    ...     salt="random_salt"
    ... )
    >>> new_user.save()
    """

    first_name = StringField(max_length=200, required=True)
    last_name = StringField(max_length=200, required=True)
    email = EmailField(unique=True, required=True)
    hashed_password = StringField(required=True)
    salt = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())
