#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .real_gas_nist_mixture import real_gas_nist_mixture
from .user_defined_function import user_defined_function
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'real_gas_nist_mixture', 'user_defined_function']

    option: option = option
    """
    option child of density.
    """
    real_gas_nist_mixture: real_gas_nist_mixture = real_gas_nist_mixture
    """
    real_gas_nist_mixture child of density.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of density.
    """
