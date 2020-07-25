from mongoengine import Document, StringField, FloatField, IntField

class Items(Document):
    """
    Documenting items to be stored.
    :param name: required string value
    :param description: optional string value, fewer than 240 characters
    :param price: optional float value
    :param quantity: optional int value
    :Example:
    >>> import mongoengine
    >>> from app import default_config
    >>> mongoengine.connect(**default_config['MONGODB_SETTINGS'])
    MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())
    >>> new_item = Items(name= "Flakes", description= "Breakfast cereals")
    >>> new_item.save()
    <Item: Item object>
    """
    meta = {'collection': 'stocks'}
    name = StringField(required=True)
    description = StringField()
    category = StringField()
    price = FloatField()
    quantity = IntField()