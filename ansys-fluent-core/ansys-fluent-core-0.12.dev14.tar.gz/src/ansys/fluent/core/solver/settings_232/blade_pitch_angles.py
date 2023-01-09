#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .blade_pitch_collective import blade_pitch_collective
from .blade_pitch_cyclic_sin import blade_pitch_cyclic_sin
from .blade_pitch_cyclic_cos import blade_pitch_cyclic_cos
class blade_pitch_angles(Group):
    """
    Menu to define the rotor pitch and flapping angles.
    
     - blade-pitch-collective    : , 
     - blade-pitch-cyclic-sin    : , 
     - blade-pitch-cyclic-cos    : , 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "blade-pitch-angles"

    child_names = \
        ['blade_pitch_collective', 'blade_pitch_cyclic_sin',
         'blade_pitch_cyclic_cos']

    blade_pitch_collective: blade_pitch_collective = blade_pitch_collective
    """
    blade_pitch_collective child of blade_pitch_angles.
    """
    blade_pitch_cyclic_sin: blade_pitch_cyclic_sin = blade_pitch_cyclic_sin
    """
    blade_pitch_cyclic_sin child of blade_pitch_angles.
    """
    blade_pitch_cyclic_cos: blade_pitch_cyclic_cos = blade_pitch_cyclic_cos
    """
    blade_pitch_cyclic_cos child of blade_pitch_angles.
    """
