#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .forward_scattering_factor import forward_scattering_factor
from .asymmetry_factor import asymmetry_factor
class delta_eddington(Group):
    """
    'delta_eddington' child.
    """

    fluent_name = "delta-eddington"

    child_names = \
        ['forward_scattering_factor', 'asymmetry_factor']

    forward_scattering_factor: forward_scattering_factor = forward_scattering_factor
    """
    forward_scattering_factor child of delta_eddington.
    """
    asymmetry_factor: asymmetry_factor = asymmetry_factor
    """
    asymmetry_factor child of delta_eddington.
    """
