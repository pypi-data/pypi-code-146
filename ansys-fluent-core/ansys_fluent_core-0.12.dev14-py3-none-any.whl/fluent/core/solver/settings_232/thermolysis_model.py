#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .single_rate import single_rate
from .secondary_rate import secondary_rate
from .value import value
class thermolysis_model(Group):
    """
    'thermolysis_model' child.
    """

    fluent_name = "thermolysis-model"

    child_names = \
        ['option', 'single_rate', 'secondary_rate', 'value']

    option: option = option
    """
    option child of thermolysis_model.
    """
    single_rate: single_rate = single_rate
    """
    single_rate child of thermolysis_model.
    """
    secondary_rate: secondary_rate = secondary_rate
    """
    secondary_rate child of thermolysis_model.
    """
    value: value = value
    """
    value child of thermolysis_model.
    """
