import time
from typing import Any, Dict, List, Optional, TypeAlias, Union

import pandas as pd
import pyproj
import requests
import shapely.geometry as geometry
import shapely.wkt as wkt
import xmltodict
from requests.adapters import HTTPAdapter, Retry
from shapely.ops import linemerge, transform

xy_vegref: TypeAlias = Dict[str, Union[float, int]]
# Veginfo is a unsatable complex dict, so we just use Any
veginfo: TypeAlias = Dict[str, Any]  # type: ignore


def format_road_ref(roadref: str) -> str:
    """
        Makes sure that roadref is on format "RV15S14D1m2023"

    Args:
        roadref (str): roadref to be formatted

    Returns:
        str: formatted roadref
    """

    return roadref.replace(" ", "")


def split_road_ref(roadref: str) -> Optional[List[str]]:
    """
        Splits roadref into parts

    Args:
        roadref (str): a roadref on format "RV15 S14D1 m3403-4066"

    Returns:
        [str, str]: Tuple of start and stop point
    """

    roadparts = roadref.split(" m")

    if len(roadparts) != 2:
        return None
    meterparts = roadparts[1].split("-")
    return [
        f"{format_road_ref(roadparts[0])}m{meterparts[0]}",
        f"{format_road_ref(roadparts[0])}m{meterparts[1]}",
    ]


def get_road_info(roadref: str) -> Dict[str, Any]:  # type: ignore
    """
        Gets road info from visveginfo

    Args:
        roadref (str): reference to road

    Returns:
        json: json with road info
    """

    r = requests.get(
        f"https://nvdbapiles-v3.atlas.vegvesen.no/veg?vegsystemreferanse={roadref}"
    )

    return r.json()


def get_roads_info(roadrefs: str) -> Dict[str, Any]:  # type: ignore
    """
        Get road info for a list of roadrefs

    Args:
        roadrefs (str): comma separated list of roadrefs

    Returns:
        json: json with road infos
    """
    r = requests.get(
        "https://nvdbapiles-v3.atlas.vegvesen.no/veg/batch?vegsystemreferanser="
        + roadrefs
    )

    return r.json()


def get_road_route(from_xy: xy_vegref, to_xy: xy_vegref) -> Optional[veginfo]:
    """
        Gets road route between two points from visveginfo

    Args:
        from_xy (dict of {SRID: int, X: float, Y: float, Z: float}): start point
        to_xy (dict of {SRID: int, X: float, Y: float, Z: float}): end point

    Returns:
        complext dict: the road route from visveginfo
    """

    s = requests.Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[400, 500, 502, 503, 504]
    )
    s.mount("http://", HTTPAdapter(max_retries=retries))

    payload = {"AlignGeometriesWithRoute": True, "Points": [from_xy, to_xy]}
    road_r = s.post(
        "http://visveginfo-static.opentns.org/RoadInfoService/GetRouteBetweenLocations",
        json=payload,
    )

    s.close()

    time.sleep(1)

    try:
        return xmltodict.parse(road_r.text)
    except Exception as e:
        print(e)
        print(road_r.status_code)
        print(road_r.text)
        return None


def get_x_y(road_info: veginfo) -> Optional[xy_vegref]:
    """
        Gets x, y and SRID from road info

    Args:
        road_info (dict): The dict recieved from visveginfo

    Returns:
        dict of {SRID: int, X: float, Y: float, Z: float}: The x, y and SRID extracted
        from the road info or None if no geometry is found
    """

    if "geometri" in road_info:
        if "srid" in road_info["geometri"]:
            srid = int(road_info["geometri"]["srid"])
        else:
            srid = 5973

        if "wkt" in road_info["geometri"]:
            wkt_string = road_info["geometri"]["wkt"]
        else:
            wkt_string = road_info["geometri"]["WKT"]

        geom = wkt.loads(wkt_string)

        return {"SRID": srid, "X": geom.x, "Y": geom.y, "Z": geom.z}

    return None


