import copy
import datetime
from abc import abstractmethod
from typing import List, Tuple, Literal, Optional
from dataclasses import dataclass

import astropy.units as u
import numpy as np
import numpy.typing as npt
from astropy.coordinates import GCRS, SkyCoord
from astropy.coordinates.matrix_utilities import rotation_matrix
from astropy.time import Time
from astropy.wcs import WCS
from dkist_fits_specifications import spec214
from hashids import Hashids
from scipy.stats import stats
from sunpy.coordinates import HeliographicStonyhurst, sun
from sunpy.util.decorators import cached_property_based_on

from dkist_data_simulator.dataset import Dataset, Omit, key_function
from dkist_data_simulator.schemas import Schema, TimeKey
from dkist_data_simulator.spec122 import KNOWN_INSTRUMENT_TABLES
from dkist_data_simulator.util import location_of_dkist

__all__ = ["Spec214Dataset", "Spec214Schema"]


@dataclass(init=False)
class Spec214Schema(Schema):
    """
    A representation of the 214 schema.
    """

    def __init__(
        self,
        naxis: int,
        dnaxis: int,
        deaxes: int,
        daaxes: int,
        instrument=None,
        random=None,
    ):
        random = random or np.random.default_rng()
        sections = spec214.load_expanded_spec214(
            NAXIS=naxis, DNAXIS=dnaxis, DEAXES=deaxes, DAAXES=daaxes
        )
        sections.pop("compression")
        if instrument:
            if instrument not in KNOWN_INSTRUMENT_TABLES.keys():
                raise ValueError(
                    f"{instrument} does not match one of the known "
                    "instrument table names: {tuple(KNOWN_INSTRUMENT_TABLES.keys())}"
                )
            for table in KNOWN_INSTRUMENT_TABLES.keys():
                if table == instrument:
                    continue
                sections.pop(table)

        super().__init__(self.sections_from_dicts(sections.values(), random=random))


