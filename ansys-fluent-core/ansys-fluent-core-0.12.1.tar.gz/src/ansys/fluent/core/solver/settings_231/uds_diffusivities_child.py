#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .expression import expression
from .polynomial import polynomial
from .user_defined_function import user_defined_function
from .anisotropic import anisotropic
from .orthotropic import orthotropic
from .cyl_orthotropic import cyl_orthotropic
class uds_diffusivities_child(Group):
    """
    'child_object_type' of uds_diffusivities.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'value', 'expression', 'polynomial',
         'user_defined_function', 'anisotropic', 'orthotropic',
         'cyl_orthotropic']

    option: option = option
    """
    option child of uds_diffusivities_child.
    """
    value: value = value
    """
    value child of uds_diffusivities_child.
    """
    expression: expression = expression
    """
    expression child of uds_diffusivities_child.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of uds_diffusivities_child.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of uds_diffusivities_child.
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of uds_diffusivities_child.
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of uds_diffusivities_child.
    """
    cyl_orthotropic: cyl_orthotropic = cyl_orthotropic
    """
    cyl_orthotropic child of uds_diffusivities_child.
    """
