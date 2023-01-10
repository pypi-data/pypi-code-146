from typing import Optional
from .interface import WorkflowDbClient


class DummyWorkflowDbClient(WorkflowDbClient, register_name="dummy"):
    """Client without a database. Used for testing purposes."""

    def connect(self, *args, **kw):
        pass

    def disconnect(self, *args, **kw):
        pass

    def startWorkflow(self, name: str):
        pass

    def endWorkflow(self, status="finished") -> None:
        pass

    def updateWorkflowInfo(self, info: dict) -> None:
        pass

    def getWorkflowInfo(self) -> Optional[dict]:
        pass

    def startActor(
        self, name: str, info: Optional[dict] = None, script: Optional[str] = None
    ):
        pass

    def endActor(self, actorId, status="finished") -> None:
        pass

    def updateActorInfo(self, actorId, info: dict) -> None:
        pass

    def getActorInfo(self, actorId) -> Optional[None]:
        pass
