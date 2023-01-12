#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .body_force_function import body_force_function
from .collision_function import collision_function
from .dpm_time_step_function import dpm_time_step_function
from .erosion_accretion_function import erosion_accretion_function
from .film_regime_function import film_regime_function
from .interpolation_function import interpolation_function
from .impingement_model_function import impingement_model_function
from .output_function import output_function
from .scalar_update_function import scalar_update_function
from .source_function import source_function
from .splashing_distribution_function import splashing_distribution_function
from .number_of_scalars import number_of_scalars
from .maximum_udf_species import maximum_udf_species
class user_defined_functions(Group):
    """
    Main menu to set DPM user-defined functions. User-defined functions can be used to customize the discrete phase model 
    to include additional body forces, modify interphase exchange terms (sources), calculate or integrate scalar values 
    along the particle trajectory, and more.
    """

    fluent_name = "user-defined-functions"

    child_names = \
        ['body_force_function', 'collision_function',
         'dpm_time_step_function', 'erosion_accretion_function',
         'film_regime_function', 'interpolation_function',
         'impingement_model_function', 'output_function',
         'scalar_update_function', 'source_function',
         'splashing_distribution_function', 'number_of_scalars',
         'maximum_udf_species']

    body_force_function: body_force_function = body_force_function
    """
    body_force_function child of user_defined_functions.
    """
    collision_function: collision_function = collision_function
    """
    collision_function child of user_defined_functions.
    """
    dpm_time_step_function: dpm_time_step_function = dpm_time_step_function
    """
    dpm_time_step_function child of user_defined_functions.
    """
    erosion_accretion_function: erosion_accretion_function = erosion_accretion_function
    """
    erosion_accretion_function child of user_defined_functions.
    """
    film_regime_function: film_regime_function = film_regime_function
    """
    film_regime_function child of user_defined_functions.
    """
    interpolation_function: interpolation_function = interpolation_function
    """
    interpolation_function child of user_defined_functions.
    """
    impingement_model_function: impingement_model_function = impingement_model_function
    """
    impingement_model_function child of user_defined_functions.
    """
    output_function: output_function = output_function
    """
    output_function child of user_defined_functions.
    """
    scalar_update_function: scalar_update_function = scalar_update_function
    """
    scalar_update_function child of user_defined_functions.
    """
    source_function: source_function = source_function
    """
    source_function child of user_defined_functions.
    """
    splashing_distribution_function: splashing_distribution_function = splashing_distribution_function
    """
    splashing_distribution_function child of user_defined_functions.
    """
    number_of_scalars: number_of_scalars = number_of_scalars
    """
    number_of_scalars child of user_defined_functions.
    """
    maximum_udf_species: maximum_udf_species = maximum_udf_species
    """
    maximum_udf_species child of user_defined_functions.
    """
