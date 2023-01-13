import logging
import pymongo
from typing import Dict
from enum import Enum
from dataclasses import dataclass
from katatachi.utils import now_ms
from katatachi.interface.worker import Worker
from .worker_cache import WorkerCache


class WorkerRunState(Enum):
    Pending = "pending"
    Running = "running"
    Succeeded = "succeeded"
    Failed = "failed"


@dataclass
class WorkerRunMetadata:
    module_name: str
    args: Dict
    run_id: str


logger = logging.getLogger(__name__)


class WorkerRunStore(object):
    PageSizeLimit = 10

    def __init__(self, connection_string: str, db: str, worker_cache: WorkerCache):
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db]
        self.collection = self.db["worker_runs"]
        self.collection.create_index([
            ("worker_id", pymongo.ASCENDING),
            ("run_id", pymongo.ASCENDING),
        ])
        self.worker_cache = worker_cache

    def add(self, worker_run_metadata: WorkerRunMetadata, initial_state: WorkerRunState):
        module_name, args = worker_run_metadata.module_name, worker_run_metadata.args
        status, worker_or_message = self.worker_cache.load(module_name, args)
        if not status:
            raise RuntimeError(
                f"Fails to load worker, module_name={module_name}, args={args}, message={worker_or_message}"
            )
        worker = worker_or_message  # type: Worker
        worker_id = worker.get_id()

        self.collection.insert({
            "worker_id": worker_id,
            "run_id": worker_run_metadata.run_id,
            "created_ms": now_ms(),
            "logs": [],
            "state": initial_state.value,
        })

    def log(self, worker_id: str, run_id: str, message: str):
        self.collection.update_one(
            filter={
                "worker_id": worker_id,
                "run_id": run_id,
            },
            update={
                "$push": {
                    "logs": {
                        "created_ms": now_ms(),
                        "message": message,
                    }
                }
            }
        )

    def update_state(self, worker_id: str, run_id: str, state: WorkerRunState):
        self.collection.update_one(
            filter={
                "worker_id": worker_id,
                "run_id": run_id,
            },
            update={
                "$set": {
                    "state": state.value,
                }
            }
        )

    def get_runs(self, page: int):
        page -= 1
        cursor = self.collection\
            .find()\
            .sort("created_ms", pymongo.DESCENDING)\
            .skip(page * self.PageSizeLimit)\
            .limit(self.PageSizeLimit)
        runs = []
        for doc in cursor:
            runs.append({
                "worker_id": doc["worker_id"],
                "run_id": doc["run_id"],
                "created_ms": doc["created_ms"],
                "logs": doc["logs"],
                "state": doc["state"],
            })
        return runs
