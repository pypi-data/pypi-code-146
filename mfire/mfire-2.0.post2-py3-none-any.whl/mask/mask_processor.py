"""
This module should do mask preprocessing and transform geojson to netcdf.

History :
    (Vincent Chabot ) : Forcing small polygon to be represented as point or line.
    (Vincent Chabot) February 2021 :
        Adding splitting by
            - compass direction
            - altitude
"""
from pathlib import Path
from typing import List, Tuple, Union

import xarray as xr
from shapely import geometry as shp_geom
from geojson import Feature
import numpy as np
from PIL import Image, ImageDraw

import mfire.utils.hash as hashmod
from mfire.utils.xr_utils import ArrayLoader, from_0_360, from_center_to_0_360
from mfire.mask.north_south_mask import get_cardinal_masks
from mfire.mask.altitude_mask import generate_mask_by_altitude
from mfire.mask.fusion import (
    extract_areaName,
    perform_poly_fusion,
)
from mfire.localisation.area_algebre import compute_IoU
from mfire.settings import get_logger, Settings

# Logging
LOGGER = get_logger(name="mask_processor", bind="mask")


xr.set_options(keep_attrs=True)

Shape = Union[
    shp_geom.Point,
    shp_geom.MultiPoint,
    shp_geom.LineString,
    shp_geom.MultiLineString,
    shp_geom.Polygon,
    shp_geom.MultiPolygon,
]


def lon_lat_to_img(point: Tuple[float, float], gridinfo: dict) -> Tuple[float, float]:
    """
    Transform to apply to an img to get coordinates
    :param point: lon/lat of point
    :param gridinfo: geometry grid as dict
    """

    lon, lat = point
    # x / lon transform
    a_x = gridinfo["nb_c"] / (gridinfo["last_lon"] - gridinfo["first_lon"])
    b_x = -gridinfo["first_lon"] * a_x
    x = a_x * lon + b_x
    # y  / Lat transform
    a_y = gridinfo["nb_l"] / (gridinfo["last_lat"] - gridinfo["first_lat"])
    b_y = -gridinfo["first_lat"] * a_y
    y = a_y * lat + b_y
    return (x, y)


def lon_lat_shape_to_img(
    poly: shp_geom.Polygon, gridinfo: dict
) -> List[Tuple[float, float]]:
    """lon_lat_shape_to_img

    Args:
        poly (A polygon (shapely)): The polygon for which we need to find
            the exterior bound.
        gridinfo (dict): A dictionnary describing the grid.

    Returns:
        [list]: The list of exterior point of the polygon.
    """
    return [
        lon_lat_to_img(point, gridinfo)
        for point in poly.exterior.__geo_interface__["coordinates"]
    ]


def lon_lat_point_to_img(
    point: shp_geom.Point, gridinfo: dict
) -> List[Tuple[float, float]]:
    """
    Args:
        point (A Point (shapely))
        gridinfo (dict): A dictionnary describing the grid.
    """
    return [lon_lat_to_img(point.__geo_interface__["coordinates"], gridinfo)]


def lon_lat_linestring_to_img(
    line: shp_geom.LineString, gridinfo: dict
) -> List[Tuple[float, float]]:
    """lon_lat_linestring_to_img

    Args:
        line (A line (shapely)): The Line for which we need to find the exterior bound.
        gridinfo (dict): A dictionnary describing the grid.

    Returns:
        [list]: The list of point of the line.
    """
    return [
        lon_lat_to_img(point, gridinfo)
        for point in line.__geo_interface__["coordinates"]
    ]


def is_point(img_shape: List[Tuple[float, float]]) -> bool:
    """
    Permet de savoir si un polygon est en fait un point
    Args:
        img_shape ([type]): [description]

    Returns:
        [type]: [description]
    """
    mini = np.asarray(img_shape).min(axis=0)
    maxi = np.asarray(img_shape).max(axis=0)
    return np.max(maxi - mini) < 1


def is_line(img_shape: List[Tuple[float, float]]) -> bool:
    """Enable to know if a polygon is in fact a line (for a specific grid)

    Args:
        img_shape ([type]): [description]

    Returns:
        [bool]: True if it is a line, False otherwise
    """
    mini = np.asarray(img_shape).min(axis=0)
    maxi = np.asarray(img_shape).max(axis=0)
    return np.min(maxi - mini) < 1


