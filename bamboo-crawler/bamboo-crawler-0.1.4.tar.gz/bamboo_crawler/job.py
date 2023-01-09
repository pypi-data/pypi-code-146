from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from .directives.default import DefaultSearcher
from .directives.searcher import DirectiveSearcher
from .task import Task


@dataclass(frozen=True)
class Job:
    tasks: list[Task]

    def run(self, *, loop: bool = False, cooldown: float = 0.0) -> None:
        if loop:
            while True:
                self._run(cooldown=cooldown)
        else:
            self._run()

    def _run(self, *, cooldown: float = 0.0) -> None:
        for task in self.tasks:
            task.do()
        time.sleep(cooldown)

    @classmethod
    def from_job_directive(  # type: ignore
        cls,
        raw_directive: dict[str, Any],
        *,
        searcher: DirectiveSearcher = DefaultSearcher,
    ) -> Job:
        tasks = [
            searcher.define_task(
                task_name,
                definitions,
            )
            for task_name, definitions in raw_directive.items()
        ]
        return cls(tasks=tasks)

    def filter_task_by_names(self, task_names: list[str]) -> Job:
        task_by_name = {task.name: task for task in self.tasks}
        new_tasks = []
        for task_name in task_names:
            if task_name in task_by_name:
                task = task_by_name[task_name]
                new_tasks.append(task)
            else:
                raise NotImplementedError(f"Unexpected task: {task_name}")

        return self.__class__(tasks=new_tasks)
