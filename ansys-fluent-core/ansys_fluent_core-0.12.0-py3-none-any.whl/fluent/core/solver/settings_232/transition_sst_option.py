#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_roughness_correlation import enable_roughness_correlation
from .roughness_correlation_fcn import roughness_correlation_fcn
from .geometric_roughness_ht_val import geometric_roughness_ht_val
class transition_sst_option(Group):
    """
    'transition_sst_option' child.
    """

    fluent_name = "transition-sst-option"

    child_names = \
        ['enable_roughness_correlation', 'roughness_correlation_fcn',
         'geometric_roughness_ht_val']

    enable_roughness_correlation: enable_roughness_correlation = enable_roughness_correlation
    """
    enable_roughness_correlation child of transition_sst_option.
    """
    roughness_correlation_fcn: roughness_correlation_fcn = roughness_correlation_fcn
    """
    roughness_correlation_fcn child of transition_sst_option.
    """
    geometric_roughness_ht_val: geometric_roughness_ht_val = geometric_roughness_ht_val
    """
    geometric_roughness_ht_val child of transition_sst_option.
    """
