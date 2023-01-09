#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .constant_y0 import constant_y0
from .number_of_child_droplets import number_of_child_droplets
from .constant_b1 import constant_b1
from .constant_b0 import constant_b0
from .constant_cl import constant_cl
from .constant_ctau import constant_ctau
from .constant_crt import constant_crt
from .critical_weber_number import critical_weber_number
from .core_b1 import core_b1
from .constant_xi import constant_xi
from .target_number_in_parcel import target_number_in_parcel
from .constant_c0 import constant_c0
from .column_drag_coeff import column_drag_coeff
from .ligament_factor import ligament_factor
from .jet_diameter import jet_diameter
from .constant_k1 import constant_k1
from .constant_k2 import constant_k2
from .constant_tb import constant_tb
class droplet_breakup(Group):
    """
    'droplet_breakup' child.
    """

    fluent_name = "droplet-breakup"

    child_names = \
        ['option', 'constant_y0', 'number_of_child_droplets', 'constant_b1',
         'constant_b0', 'constant_cl', 'constant_ctau', 'constant_crt',
         'critical_weber_number', 'core_b1', 'constant_xi',
         'target_number_in_parcel', 'constant_c0', 'column_drag_coeff',
         'ligament_factor', 'jet_diameter', 'constant_k1', 'constant_k2',
         'constant_tb']

    option: option = option
    """
    option child of droplet_breakup.
    """
    constant_y0: constant_y0 = constant_y0
    """
    constant_y0 child of droplet_breakup.
    """
    number_of_child_droplets: number_of_child_droplets = number_of_child_droplets
    """
    number_of_child_droplets child of droplet_breakup.
    """
    constant_b1: constant_b1 = constant_b1
    """
    constant_b1 child of droplet_breakup.
    """
    constant_b0: constant_b0 = constant_b0
    """
    constant_b0 child of droplet_breakup.
    """
    constant_cl: constant_cl = constant_cl
    """
    constant_cl child of droplet_breakup.
    """
    constant_ctau: constant_ctau = constant_ctau
    """
    constant_ctau child of droplet_breakup.
    """
    constant_crt: constant_crt = constant_crt
    """
    constant_crt child of droplet_breakup.
    """
    critical_weber_number: critical_weber_number = critical_weber_number
    """
    critical_weber_number child of droplet_breakup.
    """
    core_b1: core_b1 = core_b1
    """
    core_b1 child of droplet_breakup.
    """
    constant_xi: constant_xi = constant_xi
    """
    constant_xi child of droplet_breakup.
    """
    target_number_in_parcel: target_number_in_parcel = target_number_in_parcel
    """
    target_number_in_parcel child of droplet_breakup.
    """
    constant_c0: constant_c0 = constant_c0
    """
    constant_c0 child of droplet_breakup.
    """
    column_drag_coeff: column_drag_coeff = column_drag_coeff
    """
    column_drag_coeff child of droplet_breakup.
    """
    ligament_factor: ligament_factor = ligament_factor
    """
    ligament_factor child of droplet_breakup.
    """
    jet_diameter: jet_diameter = jet_diameter
    """
    jet_diameter child of droplet_breakup.
    """
    constant_k1: constant_k1 = constant_k1
    """
    constant_k1 child of droplet_breakup.
    """
    constant_k2: constant_k2 = constant_k2
    """
    constant_k2 child of droplet_breakup.
    """
    constant_tb: constant_tb = constant_tb
    """
    constant_tb child of droplet_breakup.
    """
