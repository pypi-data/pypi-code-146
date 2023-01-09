import os
import numpy as np
from silx.io import get_data
from silx.io.url import DataUrl
from tomoscan.esrf.scan.edfscan import EDFTomoScan
from tomoscan.esrf.scan.hdf5scan import HDF5TomoScan

from ..utils import check_supported
from ..io.utils import get_compacted_dataslices
from .utils import is_hdf5_extension, get_values_from_file
from .logger import LoggerOrPrint

# Wait for next tomoscan release to ship "nexus_version"
from packaging.version import parse as parse_version
from tomoscan.version import version as tomoscan_version

_tomoscan_has_nxversion = parse_version(tomoscan_version) > parse_version("0.6.0")
#


class DatasetAnalyzer:

    _scanner = None
    kind = "none"

    """
    Base class for datasets analyzers.
    """

    def __init__(self, location, extra_options=None, logger=None):
        """
        Initialize a Dataset analyzer.

        Parameters
        ----------
        location: str
            Dataset location (directory or file name)
        extra_options: dict, optional
            Extra options on how to interpret the dataset.
        logger: logging object, optional
            Logger. If not set, messages will just be printed in stdout.
        """
        self.logger = LoggerOrPrint(logger)
        self.location = location
        self._set_extra_options(extra_options)
        self._get_excluded_projections()
        self._set_default_dataset_values()
        self._init_dataset_scan()
        self._finish_init()

    def _set_extra_options(self, extra_options):
        if extra_options is None:
            extra_options = {}
        # COMPAT.
        advanced_options = {
            "force_flatfield": False,
            "output_dir": None,
            "exclude_projections": None,
            "hdf5_entry": None,
        }
        if _tomoscan_has_nxversion:
            advanced_options["nx_version"] = 1.0
        # --
        advanced_options.update(extra_options)
        self.extra_options = advanced_options

    def _get_excluded_projections(self):
        excluded_projs = self.extra_options["exclude_projections"]
        if excluded_projs is None:
            return
        projs_idx = get_values_from_file(excluded_projs, any_size=True).astype(np.int32).tolist()
        self.logger.info("Ignoring projections: %s" % (str(projs_idx)))
        self.extra_options["exclude_projections"] = projs_idx

    def _init_dataset_scan(self, **kwargs):
        if self._scanner is None:
            raise ValueError("Base class")
        if self._scanner is HDF5TomoScan:
            if self.extra_options.get("hdf5_entry", None) is not None:
                kwargs["entry"] = self.extra_options["hdf5_entry"]
            if self.extra_options.get("nx_version", None) is not None:
                kwargs["nx_version"] = self.extra_options["nx_version"]
        if self._scanner is EDFTomoScan:
            # Assume 1 frame per file (otherwise too long to open each file)
            kwargs["n_frames"] = 1
        self.dataset_scanner = self._scanner(  # pylint: disable=E1102
            self.location, ignore_projections=self.extra_options["exclude_projections"], **kwargs
        )
        self.projections = self.dataset_scanner.projections
        self.flats = self.dataset_scanner.flats
        self.darks = self.dataset_scanner.darks
        self.n_angles = len(self.dataset_scanner.projections)
        self.radio_dims = (self.dataset_scanner.dim_1, self.dataset_scanner.dim_2)
        self._radio_dims_notbinned = self.radio_dims  # COMPAT

    def _finish_init(self):
        pass

    def _set_default_dataset_values(self):
        self._detector_tilt = None
        self.translations = None
        self.ctf_translations = None
        self.axis_position = None
        self._rotation_angles = None
        self.z_per_proj = None
        self.x_per_proj = None
        self._energy = None
        self._pixel_size = None
        self._distance = None
        self.flats_srcurrent = None

    @property
    def energy(self):
        """
        Return the energy in kev.
        """
        if self._energy is None:
            self._energy = self.dataset_scanner.energy
        return self._energy

    @energy.setter
    def energy(self, val):
        self._energy = val

    @property
    def distance(self):
        """
        Return the sample-detector distance in meters.
        """
        if self._distance is None:
            self._distance = abs(self.dataset_scanner.distance)
        return self._distance

    @distance.setter
    def distance(self, val):
        self._distance = val

    @property
    def pixel_size(self):
        """
        Return the pixel size in microns.
        """
        # TODO X and Y pixel size
        if self._pixel_size is None:
            self._pixel_size = self.dataset_scanner.pixel_size * 1e6
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, val):
        self._pixel_size = val

    def _get_rotation_angles(self):
        return self._rotation_angles  # None by default

    @property
    def rotation_angles(self):
        """
        Return the rotation angles in radians.
        """
        return self._get_rotation_angles()

    @rotation_angles.setter
    def rotation_angles(self, angles):
        self._rotation_angles = angles

    def _is_halftomo(self):
        return None  # base class

    @property
    def is_halftomo(self):
        """
        Indicates whether the current dataset was performed with half acquisition.
        """
        return self._is_halftomo()

    @property
    def detector_tilt(self):
        """
        Return the detector tilt in degrees
        """
        return self._detector_tilt

    @detector_tilt.setter
    def detector_tilt(self, tilt):
        self._detector_tilt = tilt

    @property
    def projections_srcurrent(self):
        """
        Return the synchrotron electric current for each projection.
        """
        srcurrent = self.dataset_scanner.electric_current
        if srcurrent is None or len(srcurrent) == 0:
            return None
        srcurrent_all = np.array(srcurrent)
        projections_indices = np.array(sorted(self.projections.keys()))
        if np.any(projections_indices >= len(srcurrent_all)):
            self.logger.error("Something wrong with SRCurrent: not enough values!")
            return None
        return srcurrent_all[projections_indices].astype("f")

    def check_defined_attribute(self, name, error_msg=None):
        """
        Utility function to check that a given attribute is defined.
        """
        if getattr(self, name, None) is None:
            raise ValueError(error_msg or str("No information on %s was found in the dataset" % name))


