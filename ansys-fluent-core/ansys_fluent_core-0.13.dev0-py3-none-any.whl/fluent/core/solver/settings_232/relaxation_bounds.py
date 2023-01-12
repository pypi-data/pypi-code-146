#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .relaxation_bounding_method import relaxation_bounding_method
from .default_min_max_relaxation_limits import default_min_max_relaxation_limits
from .minimum_allowed_effctive_relaxation import minimum_allowed_effctive_relaxation
from .maximum_allowed_effctive_relaxation import maximum_allowed_effctive_relaxation
class relaxation_bounds(Command):
    """
    Select relaxation bounding scheme for pseudo time method.
    
    Parameters
    ----------
        relaxation_bounding_method : str
            'relaxation_bounding_method' child.
        default_min_max_relaxation_limits : bool
            'default_min_max_relaxation_limits' child.
        minimum_allowed_effctive_relaxation : real
            'minimum_allowed_effctive_relaxation' child.
        maximum_allowed_effctive_relaxation : real
            'maximum_allowed_effctive_relaxation' child.
    
    """

    fluent_name = "relaxation-bounds"

    argument_names = \
        ['relaxation_bounding_method', 'default_min_max_relaxation_limits',
         'minimum_allowed_effctive_relaxation',
         'maximum_allowed_effctive_relaxation']

    relaxation_bounding_method: relaxation_bounding_method = relaxation_bounding_method
    """
    relaxation_bounding_method argument of relaxation_bounds.
    """
    default_min_max_relaxation_limits: default_min_max_relaxation_limits = default_min_max_relaxation_limits
    """
    default_min_max_relaxation_limits argument of relaxation_bounds.
    """
    minimum_allowed_effctive_relaxation: minimum_allowed_effctive_relaxation = minimum_allowed_effctive_relaxation
    """
    minimum_allowed_effctive_relaxation argument of relaxation_bounds.
    """
    maximum_allowed_effctive_relaxation: maximum_allowed_effctive_relaxation = maximum_allowed_effctive_relaxation
    """
    maximum_allowed_effctive_relaxation argument of relaxation_bounds.
    """
