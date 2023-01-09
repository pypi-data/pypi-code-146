#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .poisson_ratio_01 import poisson_ratio_01
from .poisson_ratio_12 import poisson_ratio_12
from .poisson_ratio_02 import poisson_ratio_02
class orthotropic_structure_nu(Group):
    """
    'orthotropic_structure_nu' child.
    """

    fluent_name = "orthotropic-structure-nu"

    child_names = \
        ['poisson_ratio_01', 'poisson_ratio_12', 'poisson_ratio_02']

    poisson_ratio_01: poisson_ratio_01 = poisson_ratio_01
    """
    poisson_ratio_01 child of orthotropic_structure_nu.
    """
    poisson_ratio_12: poisson_ratio_12 = poisson_ratio_12
    """
    poisson_ratio_12 child of orthotropic_structure_nu.
    """
    poisson_ratio_02: poisson_ratio_02 = poisson_ratio_02
    """
    poisson_ratio_02 child of orthotropic_structure_nu.
    """