def get_geom(road_route: veginfo) -> geometry:  # type: ignore[no-any-unimported]
    """Get geometry from road route

    Args:
        road_route (veginfo): Dict from visveginfo

    Returns:
        shapely.geometry: The geometry from the road route
    """
    from_proj = pyproj.CRS("EPSG:5973")
    to_proj = pyproj.CRS("EPSG:4326")

    project = pyproj.Transformer.from_crs(from_proj, to_proj, always_xy=True).transform

    if "RoadDataCollection" in road_route.keys():
        print("Got RoadDataCollection")
        x = road_route["RoadDataCollection"]["RoadDataItems"]["RoadDataItem"][0][
            "RoadReferenceAtLocation"
        ]["RoadNetPosition"]["X"]
        y = road_route["RoadDataCollection"]["RoadDataItems"]["RoadDataItem"][0][
            "RoadReferenceAtLocation"
        ]["RoadNetPosition"]["Y"]

        p = geometry.Point(float(x), float(y))
        p_transformed = transform(project, p)

        return p_transformed
    elif "ArrayOfRoadReference" in road_route.keys():
        if isinstance(road_route["ArrayOfRoadReference"]["RoadReference"], list):
            segments = []
            for roadref in road_route["ArrayOfRoadReference"]["RoadReference"]:
                segment = wkt.loads(str(roadref["WKTGeometry"]))
                line_items = list(segment.coords)
                line_items = sorted(line_items, key=lambda k: [k[1], k[0]])
                segments.append(segment)

            merged = linemerge([geometry.LineString(x) for x in segments])
            wkt_geometry = merged

        else:
            wkt_geometry = wkt.loads(
                str(road_route["ArrayOfRoadReference"]["RoadReference"]["WKTGeometry"])
            )

        g_transformed = transform(project, wkt_geometry)

        return g_transformed


def get_route(  # type: ignore[no-any-unimported]
    from_vegref: str, to_vegref: str
) -> Optional[geometry]:
    """
        Gets route between two points

    Args:
        from_vegref (str): from point on road
        to_vegref (str): to point on road

    Returns:
        wkt: the route between the two points
    """
    print(f"Henter rute for {from_vegref} – {to_vegref}")

    from_visveg_ref = format_road_ref(from_vegref)
    to_visveg_ref = format_road_ref(to_vegref)

    road_infos = get_roads_info(f"{from_visveg_ref},{to_visveg_ref}")

    from_xy = get_x_y(road_infos[from_visveg_ref])
    to_xy = get_x_y(road_infos[to_visveg_ref])

    if from_xy is None or to_xy is None:
        return None

    route = get_road_route(from_xy, to_xy)

    if route is None:
        return None

    return get_geom(route)


def _routes_iterator(  # type: ignore[no-any-unimported]
    row: pd.Series, from_col: str, to_col: str
) -> geometry:
    """
        Iterate over rows in a dataframe and get route between two points

    Args:
        row (dict): the row from the dataframe
        from_col (str): the column name for the from point
        to_col (str): the column name for the to point

    Returns:
        wkt: the route between the two points
    """
    return get_route(row[from_col], row[to_col])


def _routes_iterator_stretch(  # type: ignore[no-any-unimported]
    stretch: str,
) -> Optional[geometry]:
    """
        Iterate over rows in a dataframe and get route between two points

    Args:
        stretch (str): the stretch to get route for

    Returns:
        wkt: the route between the two points
    """
    road_refs = split_road_ref(stretch)

    if road_refs is None:
        return None

    if len(road_refs) == 2:
        return get_route(road_refs[0], road_refs[1])

    return None


def get_routes(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame,
    from_col: str = "from_vegref",
    to_col: str = "to_vegref",
    geometry_col: str = "geometry",
) -> pd.DataFrame:
    """
    Create routes between points in a dataframe

    Args:
        _df (DataFrame): a dataframe with columns for from and to points
        from_col (str, optional): name of the from road reference data column.
        Defaults to "from_vegref".
        to_col (str, optional): name of the to road reference data column.
        Defaults to "to_vegref".
        geometry_col (str, optional): name of the geometry column.
        Defaults to "geometry".

    Returns:
        DataFrame: The dataframe with a new column for the route
    """

    _df[geometry_col] = _df.apply(
        lambda x: _routes_iterator(x, from_col, to_col), axis=1
    )

    return _df


def get_routes_stretch_of_road(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, stretch: str = "vegref", geometry_col: str = "geometry"
) -> pd.DataFrame:
    """
    Create routes between points in a dataframe where the stretch of
    road is given in the same column

    Args:
        _df (DataFrame): a dataframe with a column for the stretch of road
        stretch (str, optional): name of the stretch of road data column.
        Defaults to "vegref".
        geometry_col (str, optional): name of the geometry column.
        Defaults to "geometry".

    Returns:
        DataFrame: The dataframe with a new column for the route
    """

    _df.loc[:, geometry_col] = _df.loc[:, stretch].apply(_routes_iterator_stretch)

    return _df
