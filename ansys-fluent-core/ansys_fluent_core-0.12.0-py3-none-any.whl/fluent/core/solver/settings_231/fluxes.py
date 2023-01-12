#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .mass_flow_1 import mass_flow
from .heat_transfer_1 import heat_transfer
from .heat_transfer_sensible import heat_transfer_sensible
from .rad_heat_trans import rad_heat_trans
from .film_mass_flow import film_mass_flow
from .film_heat_transfer import film_heat_transfer
from .pressure_work_1 import pressure_work
from .viscous_work import viscous_work
class fluxes(Group):
    """
    'fluxes' child.
    """

    fluent_name = "fluxes"

    command_names = \
        ['mass_flow', 'heat_transfer', 'heat_transfer_sensible',
         'rad_heat_trans', 'film_mass_flow', 'film_heat_transfer',
         'pressure_work', 'viscous_work']

    mass_flow: mass_flow = mass_flow
    """
    mass_flow command of fluxes.
    """
    heat_transfer: heat_transfer = heat_transfer
    """
    heat_transfer command of fluxes.
    """
    heat_transfer_sensible: heat_transfer_sensible = heat_transfer_sensible
    """
    heat_transfer_sensible command of fluxes.
    """
    rad_heat_trans: rad_heat_trans = rad_heat_trans
    """
    rad_heat_trans command of fluxes.
    """
    film_mass_flow: film_mass_flow = film_mass_flow
    """
    film_mass_flow command of fluxes.
    """
    film_heat_transfer: film_heat_transfer = film_heat_transfer
    """
    film_heat_transfer command of fluxes.
    """
    pressure_work: pressure_work = pressure_work
    """
    pressure_work command of fluxes.
    """
    viscous_work: viscous_work = viscous_work
    """
    viscous_work command of fluxes.
    """
