import copy
import dataclasses
import logging
import typing
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Repeat the given tasks for multiple times.

    The tasks are run on a cloned context. The outputs of a run won't be available on the next run. The tasks can use REPEAT_TASKS_INDEX environment variable to get the index of the current run.

    If float_output_names is specified, the task collects those outputs and returns a list.

    Config:
        num_repeats (int): The number of repeats.
        tasks (List[TaskDescription]): The tasks to be repeated.
        float_output_names (List[str]): The name of outputs to collect.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False
    RESOLVE_CONFIG_VARIABLES = False

    @dataclasses.dataclass
    class Inputs:
        pass

    @dataclasses.dataclass
    class Config:
        num_repeats: int
        tasks: typing.List[irisml.core.TaskDescription]
        float_output_names: typing.List[str] = dataclasses.field(default_factory=list)

    @dataclasses.dataclass
    class Outputs:
        float_output_values: typing.List[typing.List[float]]

    def execute(self, inputs):
        return self._execute(inputs, dry_run=False)

    def dry_run(self, inputs):
        return self._execute(inputs, dry_run=True)

    def _execute(self, inputs, dry_run):
        config_without_tasks = copy.deepcopy(self.config)
        config_without_tasks.tasks = []
        resolved_config = self.context.resolve(config_without_tasks)
        logger.debug(f"{resolved_config=}")

        for output_names in resolved_config.float_output_names:
            if output_names.count('.') != 1:
                raise ValueError(f"The output name must be '<task_name>.<output_name>'. Actual: {output_names}")

        tasks = []
        for task_description in self.config.tasks:
            task = irisml.core.Task(task_description)
            task.load_module()
            tasks.append(task)

        output_task_variable_names = [names.split('.') for names in resolved_config.float_output_names]

        all_output_values = []
        for index in range(resolved_config.num_repeats):
            logger.info(f"Repeat {index}: Start running the tasks.")

            context = self.context.clone()
            context.add_environment_variable('REPEAT_TASKS_INDEX', index)

            for task in tasks:
                task.execute(context, dry_run=dry_run)

            output_values = [getattr(context.get_outputs(t), v) for t, v in output_task_variable_names]
            all_output_values.append(output_values)

            logger.debug(f"Repeat {index}: The outputs are {output_values}")

        return self.Outputs(all_output_values)
