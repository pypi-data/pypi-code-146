# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "10/05/2022"


from copy import copy
from datetime import datetime
from multiprocessing.sharedctypes import Value
import os
from silx.io.utils import get_data
from typing import Optional, Union
from silx.io.url import DataUrl
from silx.io.dictdump import dicttonx
import numpy
from tomoscan.esrf import HDF5TomoScan, EDFTomoScan
from tomoscan.serie import Serie
from tomoscan.esrf.scan.hdf5scan import ImageKey
from tomoscan.nexus.paths.nxtomo import get_paths as _get_nexus_paths
from tomoscan.scanbase import TomoScanBase
from scipy.ndimage import shift as shift_scipy
from nxtomomill.nexus import NXtomo
from nabu.io.utils import DatasetReader
from tomoscan.esrf.scan.utils import (
    get_compacted_dataslices,
)  # this version has a 'return_url_set' needed here. At one point they should be merged together
from nabu.stitching.frame_composition import ZFrameComposition
from nabu.stitching.utils import find_relative_shifts
from nabu.stitching.config import (
    KEY_CROSS_CORRELATION_SLICE,
    KEY_X_CROSS_CORRELATION_FUNC,
    KEY_Y_CROSS_CORRELATION_FUNC,
    PreProcessedZStitchingConfiguration,
    PostProcessedZStitchingConfiguration,
    ZStitchingConfiguration,
)
from nabu.utils import Progress
from nabu import version as nabu_version
from nabu.io.writer import get_datetime
from .overlap import (
    DEFAULT_OVERLAP_STRATEGY,
    OverlapKernelBase,
    OverlapStichingStrategy,
    ZStichOverlapKernel,
)
from tomoscan.io import HDF5File
import h5py
import logging

_logger = logging.getLogger(__name__)


def z_stitching(configuration: ZStitchingConfiguration, progress=None) -> DataUrl:
    """
    Apply stitching from provided configuration.
    Return a DataUrl with the created NXtomo or Volume
    """
    if isinstance(configuration, PreProcessedZStitchingConfiguration):
        stitcher = PreProcessZStitcher(configuration=configuration, progress=progress)
    elif isinstance(configuration, PostProcessedZStitchingConfiguration):
        raise NotImplementedError
    else:
        raise TypeError(
            f"configuration is expected to be in {(PreProcessedZStitchingConfiguration, PostProcessedZStitchingConfiguration)}. {type(configuration)} provided"
        )
    return stitcher.stitch()


