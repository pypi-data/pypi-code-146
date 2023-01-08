from .. import mongo

from .base_document import BaseDocument

class Config(mongo.Document):
    min_version_code = mongo.IntField(unique=True, required=True)
    require_update = mongo.BooleanField(default=False)

    properties = mongo.DictField(default=dict())

    meta = {
        'collection' : 'configs'
    }

    def __repr__(self):
           return "<Config '{}'>".format(self.properties)