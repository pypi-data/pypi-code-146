#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .shape_factor import shape_factor
from .cunningham_factor import cunningham_factor
class particle_drag(Group):
    """
    'particle_drag' child.
    """

    fluent_name = "particle-drag"

    child_names = \
        ['option', 'shape_factor', 'cunningham_factor']

    option: option = option
    """
    option child of particle_drag.
    """
    shape_factor: shape_factor = shape_factor
    """
    shape_factor child of particle_drag.
    """
    cunningham_factor: cunningham_factor = cunningham_factor
    """
    cunningham_factor child of particle_drag.
    """
