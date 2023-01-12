#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .uds_bc_child import uds_bc_child

class uds_bc(NamedObject[uds_bc_child], _CreatableNamedObjectMixin[uds_bc_child]):
    """
    'uds_bc' child.
    """

    fluent_name = "uds-bc"

    child_object_type: uds_bc_child = uds_bc_child
    """
    child_object_type of uds_bc.
    """
