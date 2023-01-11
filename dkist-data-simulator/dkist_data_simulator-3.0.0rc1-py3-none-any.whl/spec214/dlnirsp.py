import astropy.units as u
import numpy as np
from astropy.wcs import WCS

from .core import Spec214Dataset


class BaseDLNIRSPDataset(Spec214Dataset):
    """
    A base class for DL-NIRSP datasets.
    """

    def __init__(
        self,
        n_exposures,
        n_stokes,
        time_delta,
        *,
        linewave,
        array_shape=(100, 100, 100)
    ):

        if not n_exposures:
            raise NotImplementedError(
                "Support for less than 4D DLNIRSP datasets is not implemented."
            )

        array_shape = list(array_shape)

        dataset_shape_rev = list(array_shape) + [n_exposures]
        if n_stokes > 1:
            dataset_shape_rev += [n_stokes]

        super().__init__(
            dataset_shape_rev[::-1],
            array_shape,
            time_delta=time_delta,
            instrument="dlnirsp",
        )

        self.add_constant_key("DTYPE1", "SPATIAL")
        self.add_constant_key("DPNAME1", "spatial x")
        self.add_constant_key("DWNAME1", "helioprojective longitude")
        self.add_constant_key("DUNIT1", "arcsec")

        self.add_constant_key("DTYPE2", "SPATIAL")
        self.add_constant_key("DPNAME2", "spatial y")
        self.add_constant_key("DWNAME2", "helioprojective latitude")
        self.add_constant_key("DUNIT2", "arcsec")

        self.add_constant_key("DTYPE3", "SPECTRAL")
        self.add_constant_key("DPNAME3", "wavelength")
        self.add_constant_key("DWNAME3", "wavelength")
        self.add_constant_key("DUNIT3", "nm")

        self.add_constant_key("DTYPE4", "TEMPORAL")
        self.add_constant_key("DPNAME4", "exposure number")
        self.add_constant_key("DWNAME4", "time")
        self.add_constant_key("DUNIT4", "s")

        if n_stokes > 1:
            self.add_constant_key("DTYPE5", "STOKES")
            self.add_constant_key("DPNAME5", "stokes")
            self.add_constant_key("DWNAME5", "stokes")
            self.add_constant_key("DUNIT5", "")
            self.stokes_file_axis = 0

        self.add_constant_key("LINEWAV", linewave.to_value(u.nm))

        # TODO: What is this value??
        self.plate_scale = (
            10 * u.arcsec / u.pix,
            10 * u.arcsec / u.pix,
            1 * u.nm / u.pix,
        )
        self.n_stokes = n_stokes


class SimpleDLNIRSPDataset(BaseDLNIRSPDataset):
    """
    A simple five dimensional DLNIRSP dataset with a HPC grid aligned to the pixel axes.
    """

    name = "dlnirsp-simple"

    @property
    def non_temporal_file_axes(self):
        if self.n_stokes > 1:
            # This is the index in file shape so third file dimension
            return (0,)
        return super().non_temporal_file_axes

    @property
    def data(self):
        return np.random.random(self.array_shape)

    @property
    def fits_wcs(self):
        if self.array_ndim != 3:
            raise ValueError(
                "DLNIRSP dataset generator expects a three dimensional FITS WCS."
            )

        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = (
            self.array_shape[2] / 2,
            self.array_shape[1] / 2,
            self.array_shape[0] / 2,
        )
        w.wcs.crval = 0, 0, 0
        w.wcs.cdelt = [self.plate_scale[i].value for i in range(self.array_ndim)]
        w.wcs.cunit = "arcsec", "arcsec", "nm"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN", "WAVE"
        w.wcs.pc = np.identity(self.array_ndim)
        return w