class EDFDatasetAnalyzer(DatasetAnalyzer):
    """
    EDF Dataset analyzer for legacy ESRF acquisitions
    """

    _scanner = EDFTomoScan
    kind = "edf"

    def _finish_init(self):
        self.remove_unused_radios()

    def remove_unused_radios(self):
        """
        Remove "unused" radios.
        This is used for legacy ESRF scans.
        """
        # Extraneous projections are assumed to be on the end
        projs_indices = sorted(self.projections.keys())
        used_radios_range = range(projs_indices[0], len(self.projections))
        radios_not_used = []
        for idx in self.projections.keys():
            if idx not in used_radios_range:
                radios_not_used.append(idx)
        for idx in radios_not_used:
            self.projections.pop(idx)
        return radios_not_used

    def _get_flats_darks(self):
        return

    @property
    def hdf5_entry(self):
        """
        Return the HDF5 entry of the current dataset.
        Not applicable for EDF (return None)
        """
        return None

    def _is_halftomo(self):
        return None


class HDF5DatasetAnalyzer(DatasetAnalyzer):
    """
    HDF5 dataset analyzer
    """

    _scanner = HDF5TomoScan
    kind = "hdf5"

    @property
    def z_translation(self):
        raw_data = np.array(self.dataset_scanner.z_translation)
        projs_idx = np.array(list(self.projections.keys()))
        filtered_data = raw_data[projs_idx]
        return 1.0e6 * filtered_data / self.pixel_size

    @property
    def x_translation(self):
        raw_data = np.array(self.dataset_scanner.x_translation)
        projs_idx = np.array(list(self.projections.keys()))
        filtered_data = raw_data[projs_idx]
        return 1.0e6 * filtered_data / self.pixel_size

    def _get_rotation_angles(self):
        if self._rotation_angles is None:
            angles = np.array(self.dataset_scanner.rotation_angle)
            projs_idx = np.array(list(self.projections.keys()))
            angles = angles[projs_idx]
            self._rotation_angles = np.deg2rad(angles)
        return self._rotation_angles

    def _get_dataset_hdf5_url(self):
        if len(self.projections) > 0:
            frames_to_take = self.projections
        elif len(self.flats) > 0:
            frames_to_take = self.flats
        elif len(self.darks) > 0:
            frames_to_take = self.darks
        else:
            raise ValueError("No projections, no flats and no darks ?!")
        first_proj_idx = sorted(frames_to_take.keys())[0]
        first_proj_url = frames_to_take[first_proj_idx]
        return DataUrl(
            file_path=first_proj_url.file_path(), data_path=first_proj_url.data_path(), data_slice=None, scheme="silx"
        )

    @property
    def dataset_hdf5_url(self):
        return self._get_dataset_hdf5_url()

    @property
    def hdf5_entry(self):
        """
        Return the HDF5 entry of the current dataset
        """
        return self.dataset_scanner.entry

    def _is_halftomo(self):
        try:
            is_halftomo = self.dataset_scanner.field_of_view.value.lower() == "half"
        except:
            is_halftomo = None
        return is_halftomo

    def get_data_slices(self, what):
        """
        Return indices in the data volume where images correspond to a given kind.

        Parameters
        ----------
        what: str
            Which keys to get. Can be "projections", "flats", "darks"

        Returns
        --------
        slices: list of slice
            A list where each item is a slice.
        """
        check_supported(what, ["projections", "flats", "darks"], "image type")
        images = getattr(self, what)  # dict
        # we can't directly use set() on slice() object (unhashable). Use tuples
        slices = set()
        for du in get_compacted_dataslices(images).values():
            if du.data_slice() is not None:
                s = (du.data_slice().start, du.data_slice().stop)
            else:
                s = None
            slices.add(s)
        slices_list = [slice(item[0], item[1]) if item is not None else None for item in list(slices)]
        return slices_list


