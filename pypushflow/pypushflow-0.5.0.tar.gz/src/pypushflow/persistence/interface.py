from typing import Callable, Optional


class WorkflowDbClient:
    """Client interface of a database for storing workflow executions."""

    _REGISTRY = dict()
    _ACTORINFO_FILTERS = list()

    def __init_subclass__(cls, register_name=None) -> None:
        super().__init_subclass__()
        if register_name:
            WorkflowDbClient._REGISTRY[register_name] = cls

    @classmethod
    def get_dbclient_class(cls, name):
        return WorkflowDbClient._REGISTRY.get(name, None)

    @classmethod
    def register_actorinfo_filter(cls, method: Callable[[dict], dict]):
        if method not in cls._ACTORINFO_FILTERS:
            WorkflowDbClient._ACTORINFO_FILTERS.append(method)

    @classmethod
    def apply_actorinfo_filters(cls, info: dict) -> dict:
        for method in WorkflowDbClient._ACTORINFO_FILTERS:
            info = method(info)
        return info

    def connect(self, *args, **kw):
        raise NotImplementedError

    def disconnect(self, *args, **kw):
        raise NotImplementedError

    def startWorkflow(self, name: str):
        raise NotImplementedError

    def endWorkflow(self, status="finished") -> None:
        raise NotImplementedError

    def updateWorkflowInfo(self, info: dict) -> None:
        raise NotImplementedError

    def setWorkflowStatus(self, status: str) -> None:
        self.updateWorkflowInfo({"status": status})

    def getWorkflowInfo(self) -> Optional[dict]:
        raise NotImplementedError

    def startActor(
        self, name: str, info: Optional[dict] = None, script: Optional[str] = None
    ):
        raise NotImplementedError

    def endActor(self, actorId, status="finished") -> None:
        raise NotImplementedError

    def updateActorInfo(self, actorId, info: dict) -> None:
        raise NotImplementedError

    def setActorStatus(self, actorId, status: str) -> None:
        self.updateActorInfo(actorId, {"status": status})

    def getActorInfo(self, actorId) -> Optional[None]:
        raise NotImplementedError
