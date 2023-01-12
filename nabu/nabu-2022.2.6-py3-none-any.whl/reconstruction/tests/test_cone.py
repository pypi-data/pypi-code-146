import pytest
import numpy as np
from scipy.ndimage import gaussian_filter
try:
    import astra
    __has_astra__ = True
except ImportError:
    __has_astra__ = False
from nabu.cuda.utils import __has_pycuda__, get_cuda_context
from nabu.testutils import __do_large_mem_tests__
if __has_pycuda__:
    from nabu.reconstruction.cone import ConebeamReconstructor
from nabu.utils import subdivide_into_overlapping_segment


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.vol_shape = (128, 126, 126)
    cls.n_angles = 180
    cls.prj_width = 192  # detector larger than the sample
    cls.src_orig_dist = 1000
    cls.volume, cls.cone_data = generate_hollow_cube_cone_sinograms(
        cls.vol_shape, cls.n_angles, cls.src_orig_dist, prj_width=cls.prj_width
    )
    if __has_pycuda__:
        cls.ctx = get_cuda_context()


@pytest.mark.skipif(not (__has_pycuda__ and __has_astra__), reason="Need pycuda and astra for this test")
@pytest.mark.usefixtures("bootstrap")
class TestCone:
    def _create_cone_reconstructor(self, relative_z_position=None):
        return ConebeamReconstructor(
            self.cone_data.shape,
            self.src_orig_dist,
            relative_z_position=relative_z_position,
            volume_shape=self.volume.shape,
            cuda_options={"ctx": self.ctx},
        )

    def test_simple_cone_reconstruction(self):
        C = self._create_cone_reconstructor()
        res = C.reconstruct(self.cone_data)
        delta = np.abs(res - self.volume)

        # Can we do better ? We already had to lowpass-filter the volume!
        # First/last slices are OK
        assert np.max(delta[:8]) < 1e-5
        assert np.max(delta[-8:]) < 1e-5
        # Middle region has a relatively low error
        assert np.max(delta[40:-40]) < 0.11
        # Transition zones between "zero" and "cube" has a large error
        assert np.max(delta[10:25]) < 0.3
        assert np.max(delta[-25:-10]) < 0.3
        # End of transition zones have a smaller error
        np.max(delta[25:40]) < 0.15
        np.max(delta[-40:-25]) < 0.15

    def test_against_explicit_astra_calls(self):
        C = self._create_cone_reconstructor()
        res = C.reconstruct(self.cone_data)
        #
        # Check that ConebeamReconstructor is consistent with these calls to astra
        #
        angles = np.linspace(0, 2 * np.pi, self.n_angles, True)
        # "vol_geom" shape layout is (y, x, z). But here this geometry is used for the reconstruction
        # (i.e sinogram -> volume)and not for projection (volume -> sinograms).
        # So we assume a square slice. Mind that this is a particular case.
        vol_geom = astra.create_vol_geom(self.vol_shape[2], self.vol_shape[2], self.vol_shape[0])
        proj_geom = astra.create_proj_geom(
            "cone", 1.0, 1.0, self.cone_data.shape[0], self.prj_width, angles, self.src_orig_dist, 0.0
        )
        sino_id = astra.data3d.create("-sino", proj_geom, data=self.cone_data)
        rec_id = astra.data3d.create("-vol", vol_geom)

        cfg = astra.astra_dict("FDK_CUDA")
        cfg["ReconstructionDataId"] = rec_id
        cfg["ProjectionDataId"] = sino_id
        alg_id = astra.algorithm.create(cfg)
        astra.algorithm.run(alg_id)

        res_astra = astra.data3d.get(rec_id)

        # housekeeping
        astra.algorithm.delete(alg_id)
        astra.data3d.delete(rec_id)
        astra.data3d.delete(sino_id)

        assert (
            np.max(np.abs(res - res_astra)) < 5e-4
        ), "ConebeamReconstructor results are inconsistent with plain calls to astra"

    def test_full_vs_partial_cone_geometry(self):
        """
        In the ideal case, all the data volume (and reconstruction) fits in memory.
        In practice this is rarely the case, so we have to reconstruct the volume slabs by slabs.
        The slabs should be slightly overlapping to avoid "stitching" artefacts at the edges.
        """
        # Astra seems to duplicate the projection data, even if all GPU memory is handled externally
        # Let's try with (n_z * n_y * n_x + 2 * n_a * n_z * n_x) * 4  <  mem_limit
        # 256^3 seems OK with n_a = 200 (180 MB)
        n_z = n_y = n_x = 256
        n_a = 200
        src_orig_dist = 1000

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x), n_angles=n_a, src_orig_dist=src_orig_dist
        )
        C_full = ConebeamReconstructor(cone_data.shape, src_orig_dist, cuda_options={"ctx": self.ctx})
        proj_id, projs_full_geom = astra.create_sino3d_gpu(volume, C_full.proj_geom, C_full.vol_geom)
        astra.data3d.delete(proj_id)

        # Do the same slab-by-slab
        inner_slab_size = 64
        overlap = 16
        slab_size = inner_slab_size + overlap * 2
        slabs = subdivide_into_overlapping_segment(n_z, slab_size, overlap)

        projs_partial_geom = np.zeros_like(projs_full_geom)
        for slab in slabs:
            z_min, z_inner_min, z_inner_max, z_max = slab
            rel_z_pos = (z_min + z_max) / 2 - n_z / 2

            subvolume = volume[z_min:z_max, :, :]

            C = ConebeamReconstructor(
                (z_max - z_min, n_a, n_x), src_orig_dist, cuda_options={"ctx": self.ctx},
                relative_z_position=rel_z_pos
            )
            proj_id, projs = astra.create_sino3d_gpu(subvolume, C.proj_geom, C.vol_geom)
            astra.data3d.delete(proj_id)

            projs_partial_geom[z_inner_min:z_inner_max] = projs[z_inner_min - z_min:z_inner_max-z_min]

        error_profile = [
            np.max(np.abs(proj_partial - proj_full))
            for proj_partial, proj_full in zip(projs_partial_geom, projs_full_geom)
        ]
        assert np.all(np.isclose(error_profile, 0.0, atol=1/64)), "Mismatch between full-cone and slab geometries"


def generate_hollow_cube_cone_sinograms(vol_shape, n_angles, src_orig_dist, prj_width=None, apply_filter=True):
    # Adapted from Astra toolbox python samples

    n_z, n_y, n_x = vol_shape
    vol_geom = astra.create_vol_geom(n_y, n_x, n_z)

    prj_width = prj_width or n_x
    prj_height = n_z
    angles = np.linspace(0, 2 * np.pi, n_angles, True)
    proj_geom = astra.create_proj_geom("cone", 1.0, 1.0, prj_height, prj_width, angles, src_orig_dist, 0.0)

    # hollow cube
    cube = np.zeros(astra.geom_size(vol_geom), dtype="f")
    d = int(min(n_x, n_y)/2 * (1 - np.sqrt(2) / 2))
    cube[20:-20, d:-d, d:-d] = 1
    cube[40:-40, d+20:-(d+20), d+20:-(d+20)] = 0

    # High-frequencies yield cannot be accurately retrieved
    if apply_filter:
        cube = gaussian_filter(cube, (1.0, 1.0, 1.0))

    proj_id, proj_data = astra.create_sino3d_gpu(cube, proj_geom, vol_geom)
    astra.data3d.delete(proj_id)  # (n_z, n_angles, n_x)

    return cube, proj_data