def analyze_dataset(dataset_path, extra_options=None, logger=None):
    if not (os.path.isdir(dataset_path)):
        if not (os.path.isfile(dataset_path)):
            raise ValueError("Error: %s no such file or directory" % dataset_path)
        if not (is_hdf5_extension(os.path.splitext(dataset_path)[-1].replace(".", ""))):
            raise ValueError("Error: expected a HDF5 file")
        dataset_analyzer_class = HDF5DatasetAnalyzer
    else:  # directory -> assuming EDF
        dataset_analyzer_class = EDFDatasetAnalyzer
    dataset_structure = dataset_analyzer_class(dataset_path, extra_options=extra_options, logger=logger)
    return dataset_structure


def get_0_180_radios(dataset_info, return_indices=False):
    """
    Get the radios at 0 degres and 180 degrees.

    Parameters
    ----------
    dataset_info: `DatasetAnalyzer` instance
        Data structure with the dataset information
    return_indices: bool, optional
        Whether to return radios indices along with the radios array.

    Returns
    -------
    res: array or tuple
        If return_indices is True, return a tuple (radios, indices).
        Otherwise, return an array with the radios.
    """
    radios_indices = []
    radios_indices = sorted(dataset_info.projections.keys())
    angles = dataset_info.rotation_angles
    angles = angles - angles.min()
    i_0 = np.argmin(np.abs(angles))
    i_180 = np.argmin(np.abs(angles - np.pi))
    _min_indices = [i_0, i_180]
    radios_indices = [radios_indices[i_0], radios_indices[i_180]]
    n_radios = 2
    radios = np.zeros((n_radios,) + dataset_info.radio_dims[::-1], "f")
    for i in range(n_radios):
        radio_idx = radios_indices[i]
        radios[i] = get_data(dataset_info.projections[radio_idx]).astype("f")
    if return_indices:
        return radios, radios_indices
    else:
        return radios
