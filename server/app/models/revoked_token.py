from mongoengine import Document, StringField

class RevokedToken(Document):
    jti = StringField(primary_key=True, index=True)
