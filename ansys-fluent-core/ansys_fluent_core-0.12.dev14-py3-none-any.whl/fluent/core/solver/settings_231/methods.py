#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .pv_coupling_controls import pv_coupling_controls
from .pv_coupling_method import pv_coupling_method
from .gradient_controls import gradient_controls
from .specify_gradient_method import specify_gradient_method
class methods(Group):
    """
    'methods' child.
    """

    fluent_name = "methods"

    child_names = \
        ['pv_coupling_controls', 'pv_coupling_method', 'gradient_controls',
         'specify_gradient_method']

    pv_coupling_controls: pv_coupling_controls = pv_coupling_controls
    """
    pv_coupling_controls child of methods.
    """
    pv_coupling_method: pv_coupling_method = pv_coupling_method
    """
    pv_coupling_method child of methods.
    """
    gradient_controls: gradient_controls = gradient_controls
    """
    gradient_controls child of methods.
    """
    specify_gradient_method: specify_gradient_method = specify_gradient_method
    """
    specify_gradient_method child of methods.
    """
