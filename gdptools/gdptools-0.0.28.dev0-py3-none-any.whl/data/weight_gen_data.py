"""Data classes used in aggregation."""
from dataclasses import dataclass

import geopandas as gpd


@dataclass(repr=True)
class WeightData(object):
    """Simple dataclass for tranferring prepared user data to the CalcWeightEngine."""

    feature: gpd.GeoDataFrame
    id_feature: str
    grid_cells: gpd.GeoDataFrame
