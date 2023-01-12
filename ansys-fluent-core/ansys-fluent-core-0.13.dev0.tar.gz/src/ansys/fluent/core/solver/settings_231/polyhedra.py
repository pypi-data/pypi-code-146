#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .options import options
from .convert_domain import convert_domain
from .convert_hanging_nodes import convert_hanging_nodes
from .convert_hanging_node_zones import convert_hanging_node_zones
from .convert_skewed_cells_1 import convert_skewed_cells
class polyhedra(Group):
    """
    Enter the polyhedra menu.
    """

    fluent_name = "polyhedra"

    child_names = \
        ['options']

    options: options = options
    """
    options child of polyhedra.
    """
    command_names = \
        ['convert_domain', 'convert_hanging_nodes',
         'convert_hanging_node_zones', 'convert_skewed_cells']

    convert_domain: convert_domain = convert_domain
    """
    convert_domain command of polyhedra.
    """
    convert_hanging_nodes: convert_hanging_nodes = convert_hanging_nodes
    """
    convert_hanging_nodes command of polyhedra.
    """
    convert_hanging_node_zones: convert_hanging_node_zones = convert_hanging_node_zones
    """
    convert_hanging_node_zones command of polyhedra.
    """
    convert_skewed_cells: convert_skewed_cells = convert_skewed_cells
    """
    convert_skewed_cells command of polyhedra.
    """
