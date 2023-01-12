#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .random_eddy_lifetime import random_eddy_lifetime
from .number_of_tries import number_of_tries
from .time_scale_constant import time_scale_constant
class turbulent_dispersion(Group):
    """
    'turbulent_dispersion' child.
    """

    fluent_name = "turbulent-dispersion"

    child_names = \
        ['option', 'random_eddy_lifetime', 'number_of_tries',
         'time_scale_constant']

    option: option = option
    """
    option child of turbulent_dispersion.
    """
    random_eddy_lifetime: random_eddy_lifetime = random_eddy_lifetime
    """
    random_eddy_lifetime child of turbulent_dispersion.
    """
    number_of_tries: number_of_tries = number_of_tries
    """
    number_of_tries child of turbulent_dispersion.
    """
    time_scale_constant: time_scale_constant = time_scale_constant
    """
    time_scale_constant child of turbulent_dispersion.
    """
