#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .coefficient import coefficient
from .update_dissipation import update_dissipation
from .update_viscous import update_viscous
class multi_stage_child(Group):
    """
    'child_object_type' of multi_stage.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['coefficient', 'update_dissipation', 'update_viscous']

    coefficient: coefficient = coefficient
    """
    coefficient child of multi_stage_child.
    """
    update_dissipation: update_dissipation = update_dissipation
    """
    update_dissipation child of multi_stage_child.
    """
    update_viscous: update_viscous = update_viscous
    """
    update_viscous child of multi_stage_child.
    """
