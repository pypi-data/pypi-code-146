import astropy.units as u
import numpy as np
from astropy.wcs import WCS

from .core import Spec214Dataset, TimeVaryingWCSGenerator


class BaseCryoSPDataset(Spec214Dataset):
    """
    A base class for Cryo-NIRSP datasets.
    """

    def __init__(
        self,
        n_maps: int,
        n_steps: int,
        n_stokes: int,
        time_delta: float,
        *,
        linewave: float,
        detector_shape: (int, int) = (1024, 1024),
        slit_width=0.06 * u.arcsec,
        raster_step=None,
    ):
        if n_maps < 1:
            raise ValueError("Having fewer than one map just doesn't make sense.")

        if n_steps <= 1:
            raise NotImplementedError(
                "Support for Cryo SP data with fewer than two raster steps is not supported."
            )

        array_shape = [1] + list(detector_shape)

        dataset_shape_rev = list(detector_shape)[::-1] + [n_steps]
        if n_maps > 1:
            dataset_shape_rev += [n_maps]

        if n_stokes > 1:
            dataset_shape_rev += [n_stokes]

        super().__init__(
            dataset_shape_rev[::-1],
            array_shape,
            time_delta=time_delta,
            instrument="cryonirsp",
        )

        self.add_constant_key("DTYPE1", "SPECTRAL")
        self.add_constant_key("DTYPE2", "SPATIAL")
        self.add_constant_key("DTYPE3", "SPATIAL")
        self.add_constant_key("DPNAME1", "wavelength")
        self.add_constant_key("DPNAME2", "slit position")
        self.add_constant_key("DPNAME3", "raster position")
        self.add_constant_key("DWNAME1", "wavelength")
        self.add_constant_key("DWNAME2", "helioprojective latitude")
        self.add_constant_key("DWNAME3", "helioprojective longitude")
        self.add_constant_key("DUNIT1", "nm")
        self.add_constant_key("DUNIT2", "arcsec")
        self.add_constant_key("DUNIT3", "arcsec")

        next_index = 4
        if n_maps > 1:
            self.add_constant_key(f"DTYPE{next_index}", "TEMPORAL")
            self.add_constant_key(f"DPNAME{next_index}", "scan number")
            self.add_constant_key(f"DWNAME{next_index}", "time")
            self.add_constant_key(f"DUNIT{next_index}", "s")
            next_index += 1

        if n_stokes > 1:
            self.add_constant_key(f"DTYPE{next_index}", "STOKES")
            self.add_constant_key(f"DPNAME{next_index}", "stokes")
            self.add_constant_key(f"DWNAME{next_index}", "stokes")
            self.add_constant_key(f"DUNIT{next_index}", "")
            self.stokes_file_axis = 0

        self.add_constant_key("LINEWAV", linewave.to_value(u.nm))

        self.linewave = linewave

        # TODO: Numbers
        self.plate_scale = 0.06 * u.arcsec / u.pix
        self.spectral_scale = 0.01 * u.nm / u.pix
        self.slit_width = slit_width
        self.n_stokes = n_stokes
        self.n_steps = n_steps
        self.raster_step = raster_step if raster_step is not None else self.slit_width

    def calculate_raster_crpix(self):
        """
        A helper method to calculate the crpix3 value for a frame.

        The CRPIX3 value is used to calculate the offset from the CRVAL3
        reference coordinate.
        Because CDELT3 is the slit width (so that the extent of the dummy axis
        is correct), the value of CRPIX3 will not be an integer when the raster
        step size is not equal to the slit width (an under or over sampled
        raster).
        """
        # These are 0 indexed
        raster_index = self.file_index[-1] * u.pix
        raster_pixel_number = raster_index - (self.n_steps / 2) * u.pix
        angular_offset = self.raster_step * raster_pixel_number
        pixel_offset = angular_offset / self.slit_width

        return 1 + pixel_offset.to_value(u.pix)


