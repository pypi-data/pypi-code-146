#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .particle_thermolysis_rate import particle_thermolysis_rate
from .film_thermolysis_rate import film_thermolysis_rate
class secondary_rate(Group):
    """
    'secondary_rate' child.
    """

    fluent_name = "secondary-rate"

    child_names = \
        ['particle_thermolysis_rate', 'film_thermolysis_rate']

    particle_thermolysis_rate: particle_thermolysis_rate = particle_thermolysis_rate
    """
    particle_thermolysis_rate child of secondary_rate.
    """
    film_thermolysis_rate: film_thermolysis_rate = film_thermolysis_rate
    """
    film_thermolysis_rate child of secondary_rate.
    """
