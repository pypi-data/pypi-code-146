from .. import mongo

from .base_document import BaseDocument

class Ingredient(BaseDocument):
    name = mongo.StringField(required=True)
    description = mongo.StringField()
    note = mongo.StringField()
    edible = mongo.BooleanField()
    freezed = mongo.BooleanField()
    availabilityMonths = mongo.ListField(
        mongo.IntField(min_value=1, max_value=12), max_length=12, default=None
    )
    tags = mongo.ListField(
        mongo.StringField(), default=None
    )

    meta = {
        'collection' : 'ingredients'
    }

    def __repr__(self):
           return "<Ingredient '{}'>".format(self.name)