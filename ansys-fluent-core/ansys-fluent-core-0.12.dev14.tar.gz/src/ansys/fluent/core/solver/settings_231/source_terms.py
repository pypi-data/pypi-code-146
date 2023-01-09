#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .linearization import linearization
from .implicit_momentum_coupling import implicit_momentum_coupling
from .implicit_source_term_coupling import implicit_source_term_coupling
from .linear_growth_of_dpm_source_terms import linear_growth_of_dpm_source_terms
from .reset_sources_at_timestep import reset_sources_at_timestep
class source_terms(Group):
    """
    'source_terms' child.
    """

    fluent_name = "source-terms"

    child_names = \
        ['linearization', 'implicit_momentum_coupling',
         'implicit_source_term_coupling', 'linear_growth_of_dpm_source_terms',
         'reset_sources_at_timestep']

    linearization: linearization = linearization
    """
    linearization child of source_terms.
    """
    implicit_momentum_coupling: implicit_momentum_coupling = implicit_momentum_coupling
    """
    implicit_momentum_coupling child of source_terms.
    """
    implicit_source_term_coupling: implicit_source_term_coupling = implicit_source_term_coupling
    """
    implicit_source_term_coupling child of source_terms.
    """
    linear_growth_of_dpm_source_terms: linear_growth_of_dpm_source_terms = linear_growth_of_dpm_source_terms
    """
    linear_growth_of_dpm_source_terms child of source_terms.
    """
    reset_sources_at_timestep: reset_sources_at_timestep = reset_sources_at_timestep
    """
    reset_sources_at_timestep child of source_terms.
    """
