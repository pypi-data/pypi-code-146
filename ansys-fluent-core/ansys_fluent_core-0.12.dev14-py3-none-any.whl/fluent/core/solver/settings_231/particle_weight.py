#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .use import use
from .user_defined_2 import user_defined
from .value import value
from .hybrid_optimization import hybrid_optimization
class particle_weight(Group):
    """
    Set DPM particle weight.
    """

    fluent_name = "particle-weight"

    child_names = \
        ['use', 'user_defined', 'value', 'hybrid_optimization']

    use: use = use
    """
    use child of particle_weight.
    """
    user_defined: user_defined = user_defined
    """
    user_defined child of particle_weight.
    """
    value: value = value
    """
    value child of particle_weight.
    """
    hybrid_optimization: hybrid_optimization = hybrid_optimization
    """
    hybrid_optimization child of particle_weight.
    """