class Spec214Dataset(Dataset):
    """
    Generate a collection of FITS files which form a single dataset
    """

    _subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "name") and cls is not Spec214Dataset:
            Spec214Dataset._subclasses[cls.name] = cls

    def __init__(
        self,
        dataset_shape: Tuple[int, ...],
        array_shape: Tuple[int, ...],
        *,
        time_delta: float,
        start_time: datetime.datetime = None,
        instrument: Literal[tuple(KNOWN_INSTRUMENT_TABLES.keys())] = None,
        swnbin: int = 0,
        hwnbin: int = 0,
        swnroi: int = 0,
        hwnroi: int = 0,
    ):

        # We have to recalculate a bunch of stuff from the super init here to
        # expand the schema before we call the super constructor.
        data_shape = tuple(d for d in array_shape if d != 1)
        super().__init__(
            file_schema=Spec214Schema(
                naxis=len(array_shape),
                dnaxis=len(dataset_shape),
                deaxes=len(dataset_shape) - len(data_shape),
                daaxes=len(data_shape),
                instrument=instrument,
            ),
            dataset_shape=dataset_shape,
            array_shape=array_shape,
        )

        self.time_delta = time_delta
        self.start_time = start_time or datetime.datetime.fromisoformat(
            TimeKey("", False, False).generate_value()
        )

        if instrument:
            self.add_constant_key("INSTRUME", KNOWN_INSTRUMENT_TABLES[instrument])
        else:
            self.add_constant_key("INSTRUME")

        self.exposure_time = datetime.timedelta(seconds=1)

        # FITS
        self.add_constant_key("NAXIS", self.array_ndim)
        self.add_constant_key("ORIGIN", "National Solar Observatory")
        self.add_constant_key("TELESCOP", "Daniel K. Inouye Solar Telescope")
        self.add_constant_key("OBSRVTRY", "Haleakala High Altitude Observatory Site")
        self.add_constant_key("NETWORK", "NSF-DKIST")
        self.add_constant_key("HEADVERS", "pre-release")
        self.add_constant_key("TIMESYS", "UTC")
        self.add_constant_key("PROCTYPE", "L1")
        self.add_constant_key("BUNIT", "ct")

        self.add_constant_key("DSHEALTH", "Good")

        # Camera
        # Binning
        nbin = (swnbin or 1) * (hwnbin or 1)
        self.add_constant_key("NBIN", int(nbin))
        for n in range(1, self.array_ndim + 1):
            self.add_constant_key(f"NBIN{n}", int(np.sqrt(nbin)))

        if hwnbin:
            self.add_constant_key("HWBIN1", int(self.array_shape[1] / np.sqrt(hwnbin)))
            self.add_constant_key("HWBIN2", int(self.array_shape[0] / np.sqrt(hwnbin)))
        else:
            self.add_constant_key("HWBIN1", 1)
            self.add_constant_key("HWBIN2", 1)

        if swnbin:
            self.add_constant_key("SWBIN1", int(self.array_shape[1] / np.sqrt(swnbin)))
            self.add_constant_key("SWBIN2", int(self.array_shape[0] / np.sqrt(swnbin)))
        else:
            self.add_constant_key("SWBIN1", 1)
            self.add_constant_key("SWBIN2", 1)

        self.add_constant_key("SWNROI", swnroi)
        self.add_constant_key("HWNROI", hwnroi)

        # Solarnet
        self.add_constant_key("BTYPE", "phot.count")
        self.add_constant_key("SOLARNET", 1.0)
        self.add_constant_key("EXTNAME", "OBSERVATION")
        self.add_constant_key("INFO_URL", "https://youtu.be/YddwkMJG1Jo")

        # WCS
        self.add_constant_key("WCSNAME", "Helioprojective-cartesian")
        self.add_constant_key("CRDATEn")
        self.add_remove_key("LATPOLE")
        # Which file axis does stokes vary long (Python axis number)
        # if None then it varies along no axis and is always "I".
        self.stokes_file_axis = None

        # Datacenter
        self.add_constant_key("DSETID")
        self.add_constant_key("RRUNID")
        self.add_constant_key("RECIPEID")
        self.add_constant_key("RINSTID")
        self.add_constant_key("PROP_ID")
        self.add_constant_key("EXPER_ID")
        self.add_constant_key("IDSPARID")
        self.add_constant_key("IDSOBSID")
        self.add_constant_key("IDSCALID")
        self.add_constant_key("WKFLNAME")
        self.add_constant_key("WKFLVERS")

        # DKIST-ID
        self.add_constant_key("HLSVERS")
        self.add_constant_key("OBSPR_ID")
        self.add_constant_key("IP_ID")

        # Dataset

        hashids = Hashids()
        dsetid = hashids.encode(self.random.integers(0, 1000000))
        self.add_constant_key("DSETID", dsetid)
        self.add_constant_key("POINT_ID", dsetid)
        self.add_constant_key("DNAXIS", self.dataset_ndim)
        self.add_constant_key("DAAXES", self.data_ndim)
        self.add_constant_key("DEAXES", self.dataset_ndim - self.data_ndim)
        self.add_constant_key("LEVEL", 1)

        # k index keys, which is a subset of d
        for k in range(self.data_ndim + 1, self.dataset_ndim + 1):
            self.add_generator_function(f"DINDEX{k}", type(self).dindex)

        # dtypes need to be generated as a coherent set, so it needs state
        self._dtypes: Optional[List[str]] = None

        # d index keys
        for d in range(1, self.dataset_ndim + 1):
            self.add_generator_function(f"DNAXIS{d}", type(self).dnaxis)
            self.add_generator_function(f"DTYPE{d}", type(self).dtype)
            self.add_generator_function(f"DUNIT{d}", type(self).dunit)
            self.add_constant_key(f"DWNAME{d}")
            self.add_constant_key(f"DPNAME{d}")

    @property
    def data(self):
        return np.empty(self.array_shape)

    ###########################################################################
    # FITS
    ###########################################################################
    @key_function("DATE")
    def date(self, key: str):
        return datetime.datetime.now().isoformat("T")

    @key_function(
        "DATE-BEG",
        "DATE-AVG",
        "DATE-END",
        "DATEREF",
        "TELAPSE",
    )
    def date_obs(self, key: str):
        delta = datetime.timedelta(seconds=self.time_index * self.time_delta)
        frame_start = self.start_time + delta
        frame_end = frame_start + self.exposure_time

        if key in ("DATE-BEG", "DATEREF"):
            ret = frame_start

        if key == "DATE-AVG":
            ret = frame_start + ((frame_end - frame_start) / 2)

        if key == "DATE-END":
            ret = frame_end

        if key == "TELAPSE":
            return (frame_end - frame_start).seconds

        return ret.isoformat("T")

    @property
    def observer(self):
        date_avg = Time(self.date_obs("DATE-AVG"))
        dkist_pos = location_of_dkist
        dkist_itrs = dkist_pos.get_itrs(date_avg)
        dkist_hgs = dkist_pos.get_gcrs(date_avg).transform_to(
            HeliographicStonyhurst(obstime=date_avg)
        )
        return dkist_itrs, dkist_hgs

    @key_function(
        "OBSGEO-X",
        "OBSGEO-Y",
        "OBSGEO-Z",
        "OBS_VR",
    )
    def observer_location(self, key: str):
        dkist_itrs, dkist_hgs = self.observer

        if key.startswith("OBSGEO"):
            attribute = key[-1].lower()
            return getattr(dkist_itrs, attribute).to_value(u.m)

        if key == "OBS_VR":
            return dkist_hgs.velocity.d_z.to_value(u.km / u.s)

    @key_function("NAXISn")
    def naxis(self, key: str):
        fits_ind = int(key[-1])
        ind = self.array_ndim - fits_ind
        return self.array_shape[ind]

    @key_function("NBINn", "NBIN", "SWBIN1", "HWBIN1", "SWBIN2", "HWBIN2")
    def nbin(self, key: str):
        return 1

    @key_function(
        "MAXIS",
        "MAXIS1",
        "MAXIS2",
        "MINDEX1",
        "MINDEX2",
        "VBISTP",
    )
    def moasic_keys(self, key: str):
        """
        These are generated in a method so they are skipped by default but then
        can be overridden.
        """
        return Omit()

    ###########################################################################
    # WCS
    ###########################################################################
    @property
    @abstractmethod
    def fits_wcs(self):
        """
        A FITS WCS object for the current frame.
        """

    @key_function(
        "WCSAXES",
        "CRPIXn",
        "CRVALn",
        "CDELTn",
        "CUNITn",
        "CTYPEn",
    )
    def wcs_keys(self, key: str):
        return self.fits_wcs.to_header()[key]

    @key_function(
        "LONPOLE",
    )
    def wcs_set_keys(self, key: str):
        wcs = copy.deepcopy(self.fits_wcs)
        wcs.wcs.set()
        return wcs.to_header()[key]

    @key_function("PCi_j")
    def pc_keys(self, key: str):
        i = int(key[2]) - 1
        j = int(key[-1]) - 1
        default = self.fits_wcs.wcs.pc[i, j]
        return self.fits_wcs.to_header().get(key, default)

    @key_function("STOKES")
    def stokes(self, key: str):
        if self.stokes_file_axis is None:
            return "I"
        return ["I", "Q", "U", "V"][self.file_index[self.stokes_file_axis]]

    ###########################################################################
    # Camera
    ###########################################################################
    def roi_coords(self, key: str):
        n = int(key[-1]) - 1
        naxisn = self.array_shape[::-1][n]
        if "SIZ" in key:
            return naxisn / self.roin
        if "ORI" in key:
            return naxisn / self.roin * (int(key[3]) - 1)

    ###########################################################################
    # Dataset
    ###########################################################################
    @key_function("FRAMEWAV")
    def framewav(self, key: str):
        """
        Omit framewav unless explicitly added.
        """
        return Omit()

    def dnaxis(self, key: str):
        fits_ind = int(key[-1])
        ind = self.dataset_ndim - fits_ind
        return int(self.dataset_shape[ind])

    def dindex(self, key: str):
        fits_ind = int(key[-1])
        # While not all indices are generated, they count with the d index.
        ind = self.dataset_ndim - fits_ind
        return int(self.file_index[ind])

    def _not_spatial_dtype(self):
        """Generate a random dtype which isn't spatial."""
        dtype = self.file_schema["DTYPE1"].generate_value()
        if dtype == "SPATIAL":
            return self._not_spatial_dtype()
        return dtype

    def dtype(self, key: str):
        """
        Generate a random set of types and then sanitise the number and
        position of any spatial axes.
        """
        wapt_translation = {"pos": "SPATIAL", "em": "SPECTRAL", "time": "TEMPORAL"}

        if self._dtypes is None:
            self._dtypes = []
            for wapt in self.fits_wcs.world_axis_physical_types:
                atype = tuple(filter(lambda x: x[0] in wapt, wapt_translation.items()))[
                    0
                ]
                self._dtypes.append(atype[1])

            if not self._dtypes.count("SPATIAL") == 2:
                raise ValueError(
                    "It is expected the FITS WCS describe both spatial dimensions"
                )

            for _ in range(len(self._dtypes), self.dataset_ndim):
                # Non spatial dtypes shouldn't be duplicated
                # TODO: Make this not terrible
                while True:
                    new_dtype = self._not_spatial_dtype()
                    if new_dtype not in self._dtypes:
                        self._dtypes.append(new_dtype)
                        break

            if "TEMPORAL" not in self._dtypes and "SPECTRAL" in self._dtypes:
                self._dtypes[self._dtypes.index("SPECTRAL")] = "TEMPORAL"

            if "TEMPORAL" not in self._dtypes:
                self._dtypes[self._dtypes.index("STOKES")] = "TEMPORAL"

        return self._dtypes[int(key[-1]) - 1]

    def dunit(self, key: str):
        d = int(key[-1])
        type_unit_map = {
            "SPATIAL": u.arcsec,
            "SPECTRAL": u.nm,
            "TEMPORAL": u.s,
            "STOKES": u.one,
        }
        dtype = self.dtype(f"DTYPE{d}")
        unit = type_unit_map[dtype]
        if unit is not None:
            return unit.to_string(format="fits")

    ###########################################################################
    # Stats
    ###########################################################################

    @key_function(
        "DATAMIN",
        "DATAMAX",
        "DATAMEAN",
        "DATAMEDN",
        "DATARMS",
        "DATAKURT",
        "DATASKEW",
        "DATAPpp",
    )
    def stats(self, key: str):
        if key == "DATAMIN":
            return np.nanmin(self.data)
        if key == "DATAMAX":
            return np.nanmax(self.data)
        if key == "DATAMEAN":
            return np.nanmean(self.data)
        if key == "DATAMEDN":
            return np.nanmedian(self.data)
        if key == "DATARMS":
            rms = np.nanstd(self.data)
            return rms if np.isfinite(rms) else Omit()
        if key == "DATAKURT":
            kurt = stats.kurtosis(self.data, axis=None)
            return kurt if np.isfinite(kurt) else Omit()
        if key == "DATASKEW":
            skew = stats.skew(self.data, axis=None)
            return skew if np.isfinite(skew) else Omit()
        if key.startswith("DATAP"):
            return np.nanpercentile(self.data, int(key[-2:]))


