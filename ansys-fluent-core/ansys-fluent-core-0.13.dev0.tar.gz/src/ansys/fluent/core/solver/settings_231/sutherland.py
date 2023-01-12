#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .c1 import c1
from .c2 import c2
from .reference_viscosity import reference_viscosity
from .reference_temperature import reference_temperature
from .effective_temperature import effective_temperature
class sutherland(Group):
    """
    'sutherland' child.
    """

    fluent_name = "sutherland"

    child_names = \
        ['option', 'c1', 'c2', 'reference_viscosity', 'reference_temperature',
         'effective_temperature']

    option: option = option
    """
    option child of sutherland.
    """
    c1: c1 = c1
    """
    c1 child of sutherland.
    """
    c2: c2 = c2
    """
    c2 child of sutherland.
    """
    reference_viscosity: reference_viscosity = reference_viscosity
    """
    reference_viscosity child of sutherland.
    """
    reference_temperature: reference_temperature = reference_temperature
    """
    reference_temperature child of sutherland.
    """
    effective_temperature: effective_temperature = effective_temperature
    """
    effective_temperature child of sutherland.
    """
