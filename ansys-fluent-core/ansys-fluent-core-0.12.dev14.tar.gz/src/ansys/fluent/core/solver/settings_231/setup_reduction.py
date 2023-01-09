#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .use_weighting import use_weighting
from .make_steady_from_unsteady_file import make_steady_from_unsteady_file
from .weighting_variable import weighting_variable
from .reset_min_and_max import reset_min_and_max
from .set_minimum import set_minimum
from .set_maximum import set_maximum
from .use_logarithmic import use_logarithmic
from .number_of_bins import number_of_bins
from .all_variables_number_of_bins import all_variables_number_of_bins
from .list_settings import list_settings
class setup_reduction(Group):
    """
    Set up the sample data reduction by specifying all relevant options and setting parameters as desired.
    """

    fluent_name = "setup-reduction"

    child_names = \
        ['use_weighting', 'make_steady_from_unsteady_file']

    use_weighting: use_weighting = use_weighting
    """
    use_weighting child of setup_reduction.
    """
    make_steady_from_unsteady_file: make_steady_from_unsteady_file = make_steady_from_unsteady_file
    """
    make_steady_from_unsteady_file child of setup_reduction.
    """
    command_names = \
        ['weighting_variable', 'reset_min_and_max', 'set_minimum',
         'set_maximum', 'use_logarithmic', 'number_of_bins',
         'all_variables_number_of_bins', 'list_settings']

    weighting_variable: weighting_variable = weighting_variable
    """
    weighting_variable command of setup_reduction.
    """
    reset_min_and_max: reset_min_and_max = reset_min_and_max
    """
    reset_min_and_max command of setup_reduction.
    """
    set_minimum: set_minimum = set_minimum
    """
    set_minimum command of setup_reduction.
    """
    set_maximum: set_maximum = set_maximum
    """
    set_maximum command of setup_reduction.
    """
    use_logarithmic: use_logarithmic = use_logarithmic
    """
    use_logarithmic command of setup_reduction.
    """
    number_of_bins: number_of_bins = number_of_bins
    """
    number_of_bins command of setup_reduction.
    """
    all_variables_number_of_bins: all_variables_number_of_bins = all_variables_number_of_bins
    """
    all_variables_number_of_bins command of setup_reduction.
    """
    list_settings: list_settings = list_settings
    """
    list_settings command of setup_reduction.
    """
