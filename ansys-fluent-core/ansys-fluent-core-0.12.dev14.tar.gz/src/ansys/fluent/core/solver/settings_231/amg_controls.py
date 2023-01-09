#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .scalar_parameters import scalar_parameters
from .coupled_parameters import coupled_parameters
from .flexible_cycle_parameters import flexible_cycle_parameters
from .options_2 import options
class amg_controls(Group):
    """
    'amg_controls' child.
    """

    fluent_name = "amg-controls"

    child_names = \
        ['scalar_parameters', 'coupled_parameters',
         'flexible_cycle_parameters', 'options']

    scalar_parameters: scalar_parameters = scalar_parameters
    """
    scalar_parameters child of amg_controls.
    """
    coupled_parameters: coupled_parameters = coupled_parameters
    """
    coupled_parameters child of amg_controls.
    """
    flexible_cycle_parameters: flexible_cycle_parameters = flexible_cycle_parameters
    """
    flexible_cycle_parameters child of amg_controls.
    """
    options: options = options
    """
    options child of amg_controls.
    """
