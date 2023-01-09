"""User info workflow plugin module"""
from time import sleep
from typing import Sequence, Tuple

from cmem_plugin_base.dataintegration.context import (ExecutionContext,
                                                      ExecutionReport,
                                                      PluginContext)
from cmem_plugin_base.dataintegration.description import Plugin
from cmem_plugin_base.dataintegration.entity import Entities
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin


@Plugin(
    label="Report user info",
    description="Example plugin that reads user info and writes it to the execution "
    "report. ",
)
class UserInfoWorkflowPlugin(WorkflowPlugin):
    """Report user info plugin"""

    def __init__(self, context: PluginContext):
        self.init_user = context.user

    @staticmethod
    def _get_clock(counter: int) -> str:
        """returns a clock symbol"""
        clock = {
            0: "🕛",
            1: "🕐",
            2: "🕑",
            3: "🕓",
            4: "🕔",
            5: "🕕",
            6: "🕖",
            7: "🕗",
            8: "🕘",
            9: "🕚",
        }
        return clock[int(repr(counter)[-1])]

    def execute(self, inputs: Sequence[Entities], context: ExecutionContext) -> None:
        summary: list[Tuple[str, str]] = []
        warnings: list[str] = []
        if self.init_user is None or context.user is None:
            warnings.append("User info not available")
        else:
            summary.append(("Loaded by", self.init_user.user_uri()))
            summary.append(("Executed by", context.user.user_uri()))

        for count in range(1, 100):
            step = 0.1
            sleep(step)
            description = f"times {step} seconds waited 🤓 - {self._get_clock(count)}"
            context.report.update(
                ExecutionReport(
                    entity_count=count,
                    operation="wait",
                    operation_desc=description,
                )
            )

        context.report.update(
            ExecutionReport(
                summary=summary,
                warnings=warnings,
            )
        )
