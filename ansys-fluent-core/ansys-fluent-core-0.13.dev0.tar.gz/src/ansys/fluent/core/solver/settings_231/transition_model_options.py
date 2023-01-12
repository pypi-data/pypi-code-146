#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .crossflow_transition import crossflow_transition
from .critical_reynolds_number_correlation import critical_reynolds_number_correlation
from .clambda_scale import clambda_scale
from .capg_hightu import capg_hightu
from .cfpg_hightu import cfpg_hightu
from .capg_lowtu import capg_lowtu
from .cfpg_lowtu import cfpg_lowtu
from .ctu_hightu import ctu_hightu
from .ctu_lowtu import ctu_lowtu
from .rec_max import rec_max
from .rec_c1 import rec_c1
from .rec_c2 import rec_c2
from .cbubble_c1 import cbubble_c1
from .cbubble_c2 import cbubble_c2
from .rv1_switch import rv1_switch
class transition_model_options(Group):
    """
    'transition_model_options' child.
    """

    fluent_name = "transition-model-options"

    child_names = \
        ['crossflow_transition', 'critical_reynolds_number_correlation',
         'clambda_scale', 'capg_hightu', 'cfpg_hightu', 'capg_lowtu',
         'cfpg_lowtu', 'ctu_hightu', 'ctu_lowtu', 'rec_max', 'rec_c1',
         'rec_c2', 'cbubble_c1', 'cbubble_c2', 'rv1_switch']

    crossflow_transition: crossflow_transition = crossflow_transition
    """
    crossflow_transition child of transition_model_options.
    """
    critical_reynolds_number_correlation: critical_reynolds_number_correlation = critical_reynolds_number_correlation
    """
    critical_reynolds_number_correlation child of transition_model_options.
    """
    clambda_scale: clambda_scale = clambda_scale
    """
    clambda_scale child of transition_model_options.
    """
    capg_hightu: capg_hightu = capg_hightu
    """
    capg_hightu child of transition_model_options.
    """
    cfpg_hightu: cfpg_hightu = cfpg_hightu
    """
    cfpg_hightu child of transition_model_options.
    """
    capg_lowtu: capg_lowtu = capg_lowtu
    """
    capg_lowtu child of transition_model_options.
    """
    cfpg_lowtu: cfpg_lowtu = cfpg_lowtu
    """
    cfpg_lowtu child of transition_model_options.
    """
    ctu_hightu: ctu_hightu = ctu_hightu
    """
    ctu_hightu child of transition_model_options.
    """
    ctu_lowtu: ctu_lowtu = ctu_lowtu
    """
    ctu_lowtu child of transition_model_options.
    """
    rec_max: rec_max = rec_max
    """
    rec_max child of transition_model_options.
    """
    rec_c1: rec_c1 = rec_c1
    """
    rec_c1 child of transition_model_options.
    """
    rec_c2: rec_c2 = rec_c2
    """
    rec_c2 child of transition_model_options.
    """
    cbubble_c1: cbubble_c1 = cbubble_c1
    """
    cbubble_c1 child of transition_model_options.
    """
    cbubble_c2: cbubble_c2 = cbubble_c2
    """
    cbubble_c2 child of transition_model_options.
    """
    rv1_switch: rv1_switch = rv1_switch
    """
    rv1_switch child of transition_model_options.
    """
