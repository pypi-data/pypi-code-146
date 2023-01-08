from datetime import datetime
from bson import ObjectId

from .. import mongo

class BaseDocument(mongo.Document):

  _id = mongo.ObjectIdField(primary_key='True', db_field='_id', default=lambda: ObjectId())

  owner = mongo.ReferenceField('User', required=True)

  insert_timestamp = mongo.LongField(required=True, default=lambda: int(datetime.utcnow().timestamp()*1000))
  update_timestamp = mongo.LongField(required=True, default=lambda: int(datetime.utcnow().timestamp()*1000))

  meta = {
    'abstract': True,
    'strict': False
  }
