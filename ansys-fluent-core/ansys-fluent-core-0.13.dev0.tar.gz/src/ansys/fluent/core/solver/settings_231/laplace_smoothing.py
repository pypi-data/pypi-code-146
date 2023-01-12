#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enabled_2 import enabled
from .set_2 import set
class laplace_smoothing(Group):
    """
    'laplace_smoothing' child.
    """

    fluent_name = "laplace-smoothing"

    child_names = \
        ['enabled', 'set']

    enabled: enabled = enabled
    """
    enabled child of laplace_smoothing.
    """
    set: set = set
    """
    set child of laplace_smoothing.
    """
