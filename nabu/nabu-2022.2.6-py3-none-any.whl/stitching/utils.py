from typing import Optional, Union

import numpy
from nabu.stitching.overlap import OverlapStichingStrategy, ZStichOverlapKernel
from tomoscan.scanbase import TomoScanBase
import logging
from scipy.ndimage import shift as scipy_shift

_logger = logging.getLogger(__name__)


try:
    from skimage.registration import phase_cross_correlation
except ImportError:
    _logger.warning(
        "Unable to load skimage. Please install it if you want to use it for finding shifts from `find_relative_shifts`"
    )
    __has_sk_phase_correlation__ = False
else:
    __has_sk_phase_correlation__ = True


def test_overlap_stitching_strategy(overlap_1, overlap_2, stitching_strategies):
    """
    stitch the two ovrelap with all the requested strategies.
    Return a dictionary with stitching strategy as key and a result dict as value.
    result dict keys are: 'weights_overlap_1', 'weights_overlap_2', 'stiching'
    """
    res = {}
    for strategy in stitching_strategies:
        s = OverlapStichingStrategy.from_value(strategy)
        stitcher = ZStichOverlapKernel(
            stitching_strategy=s,
            overlap_height=overlap_1.shape[0],
            frame_width=overlap_1.shape[1],
        )
        stiched_overlap, w1, w2 = stitcher.stitch(overlap_1, overlap_2, check_input=True)
        res[s.value] = {
            "stitching": stiched_overlap,
            "weights_overlap_1": w1,
            "weights_overlap_2": w2,
        }
    return res


