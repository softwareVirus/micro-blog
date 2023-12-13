from mongoengine import *
import datetime

class Post(Document):
    title = StringField(max_length=200, required=True)
    content = StringField(max_length=2000, required=True)
    tags = ListField(StringField())
    author = ReferenceField('User', reverse_delete_rule=CASCADE)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
