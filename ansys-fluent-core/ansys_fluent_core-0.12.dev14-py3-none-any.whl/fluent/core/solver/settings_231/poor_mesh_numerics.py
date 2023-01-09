#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .set_1 import set
from .list_properties_2 import list_properties
class poor_mesh_numerics(Group):
    """
    'poor_mesh_numerics' child.
    """

    fluent_name = "poor-mesh-numerics"

    child_names = \
        ['set']

    set: set = set
    """
    set child of poor_mesh_numerics.
    """
    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of poor_mesh_numerics.
    """
