#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enabled_3 import enabled
from .set_5 import set
class conjugate_heat_transfer(Group):
    """
    'conjugate_heat_transfer' child.
    """

    fluent_name = "conjugate-heat-transfer"

    child_names = \
        ['enabled', 'set']

    enabled: enabled = enabled
    """
    enabled child of conjugate_heat_transfer.
    """
    set: set = set
    """
    set child of conjugate_heat_transfer.
    """
