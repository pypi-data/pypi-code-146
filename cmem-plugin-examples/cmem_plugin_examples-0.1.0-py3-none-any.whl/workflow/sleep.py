"""sleep workflow plugin module"""
from time import sleep

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import (
    Plugin,
    PluginParameter
)
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin


@Plugin(
    label="Sleep",
    plugin_id="Example-Sleep",
    description="Sleep for a certain amount of seconds",
    documentation="""
This example workflow operator sleeps for a certain amount of seconds.
""",
    parameters=[
        PluginParameter(
            name="seconds",
            label="Seconds",
            description="How long do you want to sleep.",
        ),
    ],
)
class RandomValues(WorkflowPlugin):
    """Example Workflow Plugin: Sleep"""

    def __init__(
        self,
        seconds: int = 10
    ) -> None:
        if seconds < 1:
            raise ValueError("Entities (Rows) needs to be a positive integer.")
        self.seconds = seconds

    def execute(
        self, inputs=(), context: ExecutionContext = ExecutionContext()
    ) -> None:
        self.log.info(f"Start sleeping for {self.seconds} seconds.")
        sleep(self.seconds)
        self.log.info(f"Stop sleeping for {self.seconds} seconds.")
