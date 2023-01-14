import celery
from typing import Dict, Optional
from dataclasses import dataclass
from celery.utils.log import get_task_logger
from katatachi.worker import WorkFactory
from katatachi.utils import now_ms, getenv_or_meh


@dataclass
class WorkerPayload:
    type: str
    module_name: str
    args: Dict
    created_ms: Optional[int]

    def to_json(self):
        return {
            "type": self.type,
            "module_name": self.module_name,
            "args": self.args,
            "created_ms": self.created_ms
        }

    @staticmethod
    def from_json(d: Dict):
        return WorkerPayload(
            d["type"],
            d["module_name"],
            d["args"],
            d.get("created_ms", None)
        )


DEFAULT_WORK_EXPIRATION_MS = 3600 * 1000  # 1 hour
logger = get_task_logger(__name__)


class WorkerQueue(object):
    def __init__(self, redis_url: str, work_factory: WorkFactory):
        self.celery_app = celery.Celery(
            "worker",
            broker=redis_url,
            task_serializer='pickle',
            accept_content=['pickle'],
        )

        @self.celery_app.task
        def _worker(payload: WorkerPayload):
            module_name, args, created_ms = payload.module_name, payload.args, payload.created_ms
            if created_ms is not None \
                    and created_ms + getenv_or_meh("WORK_EXPIRATION_MS", DEFAULT_WORK_EXPIRATION_MS) < now_ms():
                logger.warning(f"Work expired, module={module_name}, args={args}")
                return
            work_func_and_id = work_factory.get_work_func(module_name, args)
            if not work_func_and_id:
                return
            work_func, worker_id = work_func_and_id
            work_func()

        self._worker = _worker

    def enqueue(self, payload: WorkerPayload):
        self._worker.delay(payload)

    def start_worker(self):
        argv = [
            'worker',
            '--loglevel=DEBUG',
        ]
        self.celery_app.worker_main(argv)
