import inspect
import numpy as np
import scipy.fft
from silx.io import get_data
from ..preproc.flatfield import FlatFieldDataUrls
from ..estimation.cor import (
    CenterOfRotation,
    CenterOfRotationAdaptiveSearch,
    CenterOfRotationSlidingWindow,
    CenterOfRotationGrowingWindow,
)
from ..estimation.cor_sino import SinoCor
from ..estimation.tilt import CameraTilt
from ..estimation.utils import is_fullturn_scan
from ..resources.logger import LoggerOrPrint
from ..resources.utils import extract_parameters
from ..utils import check_supported, is_int, deprecation_warning
from .params import tilt_methods
from ..resources.dataset_analyzer import get_0_180_radios
from ..misc.rotation import Rotation
from ..io.reader import ChunkReader
from ..preproc.ccd import Log, CCDFilter
from ..misc import fourier_filters

#  local_fftn = scipy.fft.rfftn                  # rfft changes image shape.
#  local_ifftn = scipy.fft.irfftn                # when N is odd 

"""
nabu.pipeline.estimators: helper classes/functions to estimate parameters of a dataset
(center of rotation, detector tilt, etc).
"""


class CORFinder:
    """
    An application-type class for finding the Center Of Rotation (COR).
    """

    search_methods = {
        "centered": {"class": CenterOfRotation,},
        "global": {"class": CenterOfRotationAdaptiveSearch, "default_kwargs": {"low_pass": 1, "high_pass": 20},},
        "sliding-window": {"class": CenterOfRotationSlidingWindow, "default_args": ["center"],},
        "growing-window": {"class": CenterOfRotationGrowingWindow,},
    }

    def __init__(self, dataset_info, angles=None, halftomo=False, do_flatfield=True, cor_options=None, logger=None):
        """
        Initialize a CORFinder object.

        Parameters
        ----------
        dataset_info: `nabu.resources.dataset_analyzer.DatasetAnalyzer`
            Dataset information structure
        """
        # COMPAT.
        if angles is not None or halftomo is not None:
            deprecation_warning("The parameters 'angles' and 'halftomo' are now ignored and deprecated.", func_name="corfinder")
        # ---
        self.logger = LoggerOrPrint(logger)
        self.dataset_info = dataset_info
        self.do_flatfield = do_flatfield
        self.shape = dataset_info._radio_dims_notbinned[::-1]
        self._init_radios()
        self._init_flatfield()
        self._apply_flatfield()
        self._apply_tilt()
        self._default_search_method = "centered"
        if self.dataset_info.is_halftomo:
            self._default_search_method = "sliding-window"
        self._get_cor_options(cor_options)

    def _init_radios(self):
        self.radios, self._radios_indices = get_0_180_radios(self.dataset_info, return_indices=True)

    def _init_flatfield(self):
        if not (self.do_flatfield):
            return
        self.flatfield = FlatFieldDataUrls(
            self.radios.shape,
            flats=self.dataset_info.flats,
            darks=self.dataset_info.darks,
            radios_indices=self._radios_indices,
            interpolation="linear",
            convert_float=True,
        )

    def _apply_flatfield(self):
        if not (self.do_flatfield):
            return
        self.flatfield.normalize_radios(self.radios)

    def _apply_tilt(self):
        tilt = self.dataset_info.detector_tilt
        if tilt is None:
            return
        self.logger.debug("COREstimator: applying detector tilt correction of %f degrees" % tilt)
        rot = Rotation(self.shape, tilt)
        for i in range(self.radios.shape[0]):
            self.radios[i] = rot.rotate(self.radios[i])

    def _get_cor_options(self, cor_options):
        if cor_options is None:
            self.cor_options = {}
            if self.dataset_info.is_halftomo:
                self.cor_options = {"side": "right"}
            return
        try:
            cor_options = extract_parameters(cor_options)
        except Exception as exc:
            msg = "Could not extract parameters from cor_options: %s" % (str(exc))
            self.logger.fatal(msg)
            raise ValueError(msg)
        self.cor_options = cor_options

    def find_cor(self, method=None):
        """
        Find the center of rotation.

        Parameters
        ----------
        method: str, optional
            Which CoR search method to use. Default "centered".

        Returns
        -------
        cor: float
            The estimated center of rotation for the current dataset.

        Notes
        ------
        This function passes the named parameters to nabu.preproc.alignment.CenterOfRotation.find_shift.
        """
        method = method or self._default_search_method
        check_supported(method, self.search_methods.keys(), "CoR estimation method")
        cor_class = self.search_methods[method]["class"]
        cor_finder = cor_class(logger=self.logger)
        self.logger.info("Estimating center of rotation")

        default_params = self.search_methods[method].get("default_kwargs", None) or {}
        cor_exec_kwargs = default_params.copy()
        cor_exec_kwargs.update(self.cor_options)
        cor_exec_args = self.search_methods[method].get("default_args", None) or []
        # Specific to CenterOfRotationSlidingWindow
        if cor_class == CenterOfRotationSlidingWindow:
            side_param = cor_exec_kwargs.pop("side", "center")
            cor_exec_args = [side_param]
        #
        cor_exec_kwargs.pop("slice", None)
        self.logger.debug("%s(%s)" % (get_class_name(cor_class), str(cor_exec_kwargs)))
        shift = cor_finder.find_shift(self.radios[0], np.fliplr(self.radios[1]), *cor_exec_args, **cor_exec_kwargs)
        # find_shift returned a single scalar in 2020.1
        # This should be the default after 2020.2 release
        if hasattr(shift, "__iter__"):
            shift = shift[0]
        #
        res = self.shape[1] / 2 + shift
        self.logger.info("Estimated center of rotation: %.2f" % res)
        return res