class BaseCryoCIDataset(Spec214Dataset):
    """
    A base class for Cryo-NIRSP datasets.
    """

    def __init__(
        self,
        n_maps: int,
        n_steps: int,
        n_stokes: int,
        time_delta: float,
        *,
        linewave: float,
        detector_shape: (int, int) = (2048, 2048),
    ):
        if n_maps < 1:
            raise ValueError("Having fewer than one map just doesn't make sense.")

        if n_steps <= 1:
            raise NotImplementedError(
                "Support for Cryo CI data with fewer than two raster steps is not supported."
            )

        n_time_steps = n_steps * n_maps
        array_shape = tuple(detector_shape)

        dataset_shape_rev = list(detector_shape)[::-1] + [n_time_steps]
        if n_stokes > 1:
            dataset_shape_rev += [n_stokes]

        super().__init__(
            dataset_shape_rev[::-1],
            array_shape,
            time_delta=time_delta,
            instrument="cryonirsp",
        )

        self.add_constant_key("DTYPE1", "SPATIAL")
        self.add_constant_key("DTYPE2", "SPATIAL")
        self.add_constant_key("DTYPE3", "TEMPORAL")
        self.add_constant_key("DPNAME1", "spatial x")
        self.add_constant_key("DPNAME2", "spatial y")
        self.add_constant_key("DPNAME3", "scan number")
        self.add_constant_key("DWNAME1", "helioprojective latitude")
        self.add_constant_key("DWNAME2", "helioprojective longitude")
        self.add_constant_key("DWNAME3", "time")
        self.add_constant_key("DUNIT1", "arcsec")
        self.add_constant_key("DUNIT2", "arcsec")
        self.add_constant_key("DUNIT3", "s")

        if n_stokes > 1:
            self.add_constant_key("DTYPE4", "STOKES")
            self.add_constant_key("DPNAME4", "stokes")
            self.add_constant_key("DWNAME4", "stokes")
            self.add_constant_key("DUNIT4", "")
            self.stokes_file_axis = 0

        self.add_constant_key("LINEWAV", linewave.to_value(u.nm))

        self.linewave = linewave

        # TODO: Numbers
        self.plate_scale = 0.06 * u.arcsec / u.pix
        self.spectral_scale = 0.01 * u.nm / u.pix
        self.slit_width = 0.06 * u.arcsec
        self.n_stokes = n_stokes


class SimpleCryoSPDataset(BaseCryoSPDataset):
    """
    A five dimensional Cryo cube with regular raster spacing.
    """

    name = "cryo-sp-simple"

    @property
    def non_temporal_file_axes(self):
        if self.n_stokes > 1:
            # See above, Stokes is the first axis in dataset_shape
            return (self.stokes_file_axis,)
        return super().non_temporal_file_axes

    @property
    def data(self):
        return np.random.random(self.array_shape)

    @property
    def fits_wcs(self):
        if self.array_ndim != 3:
            raise ValueError(
                "Cryo SP dataset generator expects a three dimensional FITS WCS."
            )

        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = (
            self.array_shape[1] / 2,
            self.array_shape[0] / 2,
            self.file_index[-1] * -1,
        )
        # TODO: linewav is not a good centre point
        w.wcs.crval = self.linewave.to_value(u.nm), 0, 0
        w.wcs.cdelt = (
            self.spectral_scale.to_value(u.nm / u.pix),
            self.plate_scale.to_value(u.arcsec / u.pix),
            self.slit_width.to_value(u.arcsec),
        )
        w.wcs.cunit = "nm", "arcsec", "arcsec"
        w.wcs.ctype = "WAVE", "HPLT-TAN", "HPLN-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w


