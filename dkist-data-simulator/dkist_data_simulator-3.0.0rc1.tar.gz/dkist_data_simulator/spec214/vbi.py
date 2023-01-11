from typing import Literal

import astropy.units as u
import numpy as np
from astropy.wcs import WCS
from sunpy.util.decorators import cached_property_based_on

from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec214.core import Spec214Dataset, TimeVaryingWCSGenerator


class BaseVBIDataset(Spec214Dataset):
    """
    A base class for VBI datasets.
    """

    def __init__(
        self,
        n_time,
        time_delta,
        *,
        linewave,
        detector_shape=(4096, 4096),
        vbi_camera: Literal["red", "blue"] = "red",
        mosaic: bool = False
    ):

        if vbi_camera.lower() not in ["red", "blue"]:
            raise ValueError("vbi_camera must either be 'red' or 'blue'")

        if vbi_camera.lower() == "blue":
            n_pos = 9
            self.plate_scale = 0.011 * u.arcsec / u.pix
        else:
            n_pos = 4
            self.plate_scale = 0.0169 * u.arcsec / u.pix

        if not mosaic:
            n_pos = 1

        self.mosaic = mosaic
        self.n_pos = n_pos

        array_shape = tuple(detector_shape)
        dataset_shape_rev = (*detector_shape, n_time)

        super().__init__(
            dataset_shape_rev[::-1],
            array_shape,
            time_delta=time_delta,
            instrument="vbi",
        )
        self.files_shape = (*self.files_shape, n_pos)
        self.files_ndim = len(self.files_shape)
        self.n_files = int(np.product(self.files_shape))

        self.add_constant_key("DTYPE1", "SPATIAL")
        self.add_constant_key("DTYPE2", "SPATIAL")
        self.add_constant_key("DTYPE3", "TEMPORAL")
        self.add_constant_key("DPNAME1", "spatial x")
        self.add_constant_key("DPNAME2", "spatial y")
        self.add_constant_key("DPNAME3", "frame number")
        self.add_constant_key("DWNAME1", "helioprojective longitude")
        self.add_constant_key("DWNAME2", "helioprojective latitude")
        self.add_constant_key("DWNAME3", "time")
        self.add_constant_key("DUNIT1", "arcsec")
        self.add_constant_key("DUNIT2", "arcsec")
        self.add_constant_key("DUNIT3", "s")
        self.add_constant_key("LINEWAV", linewave.to_value(u.nm))

    @property
    def current_camera_pos(self) -> int:
        return self.file_index[1] + 1

    @property
    def current_dsps_repeat(self) -> int:
        return self.file_index[0]

    @property
    def data(self):
        return np.random.random(self.array_shape)


class SimpleVBIDataset(BaseVBIDataset):
    """
    A simple VBI dataset with a HPC grid aligned to the pixel axes.
    """

    name = "vbi-simple"

    def __init__(
        self,
        n_time,
        time_delta,
        *,
        linewave,
        detector_shape=(4096, 4096),
        vbi_camera: Literal["red", "blue"] = "red"
    ):
        super().__init__(
            n_time,
            time_delta,
            linewave=linewave,
            detector_shape=detector_shape,
            vbi_camera=vbi_camera,
            mosaic=False,
        )

    @property
    def fits_wcs(self):
        if self.array_ndim != 2:
            raise ValueError("VBI dataset generator expects two dimensional FITS WCS.")

        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 0, 0
        w.wcs.cdelt = [self.plate_scale.to_value(u.arcsec / u.pix) for i in range(2)]
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w


