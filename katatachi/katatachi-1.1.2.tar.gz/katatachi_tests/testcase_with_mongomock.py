import unittest
import mongomock
import pymongo
from typing import Dict, List
from katatachi.content import ContentStore
from katatachi.worker import MetadataStoreFactory, WorkerRunStore


# can't skip this
class TestCaseWithMongoMock(unittest.TestCase):
    @classmethod
    @mongomock.patch("mongodb://localhost:27017/test_db")
    def setUpClass(cls) -> None:
        cls.content_store = ContentStore("localhost:27017", "test_db")
        cls.metadata_store_factory = MetadataStoreFactory("localhost:27017", "test_db")
        cls.worker_run_store = WorkerRunStore("localhost:27017", "test_db", unittest.mock.MagicMock())

    def tearDown(self) -> None:
        self.content_store.client.drop_database("test_db")

    def actual_documents_by_id_desc(self) -> List[Dict]:
        actual_documents = []
        for d in self.content_store.collection.find(
            {}, sort=[("_id", pymongo.DESCENDING)]
        ):
            actual_documents.append(d)
        return actual_documents

    def actual_documents_without_id(self) -> List[Dict]:
        actual_cursor = self.content_store.collection.find({})
        actual_documents = []
        for actual_document in actual_cursor:
            del actual_document["_id"]
            actual_documents.append(actual_document)
        return actual_documents
