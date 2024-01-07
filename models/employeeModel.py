from mongoengine import Document, StringField, EmailField, DateTimeField, FloatField, IntField, ChoicesField

class Employee(Document):
    name = StringField(required=True)
    email = EmailField(unique=True)
    phone = StringField()
    address = StringField()
    position = StringField()
    hire_date = DateTimeField()
    salary = FloatField()
    working_hours = StringField()
    status = StringField(choices=["Active", "On Leave", "Terminated"], default="Active")

    meta = {'collection': 'employees'}  # Specify the MongoDB collection name
