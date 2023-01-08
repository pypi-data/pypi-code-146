from .. import mongo
from .base_document import BaseDocument

class SupermarketSection(mongo.EmbeddedDocument):
    MAX_SECTION_NAME_LENGTH = 50

    name = mongo.StringField(max_length=MAX_SECTION_NAME_LENGTH, required=True)
    color = mongo.IntField(max_length=MAX_SECTION_NAME_LENGTH)

class UserPreferences(BaseDocument):
    supermarket_sections = mongo.EmbeddedDocumentListField(SupermarketSection, default=None)
    
    shopping_days = mongo.ListField(mongo.IntField(min_value=1, max_value=7), default=None)
    units_of_measure = mongo.ListField(mongo.StringField(min_value=1, max_value=10), default=None)

    meta = {
        'collection' : 'user_preferences'
    }

    def __repr__(self):
           return "<UserPreferences '{}, {}'>".format(self.supermarketSections, self.shoppingDays, self.units_of_measure)