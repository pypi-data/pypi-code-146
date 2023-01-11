"""
This file generates a 5D VTF-like dataset using observations from the CRISP instrument on the SST.
"""
import astropy.units as u
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec214.core import AOMixin, WCSAMixin
from dkist_data_simulator.spec214.vtf import BaseVTFDataset


class VTFCRISP5DDataset(WCSAMixin, AOMixin, BaseVTFDataset):
    """
    A simple five dimensional VTF dataset with a HPC grid aligned to the pixel axes.
    """

    name = "vtf-crisp-5d"

    def __init__(self, data_file=None, n_wave=19, n_repeats=128, n_stokes=4):
        self.data_file = data_file
        self.hdul = None
        if data_file:
            self.hdul = fits.open(self.data_file)

        self.dataset_shape = (n_stokes, n_repeats, n_wave, 980 - 80, 966 - 80)

        # Validate we have a file which is big enough
        if np.any(
            np.array(self.dataset_shape)
            > np.array(self.hdul[0].data.shape)[[1, 0, 2, 3, 4]]
        ):
            raise ValueError(
                "The file specified has a shape too small for the requested dataset shape"
            )

        time_delta = 3
        self.linewave = 854.2 * u.nm
        self.framewave_start = 854.1 * u.nm
        self.framewave_delta = 0.105 * u.AA

        super().__init__(
            n_wave,
            n_repeats,
            n_stokes,
            time_delta,
            linewave=self.linewave,
            detector_shape=self.dataset_shape[-2:],
        )

        self.add_constant_key("WAVEMIN", self.framewave_start.to_value(u.nm))
        self.add_constant_key(
            "WAVEMAX",
            (self.framewave_start + (n_wave * self.framewave_delta)).to_value(u.nm),
        )
        self.add_constant_key("WAVEBAND", "CA II")

        self.add_constant_key("ROTCOMP", "On")

        self.plate_scale = 0.12 * u.arcsec / u.pix

    def __del__(self):
        if self.hdul:
            self.hdul.close()

    @property
    def data(self):
        if not self.data_file:
            return super().data

        fi = self.file_index
        array_index = (fi[1], fi[0], fi[2])
        return self.hdul[0].data[array_index][40:-40, 40:-40]

    @property
    def fits_wcs(self):
        if self.array_ndim != 2:
            raise ValueError("VTF dataset generator expects two dimensional FITS WCS.")

        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 0, 0
        w.wcs.cdelt = [self.plate_scale.to_value(u.arcsec / u.pix) for _ in range(2)]
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        w.wcs.dateobs = self.date_obs("DATE-AVG")

        obsgeo, _ = self.observer
        w.wcs.obsgeo = [
            obsgeo.x.to_value(u.m),
            obsgeo.y.to_value(u.m),
            obsgeo.z.to_value(u.m),
            0,
            0,
            0,
        ]

        return w

    @key_function("FRAMEWAV")
    def FRAMEWAV(self, key: str):
        wave_offset = self.framewave_delta * self.file_index[2]
        return (self.framewave_start + wave_offset).to_value(u.nm)

    @key_function("STOKES")
    def STOKES(self, key: str):
        return ["I", "Q", "U", "V"][self.file_index[0]]
