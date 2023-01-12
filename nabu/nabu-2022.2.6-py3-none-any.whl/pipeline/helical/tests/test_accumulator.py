from nabu.pipeline.helical import (gridded_accumulator, span_strategy)
from nabu.testutils import get_data

import pytest
import numpy as np
import os
import h5py


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    # This is a helical dataset derived
    # from "crayon" dataset, using 5 slices and covering 2.5 x 360 angular span
    # in halftomo, with vertical translations.

    helical_dataset = get_data("small_sparse_helical_dataset.npz")

    helical_dataset = dict([item for item in helical_dataset.items()])
    # the radios, in the dataset file, are stored by swapping angular and x dimension
    # so that the fast running dimension runs over the projections.
    # Due to the sparsity of the dataset, where only an handful of slices
    # has signal, this gives a much better compression even when the axis is translating
    # vertically
    helical_dataset["radios"] = np.array(np.swapaxes(helical_dataset["radios_transposed"], 0, 2))
    del helical_dataset["radios_transposed"]

    # adding members: radios,  dark, flats, z_pix_per_proj, x_pix_per_proj, projection_angles_deg, pixel_size_mm, phase_margin_pix,
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
    ]
    for key in dataset_keys:
        setattr(cls, key, helical_dataset[key])

    cls.rtol_regridded = 1.0e-6


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

        reconstruction_space = gridded_accumulator.get_reconstruction_space(
            span_info=span_info, min_scanwise_z=15, end_scanwise_z=18, phase_margin_pix=self.phase_margin_pix
        )


        chunk_info = span_info.get_chunk_info((reconstruction_space.my_z_min, reconstruction_space.my_z_end))

        sub_region = reconstruction_space.my_z_min - self.phase_margin_pix, reconstruction_space.my_z_end + self.phase_margin_pix

        ## useful projections
        proj_num_start, proj_num_end = chunk_info.angle_index_span

        # the first of the chunk angular range
        my_first_pnum = proj_num_start

        self.accumulator = gridded_accumulator.GriddedAccumulator(
            gridded_radios=reconstruction_space.gridded_radios,
            gridded_weights=reconstruction_space.gridded_cumulated_weights,
            diagnostic_radios=reconstruction_space.diagnostic_radios,
            diagnostic_weights=reconstruction_space.diagnostic_weights,
            diagnostic_angles=reconstruction_space.diagnostic_proj_angle,
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

        res = reconstruction_space.gridded_radios / reconstruction_space.gridded_cumulated_weights

        # check only a sub part to avoid further increasing of the file on edna site
        errmax = np.max(np.abs(res[:200, 1, -500:] - self.result_inset) / np.max(res))
        assert errmax < self.rtol_regridded, "Max error is too high"

        # uncomment this to see
        # h5py.File("processed_sinogram.h5","w")["sinogram"] = res

    def _read_data_and_apply_flats(self, sub_total_prange_slice, subchunk_slice, chunk_info, sub_region, span_info):

        my_integer_shifts_v = chunk_info.integer_shift_v[subchunk_slice]
        fract_complement_shifts_v = chunk_info.fract_complement_to_integer_shift_v[subchunk_slice]
        x_shifts_list = chunk_info.x_pix_per_proj[subchunk_slice]
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
