#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .delta_eddington import delta_eddington
from .user_defined_function import user_defined_function
class scattering_phase_function(Group):
    """
    'scattering_phase_function' child.
    """

    fluent_name = "scattering-phase-function"

    child_names = \
        ['option', 'value', 'delta_eddington', 'user_defined_function']

    option: option = option
    """
    option child of scattering_phase_function.
    """
    value: value = value
    """
    value child of scattering_phase_function.
    """
    delta_eddington: delta_eddington = delta_eddington
    """
    delta_eddington child of scattering_phase_function.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of scattering_phase_function.
    """
