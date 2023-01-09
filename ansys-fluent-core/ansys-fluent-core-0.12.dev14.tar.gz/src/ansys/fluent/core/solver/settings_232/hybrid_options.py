#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .dpm_domain import dpm_domain
from .ordered_accumulation import ordered_accumulation
class hybrid_options(Group):
    """
    'hybrid_options' child.
    """

    fluent_name = "hybrid-options"

    child_names = \
        ['dpm_domain', 'ordered_accumulation']

    dpm_domain: dpm_domain = dpm_domain
    """
    dpm_domain child of hybrid_options.
    """
    ordered_accumulation: ordered_accumulation = ordered_accumulation
    """
    ordered_accumulation child of hybrid_options.
    """
