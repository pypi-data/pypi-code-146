from tsp.core import TSP, IndexedTSP
from tsp.misc import _is_depth_column
from tsp.plots.static import trumpet_curve, time_series, colour_contour
from tsp.readers import read_gtnp, read_geotop, read_geoprecision, read_hoboware, read_ntgs, read_logr, read_csv

#TSP.__module__ = "teaspoon"

__all__ = ["TSP", "IndexedTSP"]