class AOMixin:
    """
    Provide methods to generate values in expected ranges for AO/WFC parameters.

    ATMOS_R0: Fried's parameter. Typical values for DKIST are in the 3-15 cm range. It can exceed those bounds, but not by much.
    AO_LOCK: Lock status. Use True if AO correction is on, False otherwise. You can use False when AO correction is on to represent an anomalous condition, but probably not important.
    AO_LOCKX, AO_LOCKY: Offsetting in x,y for the HOWFS. Any values in +/- 15". Should be the same for all images of a particular observing target.
    WFSLOCKX, WFSLOCKY: Offsetting in x,y for the LOWFS. Same as above.
    LIMBPOS: This is how much we are offsetting the occulter from the limb when observing the limb. Range should be +/- 15"
    LIMBRATE: This should always be 1 kHz
    FLTFWHM: This is the HOWFS filter fwhm, 20 nm.
    WFCLOCK: Same as AO___001 above, but here it is on a per-frame basis and there it is for the duration of the data acquisition. Use 0 to represent an anomolous condition, but 1 is the more likely real value.
    MATRIXID: Use any one of the following: 1600Modes, 1417Modes, 1049Modes, 663Modes, 423Modes, 256Modes, 143Modes, 74Modes, 33Modes, 18Modes, 7Modes, 3Modes. The higher number of modes are the more likely conditions. This varies depending on the seeing conditions. Larger r0 values (Fried's poaram) --> more modes that can be corrected.
    AOLOOPP: This can vary from 0 to some positive value, but 7 is a typical value. This can change from frame to frame, but not by much.
    AOLOOPI: Same as above but use 10 for a typical value.
    FRMRATE: This should always be 1970 Hz except in rare cases for engineering purposes
    FRMLOCK: This is similar to WFC__002 above but for the tip-tilt system. Use values as described above. They don't have to be the same as the WFC_002 values.
    TTLOOPP, TTLOOPI: Similar to 004 and 005 above but use 0.2 and 1 for typical values, respectively."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Assume AO is on and Locked
        self.add_constant_key("AO_LOCK", True)
        self.add_constant_key("WFCLOCK", True)
        self.add_constant_key("FRMLOCK", True)

        # AO_LOCKX, AO_LOCKY: Offsetting in x,y for the HOWFS. Any values in +/- 15".
        # WFSLOCKX, WFSLOCKY: Offsetting in x,y for the LOWFS. Same as above.
        # Should be the same for all images of a particular observing target.
        self.add_constant_key("AO_LOCKX", self._float_in_range(-15, 15))
        self.add_constant_key("AO_LOCKY", self._float_in_range(-15, 15))
        self.add_constant_key("WFSLOCKX", self._float_in_range(-15, 15))
        self.add_constant_key("WFSLOCKY", self._float_in_range(-15, 15))
        # TODO: Check this should be fixed per target
        self.add_constant_key("LIMBRPOS", self._float_in_range(-15, 15))

        self.add_constant_key("LIMBRATE", 1000)
        self.add_constant_key("FLTFWHM", 20)
        self.add_constant_key("FRMRATE", 1970)

    def _float_in_range(self, fmin, fmax):
        return self.random.uniform(fmin, fmax)

    @key_function("ATMOS_R0")
    def fried_param(self, key: str):
        """
        ATMOS_R0: Fried's parameter. Typical values for DKIST are in the
        3-15 cm range. It can exceed those bounds, but not by much.
        """
        return self._float_in_range(3, 15)

    @key_function("MATRIXID")
    def matrix_modes(self, key: str):
        values = [
            "1600Modes",
            "1417Modes",
            "1049Modes",
            "663Modes",
            "423Modes",
            "256Modes",
            "143Modes",
            "74Modes",
            "33Modes",
            "18Modes",
            "7Modes",
            "3Modes",
        ]
        return self.random.choice(values)

    @key_function("AOLOOPP")
    def aoloopp(self, key: str):
        return np.max(self.random.normal(7, 1), 0)

    @key_function("AOLOOPI")
    def aoloopi(self, key: str):
        return np.max(self.random.normal(10, 1), 0)

    @key_function("TTLOOPP")
    def ttloopp(self, key: str):
        return np.max(self.random.normal(0.2, 0.02), 0)

    @key_function("TTLOOPI")
    def ttloopi(self, key: str):
        return np.max(self.random.normal(1, 0.1), 0)


class WCSAMixin:
    """
    Add non-random keys for the alternative WCS based on the coordinates of the primary WCS.

    This takes a noticeable amount of time to compute per frame so it is opt-in.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_constant_key("WCSNAMEA", "Equatorial equinox J2000")
        self.add_remove_key("LATPOLEA")
        self.add_constant_key("CRDATEnA")

    @property
    @cached_property_based_on("index")
    def fits_wcs_a(self):
        """
        This property takes in the `fits_wcs` property and attempts to build a
        mostly accurate Equatorial WCS from the HPC one.
        """
        new_wcs = copy.deepcopy(self.fits_wcs)
        lat_ind = [
            i for i, ctype in enumerate(new_wcs.wcs.ctype) if ctype.startswith("HPLT")
        ][0]
        lon_ind = [
            i for i, ctype in enumerate(new_wcs.wcs.ctype) if ctype.startswith("HPLN")
        ][0]

        ctype = list(new_wcs.wcs.ctype)
        ctype[lon_ind] = "DEC--TAN"
        ctype[lat_ind] = "RA---TAN"

        crpix = [new_wcs.wcs.crpix[i] for i in sorted([lon_ind, lat_ind])]
        hpc_ref = SkyCoord.from_pixel(*crpix, wcs=new_wcs, mode="wcs", origin=1)
        hpc_ref = hpc_ref.replicate(observer=self.observer[1])
        gcrs_frame = GCRS(obsgeoloc=self.observer[0].cartesian, obstime=hpc_ref.obstime)

        # TODO: if we ever want to simulate data with an off-disk reference
        # point we will need to fix this:
        # with Helioprojective.assume_spherical_screen(self.observer[1], only_off_disk=True):
        gcrs = hpc_ref.transform_to(gcrs_frame)

        crval = list(new_wcs.wcs.crval)
        crval[lat_ind] = gcrs.ra.to_value(u.deg)
        crval[lon_ind] = gcrs.dec.to_value(u.deg)

        cunit = list(new_wcs.wcs.cunit)
        cunit[lat_ind] = "deg"
        cunit[lon_ind] = "deg"

        inds = tuple(sorted([lon_ind, lat_ind]))
        index = ((inds, inds), (inds, inds))
        pc = new_wcs.wcs.pc[index]
        new_pc = pc @ rotation_matrix(-1 * sun.P(hpc_ref.obstime))[:2, :2]
        new_wcs.wcs.pc[index] = new_pc

        new_wcs.wcs.ctype = ctype
        new_wcs.wcs.crval = crval
        new_wcs.wcs.cunit = cunit
        new_wcs.wcs.crpix = crpix

        return new_wcs

    @key_function(
        "WCSAXESA",
        "CRPIXnA",
        "CRVALnA",
        "CDELTnA",
        "CUNITnA",
        "CTYPEnA",
    )
    def wcs_keys_a(self, key: str):
        return self.fits_wcs_a.to_header()[key[:-1]]

    @key_function(
        "LONPOLEA",
    )
    def wcs_set_keys_a(self, key: str):
        wcs = copy.deepcopy(self.fits_wcs_a)
        wcs.wcs.set()
        return wcs.to_header()[key[:-1]]

    @key_function("PCi_jA")
    def pc_keys_a(self, key: str):
        key = key[:-1]
        i = self.array_ndim - int(key[2])
        j = self.array_ndim - int(key[-1])
        default = self.fits_wcs_a.wcs.pc[j, i]
        return self.fits_wcs_a.to_header().get(key, default)

    @key_function("SPECSYSA", "VELOSYSA")
    def specsys(self, key: str):
        if key.startswith("SPECSYS"):
            return "TOPOCENT"
        if key.startswith("VELOSYS"):
            return 0


