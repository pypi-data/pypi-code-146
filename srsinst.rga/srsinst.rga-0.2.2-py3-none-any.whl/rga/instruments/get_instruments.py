import logging
from srsgui.task import Task
from srsinst.rga import RGA100

logger = logging.getLogger(__name__)


def get_rga(task: Task, name=None) -> RGA100:
    """
    Instead of using task.get_instrument() directly in a Task subclass,
    Defining a wrapper function with a instrument return type will help
    a context-sensitive editors display  attributes available
    for the instrument class.
    """
    if name is None:
        inst = list(task.inst_dict.values())[0]
    else:
        inst = task.get_instrument(name)

    if issubclass(type(inst), RGA100):
        return inst
    else:
        logger.error('{} is not {}'.format(type(inst), RGA100))
        return None
