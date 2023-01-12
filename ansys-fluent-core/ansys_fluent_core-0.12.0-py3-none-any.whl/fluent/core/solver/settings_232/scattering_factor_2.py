#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
class scattering_factor(Group):
    """
    'scattering_factor' child.
    """

    fluent_name = "scattering-factor"

    child_names = \
        ['option']

    option: option = option
    """
    option child of scattering_factor.
    """
