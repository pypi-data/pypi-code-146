import dataclasses
import logging
from typing import List, Optional
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """'If' conditional branch.

    If the condition is True, runs the tasks in 'then_tasks'. If the 'condition' is False, run the tasks in 'else_tasks'.
    """
    VERSION = '0.1.1'
    CACHE_ENABLED = False
    RESOLVE_CONFIG_VARIABLES = False

    @dataclasses.dataclass
    class Config:
        condition: bool
        then_tasks: List[irisml.core.TaskDescription]
        else_tasks: Optional[List[irisml.core.TaskDescription]] = dataclasses.field(default_factory=list)

    def execute(self, inputs):
        return self._execute_core(inputs, dry_run=False)

    def dry_run(self, inputs):
        return self._execute_core(inputs, dry_run=True)

    def _execute_core(self, inputs, dry_run):
        resolved_condition = self.context.resolve(self.config.condition)
        logger.info(f"Condition is {resolved_condition}")

        tasks = self.config.then_tasks if resolved_condition else self.config.else_tasks
        for task_description in tasks:
            task = irisml.core.Task(task_description)
            task.load_module()
            task.execute(self.context, dry_run=dry_run)

        return self.Outputs()
