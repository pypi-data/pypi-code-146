import unittest
from pypushflow.persistence import db_client
from .besdbTestCase import BesDBTestCase


class PersistenceTests:
    def setUp(self):
        super().setUp()
        self.skip_message = ""

    def test_Workflow(self):
        name = "test_startWorkflow"
        self.db_client.startWorkflow(name=name)
        info = self.db_client.getWorkflowInfo()
        if info is None:
            self.skipTest(self.skip_message)
            return
        self.assertEqual(info["status"], "started")

        self.db_client.updateWorkflowInfo({"status": "error"})
        status = self.db_client.getWorkflowInfo()["status"]
        self.assertEqual(status, "error")

        self.db_client.endWorkflow()
        status = self.db_client.getWorkflowInfo()["status"]
        self.assertEqual(status, "error")

    def test_Actor(self):
        name = "test_startWorkflow"
        self.db_client.startWorkflow(name=name)
        actorName1 = "TestActor1"

        actorId1 = self.db_client.startActor(actorName1)
        info = self.db_client.getActorInfo(actorId1)
        if info is None:
            self.skipTest(self.skip_message)
            return
        self.assertEqual(info["status"], "started")

        self.db_client.updateActorInfo(actorId1, {"status": "error"})
        status = self.db_client.getActorInfo(actorId1)["status"]
        self.assertEqual(status, "error")

        self.db_client.endActor(actorId1)
        status = self.db_client.getActorInfo(actorId1)["status"]
        self.assertEqual(status, "error")

        actorName2 = "TestActor2"
        actorId2 = self.db_client.startActor(name=actorName2)
        status = self.db_client.getActorInfo(actorId2)["status"]
        self.assertEqual(status, "started")

        self.db_client.updateActorInfo(actorId2, {"data": {"a": 1}})
        data = self.db_client.getActorInfo(actorId2)["data"]
        self.assertEqual(data, {"a": 1})

        self.db_client.endActor(actorId2)
        status = self.db_client.getActorInfo(actorId2)["status"]
        self.assertEqual(status, "finished")


class TestDummyPersistence(unittest.TestCase, PersistenceTests):
    def setUp(self):
        super().setUp()
        self.skip_message = "dummy"
        self.db_client = db_client(db_type="dummy")
        self.db_client.connect()


class TestMemoryPersistence(unittest.TestCase, PersistenceTests):
    def setUp(self):
        super().setUp()
        self.skip_message = "requires the 'mongita' library"
        self.db_client = db_client(db_type="memory")
        self.db_client.connect()


class TestBesDBPersistence(BesDBTestCase, PersistenceTests):
    def setUp(self):
        super().setUp()
        self.skip_message = "requires external database and the 'pymongo' library"
        self.db_client = db_client(db_type="besdb")
        self.db_client.connect()
