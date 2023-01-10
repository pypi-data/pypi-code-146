"""Persistent recording of a workflow executions.

When the "PYPUSHFLOW_MONGOURL" environment variable is specified,
the default database client is the BesDB client. Otherwise the
default client is a dummy client.
"""

import os
from typing import Callable
from .interface import WorkflowDbClient
from .pymongo import PyMongoWorkflowDbClient  # noqa F401
from .besdb import BesWorkflowDbClient  # noqa F401
from .mongita import MemoryWorkflowDbClient  # noqa F401
from .dummy import DummyWorkflowDbClient  # noqa F401

DEFAULT_DB_TYPE = "dummy"


def db_client(*args, db_type=None, **kwargs) -> WorkflowDbClient:
    if db_type is None:
        if os.environ.get("PYPUSHFLOW_MONGOURL"):
            db_type = "besdb"
        else:
            db_type = DEFAULT_DB_TYPE
    db_client_class = WorkflowDbClient.get_dbclient_class(db_type)
    client = db_client_class(*args, **kwargs)
    client.connect()
    return client


def register_actorinfo_filter(method: Callable):
    WorkflowDbClient.register_actorinfo_filter(method)
