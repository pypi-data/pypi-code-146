#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .model import model
from .options_2 import options
from .controls import controls
from .expert import expert
class structure(Group):
    """
    'structure' child.
    """

    fluent_name = "structure"

    child_names = \
        ['model', 'options', 'controls', 'expert']

    model: model = model
    """
    model child of structure.
    """
    options: options = options
    """
    options child of structure.
    """
    controls: controls = controls
    """
    controls child of structure.
    """
    expert: expert = expert
    """
    expert child of structure.
    """