def get_gridinfo(grid_da: xr.DataArray) -> dict:
    """Return grid's metadata.

    Args:
        grid_da (xr.DataArray): We will use only the lat/lon grid
            The grid should have latitude and longitude dimension.

    Raises:
        ValueError: _description_
        excpt: _description_
        excpt: _description_

    Returns:
        _type_: _description_
    """
    info = {
        "first_lat": grid_da.latitude[0].values.round(5),
        "last_lat": grid_da.latitude[-1].values.round(5),
        "nb_l": grid_da.latitude.size,
        "first_lon": grid_da.longitude[0].values.round(5),
        "last_lon": grid_da.longitude[-1].values.round(5),
        "nb_c": grid_da.longitude.size,
    }
    info["step_lat"] = (info["last_lat"] - info["first_lat"]) / (info["nb_l"] - 1)
    info["step_lon"] = (info["last_lon"] - info["first_lon"]) / (info["nb_c"] - 1)
    return info


def create_mask_PIL(poly: Shape, grid_da: xr.DataArray) -> xr.Dataset:
    """Create mask using PIL library.
        Passage du format vectoriel au format grille.
    Args:
       poly : La shape que l'on souhaite transformer
       grid_da(dataarray) : La grille sur laquelle on met les données

    """
    gridinfo = get_gridinfo(grid_da)
    img = Image.new("1", (int(gridinfo["nb_c"]), int(gridinfo["nb_l"])))
    if poly.geometryType() == "Polygon":
        img_shape = lon_lat_shape_to_img(poly, gridinfo=gridinfo)
        if is_point(img_shape):
            point_shape = np.floor(np.asarray(img_shape).min(axis=0))
            ImageDraw.Draw(img).point(tuple(point_shape), fill=1)
        elif is_line(img_shape):
            mini = np.asarray(img_shape).min(axis=0)
            maxi = np.asarray(img_shape).max(axis=0)
            ImageDraw.Draw(img).line([tuple(mini), tuple(maxi)], fill=1)
        else:
            ImageDraw.Draw(img).polygon(img_shape, fill=1, outline=1)
            img_holes = []
            for hole in poly.interiors:
                # --------------------------------------------------
                # The rounding is here in order to get a better hole.
                # However, for large grid, some problem can occured.
                # ---------------------------------------------------
                img_holes = [
                    tuple(np.round(lon_lat_to_img(point, gridinfo)).tolist())
                    for point in hole.coords
                ]
                ImageDraw.Draw(img).polygon(img_holes, fill=-1, outline=0)

    elif poly.geometryType() == "MultiPolygon":
        for small in poly.geoms:
            img_shape = lon_lat_shape_to_img(small, gridinfo=gridinfo)
            if is_point(img_shape):
                point_shape = np.floor(np.asarray(img_shape).min(axis=0))
                ImageDraw.Draw(img).point(tuple(point_shape), fill=1)
            elif is_line(img_shape):
                mini = np.asarray(img_shape).min(axis=0)
                maxi = np.asarray(img_shape).max(axis=0)
                ImageDraw.Draw(img).line([tuple(mini), tuple(maxi)], fill=1)
            else:
                ImageDraw.Draw(img).polygon(img_shape, fill=1, outline=1)
                for hole in shp_geom.shape(small).interiors:
                    img_holes = [
                        tuple(np.round(lon_lat_to_img(point, gridinfo)).tolist())
                        for point in hole.coords
                    ]
                    ImageDraw.Draw(img).polygon(img_holes, fill=-1, outline=0)
    elif poly.geometryType() == "Point":
        img_shape = lon_lat_point_to_img(poly, gridinfo=gridinfo)
        ImageDraw.Draw(img).point(img_shape, fill=1)
    elif poly.geometryType() == "MultiPoint":
        for point in poly.geoms:
            img_shape = lon_lat_point_to_img(point, gridinfo=gridinfo)
            ImageDraw.Draw(img).point(img_shape, fill=1)
    elif poly.geometryType() == "LineString":
        img_shape = lon_lat_linestring_to_img(poly, gridinfo=gridinfo)
        ImageDraw.Draw(img).line(img_shape, fill=1)
    elif poly.geometryType() == "MultiLineString":
        for line in poly.geoms:
            img_shape = lon_lat_linestring_to_img(line, gridinfo=gridinfo)
            ImageDraw.Draw(img).line(img_shape, fill=1)
    else:
        raise ValueError(
            f"Type of geometry {poly.geometryType()} not taken into account."
        )

    ds = xr.Dataset()
    for x in list(grid_da.dims):
        ds.coords[x] = grid_da[x].values
    ds[grid_da.name] = (grid_da.dims, np.array(img))
    return (
        ds.where(ds[grid_da.name] > 0)
        .dropna(dim=grid_da.dims[0], how="all")
        .dropna(dim=grid_da.dims[1], how="all")
    )


