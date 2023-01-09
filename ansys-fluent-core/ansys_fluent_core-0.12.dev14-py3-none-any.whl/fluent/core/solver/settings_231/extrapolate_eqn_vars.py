#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .equations_child import equations_child

class extrapolate_eqn_vars(NamedObject[equations_child], _NonCreatableNamedObjectMixin[equations_child]):
    """
    Enter the extrapolation menu.
    """

    fluent_name = "extrapolate-eqn-vars"

    child_object_type: equations_child = equations_child
    """
    child_object_type of extrapolate_eqn_vars.
    """
