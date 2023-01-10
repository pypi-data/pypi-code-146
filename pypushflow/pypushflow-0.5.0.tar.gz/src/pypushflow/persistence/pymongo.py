from typing import Optional

try:
    from bson.objectid import ObjectId
    from pymongo import MongoClient
except Exception:
    ObjectId = None
    MongoClient = None
from .mongo import MongoWorkflowDbClient


class PyMongoWorkflowDbClient(MongoWorkflowDbClient, register_name="pymongo"):
    """Client of an external Mongo database for storing workflow executions."""

    def connect(self, url: str, database: str, collection: str):
        if MongoClient is None:
            return
        client = MongoClient(url, serverSelectionTimeoutMS=1000)
        self._client = client
        self._collection = client[database][collection]

    def disconnect(self, *args, **kw):
        self._collection = None
        if self._client is not None:
            self._client.close()
            self._client = None

    def generateWorkflowId(self, oid: Optional[str] = None) -> ObjectId:
        return ObjectId(oid=oid)

    def generateActorId(self, oid: Optional[str] = None) -> ObjectId:
        return ObjectId(oid=oid)

    def _appendActorInfo(self, actorInfo: dict):
        self._collection.update_one(
            {"_id": self._workflowId}, {"$push": {"actors": actorInfo}}
        )