class MaskProcessor:
    """
    Permet de créer les masques géographiques sur les data array
    """

    def __init__(self, config_dict: dict, **kwargs):
        """
        Args:
            config_dict (dict): Dictionnaire de configuration de la production
                contenant au moins la clé 'geos'.
        Kwargs :
            output_dir : utilisé si pas de file dans le dictionnaire
        """
        self.data = config_dict
        self.change_geometry()
        self.kwargs = kwargs

    @property
    def grid_names(self) -> Tuple[str]:
        return tuple(
            p.name.split(".nc")[0] for p in Settings().altitudes_dirname.iterdir()
        )

    def get_grid_da(self, grid_name: str) -> xr.DataArray:
        return ArrayLoader(
            filename=Settings().altitudes_dirname / f"{grid_name}.nc"
        ).load()

    def change_geometry(self):
        for i, area in enumerate(self.data["geos"]["features"]):
            if shp_geom.shape(area["geometry"]).geometryType() in [
                "Polygon",
                "MultiPolygon",
                "LineString",
                "MultiLineString",
            ]:
                x = shp_geom.shape(area["geometry"]).buffer(1e-5)  # .buffer(-1e-5)
                self.data["geos"]["features"][i]["geometry"] = Feature(geometry=x)[
                    "geometry"
                ]

    def get_mask(self, grid_name: str, poly: Shape) -> xr.Dataset:
        """get_mask

        Args:
            grid_name (str): The grid name.
            poly (shapely.geometry.shape): The shape to transform in netcdf.

        Returns:
            xr.Dataset: The mask dataset.
        """
        grid_da = self.get_grid_da(grid_name)
        change_longitude = False
        if grid_da.longitude.max() > 180:
            change_longitude = True
            grid_da = from_0_360(grid_da)
        dout = create_mask_PIL(poly=poly, grid_da=grid_da)
        if change_longitude:
            dout = from_center_to_0_360(dout)
        return dout.rename(
            {"latitude": f"latitude_{grid_name}", "longitude": f"longitude_{grid_name}"}
        )

    @staticmethod
    def is_axe(feature: dict) -> bool:
        """checks if mask's geojson description represents an axis.

        Args:
            feature (_type_): the geojson feature

        Returns:
            Bool: True if its an Axis, False otherwise
        """
        return feature["properties"].get("is_axe", False)

    @staticmethod
    def merge_area(ds: xr.Dataset, merged_list: list, grid_name: str) -> xr.Dataset:
        """Permet de merger les zones.

        Args:
            ds (xr.Dataset): Le dataset de masques déjà créér
            merged_list (list): La liste des zones à créer
            grid_name (str): Le nom de la grille

        Returns:
            xr.Dataset: Les zones fusionnées.
        """
        tmp_coords = {
            f"latitude_{grid_name}": "latitude",
            f"longitude_{grid_name}": "longitude",
        }
        dgrid = ds[grid_name]
        list_area = []
        for new_zone in merged_list:
            dtemp = dgrid.sel(id=new_zone["base"]).max("id")
            IoU = compute_IoU(dtemp.rename(tmp_coords), dgrid.rename(tmp_coords))
            if IoU.max("id") < 0.97:
                dtemp = dtemp.expand_dims(dim="id").assign_coords(id=[new_zone["id"]])
                dtemp["areaName"] = (("id"), [new_zone["name"]])
                dtemp["areaType"] = (("id"), [new_zone["areaType"]])
                list_area.append(dtemp)
            else:
                LOGGER.debug(
                    f"On ne cree pas {new_zone['name']} pour cette grille {grid_name}"
                )

        if len(list_area) > 0:
            dout = xr.merge(list_area)
            res = dout.reset_coords(["areaName", "areaType"])
        else:
            res = None
        return res

    def create_masks(self):
        """
        create_masks
        This function create all the mask from a geojson dictionnary.
        The creation is performed only if the output file is not present.
        """
        dmask = xr.Dataset()
        if "mask_hash" in self.data:
            current_hash = self.data.get("mask_hash")
        else:
            handler = hashmod.MD5(self.data["geos"])
            current_hash = handler.hash
        # Pour chaque msb on va creer un nouveau fichier
        if "file" in self.data:
            fout = Path(self.data["file"])
        elif "uid" in self.data:
            fout = Path(self.kwargs.get("output_dir", "./") + self.data["uid"] + ".nc")
        else:
            raise ValueError(
                "You should have in the file something to name the output."
            )
        output_dir = fout.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        # On tri les zones pour mettre les axes en dernier
        self.data["geos"]["features"].sort(key=self.is_axe)

        merged_list = []
        for area in self.data["geos"]["features"]:
            # On recupere les infos qui nous interessent
            area_id = area["id"]
            # On récupere l'info pour savoir si c'est un axe
            is_axe = self.is_axe(area)
            # Introduire ici le truc sur le hash
            poly = shp_geom.shape(area["geometry"])

            if is_axe and poly.geometryType() in ["Polygon", "MultiPolygon"]:
                merged_list.extend(
                    perform_poly_fusion(poly, self.data["geos"], area_id)
                )

            for grid_name in self.grid_names:
                l_temp = []
                dtemp = self.get_mask_on_grid(
                    grid_name, poly, area_id, area["properties"]
                )
                l_temp.append(dtemp)
                if is_axe and poly.geometryType() in ("Polygon", "MultiPolygon"):
                    LOGGER.debug(
                        "Creating altitude and geographical mask",
                        area_id=area_id,
                        grid_name=grid_name,
                        func="create_masks",
                    )
                    ds_mask_compass = self.get_compass_area(grid_name, poly, area_id)
                    if ds_mask_compass and ds_mask_compass.id.size > 1:
                        l_temp.append(ds_mask_compass)
                    ds_mask_alti = generate_mask_by_altitude(
                        dtemp[grid_name], self.get_grid_da(grid_name), area_id + "_alt_"
                    )
                    if ds_mask_alti is not None:
                        l_temp.append(ds_mask_alti)
                try:
                    dpartial = xr.merge(l_temp)
                    dmask = xr.merge([dmask, dpartial])
                except Exception as excpt:
                    LOGGER.warning(f"Le merge partiel {l_temp}")
                    LOGGER.warning(
                        "Failed to merge masks.",
                        dmask=dmask,
                        dtemp=dtemp,
                        area_id=area_id,
                        grid_name=grid_name,
                        func="create_masks",
                    )
                    raise excpt
        # On va ajouter les régions fusionnées ensuite.
        l_temp = []
        for grid_name in self.grid_names:
            dmerged = self.merge_area(dmask, merged_list, grid_name)
            if dmerged is not None:
                l_temp.append(dmerged)
        if l_temp != []:
            dpartial = xr.merge(l_temp)
            dmask = xr.merge([dmask, dpartial])
        dmask.attrs["md5sum"] = current_hash
        dmask.to_netcdf(fout)

    def get_compass_area(self, grid_name: str, poly: Shape, area_id: str) -> xr.Dataset:
        """Effectue la découpe selon les points cardinaux

        Args:
            grid_name (str): Nom de la grille sur laquelle on veut projeter le JSON
            poly (shape): Le shape de la zone a découper
            area_id (str): L'identifiant original de la zone

        Returns:
            Dataset : Un dataset de la découpe
        """
        dmask = xr.Dataset()
        geo_B, _ = get_cardinal_masks(poly, parent_id=area_id + "_compass_")
        for area in geo_B["features"]:
            compass_poly = shp_geom.shape(area["geometry"])
            compass_id = area["id"]
            area["properties"]["type"] = "compass"
            dtemp = self.get_mask_on_grid(
                grid_name, compass_poly, compass_id, area["properties"]
            )
            try:
                dmask = xr.merge([dmask, dtemp])
            except Exception as excpt:
                LOGGER.warning(
                    "Failed to merge masks.",
                    dmask=dmask,
                    dtemp=dtemp,
                    area_id=area_id,
                    grid_name=grid_name,
                    func="get_compass_area",
                )
                raise excpt
        return dmask

    def get_mask_on_grid(
        self, grid_name: str, poly: Shape, area_id: str, properties: dict
    ) -> xr.Dataset:
        """
        Args:
            grid_name (str): La grille d'intérêt
            poly (shape): The shape we will transfer to netcdf
            area_id (str): Id
            properties (dict): Dictionnary of properties
        """
        areaType = properties.get("type", "")
        if properties.get("is_axe", False):
            areaType = "Axis"

        areaName = extract_areaName(properties)
        dtemp = self.get_mask(grid_name, poly)
        dtemp = dtemp.expand_dims(dim="id").assign_coords(id=[area_id])
        dtemp["areaName"] = (("id",), [areaName])
        dtemp["areaType"] = (("id",), [areaType])
        return dtemp