@dataclass
class TimeVaryingWCSGenerator:
    """
    This class can be used to generate a spatial `~astropy.wcs.WCS` which
    varies with time.

    The CRVAL and PC matrix vary with time all other parameters are fixed.
    """

    crval: npt.ArrayLike  # naxis long
    """Initial value of the reference coordinate."""

    rotation_angle: u.Quantity  # scalar
    """Initial value of the rotation angle."""

    crpix: npt.ArrayLike  # naxis long
    """The reference pixel."""

    cdelt: npt.ArrayLike  # naxis long
    """The plate scale."""

    pointing_shift_rate: u.Quantity  # naxis long, u.deg / u.s
    """The rate at which the pointing should shift."""

    rotation_shift_rate: u.Quantity  # scalar, u.deg / u.s
    """The rate at which the rotation matrix should change."""

    cunit: Tuple[str, ...] = ("arcsec", "arcsec")
    """The units for the WCS axes."""

    ctype: Tuple[str, ...] = ("HPLN-TAN", "HPLT-TAN")
    """The types of the WCS axes."""

    jitter: bool = False
    """
    If `True` the rate of change will randomly change.

    Leading to a non-linear, but monotonic, change.
    """

    static_axes: Tuple[int, ...] = None
    """Any axes in the WCS which do not vary."""

    @property
    def constant_wcs(self):
        naxis = len(self.crpix)
        w = WCS(naxis=naxis)
        w.wcs.crpix = self.crpix
        w.wcs.cdelt = self.cdelt
        w.wcs.cunit = self.cunit
        w.wcs.ctype = self.ctype
        w.wcs.crval = self.crval
        w.wcs.pc = np.identity(naxis)
        return w

    @property
    def random_jitter(self):
        if not self.jitter:
            return 1
        return np.random.random_sample()

    @property
    def varying_axes(self):
        static_axes = self.static_axes or []
        return np.array([i for i in range(len(self.crpix)) if i not in static_axes])

    def generate_wcs(self, dt: u.s):
        """
        Generate the WCS based on the time offset.
        """
        w = self.constant_wcs

        pointing_shift_rate = self.random_jitter * self.pointing_shift_rate
        crval_cunit_zip = [[self.crval[i], self.cunit[i]] for i in self.varying_axes]
        new_crval = [u.Quantity(cv, unit=cu) for cv, cu in crval_cunit_zip]
        new_crval = u.Quantity(
            [cv + (psr * dt) for cv, psr in zip(new_crval, pointing_shift_rate)]
        )

        rotation_shift_rate = self.random_jitter * self.rotation_shift_rate
        rotation_angle = self.rotation_angle + rotation_shift_rate * dt

        crval = np.array(w.wcs.crval)
        crval[self.varying_axes] = new_crval.value
        w.wcs.crval = crval

        pc = np.array(w.wcs.pc)
        celestial_pc = rotation_matrix(rotation_angle)[:2, :2]
        # TODO: Use numpy indexing here not this travesty
        for x, i in enumerate(self.varying_axes):
            for y, j in enumerate(self.varying_axes):
                pc[i, j] = celestial_pc[x, y]
        w.wcs.pc = pc

        return w
