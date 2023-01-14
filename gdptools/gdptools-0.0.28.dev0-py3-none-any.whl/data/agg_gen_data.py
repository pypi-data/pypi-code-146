"""Dataclasses used in aggregation."""
from dataclasses import dataclass
from typing import List

from geopandas import GeoDataFrame
from xarray import DataArray

from gdptools.data.odap_cat_data import CatGrids
from gdptools.data.odap_cat_data import CatParams


@dataclass(repr=True)
class AggData(object):
    """AggData is a convenience container of data necessary for aggregation.

    Data provided in one of UserData inherited classes will be prepped for aggregation,
    including subsetting the gridded data by the features bounding box, and by the time-
    period selected.  In addition if the gridded data is defined between 0-360 degrees
    longitude it will be shifted to -180 - 180 degrees.  For each variable in the
    user_data attribute of either the WeightGen or AggGen classes, a dict of
    {var: AggData} will be generated in the AggGen.calculate_agg() method.

    Args:
        variable (str): Variable name.
        cat_param (CatParams): Catparams data class containing parameter metadata.
        cat_grid (CatGrids): CatGrids data class containing grid metadata.
        da: (DataArray): The spatially and temporally subsetted variable DataArray.
        feature (GeoDataFrame): The user-supplied feature file represented as a
            GeoDataFrame.
        id_feature (str): The feature id (column header) in the GeoDataFrame.
        period (List[str]): A list of dates representing the starting and ending date to
            process.
    """

    variable: str
    cat_param: CatParams
    cat_grid: CatGrids
    da: DataArray
    feature: GeoDataFrame
    id_feature: str
    period: List[str]