class ZStitcher:
    def __init__(self, configuration, progress: Progress = None) -> None:
        if not isinstance(configuration, ZStitchingConfiguration):
            raise TypeError
        self._configuration = copy(configuration)
        # copy configuration because we will edit it
        self._progress = progress
        # z serie must be defined from daughter class
        assert hasattr(self, "_z_serie")

        def is_auto(param):
            return param in ("auto", ("auto",))

        # 'expend' auto shift request if only set once for all
        if is_auto(self.configuration.x_shifts):
            self.configuration.x_shifts = [
                "auto",
            ] * (len(self.z_serie) - 1)
        elif numpy.isscalar(self.configuration.x_shifts):
            self.configuration.x_shifts = [
                self.configuration.x_shifts,
            ] * (len(self.z_serie) - 1)

        # 'expend' overlaph height and
        if is_auto(self.configuration.overlap_height):
            self.configuration.overlap_height = [
                "auto",
            ] * (len(self.z_serie) - 1)
        elif numpy.isscalar(self.configuration.overlap_height):
            self.configuration.overlap_height = [self.configuration.overlap_height] * (len(self.z_serie) - 1)

        # 'expend' stitching height
        if is_auto(self.configuration.stitching_height):
            self.configuration.stitching_height = [
                "auto",
            ] * (len(self.z_serie) - 1)
        elif numpy.isscalar(self._configuration.stitching_height):
            self.configuration.stitching_height = [self.configuration.stitching_height] * (len(self.z_serie) - 1)

    def stitch(self) -> DataUrl:
        """
        Apply expected stitch from configuration and return the DataUrl of the object created
        """
        raise NotImplementedError("base class")

    def _compute_shifts(self):
        raise NotImplementedError("base class")

    @property
    def z_serie(self) -> Serie:
        return self._z_serie

    @property
    def configuration(self) -> ZStitchingConfiguration:
        return self._configuration

    @property
    def progress(self) -> Optional[Progress]:
        return self._progress

    @staticmethod
    def get_overlap_areas(
        lower_frame: numpy.ndarray,
        upper_frame: numpy.ndarray,
        real_overlap: int,
        stitching_height: int,
    ):
        """
        return the requested area from lower_frame and upper_frame.

        Lower_frame contains at the end of it the 'real overlap' with the upper_frame.
        Upper_frame contains the 'real overlap' at the end of it.

        For some reason the user can ask the stitching height to be smaller than the `real overlap`.

        Here are some drawing to have a better of view of those regions:

        .. image:: images/stitching/z_stitch_real_overlap.png
            :width: 600

        .. image:: z_stitch_stitch_height.png
            :width: 600
        """
        assert real_overlap >= 0
        assert stitching_height >= 0
        if stitching_height > real_overlap:
            raise ValueError(f"stitching height ({stitching_height}) larger than existing overlap ({real_overlap}).")
        real_overlap_0 = lower_frame[-real_overlap:]
        real_overlap_1 = upper_frame[:real_overlap]
        if not real_overlap_0.shape == real_overlap_1.shape:
            raise RuntimeError(
                f"lower and upper frame have different overlap size ({real_overlap_0.shape} vs {real_overlap_1.shape})"
            )
        low_pos = int(real_overlap // 2 - stitching_height // 2)
        hight_pos = int(real_overlap // 2 + stitching_height // 2) + (stitching_height) % 2
        # if there is one more line to take on one side take it on the lower_frame side
        assert real_overlap_0[low_pos:hight_pos].shape == real_overlap_1[low_pos:hight_pos].shape
        return real_overlap_0[low_pos:hight_pos], real_overlap_1[low_pos:hight_pos]

    @staticmethod
    def stitch_frames(
        frames: tuple,
        x_relative_shifts: tuple,
        y_overlap_heights: tuple,
        output_dtype: numpy.ndarray,
        output_dataset: Optional[Union[h5py.Dataset, numpy.ndarray]] = None,
        check_inputs=True,
        shift_mode="nearest",
        overlap_kernels=None,
        i_frame=None,
    ) -> numpy.ndarray:
        """
        shift frames according to provided `shifts` (as y, x tuples) then stitch all the shifted frames together and
        save them to output_dataset.

        :param tuple frames: element must be a DataUrl or a 2D numpy array
        """
        if check_inputs:
            if len(frames) < 2:
                raise ValueError(f"Not enought frames provided for stitching ({len(frames)} provided)")
            if len(frames) != len(x_relative_shifts) + 1:
                raise ValueError(
                    f"Incoherent number of shift provided ({len(x_relative_shifts)}) compare to number of frame ({len(frames)}). len(frames) - 1 expected"
                )
            if len(x_relative_shifts) != len(y_overlap_heights):
                raise ValueError(
                    f"expect to have the same number of x_relative_shifts ({len(x_relative_shifts)}) and y_overlap ({len(y_overlap_heights)})"
                )

        def check_frame_is_2d(frame):
            if frame.ndim != 2:
                raise ValueError(f"2D frame expected when {frame.ndim}D provided")

        # step_0 load data if from url
        data = []
        for frame in frames:
            if isinstance(frame, DataUrl):
                data_frame = get_data(frame)
                if check_inputs:
                    check_frame_is_2d(data_frame)
                data.append(data_frame)
            elif isinstance(frame, numpy.ndarray):
                if check_inputs:
                    check_frame_is_2d(frame)
                data.append(frame)
            else:
                raise TypeError(f"frames are expected to be DataUrl or 2D numpy array. Not {type(frame)}")
        # step 1: shift each frames (except the first one)
        x_shifted_data = [data[0]]
        for frame, x_relative_shift in zip(data[1:], x_relative_shifts):
            # note: for now we only shift data in x. the y shift is handled in the FrameComposition
            x_relative_shift = numpy.asarray(x_relative_shift).astype(numpy.int8)
            if x_relative_shift == 0:
                shifted_frame = frame
            else:
                # TO speed up: should use the Fourier transform
                shifted_frame = shift_scipy(
                    frame,
                    mode=shift_mode,
                    shift=[0, -x_relative_shift],
                    order=1,
                )
            x_shifted_data.append(shifted_frame)

        # step 2: create stitched frame
        if overlap_kernels is None:
            overlap_kernels = ZStichOverlapKernel(frame_width=data[0].shape[1])
        stitched_frame = z_stitch_raw_frames(
            frames=x_shifted_data,
            y_shifts=[-abs(y_overlap_height) for y_overlap_height in y_overlap_heights],
            overlap_kernels=overlap_kernels,
            check_inputs=check_inputs,
            output_dtype=output_dtype,
        )

        # step 3: dump stitched frame
        if output_dataset is not None and i_frame is not None:
            output_dataset[i_frame] = stitched_frame
        return stitched_frame


class PreProcessZStitcher(ZStitcher):
    def __init__(self, configuration, progress=None) -> None:
        # z serie must be defined first
        self._z_serie = Serie("z-serie", iterable=configuration.input_scans, use_identifiers=False)
        self._reading_orders = []
        self._x_flips = []
        self._y_flips = []
        # some scan can have been taken in the opposite order (so must be read on the opposite order one from the other)
        super().__init__(configuration, progress)

    @property
    def reading_order(self):
        """
        as scan can be take on one direction or the order (rotation goes from X to Y then from Y to X)
        we might need to read data from one direction or another
        """
        return self._reading_orders

    @property
    def x_flips(self) -> list:
        return self._x_flips

    @property
    def y_flips(self) -> list:
        return self._y_flips

    def stitch(self):
        if self.progress is not None:
            self.progress.set_name("order scans")
        self._order_scans()
        if self.progress is not None:
            self.progress.set_name("check inputs")
        self._check_inputs()
        if self.progress is not None:
            self.progress.set_name("compute flat field")
        self._compute_reduced_flats_and_darks()
        if self.progress is not None:
            self.progress.set_name("compute shift")
        self._compute_shifts()
        if self.progress is not None:
            self.progress.set_name("stitch projections, save them and create NXtomo")
        self._create_nx_tomo()
        if self.progress is not None:
            self.progress.set_name("dump configuration")
        self._dump_stitching_configuration()
        return DataUrl(
            file_path=self.configuration.output_file_path,
            data_path=self.configuration.output_data_path,
            scheme="h5py",
        )

    def _order_scans(self):
        """
        ensure scans are in z increasing order
        """

        def get_min_z(scan):
            return scan.get_bounding_box(axis="z").min

        sorted_z_serie = Serie(
            self.z_serie.name,
            sorted(self.z_serie[:], key=get_min_z, reverse=True),
            use_identifiers=False,
        )
        if sorted_z_serie != self.z_serie:
            if sorted_z_serie[:] != self.z_serie[::-1]:
                raise ValueError("Unable to get comprehensive input. Z (decreasing) ordering is not respected.")
            else:
                _logger.warning(
                    f"z decreasing order haven't been respected. Need to reorder z serie ({[str(scan) for scan in sorted_z_serie[:]]}). Will also reorder overlap height, stitching height and invert shifts"
                )

            self.configuration.overlap_height = self.configuration.overlap_height[::-1]
            self.configuration.x_shifts = [
                -x_shift if x_shift != "auto" else x_shift for x_shift in self.configuration.x_shifts
            ]
            self.configuration.stitching_height = self.configuration.stitching_height[::-1]

        self._z_serie = sorted_z_serie

    def _check_inputs(self):
        """
        insure input data is coherent
        """
        n_scans = len(self.z_serie)
        if n_scans == 0:
            raise ValueError("no scan to stich together")

        # check number of shift provided
        if len(self.configuration.x_shifts) != (n_scans - 1):
            raise ValueError(f"expect {n_scans -1} shift defined. Get {len(self.configuration.x_shifts)}")

        if len(self.configuration.overlap_height) != (n_scans - 1):
            raise ValueError(f"expect {n_scans - 1} overlap defined. Get {len(self.configuration.overlap_height)}")

        if len(self.configuration.stitching_height) != (n_scans - 1):
            raise ValueError(
                f"expect {n_scans - 1} stitching height defined. Get {len(self.configuration.overlap_height)}"
            )

        for scan in self.z_serie:
            if scan.x_flipped is None or scan.y_flipped is None:
                _logger.warning(
                    f"Found at least one scan with no frame flips information ({scan}). Will consider those are unflipped. Might end up with some inverted frame errors."
                )
                break

        self._reading_orders = []
        # the first scan will define the expected reading orderd, and expected flip.
        # if all scan are flipped then we will keep it this way
        self._reading_orders.append(1)

        # check scans are coherent (nb projections, rotation angle, energy...)
        for scan_0, scan_1 in zip(self.z_serie[0:-1], self.z_serie[1:]):
            if len(scan_0.projections) != len(scan_1.projections):
                raise ValueError(f"{scan_0} and {scan_1} have a different number of projections")
            if isinstance(scan_0, HDF5TomoScan) and isinstance(scan_1, HDF5TomoScan):
                # check rotation (only of is an HDF5TomoScan)
                scan_0_angles = numpy.asarray(scan_0.rotation_angle)
                scan_0_projections_angles = scan_0_angles[
                    numpy.asarray(scan_0.image_key_control) == ImageKey.PROJECTION.value
                ]
                scan_1_angles = numpy.asarray(scan_1.rotation_angle)
                scan_1_projections_angles = scan_1_angles[
                    numpy.asarray(scan_1.image_key_control) == ImageKey.PROJECTION.value
                ]
                if not numpy.allclose(scan_0_projections_angles, scan_1_projections_angles, atol=10e-1):
                    if numpy.allclose(
                        scan_0_projections_angles,
                        scan_1_projections_angles[::-1],
                        atol=10e-1,
                    ):
                        reading_order = -1 * self._reading_orders[-1]
                    else:
                        raise ValueError(f"Angles from {scan_0} and {scan_1} are different")
                else:
                    reading_order = 1 * self._reading_orders[-1]
                self._reading_orders.append(reading_order)
            # check energy
            if scan_0.energy is None:
                _logger.warning(f"no energy found for {scan_0}")
            elif not numpy.isclose(scan_0.energy, scan_1.energy, rtol=1e-03):
                _logger.warning(
                    f"different energy found between {scan_0} ({scan_0.energy}) and {scan_1} ({scan_1.energy})"
                )
            # check FOV
            if not scan_0.field_of_view == scan_1.field_of_view:
                raise ValueError(f"{scan_0} and {scan_1} have different field of view")
            # check distance
            if scan_0.distance is None:
                _logger.warning(f"no distance found for {scan_0}")
            elif not numpy.isclose(scan_0.distance, scan_1.distance, rtol=10e-3):
                raise ValueError(f"{scan_0} and {scan_1} have different sample / detector distance")
            # check pixel size
            if not numpy.isclose(scan_0.x_pixel_size, scan_1.x_pixel_size):
                raise ValueError(
                    f"{scan_0} and {scan_1} have different x pixel size. {scan_0.x_pixel_size} vs {scan_1.x_pixel_size}"
                )
            if not numpy.isclose(scan_0.y_pixel_size, scan_1.y_pixel_size):
                raise ValueError(
                    f"{scan_0} and {scan_1} have different y pixel size. {scan_0.y_pixel_size} vs {scan_1.y_pixel_size}"
                )
            # check magnification (only if is HDF5TomoScan)
            if isinstance(scan_0, HDF5TomoScan) and isinstance(scan_1, HDF5TomoScan):
                if not numpy.isclose(scan_0.magnification, scan_1.magnification):
                    raise ValueError(
                        f"{scan_0} and {scan_1} have different magnification. {scan_0.magnification} vs {scan_1.magnification}"
                    )
            if scan_0.dim_1 != scan_1.dim_1:
                raise ValueError(
                    f"projections width are expected to be the same. Not the canse for {scan_0} ({scan_0.dim_1} and {scan_1} ({scan_1.dim_1}))"
                )

        for scan in self.z_serie:
            # check x, y and z translation are constant (only if is an HDF5TomoScan)
            if isinstance(scan_0, HDF5TomoScan) and isinstance(scan_1, HDF5TomoScan):
                if scan.x_translation is not None and not numpy.isclose(
                    min(scan.x_translation), max(scan.x_translation)
                ):
                    _logger.warning(
                        "x translations appears to be evolving over time. Might end up with wrong stitching"
                    )
                if scan.y_translation is not None and not numpy.isclose(
                    min(scan.y_translation), max(scan.y_translation)
                ):
                    _logger.warning(
                        "y translations appears to be evolving over time. Might end up with wrong stitching"
                    )
                if scan.z_translation is not None and not numpy.isclose(
                    min(scan.z_translation), max(scan.z_translation)
                ):
                    _logger.warning(
                        "z translations appears to be evolving over time. Might end up with wrong stitching"
                    )

    def _compute_reduced_flats_and_darks(self):
        """
        TODO: should be done with nabu stuff !!!
        """
        for scan in self.z_serie:
            try:
                reduced_darks = scan.load_reduced_darks()
            except:
                _logger.info("no reduced dark found. Try to compute them.")
            if reduced_darks in (None, {}):
                reduced_darks = scan.compute_reduced_darks()
                try:
                    # if we don't have write in the folder containing the .nx for example
                    scan.save_reduced_darks(reduced_darks)
                except:
                    pass
            scan.set_reduced_darks(reduced_darks)

            try:
                reduced_flats = scan.load_reduced_flats()
            except:
                _logger.info("no reduced flats found. Try to compute them.")
            if reduced_flats in (None, {}):
                reduced_flats = scan.compute_reduced_flats()
                try:
                    # if we don't have write in the folder containing the .nx for example
                    scan.save_reduced_flats(reduced_flats)
                except:
                    pass
            scan.set_reduced_flats(reduced_flats)

    def _compute_shifts(self):
        """
        compute all shift requested (set to 'auto' in the configuration)
        """
        n_scans = len(self.configuration.input_scans)
        if n_scans == 0:
            raise ValueError("no scan to stich provided")

        # get shift
        final_shifts = []

        projection_for_shift = self.configuration.auto_relative_shift_params.get(KEY_CROSS_CORRELATION_SLICE, "middle")
        x_cross_correlation_function = self.configuration.auto_relative_shift_params.get(
            KEY_X_CROSS_CORRELATION_FUNC, None
        )
        y_cross_correlation_function = self.configuration.auto_relative_shift_params.get(
            KEY_Y_CROSS_CORRELATION_FUNC, None
        )

        for scan_0, scan_1, order_s0, order_s1, x_relative_shift, y_overlap in zip(
            self.z_serie[:-1],
            self.z_serie[1:],
            self.reading_order[:-1],
            self.reading_order[1:],
            self.configuration.x_shifts,
            self.configuration.overlap_height,
        ):
            # compute relative shift
            if x_relative_shift == "auto" or y_overlap == "auto":
                found_y, found_x = find_relative_shifts(
                    scan_0=scan_0,
                    scan_1=scan_1,
                    projection_for_shift=projection_for_shift,
                    x_cross_correlation_function=x_cross_correlation_function,
                    y_cross_correlation_function=y_cross_correlation_function,
                    invert_order=order_s1 != order_s0,
                    auto_flip=True,
                )

            final_shift = (
                found_y if y_overlap == "auto" else y_overlap,
                found_x if x_relative_shift == "auto" else x_relative_shift,
            )

            _logger.info(
                f"between {scan_0} and {scan_1} found a shift of {final_shift}. cross_correlation function used are: {x_cross_correlation_function} for x and {y_cross_correlation_function} for y"
            )
            final_shifts.append(final_shift)

        # set back values
        self.configuration.x_shifts = [final_shift[1] for final_shift in final_shifts]
        self.configuration.overlap_height = [abs(final_shift[0]) for final_shift in final_shifts]

    @staticmethod
    def _data_bunch_iterator(n_projections, bunch_size):
        proj_i = 0
        while n_projections - proj_i > bunch_size:
            yield (proj_i - bunch_size, proj_i)
            proj_i += bunch_size
        else:
            yield (proj_i, n_projections - 1)

    @staticmethod
    def _get_bunch_of_data(bunch_start: int, bunch_end: int, scans: tuple, scans_projections_indexes: tuple):
        """
        goal is to load contiguous projections as much as possible...

        :param scans_with_proj_indexes: tuple with scans and scan projection indexes to be loaded
        :return: list of list. For each frame we want to stitch contains the (flat fielded) frames to stich together
        """
        assert len(scans) == len(scans_projections_indexes)
        scans_proj_urls = []
        # for each scan store the real indices and the data url

        for scan, scan_projection_indexes in zip(scans, scans_projections_indexes):
            scan_proj_urls = {}
            # for each scan get the list of url to be loaded
            for i_proj in range(bunch_start, bunch_end):
                # for scan, scan_projections_indexes in zip(
                #     scans, scans_projections_indexes
                # ):
                proj_index_in_full_scan = scan_projection_indexes[i_proj]
                scan_proj_urls[proj_index_in_full_scan] = scan.projections[proj_index_in_full_scan]
            scans_proj_urls.append(scan_proj_urls)

        # then load data
        all_scan_final_data = numpy.empty((bunch_end - bunch_start, len(scans)), dtype=object)

        for i_scan, scan_urls in enumerate(scans_proj_urls):
            i_frame = 0
            _, set_of_compacted_slices = get_compacted_dataslices(scan_urls, return_url_set=True)
            for _, url in set_of_compacted_slices.items():
                url = DataUrl(
                    file_path=url.file_path(),
                    data_path=url.data_path(),
                    scheme="silx",
                    data_slice=url.data_slice(),
                )
                loaded_slices = get_data(url)
                if loaded_slices.ndim == 3:
                    n_slice = loaded_slices.shape[0]
                else:
                    n_slice = 1
                    loaded_slices = [
                        loaded_slices,
                    ]
                scan_indexes = list(scan_urls.keys())
                data = scan.flat_field_correction(
                    loaded_slices,
                    range(
                        scan_indexes[i_frame],
                        scan_indexes[i_frame] + n_slice,
                    ),
                )
                flip_lr = scans[i_scan].get_x_flipped(default=False)
                flip_ud = scans[i_scan].get_y_flipped(default=False)
                for frame in data:
                    f_frame = frame
                    if flip_lr:
                        f_frame = numpy.fliplr(f_frame)
                    if flip_ud:
                        f_frame = numpy.flipud(f_frame)

                    all_scan_final_data[i_frame, i_scan] = f_frame
                    i_frame += 1

        return all_scan_final_data

    def _create_nx_tomo(self):
        """
        create final NXtomo with stitched frames.
        Policy: save all projections flat fielded. So this NXtomo will only contain projections (no dark and no flat).
        But nabu will be able to reconstruct it with field `flatfield` set to False
        """
        if "auto" in self.configuration.x_shifts:
            raise RuntimeError("Looks like some shift haven't been computed")
        nx_tomo = NXtomo()

        nx_tomo.energy = self.z_serie[0].energy
        start_times = list(filter(None, [scan.start_time for scan in self.z_serie]))
        end_times = list(filter(None, [scan.end_time for scan in self.z_serie]))

        if len(start_times) > 0:
            nx_tomo.start_time = (
                numpy.asarray([numpy.datetime64(start_time) for start_time in start_times]).min().astype(datetime)
            )
        else:
            _logger.warning("Unable to find any start_time from input")
        if len(end_times) > 0:
            nx_tomo.end_time = (
                numpy.asarray([numpy.datetime64(end_time) for end_time in end_times]).max().astype(datetime)
            )
        else:
            _logger.warning("Unable to find any end_time from input")

        title = ",".join([scan.sequence_name or "" for scan in self.z_serie])
        nx_tomo.title = f"stitch done from {title}"

        # handle detector (without frames)
        nx_tomo.instrument.detector.field_of_view = self.z_serie[0].field_of_view
        nx_tomo.instrument.detector.distance = self.z_serie[0].distance
        nx_tomo.instrument.detector.x_pixel_size = self.z_serie[0].x_pixel_size
        nx_tomo.instrument.detector.y_pixel_size = self.z_serie[0].y_pixel_size
        nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION] * len(self.z_serie[0].projections)
        nx_tomo.instrument.detector.tomo_n = len(self.z_serie[0].projections)
        if isinstance(self.z_serie[0], HDF5TomoScan):
            nx_tomo.instrument.detector.magnification = self.z_serie[0].magnification
        # note: stitching process insure unflipping of frames
        nx_tomo.instrument.detector.x_flipped = False
        nx_tomo.instrument.detector.y_flipped = False

        if isinstance(self.z_serie[0], HDF5TomoScan):
            # note: first scan is always the reference as order to read data (so no rotation_angle inversion here)
            rotation_angle = numpy.asarray(self.z_serie[0].rotation_angle)
            nx_tomo.sample.rotation_angle = rotation_angle[
                numpy.asarray(self.z_serie[0].image_key_control) == ImageKey.PROJECTION.value
            ]
        elif isinstance(self.z_serie[0], EDFTomoScan):
            nx_tomo.sample.rotation_angle = numpy.linspace(
                start=0, stop=self.z_serie[0].scan_range, num=self.z_serie[0].tomo_n
            )
        else:
            raise NotImplementedError(
                f"scan type ({type(self.z_serie[0])} is not handled)",
                HDF5TomoScan,
                isinstance(self.z_serie[0], HDF5TomoScan),
            )

        # handle sample
        n_frames = len(nx_tomo.sample.rotation_angle)
        if False not in [isinstance(scan, HDF5TomoScan) for scan in self.z_serie]:
            # we consider the new x, y and z position to be at the center of the one created
            x_translation = [scan.x_translation for scan in self.z_serie if scan.x_translation is not None]
            nx_tomo.sample.x_translation = [numpy.asarray(x_translation).mean()] * n_frames
            y_translation = [scan.y_translation for scan in self.z_serie if scan.y_translation is not None]
            nx_tomo.sample.y_translation = [numpy.asarray(y_translation).mean()] * n_frames
            z_translation = [scan.z_translation for scan in self.z_serie if scan.z_translation is not None]
            nx_tomo.sample.z_translation = [numpy.asarray(z_translation).mean()] * n_frames

            nx_tomo.sample.name = self.z_serie[0].sample_name

        # compute stiched frame shape
        n_proj = len(self.z_serie[0].projections)
        y_overlaps = self.configuration.overlap_height
        stitched_frame_shape = (
            n_proj,
            int(
                numpy.asarray([scan.dim_2 for scan in self.z_serie]).sum()
                - numpy.asarray([abs(overlap) for overlap in y_overlaps]).sum()
            ),
            self.z_serie[0].dim_1,
        )

        # get expected output dataset first (just in case output and input files are the same)
        first_proj_idx = sorted(self.z_serie[0].projections.keys())[0]
        first_proj_url = self.z_serie[0].projections[first_proj_idx]
        if h5py.is_hdf5(first_proj_url.file_path()):
            first_proj_url = DataUrl(
                file_path=first_proj_url.file_path(),
                data_path=first_proj_url.data_path(),
                scheme="h5py",
            )

        # first save the NXtomo entry without the frame
        # dicttonx will fail if the folder does not exists
        os.makedirs(os.path.dirname(self.configuration.output_file_path), exist_ok=True)
        nx_tomo.save(
            file_path=self.configuration.output_file_path,
            data_path=self.configuration.output_data_path,
            nexus_path_version=self.configuration.output_nexus_version,
            overwrite=self.configuration.overwrite_results,
        )

        _logger.info(
            f"reading order is {self.reading_order}",
        )

        # append frames ("instrument/detactor/data" dataset)
        with HDF5File(filename=self.configuration.output_file_path, mode="a") as h5f:
            # note: nx_tomo.save already handles the possible overwrite conflict by removing
            # self.configuration.output_file_path or raising an error

            stitched_frame_path = "/".join(
                [
                    self.configuration.output_data_path,
                    _get_nexus_paths(self.configuration.output_nexus_version).PROJ_PATH,
                ]
            )

            projection_dataset = h5f.create_dataset(
                name=stitched_frame_path,
                shape=stitched_frame_shape,
                dtype=self.configuration.output_dtype,
            )
            # TODO: we could also create in several time and create a virtual dataset from it.
            scans_projections_indexes = []
            for scan, reverse in zip(self.z_serie, self.reading_order):
                scans_projections_indexes.append(sorted(scan.projections.keys(), reverse=(reverse == -1)))
            if self.progress:
                self.progress.set_max_advancement(len(scan.projections.keys()))

            # for each indexes create a value which is the list of url to stitch together
            # for now only try to do the first two
            overlap_kernels = []
            for overlap_height in self.configuration.overlap_height:
                overlap_kernels.append(
                    ZStichOverlapKernel(
                        frame_width=self.z_serie[0].dim_1,
                        stitching_strategy=self.configuration.stitching_strategy,
                        overlap_height=-1 if overlap_height == "auto" else overlap_height,
                    )
                )

            i_proj = 0
            for bunch_start, bunch_end in self._data_bunch_iterator(len(scan.projections), bunch_size=50):
                for data_frames in self._get_bunch_of_data(
                    bunch_start,
                    bunch_end,
                    scans=self.z_serie,
                    scans_projections_indexes=scans_projections_indexes,
                ):
                    # TODO: try to do this in parallel or at least dump then in one go. but not sure this last one would speed up.
                    # should be handled by the flushing mecanism
                    ZStitcher.stitch_frames(
                        frames=data_frames,
                        x_relative_shifts=self.configuration.x_shifts,
                        y_overlap_heights=self.configuration.overlap_height,
                        output_dataset=projection_dataset,
                        overlap_kernels=overlap_kernels,
                        i_frame=i_proj,
                        output_dtype=self.configuration.output_dtype,
                    )
                    if self.progress is not None:
                        self.progress.increase_advancement()
                    i_proj += 1

            # create link to this dataset that can be missing
            # "data/data" link
            if "data" in h5f[self.configuration.output_data_path]:
                data_group = h5f[self.configuration.output_data_path]["data"]
                if not stitched_frame_path.startswith("/"):
                    stitched_frame_path = "/" + stitched_frame_path
                data_group["data"] = h5py.SoftLink(stitched_frame_path)
                if "default" not in h5f[self.configuration.output_data_path].attrs:
                    h5f[self.configuration.output_data_path].attrs["default"] = "data"
                for attr_name, attr_value in zip(
                    ("NX_class", "SILX_style/axis_scale_types", "signal"),
                    ("NXdata", ["linear", "linear"], "data"),
                ):
                    if attr_name not in data_group.attrs:
                        data_group.attrs[attr_name] = attr_value

        return nx_tomo

    def _dump_stitching_configuration(self):
        """dump configuration used for stitching at the NXtomo entry"""
        process_name = "stitching_configuration"
        config_dict = self.configuration.to_dict()
        # adding nabu specific information
        nabu_process_info = {
            "@NX_class": "NXentry",
            f"{process_name}@NX_class": "NXprocess",
            f"{process_name}/program": "nabu-stitching",
            f"{process_name}/version": nabu_version,
            f"{process_name}/date": get_datetime(),
            f"{process_name}/configuration": config_dict,
        }

        dicttonx(
            nabu_process_info,
            h5file=self.configuration.output_file_path,
            h5path=self.configuration.output_data_path,
            update_mode="replace",
            mode="a",
        )


def z_stitch_raw_frames(
    frames: tuple,
    y_shifts: tuple,
    output_dtype: numpy.dtype = numpy.float32,
    check_inputs=True,
    overlap_kernels: Optional[Union[ZStichOverlapKernel, tuple]] = None,
    raw_frames_compositions: Optional[ZFrameComposition] = None,
    overlap_frames_compositions: Optional[ZFrameComposition] = None,
) -> numpy.ndarray:
    """
    stitches raw frames (already shifted and flat fielded !!!) together using
    raw stitching (no pixel interpolation, y_overlap_in_px is expected to be a int)
    returns stitched_projection, raw_img_1, raw_img_2, computed_overlap
    proj_0 and pro_1 are already expected to be in a row. Having stitching_height_in_px in common. At top of proj_0
    and at bottom of proj_1

    :param tuple frames: tuple of 2D numpy array
    :param stitching_heights_in_px: scalar value of the stitching to apply or a list of len(frames) - 1 size with each stitching_height to apply between each couple of frame
    :param raw_frames_compositions: pre computed raw frame composition. If not provided will compute them. allow providing it to speed up calculation
    :param overlap_frames_compositions: pre computed stitched frame composition. If not provided will compute them. allow providing it to speed up calculation
    :param overlap_kernels: ZStichOverlapKernel overlap kernel to be used or a list of kernel (one per overlap). Define startegy and overlap heights
    :param numpy.dtype output_dtype: dataset dtype. For now must be provided because flat field corrcetion change data type (numpy.float32 for now)
    """
    if overlap_kernels is None:
        # handle overlap area
        if overlap_kernels is None and len(frames) > 0:
            # FIXME !
            # pylint: disable= E1123,E1120
            proj_0 = frames[0]
            overlap_kernels = ZStichOverlapKernel(
                stitching_strategy=DEFAULT_OVERLAP_STRATEGY,
                overlap_height=proj_0.shape[0],
                frame_width=proj_0.shape[1],
            )
        if isinstance(overlap_kernels, OverlapKernelBase):
            overlap_kernels = [copy(overlap_kernels) for _ in (len(frames) - 1)]

    if check_inputs:

        def check_proj(proj):
            if not isinstance(proj, numpy.ndarray) and proj.ndim == 2:
                raise ValueError(f"frames are expected to be 2D numpy array")

        [check_proj(frame) for frame in frames]

        for proj_0, proj_1 in zip(frames[:-1], frames[1:]):
            if proj_0.shape[1] != proj_1.shape[1]:
                raise ValueError("Both projections are expected to have the same width")
        for proj_0, proj_1, kernel in zip(frames[:-1], frames[1:], overlap_kernels):
            if proj_0.shape[0] <= kernel.overlap_height:
                raise ValueError(
                    f"proj_0 height ({proj_0.shape[0]}) is less than kernel overlap ({kernel.overlap_height})"
                )
            if proj_1.shape[0] <= kernel.overlap_height:
                raise ValueError(
                    f"proj_1 height ({proj_1.shape[0]}) is less than kernel overlap ({kernel.overlap_height})"
                )

    # cast shift in int: for now only case handled
    y_shifts = [int(y_shift) for y_shift in y_shifts]
    # step 0: create numpy array that will contain stitching
    stitched_projection_shape = (
        # here we only handle frames because shift are already done
        # + because shift are expected to be negative
        int(
            numpy.asarray([frame.shape[0] for frame in frames]).sum() + numpy.asarray(y_shifts).sum(),
        ),
        frames[0].shape[1],
    )
    stitch_array = numpy.empty(stitched_projection_shape, dtype=output_dtype)

    # step 1: set kernel overlap height if undefined
    for y_shift, kernel in zip(y_shifts, overlap_kernels):
        if kernel.overlap_height in (-1, None):
            kernel.overlap_height = abs(y_shift)

    # step 2: set raw data

    # fill stitch array with raw data raw data
    if raw_frames_compositions is None:
        raw_frames_compositions = ZFrameComposition.compute_raw_frame_compositions(
            frames=frames,
            overlap_kernels=overlap_kernels,
            y_shifts=y_shifts,
        )
    raw_frames_compositions.compose(
        output_frame=stitch_array,
        input_frames=frames,
    )

    # step 3 set stitched data

    # 3.1 create stitched overlaps
    stitched_overlap = []
    for frame_0, frame_1, kernel, y_shift in zip(frames[:-1], frames[1:], overlap_kernels, y_shifts):
        if y_shift >= 0:
            raise ValueError("No overlap found. Unagle to do stitching on it")

        frame_0_overlap, frame_1_overlap = ZStitcher.get_overlap_areas(
            frame_0,
            frame_1,
            real_overlap=abs(y_shift),
            stitching_height=kernel.overlap_height,
        )
        assert (
            frame_0_overlap.shape[0] == frame_1_overlap.shape[0] == kernel.overlap_height
        ), f"{frame_0_overlap.shape[0]} == {frame_1_overlap.shape[0]} == {kernel.overlap_height}"

        stitched_overlap.append(
            kernel.stitch(
                frame_0_overlap,
                frame_1_overlap,
            )[0]
        )
    # 3.2 fill stitched overlap on output array
    if overlap_frames_compositions is None:
        overlap_frames_compositions = ZFrameComposition.compute_stitch_frame_composition(
            frames=frames,
            overlap_kernels=overlap_kernels,
            y_shifts=y_shifts,
        )
    overlap_frames_compositions.compose(
        output_frame=stitch_array,
        input_frames=stitched_overlap,
    )

    return stitch_array
