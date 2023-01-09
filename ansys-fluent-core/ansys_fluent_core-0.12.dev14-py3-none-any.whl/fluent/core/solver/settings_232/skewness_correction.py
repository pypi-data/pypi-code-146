#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .limit_pressure_correction_gradient import limit_pressure_correction_gradient
class skewness_correction(Group):
    """
    Skewness correction related stabiity controls for multiphase flow.
    """

    fluent_name = "skewness-correction"

    child_names = \
        ['limit_pressure_correction_gradient']

    limit_pressure_correction_gradient: limit_pressure_correction_gradient = limit_pressure_correction_gradient
    """
    limit_pressure_correction_gradient child of skewness_correction.
    """
