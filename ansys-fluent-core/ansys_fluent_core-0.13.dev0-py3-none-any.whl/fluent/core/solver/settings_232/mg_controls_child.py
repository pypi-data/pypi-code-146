#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .cycle_type import cycle_type
from .termination_criteria import termination_criteria
from .residual_reduction_tolerance import residual_reduction_tolerance
from .method_1 import method
from .stabilization import stabilization
class mg_controls_child(Group):
    """
    'child_object_type' of mg_controls.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['cycle_type', 'termination_criteria', 'residual_reduction_tolerance',
         'method', 'stabilization']

    cycle_type: cycle_type = cycle_type
    """
    cycle_type child of mg_controls_child.
    """
    termination_criteria: termination_criteria = termination_criteria
    """
    termination_criteria child of mg_controls_child.
    """
    residual_reduction_tolerance: residual_reduction_tolerance = residual_reduction_tolerance
    """
    residual_reduction_tolerance child of mg_controls_child.
    """
    method: method = method
    """
    method child of mg_controls_child.
    """
    stabilization: stabilization = stabilization
    """
    stabilization child of mg_controls_child.
    """
