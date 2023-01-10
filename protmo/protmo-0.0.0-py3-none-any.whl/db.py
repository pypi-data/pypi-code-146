from pymongo import MongoClient
from google.protobuf.json_format import MessageToDict, ParseDict
import uuid
import time
from typing import Dict
from typing import List

from protmo.pm import Message

DB_KEY = 1


class Db:
    '''
    Db is an abstration on top of MongoDb and provides a fitting interface to
    integrate with the rest of the application and one, that can be potentially
    overridden by different database layers in the future. It should be the only
    class, that knowns about internals of Mongodb.
    '''

    def __init__(self, host: str, port: int, name: str) -> None:
        self.client = MongoClient(host, port)
        self.name = name
        self.db = self.client[name]

    def store(self, message: Message) -> Message:
        '''
        Takes a message, converts it into a mongodb-compatible JSON and stores it
        in a mongodb collection. Message only wraps protobuf-messages, thus generating
        a json from it can be done with the usual probuf mechanisms (e.g. MessageToDict).
        The id of the message plays an important role. If the message defines an id (of
        type string) it is used as document-id.

        The message.full_name is used as the name of the collection. If the collection
        does not already exist, it is created on the fly.

        If the document already exists in the collection (only possible if the passed
        message has an ID), it is updated.

        If the new message has less fields than the
        document in the database, the fields are not deleted. This can happen, if you
        roll back your change where you added a field to you protobuf-message definition.
        In this way, no data is lost.
        '''

        # TODO: check if it is already a proto-message,
        #       or wether it is a wrapped one
        table = self.db[message.DESCRIPTOR.full_name]

        doc = MessageToDict(message)
        if not doc.get('id'):
            doc['id'] = str(uuid.uuid4())

        updating = bool(table.find_one({'_id': doc['id']}))
        if hasattr(message, 'set_defaults'):
            message.set_defaults(creating=not updating)

        doc2 = MessageToDict(message)
        doc2['id'] = doc['id']
        doc2['_id'] = doc['id']
        doc = doc2

        # TODO: use upsert
        if updating:
            table.update_one({'_id': doc['id']}, {'$set': doc})
        else:
            table.insert_one(doc)

        # This does return a protobuf-message / object of the same type
        # as it was given as parameter in the signature, as we pass in
        # the message (from the parameter), which ParseDict fills with
        # the contents of the doc.
        # ignore_unknown_fields makes it OK, that there are more fields
        # in the database-doc than in the message. This happens when we
        # store metadata, like _id or deleted a field (we don't want to
        # loose this data)
        return ParseDict(doc, message, ignore_unknown_fields=True)

    def query(self, messageClass: type, query: Dict = {},
              include_deleted: bool = False) -> List[Message]:
        '''
        Takes the Message-Class (so that it knows which collection to query) and
        a mongodb-syle query and returns all documents that mongodb finds, converted
        to the message.
        It returns a list of Message of the same type as the messageType in the
        parameter-list.
        Per default, it ignores soft-deleted entries (which have _deleted=True set
        in the document). But if you set include_deleted, they can become part of the
        result as well.
        '''

        message = messageClass()
        table = self.db[message.DESCRIPTOR.full_name]

        soft_delete_condition = {'$or': [{'_deleted': None}, {
            '_deleted': {'$exists': include_deleted}}]}
        docs = table.find({'$and': [query, soft_delete_condition]})
        res = []
        for doc in docs:
            res.append(
                ParseDict(
                    doc,
                    messageClass(),
                    ignore_unknown_fields=True))
        return res

    def delete(self, message: Message, hard: bool = False):
        '''
        Soft-deletes a given message from the mongodb collection. If you set
        hard=True, is actually deleted. Soft-delete means, that _deleted=True is set
        to the document, which is per default ignored then by the query method
        '''
        table = self.db[message.DESCRIPTOR.full_name]
        if hard:  # hard-delte
            table.delete_one({'_id': message.id})
        else:  # soft-delete
            timestamp = int(time.time() * 1000)
            table.update_one({'_id': message.id},
                             {'$set': {'_deleted': timestamp}})

    def undelete(self, message: Message):
        '''
        You can use this to undo a soft-delete. Just remove the '_deleted=True'
        from the document in the collection.
        '''
        table = self.db[message.DESCRIPTOR.full_name]
        table.update_one({'_id': message.id}, {'$set': {'_deleted': None}})