# alias
COREstimator = CORFinder


class SinoCORFinder:
    """
    A class for finding Center of Rotation based on 360 degrees sinograms.
    This class handles the steps of building the sinogram from raw radios.
    """

    search_methods = ["sino-coarse-to-fine", "sliding-window", "growing-window"]
    default_method = "sino-coarse-to-fine"

    def __init__(self, dataset_info, slice_idx, subsampling=10, do_flatfield=True, cor_options=None, logger=None):
        """
        Initialize a SinoCORFinder object.

        Parameters
        ---------
        dataset_info: `nabu.resources.dataset_analyzer.DatasetAnalyzer`
            Dataset information structure
        slice_idx: int or str
            Which slice index to take for building the sinogram.
            For example slice_idx=0 means that we extract the first line of each projection.
            Value can also be "first", "top", "middle", "last", "bottom".
        subsampling: int, float
            subsampling strategy when building sinograms.
            As building the complete sinogram from raw projections might be tedious, the reading is done with subsampling.
            A positive integer value means the subsampling step (i.e `projections[::subsampling]`).
            A negative integer value means we take -subsampling projections in total.
            A float value indicates the angular step in DEGREES.
        do_flatfield: bool, optional
            Whether to perform flat-field normalization. Default is True.
        cor_options: str
            User options for the auto-CoR method.
        logger: Logger, optional
            Logging object
        """
        self.logger = LoggerOrPrint(logger)
        self.dataset_info = dataset_info
        self._check_360()
        self._set_slice_idx(slice_idx)
        self._set_subsampling(subsampling)
        self._load_raw_sinogram()
        self._flatfield(do_flatfield)
        self._get_sinogram()
        self._get_cor_options(cor_options)

    _get_cor_options = CORFinder._get_cor_options

    def _check_360(self):
        if self.dataset_info.dataset_scanner.scan_range == 360:
            return
        if not is_fullturn_scan(self.dataset_info.rotation_angles):
            raise ValueError("Sinogram-based Center of Rotation estimation can only be used for 360 degrees scans")

    def _set_slice_idx(self, slice_idx):
        n_z = self.dataset_info.radio_dims[1]
        if isinstance(slice_idx, str):
            str_to_idx = {"top": 0, "first": 0, "middle": n_z // 2, "bottom": n_z - 1, "last": n_z - 1}
            check_supported(slice_idx, str_to_idx.keys(), "slice location")
            slice_idx = str_to_idx[slice_idx]
        self.slice_idx = slice_idx

    def _set_subsampling(self, subsampling):
        projs_idx = sorted(self.dataset_info.projections.keys())
        if is_int(subsampling):
            if subsampling < 0:  # Total number of angles
                n_angles = -subsampling
                indices_float = np.linspace(projs_idx[0], projs_idx[-1], n_angles, endpoint=True)
                self.projs_indices = np.round(indices_float).astype(np.int32).tolist()
            else:  # Subsampling step
                self.projs_indices = projs_idx[::subsampling]
        else:  # Angular step
            raise NotImplementedError()

    def _load_raw_sinogram(self):
        if self.slice_idx is None:
            raise ValueError("Unknow slice index")
        # Subsample projections
        files = {}
        for idx in self.projs_indices:
            files[idx] = self.dataset_info.projections[idx]
        self.files = files
        self.data_reader = ChunkReader(
            self.files, sub_region=(None, None, self.slice_idx, self.slice_idx + 1), convert_float=True,
        )
        self.data_reader.load_files()
        self._radios = self.data_reader.files_data

    def _flatfield(self, do_flatfield):
        self.do_flatfield = bool(do_flatfield)
        if not self.do_flatfield:
            return
        flatfield = FlatFieldDataUrls(
            self._radios.shape,
            self.dataset_info.flats,
            self.dataset_info.darks,
            radios_indices=self.projs_indices,
            sub_region=(None, None, self.slice_idx, self.slice_idx + 1),
        )
        flatfield.normalize_radios(self._radios)

    def _get_sinogram(self):
        log = Log(self._radios.shape, clip_min=1e-6, clip_max=10.0)
        sinogram = self._radios[:, 0, :].copy()
        log.take_logarithm(sinogram)
        self.sinogram = sinogram

    @staticmethod
    def _split_sinogram(sinogram):
        n_a_2 = sinogram.shape[0] // 2
        img_1, img_2 = sinogram[:n_a_2], sinogram[n_a_2:]
        return img_1, img_2

    def _find_cor_sliding_window(self):
        cor_finder = CenterOfRotationSlidingWindow(logger=self.logger)

        img_1, img_2 = self._split_sinogram(self.sinogram)
        kwargs = update_func_kwargs(cor_finder.find_shift, self.cor_options)
        side = self.cor_options.get("side", "right")
        kwargs.pop("side", None)
        self.logger.debug("CenterOfRotationSlidingWindow.find_shift(%s)" % str(kwargs))
        cor = cor_finder.find_shift(img_1, img_2, side, **kwargs)
        return cor + self.sinogram.shape[1] / 2.0

    def _find_cor_growing_window(self):
        cor_finder = CenterOfRotationGrowingWindow(logger=self.logger)

        img_1, img_2 = self._split_sinogram(self.sinogram)
        kwargs = update_func_kwargs(cor_finder.find_shift, self.cor_options)
        self.logger.debug("CenterOfRotationGrowingWindow.find_shift(%s)" % str(kwargs))
        cor = cor_finder.find_shift(img_1, img_2, **kwargs)

        return cor + self.sinogram.shape[1] / 2.0

    def _find_cor_coarse2fine(self):
        side = self.cor_options.get("side", "right")
        window_width = self.cor_options.get("window_width", None)
        neighborhood = self.cor_options.get("neighborhood", 7)
        shift_value = self.cor_options.get("shift_value", 0.1)
        cor_finder = SinoCor(self.sinogram, logger=self.logger)
        self.logger.debug("SinoCor.estimate_cor_coarse(side=%s, window_width=%s)" % (str(side), str(window_width)))
        cor_finder.estimate_cor_coarse(side=side, window_width=window_width)
        self.logger.debug("SinoCor.estimate_cor_fine(neighborhood=%s, shift_value=%s)" % (str(neighborhood), str(shift_value)))
        cor = cor_finder.estimate_cor_fine(neighborhood=neighborhood, shift_value=shift_value)
        return cor

    def find_cor(self, method=None):
        method = method or self.default_method
        cor_estimation_function = {
            "sino-coarse-to-fine": self._find_cor_coarse2fine,
            "sliding-window": self._find_cor_sliding_window,
            "growing-window": self._find_cor_growing_window,
        }
        check_supported(method, cor_estimation_function.keys(), "sinogram-based CoR estimation method")
        res = cor_estimation_function[method]()
        return res


# alias
SinoCOREstimator = SinoCORFinder


class CompositeCORFinder:
    """
    Class and method to prepare sinogram and calculate COR
    The pseudo sinogram is built with shrinked radios taken every theta_interval degres

    Compared to first writing by Christian Nemoz:
        -- gives the same result of the original octave script on the dataset sofar tested
        -- The meaning of parameter n_subsampling_y (alias subsampling_y)is now the number of lines which are taken from
           every radio. This is more meaningful in terms of amout of collected information because it
           does not depend on the radio size. Moreover this is what was done in the octave script
        -- The spike_threshold has been added with default to 0.04
        -- The angular sampling is every 5 degree by default, as it is now the case also in the octave script
        -- The finding of the optimal overlap is doing by looping over the possible overlap, according to the overlap.
           After a first testing phase by Elodie we, this part, which is the time consuming part, can be accelerated
           by several order of magnitude without modifing the final result
    """

    def __init__(
        self,
        dataset_info,
        oversampling=4,
        theta_interval=5,
        n_subsampling_y=10,
        take_log=True,
        cor_options=None,
        spike_threshold=0.04,
        logger=None,
    ):

        self.dataset_info = dataset_info
        self.logger = LoggerOrPrint(logger)

        # the algorithm can work for angular ranges larger than 1.2*pi
        # up to an arbitrarily number of turns as it is the case in helical scans
        self.spike_threshold = spike_threshold
        # the following line is necessary for multi-turns scan because the encoders is always
        # in the interval 0-360
        self.unwrapped_rotation_angles = np.unwrap(self.dataset_info.rotation_angles)

        self.angle_min = self.unwrapped_rotation_angles.min()
        self.angle_max = self.unwrapped_rotation_angles.max()

        self.sx, self.sy = self.dataset_info.radio_dims

        if (self.angle_max - self.angle_min) < 1.2 * np.pi:
            useful_span = None
            raise ValueError(
                f"""Sinogram-based Center of Rotation estimation can only be used for scans over more than 180 degrees. 
                                 Your angular span was barely above 180 degrees, it was in fact {((self.angle_max - self.angle_min)/np.pi):.2f} x 180
                                 and it is not considered to be enough by the discriminating condition which requires at least 1.2 half-turns
                              """
            )
        else:
            useful_span = min(np.pi, (self.angle_max - self.angle_min) - np.pi)
            # readapt theta_interval accordingly if the span is smaller than pi
            if useful_span < np.pi:
                theta_interval = theta_interval * useful_span / np.pi

        self._get_cor_options(cor_options)

        self.take_log = take_log
        self.ovs = oversampling
        self.theta_interval = theta_interval

        target_sampling_y = np.round(np.linspace(0, self.sy - 1, n_subsampling_y + 2)).astype(int)[1:-1]

        if self.spike_threshold is not None:
            # take also one line below and on above for each line
            # to provide appropriate margin
            self.sampling_y = np.zeros([3 * len(target_sampling_y)], "i")
            self.sampling_y[0::3] = np.maximum(0, target_sampling_y - 1)
            self.sampling_y[2::3] = np.minimum(self.sy - 1, target_sampling_y + 1)
            self.sampling_y[1::3] = target_sampling_y

            self.ccd_correction = CCDFilter((len(self.sampling_y), self.sx), median_clip_thresh=self.spike_threshold)
        else:
            self.sampling_y = target_sampling_y

        self.nproj = self.dataset_info.n_angles

        my_condition = np.less(self.unwrapped_rotation_angles + np.pi, self.angle_max) * np.less(
            self.unwrapped_rotation_angles, self.angle_min + useful_span
        )

        possibly_probed_angles = self.unwrapped_rotation_angles[my_condition]
        possibly_probed_indices = np.arange(len(self.unwrapped_rotation_angles))[my_condition]

        self.dproj = round(len(possibly_probed_angles) / np.rad2deg(useful_span) * self.theta_interval)

        self.probed_angles = possibly_probed_angles[:: self.dproj]
        self.probed_indices = possibly_probed_indices[:: self.dproj]

        self.absolute_indices = sorted(self.dataset_info.projections.keys())

        self.flatfield = FlatFieldDataUrls(
            (len(self.absolute_indices), self.sy, self.sx),
            self.dataset_info.flats,
            self.dataset_info.darks,
            radios_indices=self.absolute_indices,
            dtype=np.float64,
        )
        self.mlog = Log((1,) + self.flatfield.shape, clip_min=1e-6, clip_max=10.0)
        self.sx, self.sy = self.dataset_info.radio_dims
        self.rcor_abs = round(self.sx / 2.0)
        self.cor_acc = round(self.sx / 2.0)

        self.nprobed = len(self.probed_angles)

        # initialize sinograms and radios arrays
        self.sino = np.zeros([2 * self.nprobed * n_subsampling_y, (self.sx - 1) * self.ovs + 1], "f")
        self._loaded = False

        self.high_pass = self.cor_options["high_pass"]
        img_filter = fourier_filters.get_bandpass_filter(
            (self.sino.shape[0] // 2, self.sino.shape[1]),
            cutoff_lowpass=self.cor_options["low_pass"] * self.ovs,
            cutoff_highpass=self.high_pass * self.ovs,
            use_rfft=False,  # rfft changes the image dimensions lenghts to even if odd
            data_type=np.float64,
        )

        # we are interested in filtering only along the x dimension only

        img_filter[:] = img_filter[0]
        self.img_filter = img_filter

    def _oversample(self, radio):
        """oversampling in the horizontal direction"""
        if self.ovs == 1:
            return radio
        result = np.zeros([radio.shape[0], (radio.shape[1] - 1) * self.ovs + 1], "f")
        result[:, :: self.ovs] = radio

        for i in range(1, self.ovs):
            f = i / self.ovs
            result[:, i :: self.ovs] = (1 - f) * result[:, 0 : -self.ovs : self.ovs] + f * result[:, self.ovs :: self.ovs]

        return result

    def _get_cor_options(self, cor_options):
        default_dict = {"low_pass": 0.4, "high_pass": 10, "side": "center", "near_pos": 0, "near_width": 20}
        if self.dataset_info.is_halftomo:
            default_dict["side"] = "right"

        if cor_options is None:
            cor_options = {}
        else:
            try:
                cor_options = extract_parameters(cor_options.strip())
            except Exception as exc:
                msg = "Could not extract parameters from cor_options: %s" % (str(exc))
                self.logger.fatal(msg)
                raise ValueError(msg)

        default_dict.update(cor_options)
        cor_options = default_dict

        self.cor_options = cor_options

    def get_radio(self, image_num):
        #  radio_dataset_idx = self.absolute_indices[image_num]
        radio_dataset_idx = image_num
        data_url = self.dataset_info.projections[radio_dataset_idx]
        radio = get_data(data_url).astype(np.float64)
        self.flatfield.normalize_single_radio(radio, radio_dataset_idx, dtype=radio.dtype)
        if self.take_log:
            self.mlog.take_logarithm(radio)

        radio = radio[self.sampling_y]
        if self.spike_threshold is not None:
            self.ccd_correction.median_clip_correction(radio, output=radio)
            radio = radio[1::3]
        return radio

    def get_sino(self, reload=False):
        """
        Build sinogram (composite image) from the radio files
        """
        if self._loaded and not reload:
            return self.sino

        sorting_indexes = np.argsort(self.unwrapped_rotation_angles)

        sorted_all_angles = self.unwrapped_rotation_angles[sorting_indexes]
        sorted_angle_indexes = np.arange(len(self.unwrapped_rotation_angles))[sorting_indexes]

        irad = 0
        for prob_a, prob_i in zip(self.probed_angles, self.probed_indices):
            radio1 = self.get_radio(self.absolute_indices[prob_i])
            other_angle = prob_a + np.pi

            insertion_point = np.searchsorted(sorted_all_angles, other_angle)
            if insertion_point > 0 and insertion_point < len(sorted_all_angles):
                other_i_l = sorted_angle_indexes[insertion_point - 1]
                other_i_h = sorted_angle_indexes[insertion_point]
                radio_l = self.get_radio(self.absolute_indices[other_i_l])
                radio_h = self.get_radio(self.absolute_indices[other_i_h])
                f = (other_angle - sorted_all_angles[insertion_point - 1]) / (
                    sorted_all_angles[insertion_point] - sorted_all_angles[insertion_point - 1]
                )
                radio2 = (1 - f) * radio_l + f * radio_h
            else:
                if insertion_point == 0:
                    other_i = sorted_angle_indexes[0]
                elif insertion_point == len(sorted_all_angles):
                    other_i = sorted_angle_indexes[insertion_point - 1]
                radio2 = self.get_radio(self.absolute_indices[other_i])

            self.sino[irad : irad + radio1.shape[0], :] = self._oversample(radio1)
            self.sino[
                irad + self.nprobed * radio1.shape[0] : irad + self.nprobed * radio1.shape[0] + radio1.shape[0], :
            ] = self._oversample(radio2)

            irad = irad + radio1.shape[0]

        self.sino[np.isnan(self.sino)] = 0.0001  # ?
        return self.sino

    _find_cor_coarse2fine = SinoCORFinder._find_cor_coarse2fine

    def find_cor(self, reload=False, **kwargs):
        self.sinogram = self.get_sino(reload=reload)

        dim_v, dim_h = self.sinogram.shape
        assert dim_v % 2 == 0, " this should not happen "
        dim_v = dim_v // 2

        radio1 = self.sinogram[:dim_v]
        radio2 = self.sinogram[dim_v:]

        orig_sy, orig_ovsd_sx = radio1.shape

        radio1 = scipy.fft.ifftn(
            scipy.fft.fftn(radio1, axes=(-2, -1)) * self.img_filter, axes=(-2, -1)
        ).real  # TODO: convolute only along x
        radio2 = scipy.fft.ifftn(
            scipy.fft.fftn(radio2, axes=(-2, -1)) * self.img_filter, axes=(-2, -1)
        ).real  # TODO: convolute only along x

        tmp_sy, ovsd_sx = radio1.shape
        assert orig_sy == tmp_sy and orig_ovsd_sx == ovsd_sx, "this should not happen"

        if self.cor_options["side"] == "center":
            overlap_min = max(round(ovsd_sx - ovsd_sx / 3), 4)
            overlap_max = min(round(ovsd_sx + ovsd_sx / 3), 2 * ovsd_sx - 4)
        elif self.cor_options["side"] == "right":
            overlap_min = max(4, self.ovs * self.high_pass * 3)
            overlap_max = ovsd_sx
        elif self.cor_options["side"] == "left":
            overlap_min = ovsd_sx
            overlap_max = min(2 * ovsd_sx - 4, 2 * ovsd_sx - self.ovs * self.ovs * self.high_pass * 3)
        elif self.cor_options["side"] == "all":
            overlap_min = max(4, self.ovs * self.high_pass * 3)
            overlap_max = min(2 * ovsd_sx - 4, 2 * ovsd_sx - self.ovs * self.ovs * self.high_pass * 3)

        elif self.cor_options["side"] == "near":

            near_pos = self.cor_options["near_pos"]
            near_width = self.cor_options["near_width"]

            overlap_min = max(4, ovsd_sx - 2 * self.ovs * (near_pos + near_width))
            overlap_max = min(2 * ovsd_sx - 4, ovsd_sx - 2 * self.ovs * (near_pos - near_width))

        else:
            message = f""" The cor options "side" can only have one of the three possible values ["","",""].
            But it has the value "{self.cor_options["side"]}" instead
            """
            raise ValueError(message)

        if overlap_min > overlap_max:
            message = f""" There is no safe search range in find_cor once the margins corresponding to the high_pass filter are discarded.
            Try reducing the low_pass parameter in cor_options
            """
            raise ValueError(message)

        self.logger.info("looking for overlap from min %.2f and max %.2f\n" % (overlap_min / self.ovs, overlap_max / self.ovs))

        best_overlap = overlap_min
        best_value = np.inf
        for z in range(int(overlap_min), int(overlap_max) + 1):
            if z <= ovsd_sx:
                my_z = z
                my_radio1 = radio1
                my_radio2 = radio2
            else:
                my_z = ovsd_sx - (z - ovsd_sx)
                my_radio1 = np.fliplr(radio1)
                my_radio2 = np.fliplr(radio2)

            common_left = np.fliplr(my_radio1[:, ovsd_sx - my_z :])[:, : -(self.ovs * self.high_pass * 2)]
            common_right = my_radio2[:, ovsd_sx - my_z : -(self.ovs * self.high_pass * 2)]
            common = common_right - common_left

            value = np.linalg.norm(common)
            norm_diff2 = value * value

            if common_right.size == 0 :
                continue
            norm_right = np.linalg.norm(common_right)
            norm_left = np.linalg.norm(common_left)

            value = norm_diff2 / (norm_right * norm_left)

            min_value = min(best_value, value)

            if min_value == value:
                best_overlap = z
                best_value = min_value
            self.logger.debug(
                "testing an overlap of %.2f pixels, actual best overlap is %.2f pixels over %d\r"
                % (z / self.ovs, best_overlap / self.ovs, ovsd_sx),
            )

        offset = (ovsd_sx - best_overlap) / self.ovs / 2
        cor_abs = (self.sx - 1) / 2 + offset
        self.logger.info("Found an optimal cor at %e (absolute)\n" % cor_abs)

        return cor_abs


# alias
CompositeCOREstimator = CompositeCORFinder


def get_function_default_kwargs(func):
    defaults_kwargs_vals = func.__defaults__
    varnames = func.__code__.co_varnames


# Some heavily inelegant things going on here
def get_default_kwargs(func):
    params = inspect.signature(func).parameters
    res = {}
    for param_name, param in params.items():
        if param.default != inspect._empty:
            res[param_name] = param.default
    return res


def update_func_kwargs(func, options):
    res_options = get_default_kwargs(func)
    for option_name, option_val in options.items():
        if option_name in res_options:
            res_options[option_name] = options[option_name]
    return res_options


def get_class_name(class_object):
    return str(class_object).split(".")[-1].strip(">").strip("'").strip('"')


class DetectorTiltEstimator:
    """
    Helper class for detector tilt estimation.
    It automatically chooses the right radios and performs flat-field.
    """

    default_tilt_method = "1d-correlation"
    # Given a tilt angle "a", the maximum deviation caused by the tilt (in pixels) is
    #  N/2 * |sin(a)|  where N is the number of pixels
    # We ignore tilts causing less than 0.25 pixel deviation: N/2*|sin(a)| < tilt_threshold
    tilt_threshold = 0.25

    def __init__(self, dataset_info, do_flatfield=True, logger=None, autotilt_options=None):
        """
        Initialize a detector tilt estimator helper.

        Parameters
        ----------
        dataset_info: `dataset_info` object
            Data structure with the dataset information.
        do_flatfield: bool, optional
            Whether to perform flat field on radios.
        logger: `Logger` object, optional
            Logger object
        autotilt_options: dict, optional
            named arguments to pass to the detector tilt estimator class.
        """
        self._set_params(dataset_info, do_flatfield, logger, autotilt_options)
        self.radios, self.radios_indices = get_0_180_radios(dataset_info, return_indices=True)
        self._init_flatfield()
        self._apply_flatfield()

    def _set_params(self, dataset_info, do_flatfield, logger, autotilt_options):
        self.dataset_info = dataset_info
        self.do_flatfield = bool(do_flatfield)
        self.logger = LoggerOrPrint(logger)
        self._get_autotilt_options(autotilt_options)

    def _init_flatfield(self):
        if not (self.do_flatfield):
            return
        self.flatfield = FlatFieldDataUrls(
            self.radios.shape,
            flats=self.dataset_info.flats,
            darks=self.dataset_info.darks,
            radios_indices=self.radios_indices,
            interpolation="linear",
            convert_float=True,
        )

    def _apply_flatfield(self):
        if not (self.do_flatfield):
            return
        self.flatfield.normalize_radios(self.radios)

    def _get_autotilt_options(self, autotilt_options):
        if autotilt_options is None:
            self.autotilt_options = None
            return
        try:
            autotilt_options = extract_parameters(autotilt_options)
        except Exception as exc:
            msg = "Could not extract parameters from autotilt_options: %s" % (str(exc))
            self.logger.fatal(msg)
            raise ValueError(msg)
        self.autotilt_options = autotilt_options
        if "threshold" in autotilt_options:
            self.tilt_threshold = autotilt_options.pop("threshold")

    def find_tilt(self, tilt_method=None):
        """
        Find the detector tilt.

        Parameters
        ----------
        tilt_method: str, optional
            Which tilt estimation method to use.
        """
        if tilt_method is None:
            tilt_method = self.default_tilt_method
        check_supported(tilt_method, set(tilt_methods.values()), "tilt estimation method")
        self.logger.info("Estimating detector tilt angle")
        autotilt_params = {
            "roi_yxhw": None,
            "median_filt_shape": None,
            "padding_mode": None,
            "peak_fit_radius": 1,
            "high_pass": None,
            "low_pass": None,
        }
        autotilt_params.update(self.autotilt_options or {})
        self.logger.debug("%s(%s)" % ("CameraTilt", str(autotilt_params)))

        tilt_calc = CameraTilt()
        tilt_cor_position, camera_tilt = tilt_calc.compute_angle(
            self.radios[0], np.fliplr(self.radios[1]), method=tilt_method, **autotilt_params
        )
        self.logger.info("Estimated detector tilt angle: %f degrees" % camera_tilt)
        # Ignore too small tilts
        max_deviation = np.max(self.dataset_info.radio_dims) * np.abs(np.sin(np.deg2rad(camera_tilt)))
        if self.dataset_info.is_halftomo:
            max_deviation *= 2
        if max_deviation < self.tilt_threshold:
            self.logger.info(
                "Estimated tilt angle (%.3f degrees) results in %.2f maximum pixels shift, which is below threshold (%.2f pixel). Ignoring the tilt, no correction will be done."
                % (camera_tilt, max_deviation, self.tilt_threshold)
            )
            camera_tilt = None
        return camera_tilt


# alias
TiltFinder = DetectorTiltEstimator
