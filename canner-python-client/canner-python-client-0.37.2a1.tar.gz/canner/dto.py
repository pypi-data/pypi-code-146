from enum import Enum
from typing import Optional, Union
from dataclasses import dataclass


class SqlQueryStatus(Enum):
    QUEUED = "QUEUED"
    # Query has been accepted and is awaiting execution.
    WAITING_FOR_RESOURCES = "WAITING_FOR_RESOURCES"
    # Query is waiting for the required resources (beta).
    DISPATCHING = "DISPATCHING"
    # Query is being dispatched to a coordinator.
    PLANNING = "PLANNING"
    # Query is being planned.
    STARTING = "STARTING"
    # Query execution is being started.
    RUNNING = "RUNNING"
    # Query has at least one running task.
    FINISHING = "FINISHING"
    # Query is finishing (e.g. commit for autocommit queries)
    FINISHED = "FINISHED"
    # Query has finished executing and all output has been consumed.
    EXPIRED = "EXPIRED"
    # Query has expired.
    FAILED = "FAILED"
    # Query execution failed.
    CANCELED = "CANCELED"
    ABORTED = "ABORTED"
    PLANNED = "PLANNED"


@dataclass(frozen=True)
class SqlQueryResult(object):
    id: str
    status: str
    error: dict
    statementId: str
    rowCount: int = 0
    columns: Optional[Union[dict, list]] = None
    location: Optional[str] = None

    # just for rename use
    @property
    def row_count(self) -> int:
        return self.rowCount
