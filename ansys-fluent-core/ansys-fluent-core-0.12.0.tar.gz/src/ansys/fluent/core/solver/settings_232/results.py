#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .graphics import graphics
from .scene import scene
from .surfaces_2 import surfaces
from .animations import animations
from .plot_2 import plot
from .report_1 import report
class results(Group):
    """
    'results' child.
    """

    fluent_name = "results"

    child_names = \
        ['graphics', 'scene', 'surfaces', 'animations', 'plot', 'report']

    graphics: graphics = graphics
    """
    graphics child of results.
    """
    scene: scene = scene
    """
    scene child of results.
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of results.
    """
    animations: animations = animations
    """
    animations child of results.
    """
    plot: plot = plot
    """
    plot child of results.
    """
    report: report = report
    """
    report child of results.
    """
