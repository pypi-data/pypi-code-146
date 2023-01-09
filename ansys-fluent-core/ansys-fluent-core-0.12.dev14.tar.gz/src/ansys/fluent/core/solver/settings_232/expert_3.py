#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .reactions_1 import reactions
from .reaction_source_term_relaxation_factor import reaction_source_term_relaxation_factor
from .numerics_pbns import numerics_pbns
from .numerics_dbns import numerics_dbns
class expert(Group):
    """
    Enter expert menu.
    """

    fluent_name = "expert"

    child_names = \
        ['reactions', 'reaction_source_term_relaxation_factor',
         'numerics_pbns', 'numerics_dbns']

    reactions: reactions = reactions
    """
    reactions child of expert.
    """
    reaction_source_term_relaxation_factor: reaction_source_term_relaxation_factor = reaction_source_term_relaxation_factor
    """
    reaction_source_term_relaxation_factor child of expert.
    """
    numerics_pbns: numerics_pbns = numerics_pbns
    """
    numerics_pbns child of expert.
    """
    numerics_dbns: numerics_dbns = numerics_dbns
    """
    numerics_dbns child of expert.
    """
