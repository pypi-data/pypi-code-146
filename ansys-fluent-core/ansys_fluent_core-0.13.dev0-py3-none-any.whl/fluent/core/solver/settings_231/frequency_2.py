#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_12 import option
from .iterations import iterations
from .time_steps import time_steps
class frequency(Group):
    """
    Define the frequency at which cells in the register are automatically marked for poor mesh numerics treatment.
    """

    fluent_name = "frequency"

    child_names = \
        ['option', 'iterations', 'time_steps']

    option: option = option
    """
    option child of frequency.
    """
    iterations: iterations = iterations
    """
    iterations child of frequency.
    """
    time_steps: time_steps = time_steps
    """
    time_steps child of frequency.
    """
