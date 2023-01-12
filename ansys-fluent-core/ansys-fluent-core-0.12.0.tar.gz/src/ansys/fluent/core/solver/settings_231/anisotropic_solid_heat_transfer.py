#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .flux import flux
from .gradient import gradient
class anisotropic_solid_heat_transfer(Group):
    """
    'anisotropic_solid_heat_transfer' child.
    """

    fluent_name = "anisotropic-solid-heat-transfer"

    child_names = \
        ['flux', 'gradient']

    flux: flux = flux
    """
    flux child of anisotropic_solid_heat_transfer.
    """
    gradient: gradient = gradient
    """
    gradient child of anisotropic_solid_heat_transfer.
    """
