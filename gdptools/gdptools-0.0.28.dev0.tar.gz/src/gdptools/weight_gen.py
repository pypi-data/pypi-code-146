"""Calculate weights."""
import time
from typing import Any
from typing import Literal
from typing import Optional

import geopandas as gpd
import pandas as pd

from gdptools.data.user_data import UserData
from gdptools.data.weight_gen_data import WeightData
from gdptools.weights.calc_weight_engines import ParallelWghtGenEngine
from gdptools.weights.calc_weight_engines import SerialWghtGenEngine

WEIGHT_GEN_METHODS = Literal["serial", "parallel"]
""" Methods used in WghtGen class.

seerial: Iterates through polygons to calculate weights.  Sufficient for most cases.
parallel: Chunks polygons and distributes to available processors.  Provides a
    substantial speedup when there is a large number of polygons.

Raises:
    TypeError: If value is not one of "serial" or "parallel".

Returns:
    _type_: str
"""


class WeightGen:
    """Class for weight calculation."""

    def __init__(
        self,
        user_data: UserData,
        method: WEIGHT_GEN_METHODS,
        output_file: str,
        weight_gen_crs: Any,
        verbose: Optional[bool] = False,
    ) -> None:
        """Weight generation class.

        Args:
            user_data (UserData): _description_
            method (WEIGHT_GEN_METHODS): :data: `gdptools.weights.WeightGen.WEIGHT_GEN_METHODS`
            output_file (str): _description_
            weight_gen_crs (Any): _description_
            verbose (Optional[bool], optional): _description_. Defaults to False.

        Raises:
            TypeError: _description_
        """
        self._user_data = user_data
        self._method = method
        self._output_file = output_file
        self._weight_gen_crs = weight_gen_crs
        self._verbose = verbose
        self._weight_data = None
        self._intersections = None

        if self._method == "serial":
            self.__calc_method = SerialWghtGenEngine
            print("Using serial engine")
        elif self._method == "parallel":
            self.__calc_method = ParallelWghtGenEngine
            print("Using parallel engine")
        else:
            raise TypeError(f"method: {self._method} not in [serial, parallel]")

    def calculate_weights(self, intersections: Optional[bool] = False) -> pd.DataFrame:
        """Calculate weights.

        Args:
            intersections (Optional[bool], optional): _description_. Defaults to False.

        Returns:
            pd.DataFrame: _description_
        """
        tstrt = time.perf_counter()
        self._weight_data: WeightData = self._user_data.prep_wght_data()
        tend = time.perf_counter()
        print(f"Data preparation finished in {tend - tstrt:0.4f} seconds")
        if intersections:
            print("Saving interesections in weight generation.")
            weights, self._intersections = self.__calc_method().calc_weights(
                poly=self._weight_data.feature,
                poly_idx=self._weight_data.id_feature,
                grid_cells=self._weight_data.grid_cells,
                wght_gen_crs=self._weight_gen_crs,
                filename=self._output_file,
                intersections=intersections,
                verbose=self._verbose,
            )
        else:
            weights = self.__calc_method().calc_weights(
                poly=self._weight_data.feature,
                poly_idx=self._weight_data.id_feature,
                grid_cells=self._weight_data.grid_cells,
                wght_gen_crs=self._weight_gen_crs,
                filename=self._output_file,
                intersections=intersections,
                verbose=self._verbose,
            )
        return weights

    @property
    def grid_cells(self) -> gpd.GeoDataFrame:
        """Return grid_cells."""
        if self._weight_data.grid_cells is None:
            print("grid_cells not calculated yet. Run calculate_weights().")
        return self._weight_data.grid_cells

    @property
    def intersections(self) -> gpd.GeoDataFrame:
        """Return intersections."""
        if self._intersections is None:
            print(
                "intersections not calculated, "
                "Run calculate_weights(intersectiosn=True)"
            )
        return self._intersections
