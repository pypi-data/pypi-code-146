#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .local_dt_child import local_dt_child

class global_dt(NamedObject[local_dt_child], _NonCreatableNamedObjectMixin[local_dt_child]):
    """
    'global_dt' child.
    """

    fluent_name = "global-dt"

    child_object_type: local_dt_child = local_dt_child
    """
    child_object_type of global_dt.
    """
