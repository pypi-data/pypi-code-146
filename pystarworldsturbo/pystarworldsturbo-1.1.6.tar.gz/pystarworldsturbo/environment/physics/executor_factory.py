from pyoptional.pyoptional import PyOptional

from .action_executor import ActionExecutor
from ...common.action import Action
from ...utils.utils import ignore


class ExecutorFactory():
    @staticmethod
    def get_executor_for(action: Action) -> PyOptional[ActionExecutor]:
        # Abstract.
        ignore(action)

        raise NotImplementedError()