def find_relative_shifts(
    scan_0: TomoScanBase,
    scan_1: TomoScanBase,
    projection_for_shift: Union[int, str] = "middle",
    invert_order: bool = False,
    x_cross_correlation_function=None,
    y_cross_correlation_function=None,
    auto_flip: bool = True,
) -> tuple:
    """
    deduce the relative shift between the two scans.
    Expected behavior:
    * compute expected overlap area from z_translations and (sample) pixel size
    * call a cross correlation function from the overlap area to compute the x shift and polish the y shift from `projection_for_shift`

    :param TomoScanBase scan_0:
    :param TomoScanBase scan_1:
    :param Union[int,str] projection_for_shift: index fo the projection to use (in projection space or in scan space ?. For now in projection) or str. If str must be in (`middle`, `first`, `last`)
    :param str x_cross_correlation_function: optional method to refine x shift from computing cross correlation. For now valid values are: ("skimage", "skimage-fourier")
    :param str y_cross_correlation_function: optional method to refine y shift from computing cross correlation. For now valid values are: ("skimage", "skimage-fourier")
    :param int minimal_overlap_area_for_cross_correlation: if first approximated overlap shift found from z_translation is lower than this value will fall back on taking the full image for the cross correlation and log a warning
    :param bool invert_order: are projections inverted between the two scans (case if rotation angle are inverted)
    :param bool auto_flip: if True then will automatically flip frames to get a "homogeneous" result based on unflipped frames
    :return: relative shift of scan_1 with scan_0 as reference: (y_shift, x_shift)
    :rtype: tuple

    :warning: this function will flip left-right and up-down frames by default. So it will return shift according to this information
    """

    def get_flat_fielded_proj(scan: TomoScanBase, proj_index: int, reverse: bool, revert_x: bool, revert_y):
        first_proj_idx = sorted(scan_1.projections.keys(), reverse=reverse)[proj_index]
        ff = scan.flat_field_correction(
            (scan.projections[first_proj_idx],),
            (first_proj_idx,),
        )[0]
        if auto_flip and revert_x:
            ff = numpy.fliplr(ff)
        if auto_flip and revert_y:
            ff = numpy.flipud(ff)
        return ff

    if isinstance(projection_for_shift, str):
        if projection_for_shift.lower() == "first":
            projection_for_shift = 0
        elif projection_for_shift.lower() == "last":
            projection_for_shift = -1
        elif projection_for_shift.lower() == "middle":
            projection_for_shift = len(scan_0.projections) // 2
        else:
            try:
                projection_for_shift = int(projection_for_shift)
            except ValueError:
                raise ValueError(
                    f"{projection_for_shift} cannot be cast to an int and is not one of the possible ('first', 'last', 'middle')"
                )
    elif not isinstance(projection_for_shift, (int, numpy.number)):
        raise TypeError(
            f"projection_for_shift is expected to be an int. Not {type(projection_for_shift)} - {projection_for_shift}"
        )

    proj_0 = get_flat_fielded_proj(
        scan_0,
        projection_for_shift,
        reverse=False,
        revert_x=scan_0.get_x_flipped(default=False),
        revert_y=scan_0.get_y_flipped(default=False),
    )
    proj_1 = get_flat_fielded_proj(
        scan_1,
        projection_for_shift,
        reverse=invert_order,
        revert_x=scan_1.get_x_flipped(default=False),
        revert_y=scan_1.get_y_flipped(default=False),
    )

    # get overlap area from z
    scan_0_y_bb = scan_0.get_bounding_box(axis="z")
    scan_1_y_bb = scan_1.get_bounding_box(axis="z")

    scan_0_scan_1_overlap = scan_0_y_bb.get_overlap(scan_1_y_bb)

    if scan_0_scan_1_overlap is not None:
        overlap = scan_0_scan_1_overlap.max - scan_0_scan_1_overlap.min
        overlap_percentage = (overlap) / (scan_0_y_bb.max - scan_0_y_bb.min)
        y_overlap_frm_position_in_pixel = int(overlap_percentage * scan_0.dim_2)
        overlap_1 = proj_0[-y_overlap_frm_position_in_pixel:]
        overlap_2 = proj_1[:y_overlap_frm_position_in_pixel:]
    else:
        _logger.warning(
            "no overlap founds from scan metadata. Take the full image to try to find an overlap. Automatic shift deduction has an higher probability to fail"
        )

    x_found_shift = 0
    y_found_shift = -y_overlap_frm_position_in_pixel

    if x_cross_correlation_function in ("skimage", "skimage-fourier"):
        if not __has_sk_phase_correlation__:
            raise ValueError("scikit-image not installed. Cannot do phase correlation from it")
        if x_cross_correlation_function == "skimage-fourier":
            overlap_1 = numpy.fft.fftn(overlap_1)
            overlap_2 = numpy.fft.fftn(overlap_2)
            space = "fourier"
        else:
            space = "real"
        found_shift, _, _ = phase_cross_correlation(reference_image=overlap_1, moving_image=overlap_2, space=space)
        x_found_shift = found_shift[1]
    elif x_cross_correlation_function is not None:
        raise ValueError(f"requested cross correlation function not handled ({x_cross_correlation_function})")

    if y_cross_correlation_function in ("skimage", "skimage-fourier"):
        if not __has_sk_phase_correlation__:
            raise ValueError("scikit-image not installed. Cannot do phase correlation from it")
        if y_cross_correlation_function == "skimage-fourier":
            overlap_1 = numpy.fft.fftn(overlap_1)
            overlap_2 = numpy.fft.fftn(overlap_2)
            space = "fourier"
        else:
            space = "real"
        found_shift, _, _ = phase_cross_correlation(reference_image=overlap_1, moving_image=overlap_2, space=space)
        y_found_shift = found_shift[0] - y_overlap_frm_position_in_pixel
    elif y_cross_correlation_function is not None:
        raise ValueError(f"requested cross correlation function not handled ({y_cross_correlation_function})")

    #
    if y_found_shift > 0:
        _logger.warning(
            f"found a positive shift ({found_shift[0]}) when a negative one is expected. Are you sure about the scan z ordering. This is likely z stitching will fails"
        )

    return tuple([int(y_found_shift), int(x_found_shift)])
