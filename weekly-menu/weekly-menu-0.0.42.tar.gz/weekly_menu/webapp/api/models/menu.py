from .. import mongo

from .base_document import BaseDocument

class Menu(BaseDocument):
    name = mongo.StringField()
    date = mongo.DateField(required=True)
    meal = mongo.StringField()
    recipes = mongo.ListField(
        mongo.ReferenceField('Recipe', reverse_delete_rule=mongo.PULL), default=None
    )

    #It could be useful to have an history of user's menu also when they leave
    # REMOVED - probably not usefull
    # owner = mongo.ReferenceField('User', required=True, reverse_delete_rule=mongo.NULLIFY)

    meta = {
        'collection' : 'menu'
    }

    def __repr__(self):
           return "<Menu '{}'>".format(self.name)
