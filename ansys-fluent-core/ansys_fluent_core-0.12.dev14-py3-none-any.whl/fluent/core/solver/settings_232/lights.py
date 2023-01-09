#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .headlight_setting import headlight_setting
from .lights_on import lights_on
from .lighting_interpolation import lighting_interpolation
from .set_ambient_color import set_ambient_color
from .set_light import set_light
class lights(Group):
    """
    'lights' child.
    """

    fluent_name = "lights"

    child_names = \
        ['headlight_setting', 'lights_on', 'lighting_interpolation']

    headlight_setting: headlight_setting = headlight_setting
    """
    headlight_setting child of lights.
    """
    lights_on: lights_on = lights_on
    """
    lights_on child of lights.
    """
    lighting_interpolation: lighting_interpolation = lighting_interpolation
    """
    lighting_interpolation child of lights.
    """
    command_names = \
        ['set_ambient_color', 'set_light']

    set_ambient_color: set_ambient_color = set_ambient_color
    """
    set_ambient_color command of lights.
    """
    set_light: set_light = set_light
    """
    set_light command of lights.
    """
