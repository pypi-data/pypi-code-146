#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .physical_models_2 import physical_models
from .dynamic_mesh import dynamic_mesh
from .mesh_adaption import mesh_adaption
class load_balance(Group):
    """
    'load_balance' child.
    """

    fluent_name = "load-balance"

    child_names = \
        ['physical_models', 'dynamic_mesh', 'mesh_adaption']

    physical_models: physical_models = physical_models
    """
    physical_models child of load_balance.
    """
    dynamic_mesh: dynamic_mesh = dynamic_mesh
    """
    dynamic_mesh child of load_balance.
    """
    mesh_adaption: mesh_adaption = mesh_adaption
    """
    mesh_adaption child of load_balance.
    """
