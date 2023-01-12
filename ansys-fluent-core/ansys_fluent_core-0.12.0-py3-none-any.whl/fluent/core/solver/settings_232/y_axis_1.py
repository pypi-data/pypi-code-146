#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .draw_major_rules import draw_major_rules
from .major_rule_weight import major_rule_weight
from .major_rule_line_color import major_rule_line_color
from .draw_minor_rules import draw_minor_rules
from .minor_rule_weight import minor_rule_weight
from .minor_rule_line_color import minor_rule_line_color
class y_axis(Group):
    """
    'y_axis' child.
    """

    fluent_name = "y-axis"

    child_names = \
        ['draw_major_rules', 'major_rule_weight', 'major_rule_line_color',
         'draw_minor_rules', 'minor_rule_weight', 'minor_rule_line_color']

    draw_major_rules: draw_major_rules = draw_major_rules
    """
    draw_major_rules child of y_axis.
    """
    major_rule_weight: major_rule_weight = major_rule_weight
    """
    major_rule_weight child of y_axis.
    """
    major_rule_line_color: major_rule_line_color = major_rule_line_color
    """
    major_rule_line_color child of y_axis.
    """
    draw_minor_rules: draw_minor_rules = draw_minor_rules
    """
    draw_minor_rules child of y_axis.
    """
    minor_rule_weight: minor_rule_weight = minor_rule_weight
    """
    minor_rule_weight child of y_axis.
    """
    minor_rule_line_color: minor_rule_line_color = minor_rule_line_color
    """
    minor_rule_line_color child of y_axis.
    """
