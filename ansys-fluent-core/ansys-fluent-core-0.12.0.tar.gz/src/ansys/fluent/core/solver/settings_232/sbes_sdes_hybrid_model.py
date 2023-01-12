#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .sbes_sdes_hybrid_model_optn import sbes_sdes_hybrid_model_optn
from .user_defined_fcn_for_sbes import user_defined_fcn_for_sbes
class sbes_sdes_hybrid_model(Group):
    """
    'sbes_sdes_hybrid_model' child.
    """

    fluent_name = "sbes-sdes-hybrid-model"

    child_names = \
        ['sbes_sdes_hybrid_model_optn', 'user_defined_fcn_for_sbes']

    sbes_sdes_hybrid_model_optn: sbes_sdes_hybrid_model_optn = sbes_sdes_hybrid_model_optn
    """
    sbes_sdes_hybrid_model_optn child of sbes_sdes_hybrid_model.
    """
    user_defined_fcn_for_sbes: user_defined_fcn_for_sbes = user_defined_fcn_for_sbes
    """
    user_defined_fcn_for_sbes child of sbes_sdes_hybrid_model.
    """
