import logging
import time
from katatachi.worker import WorkFactory
from katatachi.utils import now_ms, getenv_or_meh
from .worker_queue import WorkerQueue

logger = logging.getLogger(__name__)

DEFAULT_WORK_EXPIRATION_MS = 3600 * 1000  # 1 hour
WORKER_POLLING_INTERVAL = 5


def poll(worker_queue: WorkerQueue, work_factory: WorkFactory):
    payload = worker_queue.blocking_dequeue()
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


def start_worker_blocking(worker_queue: WorkerQueue, work_factory: WorkFactory):
    try:
        while True:
            poll(worker_queue, work_factory)
            time.sleep(WORKER_POLLING_INTERVAL)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Worker stopping...")
