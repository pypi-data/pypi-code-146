#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .remove_limiter import remove_limiter
from .report_leidenfrost_temperature import report_leidenfrost_temperature
from .set_offset_above_film_boiling_temperature import set_offset_above_film_boiling_temperature
class wall_film_temperature_limiter(Group):
    """
    'wall_film_temperature_limiter' child.
    """

    fluent_name = "wall-film-temperature-limiter"

    child_names = \
        ['remove_limiter', 'report_leidenfrost_temperature',
         'set_offset_above_film_boiling_temperature']

    remove_limiter: remove_limiter = remove_limiter
    """
    remove_limiter child of wall_film_temperature_limiter.
    """
    report_leidenfrost_temperature: report_leidenfrost_temperature = report_leidenfrost_temperature
    """
    report_leidenfrost_temperature child of wall_film_temperature_limiter.
    """
    set_offset_above_film_boiling_temperature: set_offset_above_film_boiling_temperature = set_offset_above_film_boiling_temperature
    """
    set_offset_above_film_boiling_temperature child of wall_film_temperature_limiter.
    """
