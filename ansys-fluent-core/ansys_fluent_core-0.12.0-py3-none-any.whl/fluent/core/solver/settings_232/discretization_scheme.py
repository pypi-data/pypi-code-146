#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .turb_visc_func_mf_child import turb_visc_func_mf_child

class discretization_scheme(NamedObject[turb_visc_func_mf_child], _NonCreatableNamedObjectMixin[turb_visc_func_mf_child]):
    """
    'discretization_scheme' child.
    """

    fluent_name = "discretization-scheme"

    child_object_type: turb_visc_func_mf_child = turb_visc_func_mf_child
    """
    child_object_type of discretization_scheme.
    """
