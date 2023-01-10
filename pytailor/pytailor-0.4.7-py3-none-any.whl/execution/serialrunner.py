from typing import Optional, List

from pytailor.clients import RestClient
from pytailor.models import TaskCheckout, TaskExecutionData
from pytailor.utils import get_logger
from .taskrunner import run_task


class SerialRunner:
    def __init__(
        self,
        project_id: str,
        worker_name: str,
        workflow_id: str,
        capabilities: List[str] = None,
    ):
        self.project_id = project_id
        self.worker_name = worker_name
        self.workflow_id = workflow_id
        self.capabilities = capabilities or ["pytailor"]

    def run(self):
        logger = get_logger("SerialRunner")
        logger.info(f"Starting workflow with id {self.workflow_id}")

        # checkout and run tasks

        checkout_query = TaskCheckout(
            worker_capabilities=self.capabilities,
            worker_name=self.worker_name,
            workflows=[self.workflow_id],
        )

        checkout = self.do_checkout(checkout_query)

        while checkout:
            run_task(checkout)
            checkout = self.do_checkout(checkout_query)

        logger.info(f"Workflow with id {self.workflow_id} finished")

    def do_checkout(self, checkout_query: TaskCheckout) -> Optional[TaskExecutionData]:
        with RestClient() as client:
            return client.checkout_task(checkout_query)
