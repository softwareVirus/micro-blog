from mongoengine import *
import datetime

class User(Document):
    first_name = StringField(max_length=200, required=True)
    last_name = StringField(max_length=200, required=True)
    email = EmailField(unique=True, required=True)
    hashed_password = StringField(required=True)
    salt = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
