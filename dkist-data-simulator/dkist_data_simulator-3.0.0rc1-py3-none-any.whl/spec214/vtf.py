import astropy.units as u
import numpy as np
from astropy.wcs import WCS

from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec214.core import Spec214Dataset


class BaseVTFDataset(Spec214Dataset):
    """
    A base class for VTF datasets.
    """

    def __init__(
        self,
        n_wave,
        n_repeats,
        n_stokes,
        time_delta,
        *,
        linewave,
        detector_shape=(4096, 4096)
    ):

        if not n_wave or not n_repeats:
            raise NotImplementedError(
                "Support for less than 4D VTF datasets is not implemented."
            )

        array_shape = list(detector_shape)

        dataset_shape_rev = list(detector_shape) + [n_wave, n_repeats]
        if n_stokes > 1:
            dataset_shape_rev += [n_stokes]

        super().__init__(
            dataset_shape_rev[::-1],
            array_shape,
            time_delta=time_delta,
            instrument="vtf",
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
        self.add_constant_key("DPNAME3", "scan position")
        self.add_constant_key("DWNAME3", "wavelength")
        self.add_constant_key("DUNIT3", "nm")

        self.add_constant_key("DTYPE4", "TEMPORAL")
        self.add_constant_key("DPNAME4", "scan repeat number")
        self.add_constant_key("DWNAME4", "time")
        self.add_constant_key("DUNIT4", "s")

        if n_stokes > 1:
            self.add_constant_key("DTYPE5", "STOKES")
            self.add_constant_key("DPNAME5", "stokes")
            self.add_constant_key("DWNAME5", "stokes")
            self.add_constant_key("DUNIT5", "")
            self.stokes_file_axis = 0

        self.linewave = linewave
        self.add_constant_key("LINEWAV", linewave.to_value(u.nm))

        # TODO: Check this value is right
        self.plate_scale = 0.012 * u.arcsec / u.pix
        self.n_stokes = n_stokes

    @key_function("FRAMEWAV")
    def framewav(self, key: str):
        """
        Add a random framewav around the line centre
        """
        return self.linewave.to_value(u.nm) - (np.random.random() - 0.5) * 10

    @property
    def non_temporal_file_axes(self):
        if self.n_stokes > 1:
            # This is the index in file shape so third file dimension
            return (0,)
        return super().non_temporal_file_axes


class SimpleVTFDataset(BaseVTFDataset):
    """
    A simple five dimensional VTF dataset with a HPC grid aligned to the pixel axes.
    """

    name = "vtf-simple"

    @property
    def data(self):
        return np.random.random(self.array_shape)

    @property
    def fits_wcs(self):
        if self.array_ndim != 2:
            raise ValueError("VTF dataset generator expects two dimensional FITS WCS.")

        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 0, 0
        w.wcs.cdelt = [self.plate_scale.to_value(u.arcsec / u.pix) for i in range(2)]
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w