class SimpleCryoCIDataset(BaseCryoCIDataset):
    """
    A five dimensional Cryo cube with regular raster spacing.
    """

    name = "cryo-ci-simple"

    @property
    def non_temporal_file_axes(self):
        if self.n_stokes > 1:
            # See above, Stokes is the first axis in dataset_shape
            return (self.stokes_file_axis,)
        return super().non_temporal_file_axes

    @property
    def data(self):
        return np.random.random(self.array_shape)

    @property
    def fits_wcs(self):
        if self.array_ndim != 2:
            raise ValueError(
                "Cryo CI dataset generator expects a two dimensional FITS WCS."
            )

        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 0, 0
        w.wcs.cdelt = [self.plate_scale.to_value(u.arcsec / u.pix) for _ in range(2)]
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)

        return w


class TimeDependentCryoSPDataset(SimpleCryoSPDataset):
    """
    A version of the Cryo SP dataset where the CRVAL and PC matrix change with time.
    """

    name = "cryo-sp-time-dependent"

    def __init__(
        self,
        n_maps,
        n_steps,
        n_stokes,
        time_delta,
        *,
        linewave,
        detector_shape=(1024, 1024),
        pointing_shift_rate=10 * u.arcsec / u.s,
        rotation_shift_rate=0.5 * u.deg / u.s,
    ):

        super().__init__(
            n_maps,
            n_steps,
            n_stokes,
            time_delta,
            linewave=linewave,
            detector_shape=detector_shape,
        )

        self.wcs_generator = TimeVaryingWCSGenerator(
            cunit=(u.nm, u.arcsec, u.arcsec),
            ctype=("WAVE", "HPLT-TAN", "HPLN-TAN"),
            crval=(self.linewave.to_value(u.nm), 0, 0),
            rotation_angle=-2 * u.deg,
            crpix=(
                self.array_shape[1] / 2,
                self.array_shape[0] / 2,
                self.calculate_raster_crpix(),
            ),
            cdelt=(
                self.spectral_scale.to_value(u.nm / u.pix),
                self.plate_scale.to_value(u.arcsec / u.pix),
                self.slit_width.to_value(u.arcsec),
            ),
            pointing_shift_rate=u.Quantity([pointing_shift_rate, pointing_shift_rate]),
            rotation_shift_rate=rotation_shift_rate,
            jitter=False,
            static_axes=[0],
        )

    @property
    def fits_wcs(self):
        return self.wcs_generator.generate_wcs(self.time_index * self.time_delta * u.s)


class TimeDependentCryoCIDataset(SimpleCryoCIDataset):
    """
    A version of the Cryo CI dataset where the CRVAL and PC matrix change with time.
    """

    name = "cryo-ci-time-dependent"

    def __init__(
        self,
        n_maps,
        n_steps,
        n_stokes,
        time_delta,
        *,
        linewave,
        detector_shape=(2048, 2048),
        pointing_shift_rate=10 * u.arcsec / u.s,
        rotation_shift_rate=0.5 * u.deg / u.s,
    ):

        super().__init__(
            n_maps,
            n_steps,
            n_stokes,
            time_delta,
            linewave=linewave,
            detector_shape=detector_shape,
        )

        self.wcs_generator = TimeVaryingWCSGenerator(
            cunit=(u.arcsec, u.arcsec),
            ctype=("HPLT-TAN", "HPLN-TAN"),
            crval=(0, 0),
            rotation_angle=-2 * u.deg,
            crpix=(
                self.array_shape[1] / 2,
                self.array_shape[0] / 2,
            ),
            cdelt=(
                self.plate_scale.to_value(u.arcsec / u.pix),
                self.plate_scale.to_value(u.arcsec / u.pix),
            ),
            pointing_shift_rate=u.Quantity([pointing_shift_rate, pointing_shift_rate]),
            rotation_shift_rate=rotation_shift_rate,
            jitter=False,
            static_axes=None,
        )

    @property
    def fits_wcs(self):
        return self.wcs_generator.generate_wcs(self.time_index * self.time_delta * u.s)
