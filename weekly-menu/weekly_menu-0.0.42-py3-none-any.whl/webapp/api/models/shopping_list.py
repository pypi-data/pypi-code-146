from .. import mongo
from ..models import Ingredient

from .base_document import BaseDocument


class ShoppingListItem(mongo.EmbeddedDocument):
    checked = mongo.BooleanField(required=True)
    item = mongo.ReferenceField('Ingredient', required=True)
    supermarketSectionName = mongo.StringField()
    listPosition = mongo.IntField(min_value=0)

    quantity = mongo.FloatField(min_value=0)
    unitOfMeasure = mongo.StringField(max_length=10)

    meta = {
        'strict': False
    }


class ShoppingList(BaseDocument):
    name = mongo.StringField(required=True)
    items = mongo.EmbeddedDocumentListField('ShoppingListItem', default=None)

    meta = {
        'collection': 'shopping_lists'
    }

    def __repr__(self):
        return "<ShoppingList '{}'>".format(self.name)
