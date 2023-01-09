#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_prod_limiter import enable_prod_limiter
from .clip_factor import clip_factor
class production_limiter(Group):
    """
    'production_limiter' child.
    """

    fluent_name = "production-limiter"

    child_names = \
        ['enable_prod_limiter', 'clip_factor']

    enable_prod_limiter: enable_prod_limiter = enable_prod_limiter
    """
    enable_prod_limiter child of production_limiter.
    """
    clip_factor: clip_factor = clip_factor
    """
    clip_factor child of production_limiter.
    """
