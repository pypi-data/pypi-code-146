#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .n_theta_divisions import n_theta_divisions
from .n_phi_divisions import n_phi_divisions
from .n_theta_pixels import n_theta_pixels
from .n_phi_pixels import n_phi_pixels
class discrete_ordinates(Group):
    """
    Enable/disable the discrete ordinates radiation model.
    """

    fluent_name = "discrete-ordinates"

    child_names = \
        ['n_theta_divisions', 'n_phi_divisions', 'n_theta_pixels',
         'n_phi_pixels']

    n_theta_divisions: n_theta_divisions = n_theta_divisions
    """
    n_theta_divisions child of discrete_ordinates.
    """
    n_phi_divisions: n_phi_divisions = n_phi_divisions
    """
    n_phi_divisions child of discrete_ordinates.
    """
    n_theta_pixels: n_theta_pixels = n_theta_pixels
    """
    n_theta_pixels child of discrete_ordinates.
    """
    n_phi_pixels: n_phi_pixels = n_phi_pixels
    """
    n_phi_pixels child of discrete_ordinates.
    """
