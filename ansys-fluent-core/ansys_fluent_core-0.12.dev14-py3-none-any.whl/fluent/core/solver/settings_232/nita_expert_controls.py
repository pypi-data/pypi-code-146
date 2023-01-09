#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .set_verbosity import set_verbosity
from .skewness_neighbor_coupling_1 import skewness_neighbor_coupling
from .hybrid_nita_settings import hybrid_nita_settings
class nita_expert_controls(Group):
    """
    Enter the nita expert controls menu.
    """

    fluent_name = "nita-expert-controls"

    child_names = \
        ['set_verbosity', 'skewness_neighbor_coupling',
         'hybrid_nita_settings']

    set_verbosity: set_verbosity = set_verbosity
    """
    set_verbosity child of nita_expert_controls.
    """
    skewness_neighbor_coupling: skewness_neighbor_coupling = skewness_neighbor_coupling
    """
    skewness_neighbor_coupling child of nita_expert_controls.
    """
    hybrid_nita_settings: hybrid_nita_settings = hybrid_nita_settings
    """
    hybrid_nita_settings child of nita_expert_controls.
    """
