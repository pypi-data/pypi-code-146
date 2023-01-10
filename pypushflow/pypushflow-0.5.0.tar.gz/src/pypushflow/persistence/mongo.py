import logging
from datetime import datetime
from typing import Optional
from .interface import WorkflowDbClient

logger = logging.getLogger(__name__)


class MongoWorkflowDbClient(WorkflowDbClient):
    """Client interface of a Mongo database for storing workflow executions."""

    def __init__(self):
        self._collection = None
        self._workflowId = None

    def generateWorkflowId(self, *args, **kw):
        raise NotImplementedError

    def generateActorId(self, *args, **kw):
        raise NotImplementedError

    def startWorkflow(self, name: str):
        if self._collection is None:
            return
        if self._workflowId is not None:
            raise RuntimeError("Workflow start already logged")
        workflowInfo = self._generateInitialWorkflowInfo()
        workflowInfo["name"] = name
        workflowInfo["status"] = "started"
        workflowInfo["startTime"] = datetime.now()
        try:
            self._collection.insert_one(workflowInfo)
        except Exception:
            self._collection = None
            logger.exception("Mongo database error")
        self._workflowId = workflowInfo["_id"]

    def endWorkflow(self, status="finished") -> None:
        if self._skip:
            return
        workflowInfo = self._workflowInfo
        if workflowInfo["status"] != "error":
            workflowInfo["status"] = status
        workflowInfo["stopTime"] = datetime.now()
        self._workflowInfo = workflowInfo

    def updateWorkflowInfo(self, info: dict) -> None:
        if self._skip:
            return
        workflowInfo = self._workflowInfo
        workflowInfo.update(info)
        self._workflowInfo = workflowInfo

    def getWorkflowInfo(self) -> Optional[dict]:
        if self._collection is None:
            return
        return self._workflowInfo

    def startActor(self, name: str, info: Optional[str] = None):
        if self._skip:
            return
        actorInfo = self._generateInitialActorInfo()
        actorInfo["name"] = name
        actorInfo["status"] = "started"
        if info:
            actorInfo.update(info)
        actorInfo["startTime"] = datetime.now()
        actorInfo = self.apply_actorinfo_filters(actorInfo)
        self._appendActorInfo(actorInfo)
        return actorInfo["_id"]

    def _appendActorInfo(self, actorInfo: dict):
        raise NotImplementedError

    def endActor(self, actorId, status="finished") -> None:
        if self._skip:
            return
        workflowInfo = self._workflowInfo
        for actorInfo in workflowInfo["actors"]:
            if actorInfo["_id"] == actorId:
                if actorInfo["status"] != "error":
                    actorInfo["status"] = status
                actorInfo["stopTime"] = datetime.now()
                self._workflowInfo = workflowInfo
                break

    def updateActorInfo(self, actorId, info: dict) -> None:
        if self._skip:
            return
        info = self.apply_actorinfo_filters(info)
        workflowInfo = self._workflowInfo
        for actorInfo in workflowInfo["actors"]:
            if actorInfo["_id"] == actorId:
                actorInfo.update(info)
                self._workflowInfo = workflowInfo
                break

    def getActorInfo(self, actorId) -> Optional[None]:
        if self._skip:
            return
        workflowInfo = self._workflowInfo
        for actorInfo in workflowInfo["actors"]:
            if actorInfo["_id"] == actorId:
                return actorInfo

    @property
    def _skip(self):
        if self._collection is None:
            return True
        if self._workflowId is None:
            raise RuntimeError("Workflow start not logged")
        return False

    def _generateInitialWorkflowInfo(self) -> dict:
        oid = self.generateWorkflowId()
        return {
            "_id": oid,
            "Request ID": str(oid),
            "name": "unknown",
            "status": "unknown",
            "actors": [],
        }

    def _generateInitialActorInfo(self) -> dict:
        oid = self.generateActorId()
        return {
            "_id": oid,
            "name": "unknown",
            "status": "unknown",
        }

    @property
    def _workflowInfo(self) -> dict:
        return self._collection.find_one({"_id": self._workflowId})

    @_workflowInfo.setter
    def _workflowInfo(self, info: dict):
        self._collection.update_one(
            {"_id": self._workflowId}, {"$set": info}, upsert=False
        )
