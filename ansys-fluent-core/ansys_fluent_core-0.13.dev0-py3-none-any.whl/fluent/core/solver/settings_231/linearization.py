#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .keep_linearized_source_terms_constant import keep_linearized_source_terms_constant
from .linearize_source_terms import linearize_source_terms
from .linearized_source_terms_limiter import linearized_source_terms_limiter
class linearization(Group):
    """
    Menu containing options to enable/disable linearization of DPM source terms. 
    Please note that source term linearization is only available if the node-based averaging option is not active.
    """

    fluent_name = "linearization"

    child_names = \
        ['keep_linearized_source_terms_constant', 'linearize_source_terms',
         'linearized_source_terms_limiter']

    keep_linearized_source_terms_constant: keep_linearized_source_terms_constant = keep_linearized_source_terms_constant
    """
    keep_linearized_source_terms_constant child of linearization.
    """
    linearize_source_terms: linearize_source_terms = linearize_source_terms
    """
    linearize_source_terms child of linearization.
    """
    linearized_source_terms_limiter: linearized_source_terms_limiter = linearized_source_terms_limiter
    """
    linearized_source_terms_limiter child of linearization.
    """
