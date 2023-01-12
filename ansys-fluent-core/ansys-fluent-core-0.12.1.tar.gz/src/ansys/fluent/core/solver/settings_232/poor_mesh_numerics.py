#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .user_defined_on_register_auto import user_defined_on_register_auto
class poor_mesh_numerics(Group):
    """
    'poor_mesh_numerics' child.
    """

    fluent_name = "poor-mesh-numerics"

    child_names = \
        ['user_defined_on_register_auto']

    user_defined_on_register_auto: user_defined_on_register_auto = user_defined_on_register_auto
    """
    user_defined_on_register_auto child of poor_mesh_numerics.
    """
