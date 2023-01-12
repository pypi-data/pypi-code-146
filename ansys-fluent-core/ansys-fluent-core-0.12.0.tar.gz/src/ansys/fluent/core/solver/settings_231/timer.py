#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .usage import usage
from .reset_1 import reset
class timer(Group):
    """
    'timer' child.
    """

    fluent_name = "timer"

    command_names = \
        ['usage', 'reset']

    usage: usage = usage
    """
    usage command of timer.
    """
    reset: reset = reset
    """
    reset command of timer.
    """
