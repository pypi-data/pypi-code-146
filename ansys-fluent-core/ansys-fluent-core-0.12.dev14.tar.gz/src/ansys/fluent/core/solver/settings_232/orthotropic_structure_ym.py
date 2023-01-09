#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .direction_0 import direction_0
from .direction_1 import direction_1
from .youngs_modulus_0 import youngs_modulus_0
from .youngs_modulus_1 import youngs_modulus_1
from .youngs_modulus_2 import youngs_modulus_2
from .shear_modulus_01 import shear_modulus_01
from .shear_modulus_12 import shear_modulus_12
from .shear_modulus_02 import shear_modulus_02
class orthotropic_structure_ym(Group):
    """
    'orthotropic_structure_ym' child.
    """

    fluent_name = "orthotropic-structure-ym"

    child_names = \
        ['direction_0', 'direction_1', 'youngs_modulus_0', 'youngs_modulus_1',
         'youngs_modulus_2', 'shear_modulus_01', 'shear_modulus_12',
         'shear_modulus_02']

    direction_0: direction_0 = direction_0
    """
    direction_0 child of orthotropic_structure_ym.
    """
    direction_1: direction_1 = direction_1
    """
    direction_1 child of orthotropic_structure_ym.
    """
    youngs_modulus_0: youngs_modulus_0 = youngs_modulus_0
    """
    youngs_modulus_0 child of orthotropic_structure_ym.
    """
    youngs_modulus_1: youngs_modulus_1 = youngs_modulus_1
    """
    youngs_modulus_1 child of orthotropic_structure_ym.
    """
    youngs_modulus_2: youngs_modulus_2 = youngs_modulus_2
    """
    youngs_modulus_2 child of orthotropic_structure_ym.
    """
    shear_modulus_01: shear_modulus_01 = shear_modulus_01
    """
    shear_modulus_01 child of orthotropic_structure_ym.
    """
    shear_modulus_12: shear_modulus_12 = shear_modulus_12
    """
    shear_modulus_12 child of orthotropic_structure_ym.
    """
    shear_modulus_02: shear_modulus_02 = shear_modulus_02
    """
    shear_modulus_02 child of orthotropic_structure_ym.
    """
