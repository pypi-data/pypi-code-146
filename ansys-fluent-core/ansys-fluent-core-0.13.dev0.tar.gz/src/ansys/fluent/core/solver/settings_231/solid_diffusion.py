#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class solid_diffusion(Group):
    """
    'solid_diffusion' child.
    """

    fluent_name = "solid-diffusion"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of solid_diffusion.
    """
    value: value = value
    """
    value child of solid_diffusion.
    """
