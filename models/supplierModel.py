from mongoengine import Document, StringField

class Supplier(Document):
    name = StringField(required=True, unique=True)
    contact_person = StringField()
    email = StringField(unique=True)
    phone = StringField()
    address = StringField()

    meta = {'collection': 'suppliers'}  # Specify the MongoDB collection name
