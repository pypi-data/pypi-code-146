#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .anisotropic_boundary_zones import anisotropic_boundary_zones
from .cell_zones import cell_zones
from .dynamic_adaption_frequency import dynamic_adaption_frequency
from .verbosity import verbosity
from .encapsulate_children import encapsulate_children
from .maximum_refinement_level import maximum_refinement_level
from .minimum_cell_quality import minimum_cell_quality
from .maximum_cell_count import maximum_cell_count
from .additional_refinement_layers import additional_refinement_layers
from .anisotropic_adaption import anisotropic_adaption
from .minimum_edge_length import minimum_edge_length
from .anisotropic_split_ratio import anisotropic_split_ratio
from .overset_adapt_dead_cells import overset_adapt_dead_cells
from .dynamic_adaption import dynamic_adaption
class set(Group):
    """
    Enter the adaption set menu.
    """

    fluent_name = "set"

    child_names = \
        ['anisotropic_boundary_zones', 'cell_zones',
         'dynamic_adaption_frequency', 'verbosity', 'encapsulate_children',
         'maximum_refinement_level', 'minimum_cell_quality',
         'maximum_cell_count', 'additional_refinement_layers',
         'anisotropic_adaption', 'minimum_edge_length',
         'anisotropic_split_ratio', 'overset_adapt_dead_cells']

    anisotropic_boundary_zones: anisotropic_boundary_zones = anisotropic_boundary_zones
    """
    anisotropic_boundary_zones child of set.
    """
    cell_zones: cell_zones = cell_zones
    """
    cell_zones child of set.
    """
    dynamic_adaption_frequency: dynamic_adaption_frequency = dynamic_adaption_frequency
    """
    dynamic_adaption_frequency child of set.
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of set.
    """
    encapsulate_children: encapsulate_children = encapsulate_children
    """
    encapsulate_children child of set.
    """
    maximum_refinement_level: maximum_refinement_level = maximum_refinement_level
    """
    maximum_refinement_level child of set.
    """
    minimum_cell_quality: minimum_cell_quality = minimum_cell_quality
    """
    minimum_cell_quality child of set.
    """
    maximum_cell_count: maximum_cell_count = maximum_cell_count
    """
    maximum_cell_count child of set.
    """
    additional_refinement_layers: additional_refinement_layers = additional_refinement_layers
    """
    additional_refinement_layers child of set.
    """
    anisotropic_adaption: anisotropic_adaption = anisotropic_adaption
    """
    anisotropic_adaption child of set.
    """
    minimum_edge_length: minimum_edge_length = minimum_edge_length
    """
    minimum_edge_length child of set.
    """
    anisotropic_split_ratio: anisotropic_split_ratio = anisotropic_split_ratio
    """
    anisotropic_split_ratio child of set.
    """
    overset_adapt_dead_cells: overset_adapt_dead_cells = overset_adapt_dead_cells
    """
    overset_adapt_dead_cells child of set.
    """
    command_names = \
        ['dynamic_adaption']

    dynamic_adaption: dynamic_adaption = dynamic_adaption
    """
    dynamic_adaption command of set.
    """
