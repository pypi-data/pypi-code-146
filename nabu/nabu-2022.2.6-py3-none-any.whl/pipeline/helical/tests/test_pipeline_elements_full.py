import os
import numpy as np
import pytest

from nabu.testutils import get_data
from nabu.preproc.ccd import Log, CCDFilter
from nabu.preproc.phase import PaganinPhaseRetrieval
from nabu.cuda.utils import get_cuda_context, __has_pycuda__
from nabu.pipeline.helical import gridded_accumulator, span_strategy
from nabu.pipeline.helical.weight_balancer import WeightBalancer
from nabu.pipeline.helical.helical_utils import find_mirror_indexes

if __has_pycuda__:
    import pycuda.gpuarray as garray
    from nabu.pipeline.helical.fbp import BackprojectorHelical as FBPClass


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    # This is a helical dataset derived
    # from "crayon" dataset, using 5 slices and covering 2.5 x 360 angular span
    # in halftomo, with vertical translations.

    #  >>> d=load("small_sparse_helical_dataset.npz")
    #  dd=dict( d.items() )
    #  >>> dd["median_clip_threshold"] = 0.04
    #  >>> savez("retouched_test.npz",**dd)

    helical_dataset = get_data("small_sparse_helical_dataset.npz")

    helical_dataset = dict(list(helical_dataset.items()))
    # the radios, in the dataset file, are stored by swapping angular and x dimension
    # so that the fast running dimension runs over the projections.
    # Due to the sparsity of the dataset, where only an handful of slices
    # has signal, this gives a much better compression even when the axis is translating
    # vertically
    helical_dataset["radios"] = np.array(np.swapaxes(helical_dataset["radios_transposed"], 0, 2))
    del helical_dataset["radios_transposed"]

    # adding members: radios,  dark, flats, z_pix_per_proj, x_pix_per_proj, projection_angles_deg,
    # pixel_size_mm, phase_margin_pix,
    #  weigth_field=weigth_field, double_flat
    dataset_keys = [
        "dark",
        "flats",
        "z_pix_per_proj",
        "x_pix_per_proj",
        "projection_angles_deg",
        "pixel_size_mm",
        "phase_margin_pix",
        "weights_field",
        "double_flat",
        "rotation_axis_position",
        "detector_shape_vh",
        "result_inset",
        "radios",
        # further  parameters, added on top of the test data which was originally made for gridded_accumulator
        "median_clip_threshold",
        "distance_m",
        "energy_kev",
        "delta_beta",
        "pixel_size_m",
        "padding_type",
        "phase_margin_for_pag",
        "rec_reference",
        "ref_tol",
        "ref_start",
        "ref_end",
    ]
    # the test dataset is the original one from the accumulator test
    # plus some patched metadeta information for phase retrieval.
    # The original dataset had phase_margin_pix and had 3 usefule slices.
    # Here, to test phase retrieval, we redefine the phase margin to the maximum
    # that we can do with such a small dataset
    helical_dataset["phase_margin_pix"] = helical_dataset["phase_margin_for_pag"]

    for key in dataset_keys:
        setattr(cls, key, helical_dataset[key])

    cls.padding_type = str(cls.padding_type)
    cls.rotation_axis_position = float(cls.rotation_axis_position)
    cls.rtol_regridded = 1.0e-6

    cls.projection_angles_rad = np.rad2deg(cls.projection_angles_deg)

    if __has_pycuda__:
        cls.ctx = get_cuda_context(cleanup_at_exit=False)
    yield
    if __has_pycuda__:
        cls.ctx.pop()


