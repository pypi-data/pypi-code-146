import logging

from fs_task_queue.core import Worker, Queue, Job

import distributed


logger = logging.getLogger(__name__)


def execute_function(job: Job):
    job()


class DaskWorker(Worker):
    def __init__(self, queue: Queue, client: distributed.Client = None, **kwargs):
        super().__init__(queue)
        if client is None:
            self.client = distributed.Client(**kwargs)
        else:
            self.client = client

    def run(self):
        logger.info(f"Starting worker {self.id} on queue={self.queue}")
        try:
            self.register_worker()
            while True:
                self.check_shutdown()
                # must send heartbeat after shutdown check
                # since heartbeat will create file if it doesn't exist
                self.send_heartbeat()
                try:
                    job = self.queue.dequeue()
                    logger.info(f"Submitted job {job} via dask client")
                    self.client.submit(execute_function, job)
                except TimeoutError:
                    pass
        finally:
            self.unregister_worker()


class DaskJob(Job):
    pass
