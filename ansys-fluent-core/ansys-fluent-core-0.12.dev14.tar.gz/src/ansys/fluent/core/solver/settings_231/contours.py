#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .auto_scale_2 import auto_scale
from .clip_to_range_2 import clip_to_range
from .surfaces_1 import surfaces
from .filled_contours import filled_contours
from .global_range_1 import global_range
from .line_contours import line_contours
from .log_scale_2 import log_scale
from .n_contour import n_contour
from .node_values_2 import node_values
from .render_mesh import render_mesh
from .coloring_2 import coloring
class contours(Group):
    """
    'contours' child.
    """

    fluent_name = "contours"

    child_names = \
        ['auto_scale', 'clip_to_range', 'surfaces', 'filled_contours',
         'global_range', 'line_contours', 'log_scale', 'n_contour',
         'node_values', 'render_mesh', 'coloring']

    auto_scale: auto_scale = auto_scale
    """
    auto_scale child of contours.
    """
    clip_to_range: clip_to_range = clip_to_range
    """
    clip_to_range child of contours.
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of contours.
    """
    filled_contours: filled_contours = filled_contours
    """
    filled_contours child of contours.
    """
    global_range: global_range = global_range
    """
    global_range child of contours.
    """
    line_contours: line_contours = line_contours
    """
    line_contours child of contours.
    """
    log_scale: log_scale = log_scale
    """
    log_scale child of contours.
    """
    n_contour: n_contour = n_contour
    """
    n_contour child of contours.
    """
    node_values: node_values = node_values
    """
    node_values child of contours.
    """
    render_mesh: render_mesh = render_mesh
    """
    render_mesh child of contours.
    """
    coloring: coloring = coloring
    """
    coloring child of contours.
    """
