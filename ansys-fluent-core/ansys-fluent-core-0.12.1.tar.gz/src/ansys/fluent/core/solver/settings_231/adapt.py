#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .refinement_criteria import refinement_criteria
from .coarsening_criteria import coarsening_criteria
from .manual_refinement_criteria import manual_refinement_criteria
from .manual_coarsening_criteria import manual_coarsening_criteria
from .set import set
from .profile import profile
from .free_hierarchy import free_hierarchy
from .multi_layer_refinement import multi_layer_refinement
from .geometry import geometry
from .adapt_mesh import adapt_mesh
from .display_adaption_cells import display_adaption_cells
from .list_adaption_cells import list_adaption_cells
class adapt(Group):
    """
    'adapt' child.
    """

    fluent_name = "adapt"

    child_names = \
        ['refinement_criteria', 'coarsening_criteria',
         'manual_refinement_criteria', 'manual_coarsening_criteria', 'set',
         'profile', 'free_hierarchy', 'multi_layer_refinement', 'geometry']

    refinement_criteria: refinement_criteria = refinement_criteria
    """
    refinement_criteria child of adapt.
    """
    coarsening_criteria: coarsening_criteria = coarsening_criteria
    """
    coarsening_criteria child of adapt.
    """
    manual_refinement_criteria: manual_refinement_criteria = manual_refinement_criteria
    """
    manual_refinement_criteria child of adapt.
    """
    manual_coarsening_criteria: manual_coarsening_criteria = manual_coarsening_criteria
    """
    manual_coarsening_criteria child of adapt.
    """
    set: set = set
    """
    set child of adapt.
    """
    profile: profile = profile
    """
    profile child of adapt.
    """
    free_hierarchy: free_hierarchy = free_hierarchy
    """
    free_hierarchy child of adapt.
    """
    multi_layer_refinement: multi_layer_refinement = multi_layer_refinement
    """
    multi_layer_refinement child of adapt.
    """
    geometry: geometry = geometry
    """
    geometry child of adapt.
    """
    command_names = \
        ['adapt_mesh', 'display_adaption_cells', 'list_adaption_cells']

    adapt_mesh: adapt_mesh = adapt_mesh
    """
    adapt_mesh command of adapt.
    """
    display_adaption_cells: display_adaption_cells = display_adaption_cells
    """
    display_adaption_cells command of adapt.
    """
    list_adaption_cells: list_adaption_cells = list_adaption_cells
    """
    list_adaption_cells command of adapt.
    """
