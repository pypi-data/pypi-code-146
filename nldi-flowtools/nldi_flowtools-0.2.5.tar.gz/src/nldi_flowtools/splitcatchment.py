"""Delineate drainage basin using NLDI and user-defined point."""
from typing import Tuple

import geojson

from .utils import check_coords
from .utils import geom_to_geojson
from .utils import get_coordsys
from .utils import get_local_catchment
from .utils import get_local_flowline
from .utils import get_on_flowline
from .utils import get_total_basin
from .utils import get_upstream_basin
from .utils import JsonFeatureCollectionType
from .utils import merge_geometry
from .utils import project_point
from .utils import split_catchment


class SplitCatchment:
    """Define inputs and outputs for the main SplitCatchment class."""

    def __init__(self: "SplitCatchment", x: float, y: float, upstream: bool) -> None:
        """Initialize Splitcatchment class."""
        self.x = x
        self.y = y
        self.catchmentIdentifier: str
        self.flowline: JsonFeatureCollectionType
        self.flw = None
        self.flwdir_transform: object
        self.projected_xy = Tuple[float, float]
        self.onFlowline: bool
        self.upstream = upstream

        # geoms
        self.catchmentGeom = None
        self.splitCatchmentGeom = None
        self.totalBasinGeom = None
        self.upstreamBasinGeom = None
        self.mergedCatchmentGeom = None
        self.nhdFlowlineGeom = None

        # outputs
        self.catchment: JsonFeatureCollectionType
        self.splitCatchment: JsonFeatureCollectionType
        self.upstreamBasin: JsonFeatureCollectionType
        self.mergedCatchment: JsonFeatureCollectionType

        # create transform
        self.transformToRaster: object
        self.transformToWGS84: object

        # kick off
        self.run()

    def serialize(self) -> geojson.feature.FeatureCollection:
        """Convert returns to GeoJSON to be exported."""
        # If upstream == False, only return the local catchment
        # and the splitcatchment geometries
        if self.upstream is False:
            feature1 = geojson.Feature(
                geometry=self.catchment,
                id="catchment",
                properties={"catchmentID": self.catchmentIdentifier},
            )
            feature2 = geojson.Feature(
                geometry=self.splitCatchment, id="splitCatchment"
            )
            featurecollection = geojson.FeatureCollection([feature1, feature2])

        # If upstream == True and the clickpoint is on a NHD FLowline,
        # return the local catchment and the merged catchment
        # (splitcatchment merged with all upstream basins)
        elif self.upstream is True and self.onFlowline is True:
            feature1 = geojson.Feature(
                geometry=self.catchment,
                id="catchment",
                properties={"catchmentID": self.catchmentIdentifier},
            )
            feature2 = geojson.Feature(
                geometry=self.mergedCatchment, id="mergedCatchment"
            )
            featurecollection = geojson.FeatureCollection([feature1, feature2])

        # If upstream == True and the clickpoint is NOT on a NHD FLowline,
        # return the local catchment and splitcatchment
        elif self.upstream is True and self.onFlowline is False:
            feature1 = geojson.Feature(
                geometry=self.catchment,
                id="catchment",
                properties={"catchmentID": self.catchmentIdentifier},
            )
            feature2 = geojson.Feature(
                geometry=self.splitCatchment, id="splitCatchment"
            )
            # feature3 = geojson.Feature(geometry=self.upstreamBasin, id='upstreamBasin')
            featurecollection = geojson.FeatureCollection([feature1, feature2])

        return featurecollection

    # main functions
    def run(self) -> None:
        """Run splitcatchment module functions."""
        # Order of these functions is important!
        check_coords(self.x, self.y)
        self.catchmentIdentifier, self.catchmentGeom = get_local_catchment(
            self.x, self.y
        )
        self.flowline, self.nhdFlowlineGeom = get_local_flowline(
            self.catchmentIdentifier
        )
        self.transformToRaster, self.transformToWGS84 = get_coordsys()
        self.projected_xy = project_point(self.x, self.y, self.transformToRaster)
        self.splitCatchmentGeom = split_catchment(
            self.catchmentGeom, self.projected_xy, self.transformToRaster
        )
        self.onFlowline = get_on_flowline(
            self.projected_xy, self.flowline, self.transformToRaster
        )
        self.catchment = geom_to_geojson(self.catchmentGeom)

        # outputs
        if self.upstream is False:
            self.splitCatchment = geom_to_geojson(self.splitCatchmentGeom)

        if self.upstream is True and self.onFlowline is True:
            self.totalBasinGeom = get_total_basin(self.catchmentIdentifier)
            self.mergedCatchmentGeom = merge_geometry(
                self.catchmentGeom, self.splitCatchmentGeom, self.totalBasinGeom
            )
            self.mergedCatchment = geom_to_geojson(self.mergedCatchmentGeom)

        if self.upstream is True and self.onFlowline is False:
            self.splitCatchment = geom_to_geojson(self.splitCatchmentGeom)
            self.totalBasinGeom = get_total_basin(self.catchmentIdentifier)
            self.upstreamBasinGeom = get_upstream_basin(
                self.catchmentGeom, self.totalBasinGeom
            )
            self.upstreamBasin = geom_to_geojson(self.upstreamBasinGeom)