class MosaicedVBIBlueDataset(BaseVBIDataset):
    """
    A mosaik'd VBI-BLUE dataset with real WCS values.
    """

    name = "vbi-mosaic-blue"

    def __init__(self, n_time, time_delta, *, linewave, detector_shape=(4096, 4096)):
        super().__init__(
            n_time,
            time_delta,
            linewave=linewave,
            vbi_camera="blue",
            mosaic=True,
            detector_shape=detector_shape,
        )

        self.add_constant_key("VBISTPAT", "5, 6, 3, 2, 1, 4, 7, 9")

        # Kind of nasty to hardcode this, but whatever
        # Taken from Blue data taken on May 11th, 2021
        self.CRVALs_by_position = {
            1: (-0.008249197036196473, -0.0006135090889007315),
            2: (-0.002317657297546805, -0.0001723610794093499),
            3: (-0.00628512107866833, -0.0004674396171848149),
            4: (-0.004281763497165903, -0.0003184451268690273),
            5: (-0.004281746141954696, -0.0003184443597246071),
            6: (-0.004321040295000408, -0.0003213684050815774),
            7: (-0.0003535952015734776, -2.629428697388573e-05),
            8: (-0.002356942994829349, -0.0001752814836928538),
            9: (-0.006245898142674184, -0.0004645083011308958),
        }
        self.CRPIXs_by_position = {
            1: (4271.916665454963, 4156.592392327204),  # M, M
            2: (880.2500395909186, 4156.592392327204),  # L, M
            3: (880.250039438403, 756.5922702407024),  # L, B
            4: (4271.916665454963, 756.5922702299208),  # M, B
            5: (7663.583169381011, 756.5922702423875),  # R, B
            6: (7663.583169379749, 4156.592392309716),  # R, M
            7: (7663.583169508412, 7556.592392317916),  # R, T
            8: (4271.916665575761, 7556.592392330609),  # M, T
            9: (880.250039413763, 7556.5923923026385),  # L, T
        }

    @property
    @cached_property_based_on("index")
    def fits_wcs(self) -> WCS:
        w = WCS(naxis=self.array_ndim)
        w.wcs.crpix = self.CRPIXs_by_position[self.current_camera_pos]
        w.wcs.crval = self.CRVALs_by_position[self.current_camera_pos]
        w.wcs.cdelt = [self.plate_scale.to_value(u.arcsec / u.pix) for _ in range(2)]
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w

    @key_function(
        "MAXIS",
        "MAXIS1",
        "MAXIS2",
        "MINDEX1",
        "MINDEX2",
        "VBISTP",
    )
    def moasic_keys(self, key: str):
        axis_length = 3
        if key == "VBISTP":
            return int(self.current_camera_pos)
        if key == "MINDEX1":
            return int((self.current_camera_pos - 1) % axis_length + 1)
        if key == "MINDEX2":
            return int((self.current_camera_pos - 1) // axis_length + 1)

        constant_keys = {
            "MAXIS": 2,
            "MAXIS1": 3,
            "MAXIS2": 3,
        }
        return constant_keys.get(key, super().moasic_keys(key))


class TimeDependentVBIDataset(SimpleVBIDataset):
    """
    A version of the VBI dataset where the CRVAL and PC matrix change with time.
    """

    name = "vbi-time-dependent"

    def __init__(
        self,
        n_time,
        time_delta,
        *,
        linewave,
        pointing_shift_rate=10 * u.arcsec / u.s,
        rotation_shift_rate=0.5 * u.deg / u.s,
        **kwargs
    ):
        super().__init__(n_time, time_delta, linewave=linewave, **kwargs)

        self.wcs_generator = TimeVaryingWCSGenerator(
            crval=(0, 0),
            rotation_angle=-2 * u.deg,
            crpix=(self.array_shape[1] / 2, self.array_shape[0] / 2),
            cdelt=[self.plate_scale.to_value(u.arcsec / u.pix) for i in range(2)],
            pointing_shift_rate=u.Quantity([pointing_shift_rate, pointing_shift_rate]),
            rotation_shift_rate=rotation_shift_rate,
            jitter=False,
        )

    @property
    def fits_wcs(self):
        return self.wcs_generator.generate_wcs(self.time_index * self.time_delta * u.s)
