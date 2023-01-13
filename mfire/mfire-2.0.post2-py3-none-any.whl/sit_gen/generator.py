from functools import cached_property
from typing import Any, Optional

import numpy as np
import xarray as xr
from tensorflow.python.keras.utils.data_utils import Sequence

__all__ = ["DataGenerator"]


class DataGenerator(Sequence):
    """
    Genere des batchs de données pour un réseau de neurones à partir d'un
    dataarray fourni en entrée.

    Après initialisation, le dataarray en entrée a la structure suivante:
    >>> my_generator.data
    <xarray.DataArray 'super_set' (valid_time: 8, latitude: 118, longitude: 95,
                               variable: 3)>
    array([[[[[...]]]]])
    Coordinates:
        * valid_time     (valid_time) datetime64[ns] 2022-07-23 ... 2022-07-23T21:0...
        * latitude       (latitude) float64 -5.75 -6.0 -6.25 ... -34.5 -34.75 -35.0
        * longitude      (longitude) float64 24.75 25.0 25.25 ... 47.75 48.0 48.25
        * variable       (variable) <U2 'msl' 'u_850' 'v_850'

    Args:
        data (xr.DataArray): dataarray contenant les données utilisées en entrée
            du réseau de neurones.
        covering (int): paramètre de recouvrement entre les patchs.
            Defaults to 0.
        patches_h (int): Hauteur des patchs. Defaults to 64.
        patches_w (int): Largeur des patchs. Defaults to 64.
        lat_min (Optional[float]): Latitude minimum. Default to None.
        lon_min (Optional[float]): Longitude minimum. Defaults to None.
        lat_max (Optional[float]): Latitude maximum. Defaults to None.
        lon_max (Optional[float]): Longitude maximum. Defaults to None.
    """

    def __init__(
        self,
        data: xr.DataArray,
        covering: int = 0,
        patches_h: int = 64,
        patches_w: int = 64,
        lat_min: Optional[float] = None,
        lon_min: Optional[float] = None,
        lat_max: Optional[float] = None,
        lon_max: Optional[float] = None,
        **kwargs,
    ):
        self.data = data
        self.covering = int(covering)
        self.patches_h = int(patches_h)
        self.patches_w = int(patches_w)
        self.lat_min = float(lat_min if lat_min is not None else data.latitude.min())
        self.lon_min = float(lon_min if lon_min is not None else data.longitude.min())
        self.lat_max = float(lat_max if lat_max is not None else data.latitude.max())
        self.lon_max = float(lon_max if lon_max is not None else data.longitude.max())

        self.data = (
            data.sortby("latitude", ascending=False)
            .sortby("longitude", ascending=True)
            .sel(
                latitude=slice(self.lat_max, self.lat_min),
                longitude=slice(self.lon_min, self.lon_max),
            )
            .transpose("valid_time", "latitude", "longitude", "variable")
        )

    def __len__(self) -> int:
        return len(self.data)

    @property
    def height(self) -> int:
        return self.data.shape[1]

    @property
    def width(self) -> int:
        return self.data.shape[2]

    @property
    def nb_vars(self) -> int:
        return self.data.shape[3]

    @cached_property
    def height_cov(self) -> int:
        return self.height - 2 * self.covering

    @cached_property
    def width_cov(self) -> int:
        return self.width - 2 * self.covering

    @cached_property
    def patches_h_cov(self) -> int:
        return self.patches_h - 2 * self.covering

    @cached_property
    def patches_w_cov(self) -> int:
        return self.patches_w - 2 * self.covering

    @cached_property
    def nb_patches_h(self) -> int:
        sup = bool((self.height + 2 * self.covering) % self.patches_h_cov)
        return self.height_cov // self.patches_h_cov + sup

    @cached_property
    def nb_patches_w(self) -> int:
        sup = bool((self.width + 2 * self.covering) % self.patches_w_cov)
        return self.width_cov // self.patches_w_cov + sup

    @cached_property
    def h_cov_is_perfect(self) -> bool:
        return not bool(self.height_cov % self.patches_h_cov)

    @cached_property
    def w_cov_is_perfect(self) -> bool:
        return not bool(self.width_cov % self.patches_w_cov)

    def __getitem__(self, index: Any) -> np.ndarray:
        """Renvoie un  batch de donnée à partir de self.data.
        Un batch consiste en une séquence de patchs de taille
        (self.patches_h, self.patches_w, self.nb_vars).

        Args:
            index (int): Index du batch

        Returns:
            np.ndarray: Séquence de patchs.
        """
        arr = self.data[index]
        if isinstance(index, int):
            arr = self.data[[index]]

        nb_patches = len(arr) * self.nb_patches_h * self.nb_patches_w

        patches = np.empty((nb_patches, self.patches_h, self.patches_w, self.nb_vars))

        for i in range(nb_patches):
            i_w = i % self.nb_patches_w
            i_h = (i // self.nb_patches_w) % self.nb_patches_h
            i_vt = (i // (self.nb_patches_w * self.nb_patches_h)) % len(arr)

            h_start = i_h * self.patches_h_cov
            if not self.h_cov_is_perfect and i_h + 1 == self.nb_patches_h:
                h_start = self.height - self.patches_h
            h_stop = h_start + self.patches_h

            w_start = i_w * self.patches_w_cov
            if not self.w_cov_is_perfect and i_w + 1 == self.nb_patches_w:
                w_start = self.width - self.patches_w
            w_stop = w_start + self.patches_w

            patches[i] = arr[i_vt, h_start:h_stop, w_start:w_stop]

        return patches

    def gather(self, patches: np.ndarray) -> np.ndarray:
        """Méthode inverse de __getitem__. Elle permet de  reconsituer des images
        à partir d'une séquence de patchs.

        Args:
            patches (np.ndarray): Séquence de patchs.

        Returns:
            np.ndarray: Images reconsitutées.
        """
        nb_patches, *_, nb_vars = patches.shape

        nb_vt = int(nb_patches // (self.nb_patches_h * self.nb_patches_w))

        arr = np.empty((nb_vt, self.height, self.width, nb_vars))

        for i in range(nb_patches):
            i_w = i % self.nb_patches_w
            i_h = (i // self.nb_patches_w) % self.nb_patches_h
            i_vt = (i // (self.nb_patches_w * self.nb_patches_h)) % nb_vt

            h_start = i_h * self.patches_h_cov
            h_step = self.patches_h - self.covering
            if not self.h_cov_is_perfect and i_h + 1 == self.nb_patches_h:
                h_start = self.height - self.patches_h
                h_step = self.patches_h
            h_thresh = 0 if i_h == 0 else self.covering

            w_start = i_w * self.patches_w_cov
            w_step = self.patches_w - self.covering
            if not self.w_cov_is_perfect and i_w + 1 == self.nb_patches_w:
                w_start = self.width - self.patches_w
                w_step = self.patches_w
            w_thresh = 0 if i_w == 0 else self.covering

            arr[
                i_vt,
                h_start + h_thresh : h_start + h_step,
                w_start + w_thresh : w_start + w_step,
            ] = patches[i, h_thresh:h_step, w_thresh:w_step]

        return arr
