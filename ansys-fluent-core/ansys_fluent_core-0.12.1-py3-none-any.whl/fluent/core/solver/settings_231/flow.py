#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .species_mass_flow import species_mass_flow
from .element_mass_flow import element_mass_flow
from .uds_flow import uds_flow
class flow(Group):
    """
    'flow' child.
    """

    fluent_name = "flow"

    command_names = \
        ['species_mass_flow', 'element_mass_flow', 'uds_flow']

    species_mass_flow: species_mass_flow = species_mass_flow
    """
    species_mass_flow command of flow.
    """
    element_mass_flow: element_mass_flow = element_mass_flow
    """
    element_mass_flow command of flow.
    """
    uds_flow: uds_flow = uds_flow
    """
    uds_flow command of flow.
    """
