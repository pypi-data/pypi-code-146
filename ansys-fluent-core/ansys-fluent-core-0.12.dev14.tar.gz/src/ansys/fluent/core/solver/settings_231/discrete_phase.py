#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_expert_view import enable_expert_view
from .general_settings import general_settings
from .injections import injections
from .numerics import numerics
from .parallel import parallel
from .physical_models_1 import physical_models
from .tracking_1 import tracking
from .user_defined_functions import user_defined_functions
class discrete_phase(Group):
    """
    Toplevel menu of the Discrete Phase multiphase model. A discrete phase model (DPM) is used when the aim is to investigate the behavior of the particles from a Lagrangian view and a discrete perspective.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['enable_expert_view', 'general_settings', 'injections', 'numerics',
         'parallel', 'physical_models', 'tracking', 'user_defined_functions']

    enable_expert_view: enable_expert_view = enable_expert_view
    """
    enable_expert_view child of discrete_phase.
    """
    general_settings: general_settings = general_settings
    """
    general_settings child of discrete_phase.
    """
    injections: injections = injections
    """
    injections child of discrete_phase.
    """
    numerics: numerics = numerics
    """
    numerics child of discrete_phase.
    """
    parallel: parallel = parallel
    """
    parallel child of discrete_phase.
    """
    physical_models: physical_models = physical_models
    """
    physical_models child of discrete_phase.
    """
    tracking: tracking = tracking
    """
    tracking child of discrete_phase.
    """
    user_defined_functions: user_defined_functions = user_defined_functions
    """
    user_defined_functions child of discrete_phase.
    """
