#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .initial_fraction_of_bridges_in_coal_lattice import initial_fraction_of_bridges_in_coal_lattice
from .initial_fraction_of_char_bridges import initial_fraction_of_char_bridges
from .lattice_coordination_number import lattice_coordination_number
from .cluster_molecular_weight import cluster_molecular_weight
from .side_chain_molecular_weight import side_chain_molecular_weight
class cpd_model(Group):
    """
    'cpd_model' child.
    """

    fluent_name = "cpd-model"

    child_names = \
        ['initial_fraction_of_bridges_in_coal_lattice',
         'initial_fraction_of_char_bridges', 'lattice_coordination_number',
         'cluster_molecular_weight', 'side_chain_molecular_weight']

    initial_fraction_of_bridges_in_coal_lattice: initial_fraction_of_bridges_in_coal_lattice = initial_fraction_of_bridges_in_coal_lattice
    """
    initial_fraction_of_bridges_in_coal_lattice child of cpd_model.
    """
    initial_fraction_of_char_bridges: initial_fraction_of_char_bridges = initial_fraction_of_char_bridges
    """
    initial_fraction_of_char_bridges child of cpd_model.
    """
    lattice_coordination_number: lattice_coordination_number = lattice_coordination_number
    """
    lattice_coordination_number child of cpd_model.
    """
    cluster_molecular_weight: cluster_molecular_weight = cluster_molecular_weight
    """
    cluster_molecular_weight child of cpd_model.
    """
    side_chain_molecular_weight: side_chain_molecular_weight = side_chain_molecular_weight
    """
    side_chain_molecular_weight child of cpd_model.
    """
