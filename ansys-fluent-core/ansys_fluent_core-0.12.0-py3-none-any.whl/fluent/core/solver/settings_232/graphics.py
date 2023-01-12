#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .contour import contour
from .mesh_2 import mesh
from .vector import vector
from .pathline import pathline
from .particle_track import particle_track
from .lic import lic
from .olic import olic
from .contours import contours
from .particle_tracks import particle_tracks
from .colors import colors
from .lights import lights
from .picture import picture
from .views import views
from .windows import windows
class graphics(Group, _ChildNamedObjectAccessorMixin):
    """
    'graphics' child.
    """

    fluent_name = "graphics"

    child_names = \
        ['contour', 'mesh', 'vector', 'pathline', 'particle_track', 'lic',
         'olic', 'contours', 'particle_tracks', 'colors', 'lights', 'picture',
         'views', 'windows']

    contour: contour = contour
    """
    contour child of graphics.
    """
    mesh: mesh = mesh
    """
    mesh child of graphics.
    """
    vector: vector = vector
    """
    vector child of graphics.
    """
    pathline: pathline = pathline
    """
    pathline child of graphics.
    """
    particle_track: particle_track = particle_track
    """
    particle_track child of graphics.
    """
    lic: lic = lic
    """
    lic child of graphics.
    """
    olic: olic = olic
    """
    olic child of graphics.
    """
    contours: contours = contours
    """
    contours child of graphics.
    """
    particle_tracks: particle_tracks = particle_tracks
    """
    particle_tracks child of graphics.
    """
    colors: colors = colors
    """
    colors child of graphics.
    """
    lights: lights = lights
    """
    lights child of graphics.
    """
    picture: picture = picture
    """
    picture child of graphics.
    """
    views: views = views
    """
    views child of graphics.
    """
    windows: windows = windows
    """
    windows child of graphics.
    """
