#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .always_use_face_centroid_with_periodics import always_use_face_centroid_with_periodics
from .interpolation import interpolation
from .boundary_layer_tracking import boundary_layer_tracking
from .check_subtet_validity import check_subtet_validity
from .use_automatic_intersection_tolerance import use_automatic_intersection_tolerance
from .use_barycentric_intersection import use_barycentric_intersection
from .particle_relocation import particle_relocation
from .remove_stuck_particles import remove_stuck_particles
from .use_barycentric_sampling import use_barycentric_sampling
from .use_quad_face_centroid import use_quad_face_centroid
class high_res_tracking_options(Group):
    """
    Main menu containing settings that control the High-Res Tracking scheme.
    When the High-Res Tracking option is enabled (default), the computational cells are decomposed into tetrahedrons
    (subtets) and the particles tracked through the subtets. This option provides a more robust tracking
    algorithm and improved variable interpolation. If High-Res Tracking is not enabled, particles are tracked through
    the computational cells directly. Flow variables that appear in particle equations either use cell-center values
    or a truncated Taylor series approximation for interpolation to the particle position.
    """

    fluent_name = "high-res-tracking-options"

    child_names = \
        ['always_use_face_centroid_with_periodics', 'interpolation',
         'boundary_layer_tracking', 'check_subtet_validity',
         'use_automatic_intersection_tolerance',
         'use_barycentric_intersection', 'particle_relocation',
         'remove_stuck_particles', 'use_barycentric_sampling',
         'use_quad_face_centroid']

    always_use_face_centroid_with_periodics: always_use_face_centroid_with_periodics = always_use_face_centroid_with_periodics
    """
    always_use_face_centroid_with_periodics child of high_res_tracking_options.
    """
    interpolation: interpolation = interpolation
    """
    interpolation child of high_res_tracking_options.
    """
    boundary_layer_tracking: boundary_layer_tracking = boundary_layer_tracking
    """
    boundary_layer_tracking child of high_res_tracking_options.
    """
    check_subtet_validity: check_subtet_validity = check_subtet_validity
    """
    check_subtet_validity child of high_res_tracking_options.
    """
    use_automatic_intersection_tolerance: use_automatic_intersection_tolerance = use_automatic_intersection_tolerance
    """
    use_automatic_intersection_tolerance child of high_res_tracking_options.
    """
    use_barycentric_intersection: use_barycentric_intersection = use_barycentric_intersection
    """
    use_barycentric_intersection child of high_res_tracking_options.
    """
    particle_relocation: particle_relocation = particle_relocation
    """
    particle_relocation child of high_res_tracking_options.
    """
    remove_stuck_particles: remove_stuck_particles = remove_stuck_particles
    """
    remove_stuck_particles child of high_res_tracking_options.
    """
    use_barycentric_sampling: use_barycentric_sampling = use_barycentric_sampling
    """
    use_barycentric_sampling child of high_res_tracking_options.
    """
    use_quad_face_centroid: use_quad_face_centroid = use_quad_face_centroid
    """
    use_quad_face_centroid child of high_res_tracking_options.
    """