@pytest.mark.skipif(not (__has_pycuda__), reason="Needs pycuda for this test")
@pytest.mark.usefixtures("bootstrap")
class TestGriddedAccumulator:
    """
    Test the GriddedAccumulator.
    Rebuilds the sinogram for some selected slices of the crayon dataset
    """

    def test_regridding(self):

        span_info = span_strategy.SpanStrategy(
            z_pix_per_proj=self.z_pix_per_proj,
            x_pix_per_proj=self.x_pix_per_proj,
            detector_shape_vh=self.detector_shape_vh,
            phase_margin_pix=self.phase_margin_pix,
            projection_angles_deg=self.projection_angles_deg,
            require_redundancy=True,
            pixel_size_mm=self.pixel_size_mm,
            logger=None,
        )

        # I would like to reconstruct from feaseable height 15 to feaseable  height 18
        # relatively to the first doable slice in the vertical translation direction
        # I get the heights in the detector frame of the first and of the last

        self.reconstruction_space = gridded_accumulator.get_reconstruction_space(
            span_info=span_info, min_scanwise_z=15, end_scanwise_z=18, phase_margin_pix=self.phase_margin_pix
        )

        chunk_info = span_info.get_chunk_info((self.reconstruction_space.my_z_min, self.reconstruction_space.my_z_end))

        sub_region = (
            self.reconstruction_space.my_z_min - self.phase_margin_pix,
            self.reconstruction_space.my_z_end + self.phase_margin_pix,
        )

        # useful projections
        proj_num_start, proj_num_end = chunk_info.angle_index_span

        # the first of the chunk angular range
        my_first_pnum = proj_num_start

        self.accumulator = gridded_accumulator.GriddedAccumulator(
            gridded_radios=self.reconstruction_space.gridded_radios,
            gridded_weights=self.reconstruction_space.gridded_cumulated_weights,
            diagnostic_radios=self.reconstruction_space.diagnostic_radios,
            diagnostic_weights=self.reconstruction_space.diagnostic_weights,
            diagnostic_angles=self.reconstruction_space.diagnostic_proj_angle,
            dark=self.dark,
            flat_indexes=[0, 7501],
            flats=self.flats,
            weights=self.weights_field,
            double_flat=self.double_flat,
        )

        # splitting in sub ranges of 100 projections
        n_granularity = 100
        pnum_start_list = list(np.arange(proj_num_start, proj_num_end, n_granularity))
        pnum_end_list = pnum_start_list[1:] + [proj_num_end]

        for pnum_start, pnum_end in zip(pnum_start_list, pnum_end_list):

            start_in_chunk = pnum_start - my_first_pnum
            end_in_chunk = pnum_end - my_first_pnum

            self._read_data_and_apply_flats(
                slice(pnum_start, pnum_end), slice(start_in_chunk, end_in_chunk), chunk_info, sub_region, span_info
            )

        res_flatfielded = self.reconstruction_space.gridded_radios / self.reconstruction_space.gridded_cumulated_weights

        # but in real pipeline the radio_shape is obtained from the pipeline get_shape utility method
        self._init_ccd_corrections(res_flatfielded.shape[1:])

        # but in the actual pipeline the argument is not given, and the processed stack is the one internally
        # kept by the pipeline object ( self.gridded_radios in the pipeline )
        self._ccd_corrections(res_flatfielded)

        self._init_phase(res_flatfielded.shape[1:])
        processed_radios = self._retrieve_phase(res_flatfielded)

        self._init_mlog(processed_radios.shape)
        self._take_log(processed_radios)

        top_margin = -self.phase_margin_pix if self.phase_margin_pix else None
        processed_weights = self.reconstruction_space.gridded_cumulated_weights[
            :, self.phase_margin_pix : top_margin, :
        ]

        self._init_weight_balancer()
        self._balance_weights(processed_weights)

        self._init_reconstructor(processed_radios.shape)

        i_slice = 0

        self.d_radios_slim.set(processed_radios[:, i_slice, :])
        self._filter()

        self._apply_weights(i_slice, processed_weights)

        res = self._reconstruct()

        test_slicing = slice(self.ref_start, self.ref_end)
        tested_inset = res[test_slicing, test_slicing]
        assert np.max(np.abs(tested_inset - self.rec_reference)) < self.ref_tol

        # uncomment the four following lines to get the slice image
        # import fabio
        # edf = fabio.edfimage.edfimage()
        # edf.data = res
        # edf.write("reconstructed_slice.edf")

        # put the test here

    def _reconstruct(self):

        axis_corrections = np.zeros_like(self.reconstruction_space.gridded_angles_rad)
        self.reconstruction.set_custom_angles_and_axis_corrections(
            self.reconstruction_space.gridded_angles_rad, axis_corrections
        )

        self.reconstruction.backprojection(self.d_radios_slim, output=self.d_rec_res)

        self.d_rec_res.get(self.rec_res)

        return self.rec_res

    def _apply_weights(self, i_slice, weights):
        """d_radios_slim is on gpu"""
        n_provided_angles = self.d_radios_slim.shape[0]

        for first_angle_index in range(0, n_provided_angles, self.num_weight_radios_per_app):

            end_angle_index = min(n_provided_angles, first_angle_index + self.num_weight_radios_per_app)
            self._d_radios_weights[: end_angle_index - first_angle_index].set(
                weights[first_angle_index:end_angle_index, i_slice]
            )
            self.d_radios_slim[first_angle_index:end_angle_index] *= self._d_radios_weights[
                : end_angle_index - first_angle_index
            ]

    def _filter(self):
        self.mirror_angle_relative_indexes = find_mirror_indexes(self.reconstruction_space.gridded_angles_deg)

        self.reconstruction.sino_filter.filter_sino(
            self.d_radios_slim,
            mirror_indexes=self.mirror_angle_relative_indexes,
            rot_center=self.rotation_axis_position,
            output=self.d_radios_slim,
        )

    def _init_reconstructor(self, processed_radios_shape):

        one_slice_data_shape = processed_radios_shape[:1] + processed_radios_shape[2:]

        self.d_radios_slim = garray.zeros(one_slice_data_shape, np.float32)

        # let's make room for loading chunck of weights without necessarily doubling the memory footprint.
        # The weights will be used to multiplied the d_radios_slim.
        # We will proceed by bunches
        self.num_weight_radios_per_app = 200
        self._d_radios_weights = garray.zeros((self.num_weight_radios_per_app,) + one_slice_data_shape[1:], np.float32)

        pixel_size_cm = self.pixel_size_m * 100

        radio_size_h = processed_radios_shape[-1]

        assert (
            2 * self.rotation_axis_position > radio_size_h
        ), """The code of this test is adapted for HA on the right. This seems to be a case
        of HA on the left because  self.rotation_axis_position={self.rotation_axis_position} and radio_size_h = {radio_size_h}
        """

        rec_dim = int(round(2 * self.rotation_axis_position))

        self.reconstruction = FBPClass(
            one_slice_data_shape,
            angles=np.zeros(processed_radios_shape[0], "f"),
            rot_center=self.rotation_axis_position,
            filter_name=None,
            slice_roi=(0, rec_dim, 0, rec_dim),
            extra_options={
                "scale_factor": 1.0 / pixel_size_cm,
                "axis_correction": np.zeros(processed_radios_shape[0], "f"),
                "padding_mode": "edge",
            },
        )
        self.reconstruction.fbp = self.reconstruction.backproj

        self.d_rec_res = garray.zeros((rec_dim, rec_dim), np.float32)
        self.rec_res = np.zeros((rec_dim, rec_dim), np.float32)

    def _init_weight_balancer(self):
        self.weight_balancer = WeightBalancer(self.rotation_axis_position, self.reconstruction_space.gridded_angles_rad)

    def _balance_weights(self, weights):
        self.weight_balancer.balance_weights(weights)

    def _retrieve_phase(self, radios):
        processed_radios = np.zeros(
            (radios.shape[0],) + (radios.shape[1] - 2 * self.phase_margin_pix,) + (radios.shape[2],), radios.dtype
        )
        for i in range(radios.shape[0]):
            processed_radios[i] = self.phase_retrieval.apply_filter(radios[i])
        return processed_radios

    def _read_data_and_apply_flats(self, sub_total_prange_slice, subchunk_slice, chunk_info, sub_region, span_info):

        my_integer_shifts_v = chunk_info.integer_shift_v[subchunk_slice]

        subr_start_z, subr_end_z = sub_region

        subr_start_z_list = subr_start_z - my_integer_shifts_v
        subr_end_z_list = subr_end_z - my_integer_shifts_v + 1

        dtasrc_start_z = max(0, subr_start_z_list.min())
        dtasrc_end_z = min(span_info.detector_shape_vh[0], subr_end_z_list.max())

        data_raw = self.radios[sub_total_prange_slice, slice(dtasrc_start_z, dtasrc_end_z), :]

        subsampling_file_slice = sub_total_prange_slice

        # my_subsampled_indexes = self.chunk_reader._sorted_files_indices[subsampling_file_slice]
        my_subsampled_indexes = (np.arange(10000))[subsampling_file_slice]

        self.accumulator.extract_preprocess_with_flats(
            subchunk_slice,
            my_subsampled_indexes,
            chunk_info,
            np.array((subr_start_z, subr_end_z), "i"),
            np.array((dtasrc_start_z, dtasrc_end_z), "i"),
            data_raw,
        )

    def _init_ccd_corrections(self, radio_shape):
        # but in real pipeline the radio_shape is obtained from the pipeline get_shape utility method
        self.ccd_correction = CCDFilter(radio_shape, median_clip_thresh=self.median_clip_threshold)

    def _ccd_corrections(self, radios):
        _tmp_radio = np.empty_like(radios[0])
        for i in range(radios.shape[0]):
            self.ccd_correction.median_clip_correction(radios[i], output=_tmp_radio)
            radios[i][:] = _tmp_radio[:]

    def _take_log(self, radios):
        self.mlog.take_logarithm(radios)

    def _init_mlog(self, radios_shape):
        log_shape = radios_shape
        clip_min = 1.0e-6
        clip_max = 1.1
        self.mlog = Log(log_shape, clip_min=clip_min, clip_max=clip_max)

    def _init_phase(self, raw_shape):
        self.phase_retrieval = PaganinPhaseRetrieval(
            raw_shape,
            distance=self.distance_m,
            energy=self.energy_kev,
            delta_beta=self.delta_beta,
            pixel_size=self.pixel_size_m,
            padding=self.padding_type,
            margin=((self.phase_margin_pix,) * 2, (0, 0)),
            use_R2C=True,
            fftw_num_threads=True,  # TODO tune in advanced params of nabu config file
        )
        if self.phase_retrieval.use_fftw:
            self.logger.debug(
                "PaganinPhaseRetrieval using FFTW with %d threads" % self.phase_retrieval.fftw.num_threads
            )
