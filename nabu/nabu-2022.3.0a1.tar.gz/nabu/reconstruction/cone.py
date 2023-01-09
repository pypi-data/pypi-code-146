import numpy as np

try:
    import astra

    __have_astra__ = True
except ImportError:
    __have_astra__ = False
from ..cuda.processing import CudaProcessing


class ConebeamReconstructor:
    """
    A reconstructor for cone-beam geometry using the astra toolbox.
    """

    def __init__(
        self,
        sinos_shape,
        source_origin_dist,
        origin_detector_dist,
        angles=None,
        volume_shape=None,
        rot_center=None,
        relative_z_position=None,
        pixel_size=None,
        cuda_options=None,
    ):
        """
        Initialize a cone beam reconstructor. This reconstructor works on slabs of data,
        meaning that one partial volume is obtained from one stack of sinograms.
        To reconstruct a full volume, the reconstructor must be called on a series of sinograms stacks, with
        an updated "relative_z_position" each time.

        Parameters
        -----------
        sinos_shape: tuple
            Shape of the sinograms stack, in the form (n_sinos, n_angles, prj_width)
        source_origin_dist: float
            Distance, in pixel units, between the beam source (cone apex) and the "origin".
            The origin is defined as the center of the sample
        origin_detector_dist: float
            Distance, in pixel units, between the center of the sample and the detector.
        angles: array, optional
            Rotation angles in radians. If provided, its length should be equal to sinos_shape[1].
        volume_shape: tuple of int, optional
            Shape of the output volume slab, in the form (n_z, n_y, n_x).
            If not provided, the output volume slab shape is (sinos_shape[0], sinos_shape[2], sinos_shape[2]).
        rot_center: float, optional
            Rotation axis position. Default is `(detector_width - 1)/2.0`
        relative_z_position: float, optional
            Position of the central slice of the slab, with respect to the full stack of slices.
            By default it is set to zero, meaning that the current slab is assumed in the middle of the stack
        pixel_size: float or tuple, optional
            Size of the pixel. Possible options:
              - Nothing is provided (default): in this case, all lengths are normalized with respect to the pixel size,
                i.e 'source_origin_dist' and 'origin_detector_dist' should be expressed in pixels (and 'pixel_size' is set to 1).
              - A scalar number is provided: in this case it is the spacing between two pixels (in each dimension)
              - A tuple is provided: in this case it is the spacing between two pixels in both dimensions,
                vertically then horizontally, i.e (detector_spacing_y, detector_spacing_x)


        Notes
        ------
        This reconstructor is using the astra toolbox [1]. Therefore the implementation uses Astra's
        reference frame, which is centered on the sample (source and detector move around the sample).
        For more information see Fig. 2 of paper [1].

        To define the cone-beam geometry, two distances are needed:
          - Source-origin distance (hereby d1)
          - Origin-detector distance (hereby d2)

        The magnification at distance d2 is m = 1+d2/d1, so given a detector pixel size p_s, the sample voxel size is p_s/m.

        To make things simpler, this class internally uses a different (but equivalent) geometry:
          - d2 is set to zero, meaning that the detector is (virtually) moved to the center of the sample
          - The detector is "re-scaled" to have a pixel size equal to the voxel size (p_s/m)

        Having the detector in the same plane as the sample center simplifies things when it comes to slab-wise reconstruction:
        defining a volume slab (in terms of z_min, z_max) is equivalent to define the detector bounds, like in parallel geometry.


        References
        -----------
        [1] Aarle, Wim & Palenstijn, Willem & Cant, Jeroen & Janssens, Eline & Bleichrodt,
        Folkert & Dabravolski, Andrei & De Beenhouwer, Jan & Batenburg, Kees & Sijbers, Jan. (2016).
        Fast and flexible X-ray tomography using the ASTRA toolbox.
        Optics Express. 24. 25129-25147. 10.1364/OE.24.025129.
        """
        self._init_cuda(cuda_options)
        self._init_geometry(
            sinos_shape,
            source_origin_dist,
            origin_detector_dist,
            pixel_size,
            angles,
            volume_shape,
            rot_center,
            relative_z_position,
        )
        self._alg_id = None
        self._vol_id = None
        self._proj_id = None

    def _init_cuda(self, cuda_options):
        cuda_options = cuda_options or {}
        self.cuda = CudaProcessing(**cuda_options)

    def _set_sino_shape(self, sinos_shape):
        if len(sinos_shape) != 3:
            raise ValueError("Expected a 3D shape")
        self.sinos_shape = sinos_shape
        self.n_sinos, self.n_angles, self.prj_width = sinos_shape

    def _set_pixel_size(self, pixel_size):
        if pixel_size is None:
            det_spacing_y = det_spacing_x = 1
        elif np.iterable(pixel_size):
            det_spacing_y, det_spacing_x = pixel_size
        else:
            # assuming scalar
            det_spacing_y = det_spacing_x = pixel_size
        self._det_spacing_y = det_spacing_y
        self._det_spacing_x = det_spacing_x

    def _init_geometry(
        self,
        sinos_shape,
        source_origin_dist,
        origin_detector_dist,
        pixel_size,
        angles,
        volume_shape,
        rot_center,
        relative_z_position,
    ):
        self._set_sino_shape(sinos_shape)
        if angles is None:
            self.angles = np.linspace(0, 2 * np.pi, self.n_angles, endpoint=True)
        else:
            self.angles = angles
        if volume_shape is None:
            volume_shape = (self.sinos_shape[0], self.sinos_shape[2], self.sinos_shape[2])
        self.volume_shape = volume_shape
        self.n_z, self.n_y, self.n_x = self.volume_shape
        self.source_origin_dist = source_origin_dist
        self.origin_detector_dist = origin_detector_dist
        self.magnification = 1 + origin_detector_dist / source_origin_dist
        self.vol_geom = astra.create_vol_geom(self.n_y, self.n_x, self.n_z)
        self.vol_shape = astra.geom_size(self.vol_geom)
        self._cor_shift = 0.0
        self.rot_center = rot_center
        if rot_center is not None:
            self._cor_shift = (self.prj_width - 1) / 2.0 - rot_center
        self._set_pixel_size(pixel_size)
        self._create_astra_proj_geometry(relative_z_position)

    def _create_astra_proj_geometry(self, relative_z_position):
        # This object has to be re-created each time, because once the modifications below are done,
        # it is no more a "cone" geometry but a "cone_vec" geometry, and cannot be updated subsequently
        # (see astra/functions.py:271)
        self.proj_geom = astra.create_proj_geom(
            "cone",
            self._det_spacing_x,
            self._det_spacing_y,
            self.n_sinos,
            self.prj_width,
            self.angles,
            self.source_origin_dist,
            self.origin_detector_dist,
        )
        self.relative_z_position = relative_z_position or 0.0
        self.proj_geom = astra.geom_postalignment(self.proj_geom, (self._cor_shift, 0))
        # Component 2 of vecs is the z coordinate of the source, component 5 is the z component of the detector position
        # We need to re-create the same inclination of the cone beam, thus we need to keep the inclination of the two z positions.
        # The detector is centered on the rotation axis, thus moving it up or down, just moves it out of the reconstruction volume.
        # We can bring back the detector in the correct volume position, by applying a rigid translation of both the detector and the source.
        # The translation is exactly the amount that brought the detector up or down, but in the opposite direction.
        vecs = self.proj_geom["Vectors"]
        vecs[:, 2] = -self.relative_z_position

    def _set_output(self, volume):
        if volume is not None:
            self.cuda.check_array(volume, self.vol_shape)
            self.cuda.set_array("output", volume, self.vol_shape)
        if volume is None:
            self.cuda.allocate_array("output", self.vol_shape)
        d_volume = self.cuda.get_array("output")
        z, y, x = d_volume.shape
        self._vol_link = astra.data3d.GPULink(d_volume.ptr, x, y, z, d_volume.strides[-2])
        self._vol_id = astra.data3d.link("-vol", self.vol_geom, self._vol_link)

    def _set_input(self, sinos):
        self.cuda.check_array(sinos, self.sinos_shape)
        self.cuda.set_array("sinos", sinos, sinos.shape)  # self.cuda.sinos is now a GPU array
        # TODO don't create new link/proj_id if ptr is the same ?
        # But it seems Astra modifies the input sinogram while doing FDK, so this might be not relevant
        d_sinos = self.cuda.get_array("sinos")
        # self._proj_data_link = astra.data3d.GPULink(d_sinos.ptr, self.prj_width, self.n_angles, self.n_z, sinos.strides[-2])
        self._proj_data_link = astra.data3d.GPULink(
            d_sinos.ptr, self.prj_width, self.n_angles, self.n_sinos, sinos.strides[-2]
        )
        self._proj_id = astra.data3d.link("-sino", self.proj_geom, self._proj_data_link)

    def _update_reconstruction(self):
        cfg = astra.astra_dict("FDK_CUDA")
        cfg["ReconstructionDataId"] = self._vol_id
        cfg["ProjectionDataId"] = self._proj_id
        # TODO more options "eg. filter" ?
        if self._alg_id is not None:
            astra.algorithm.delete(self._alg_id)
        self._alg_id = astra.algorithm.create(cfg)

    def reconstruct(self, sinos, output=None, relative_z_position=None):
        """
        sinos: numpy.ndarray or pycuda.gpuarray
            Sinograms, with shape (n_sinograms, n_angles, width)
        output: pycuda.gpuarray, optional
            Output array. If not provided, a new numpy array is returned
        relative_z_position: int, optional
            Position of the central slice of the slab, with respect to the full stack of slices.
            By default it is set to zero, meaning that the current slab is assumed in the middle of the stack
        """
        self._create_astra_proj_geometry(relative_z_position)
        self._set_input(sinos)
        self._set_output(output)
        self._update_reconstruction()
        astra.algorithm.run(self._alg_id)
        result = self.cuda.get_array("output")
        if output is None:
            result = result.get()
        self.cuda.recover_arrays_references(["sinos", "output"])
        return result

    def __del__(self):
        if self._alg_id is not None:
            astra.algorithm.delete(self._alg_id)
        if self._vol_id is not None:
            astra.data3d.delete(self._vol_id)
        if self._proj_id is not None:
            astra.data3d.delete(self._proj_id)
