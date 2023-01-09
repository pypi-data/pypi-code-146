#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .verbosity_8 import verbosity
from .time_step_method_1 import time_step_method
class pseudo_time_settings(Group):
    """
    'pseudo_time_settings' child.
    """

    fluent_name = "pseudo-time-settings"

    child_names = \
        ['verbosity', 'time_step_method']

    verbosity: verbosity = verbosity
    """
    verbosity child of pseudo_time_settings.
    """
    time_step_method: time_step_method = time_step_method
    """
    time_step_method child of pseudo_time_settings.
    """
