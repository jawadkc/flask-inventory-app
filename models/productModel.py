from mongoengine import Document, StringField, FloatField, IntField, ReferenceField

class Product(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=True)
    price = FloatField(required=True)
    quantity = IntField(default=1)
    unit_of_measure = StringField()
    category = StringField()
    brand = StringField()
    sku = StringField(required=True, unique=True)
    supplier = ReferenceField("supplierModel")  # Reference to Supplier model

    meta = {'collection': 'products'}  # Specify the MongoDB collection name
