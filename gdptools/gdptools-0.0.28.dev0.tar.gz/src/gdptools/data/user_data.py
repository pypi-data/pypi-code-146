"""Prepare user data for weight generation."""
import time
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import List
from typing import Union

import geopandas as gpd
import numpy as np
import pandas as pd
import rioxarray as rxr
import xarray as xr
from pyproj.crs import CRS

from gdptools.data.agg_gen_data import AggData
from gdptools.data.odap_cat_data import CatGrids
from gdptools.data.odap_cat_data import CatParams
from gdptools.data.weight_gen_data import WeightData
from gdptools.helpers import build_subset
from gdptools.helpers import build_subset_tiff
from gdptools.utils import _check_for_intersection
from gdptools.utils import _check_for_intersection_nc
from gdptools.utils import _get_cells_poly
from gdptools.utils import _get_data_via_catalog
from gdptools.utils import _get_shp_bounds_w_buffer
from gdptools.utils import _get_shp_file
from gdptools.utils import _get_top_to_bottom
from gdptools.utils import _read_shp_file


class UserData(ABC):
    """Prepare data for different sources for weight generation."""

    @abstractmethod
    def __init__(self) -> None:
        """Init class."""
        pass

    @abstractmethod
    def prep_wght_data(self) -> WeightData:
        """Abstract interface for generating weight data."""
        pass

    @abstractmethod
    def prep_agg_data(self) -> AggData:
        """Abstract method for preparing data for aggregation."""
        pass

    @abstractmethod
    def get_vars(self) -> list[str]:
        """Return a list of variables."""
        pass

    @abstractmethod
    def get_feature_id(self) -> str:
        """Abstract method for returning the id_feature parameter."""
        pass


class ODAPCatData(UserData):
    """Instance of UserData using OPeNDAP catalog data."""

    def __init__(
        self,
        *,
        param_dict: dict[str, dict],
        grid_dict: dict[str, dict],
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        id_feature: str,
        period: List[str],
    ) -> None:
        """Initialize PrepODAPCatData class.

        Args:
            param_dict (dict[str, dict]): Parameter metadata from OPeNDAP catalog.
            grid_dict (dict[str, dict]): Grid metadata from OPeNDAP catalog.
            f_feature (Union[str, Path, gpd.GeoDataFrame]): GeoDataFrame or any
                path-like object that can be read by geopandas.read_file().
            id_feature (str): Header in GeoDataFrame to use as index for weights.
            period (List[str]): List containing date strings defining start and end
                time slice for aggregation.
        """
        self.param_dict = param_dict
        self.grid_dict = grid_dict
        self.f_feature = f_feature
        self.id_feature = id_feature
        self.period = pd.to_datetime(period)
        self._heck_input_dicts()
        self.gdf = _read_shp_file(self.f_feature)

    def get_feature_id(self) -> str:
        """Return id_feature."""
        return self.id_feature

    def get_vars(self) -> list[str]:
        """Return list of param_dict keys, proxy for varnames."""
        return list(self.param_dict.keys())

    def prep_agg_data(self, key: str) -> AggData:
        """Prepare ODAPCatData data for aggregation methods.

        Args:
            key (str): _description_

        Returns:
            AggData: _description_
        """
        cp = self._create_catparam(key=key)
        cg = self._create_catgrid(key=key)

        is_intersect, is_degrees, is_0_360 = _check_for_intersection(
            cat_params=cp, cat_grid=cg, gdf=self.gdf
        )

        gdf, gdf_bounds = _get_shp_file(
            shp_file=self.gdf, cat_grid=cg, is_degrees=is_degrees
        )

        rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
        ds_ss = _get_data_via_catalog(
            cat_params=cp,
            cat_grid=cg,
            bounds=gdf_bounds,
            begin_date=self.period[0],
            end_date=self.period[1],
            rotate_lon=rotate_ds,
        )
        return AggData(
            variable=key,
            cat_param=cp,
            cat_grid=cg,
            da=ds_ss,
            feature=gdf,
            id_feature=self.id_feature,
            period=self.period,
        )

    def prep_wght_data(self) -> WeightData:
        """Prepare and return WeightData for weight generation."""
        # For weight generation we just need param and grid dict from one variable
        # passed to CatParms and CatGrids.
        self._heck_input_dicts()
        keys = self.get_vars()
        cp = self._create_catparam(key=keys[0])
        cg = self._create_catgrid(key=keys[0])
        gdf = _read_shp_file(self.f_feature)
        self._check_id_feature(gdf)
        is_intersect, is_degrees, is_0_360 = _check_for_intersection(
            cat_params=cp, cat_grid=cg, gdf=gdf
        )

        gdf, gdf_bounds = _get_shp_file(
            shp_file=gdf, cat_grid=cg, is_degrees=is_degrees
        )

        rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
        ds_ss = _get_data_via_catalog(
            cat_params=cp,
            cat_grid=cg,
            bounds=gdf_bounds,
            begin_date=self.period[0],
            rotate_lon=rotate_ds,
        )

        tsrt = time.perf_counter()
        ds_ss.load()
        tend = time.perf_counter()
        print(f"loading {cp.varname} in {tend-tsrt:0.4f} seconds")

        tsrt = time.perf_counter()
        gdf_grid = _get_cells_poly(
            xr_a=ds_ss,
            x=cg.X_name,
            y=cg.Y_name,
            crs_in=cg.proj,
        )
        tend = time.perf_counter()
        print(f"grid cells generated in {tend-tsrt:0.4f} seconds")

        return WeightData(feature=gdf, id_feature=self.id_feature, grid_cells=gdf_grid)

    def _check_id_feature(self, gdf):
        """Check id_feature in gdf."""
        if self.id_feature not in gdf.columns[:]:
            raise ValueError(
                f"shp_poly_idx: {self.id_feature} not in gdf columns: {gdf.columns}"
            )

    def _create_catgrid(self, key: str):
        """Create CatGrids."""
        return CatGrids(**self.grid_dict.get(key))

    def _create_catparam(self, key: str):
        """Create CatParams."""
        return CatParams(**self.param_dict.get(key))

    def _heck_input_dicts(self):
        """Check input dicts are of equal length and with at least one entry."""
        if len(self.param_dict) != len(self.grid_dict):
            raise ValueError(
                "Mismatch in key,value pairs. param_dict and grid_dict \
                should have tehe same number of keys."
            )
        if len(self.param_dict) < 1:
            raise ValueError("param_dict should have at least 1 key,value pair")


class UserCatData(UserData):
    """Instance of UserData using minium input variables to map to ODAPCatData."""

    def __init__(
        self,
        ds: Union[str, Path, xr.Dataset],
        proj_ds: Any,
        x_coord: str,
        y_coord: str,
        t_coord: str,
        var: List[str],
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        proj_feature: str,
        id_feature: str,
        period: List[str],
    ) -> None:
        """Contains data preperation methods based on UserData.

        Args:
            ds (Union[str, Path, xr.Dataset]): _description_
            proj_ds (Any): _description_
            x_coord (str): _description_
            y_coord (str): _description_
            t_coord (str): _description_
            var (List[str]): _description_
            f_feature (Union[str, Path, gpd.GeoDataFrame]): _description_
            proj_feature (str): _description_
            id_feature (str): _description_
            period (List[str]): List of 2 datetime strings representing start and end of
                period of interest.

        Raises:
            TypeError: _description_
        """
        self.ds = ds
        self.proj_ds = proj_ds
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.t_coord = t_coord
        # self.period = pd.to_datetime(period)
        self.period = period
        if not isinstance(var, List):
            raise TypeError(f"Input var {var} should be a list of variables")
        self.var = var
        self.f_feature = f_feature
        self.proj_feature = proj_feature
        self.id_feature = id_feature

    @classmethod
    def __repr__(cls) -> str:
        """Print class name."""
        return f"Class is {cls.__name__}"

    def get_feature_id(self) -> str:
        """Return id_feature."""
        return self.id_feature

    def get_vars(self) -> list[str]:
        """Return list of vars in data."""
        return self.var

    def prep_agg_data(self, key: str) -> AggData:
        """Prep AggData from UserData."""
        ds = self._get_xr_dataset()

        gdf_in = self._get_geodataframe()

        gdf_in.set_crs(self.proj_feature, inplace=True)

        gdf_bounds = _get_shp_bounds_w_buffer(
            gdf=gdf_in, ds=ds, crs=self.proj_ds, lon=self.x_coord, lat=self.y_coord
        )

        is_intersect, is_degrees, is_0_360 = _check_for_intersection_nc(
            ds=ds,
            x_name=self.x_coord,
            y_name=self.y_coord,
            proj=self.proj_ds,
            gdf=gdf_in,
        )

        if bool((not is_intersect) & is_degrees & (not is_0_360)):  # rotate
            ds.coords[self.x_coord] = (ds.coords[self.x_coord] + 180) % 360 - 180
            ds = ds.sortby(ds[self.x_coord])

        # calculate toptobottom (order of latitude coords)
        ttb = _get_top_to_bottom(ds, self.y_coord)

        subset_dict = build_subset(
            bounds=gdf_bounds,
            xname=self.x_coord,
            yname=self.y_coord,
            tname=self.t_coord,
            toptobottom=ttb,
            date_min=self.period[0],
            date_max=self.period[1],
        )

        data_ss = ds[key].sel(**subset_dict)
        cplist = self._get_user_catparams(da=data_ss)
        cglist = self._get_user_catgrids(da=data_ss)

        param_dict = dict(zip([key], cplist))  # noqa B905
        grid_dict = dict(zip([key], cglist))  # noqa B905

        # print(param_dict)

        return AggData(
            variable=key,
            cat_param=CatParams(**param_dict.get(key)),
            cat_grid=CatGrids(**grid_dict.get(key)),
            da=data_ss,
            feature=gdf_in,
            id_feature=self.id_feature,
            period=self.period,
        )

    def _get_user_catgrids(self, da: xr.DataArray):
        """Get CatGrids from UserData."""
        cglist = []
        for _var in self.var:
            cg = CatGrids(
                X_name=self.x_coord,
                Y_name=self.y_coord,
                proj=self.proj_ds,
                resX=max(np.diff(da[self.x_coord].values)),
                resY=max(np.diff(da[self.y_coord].values)),
                toptobottom=_get_top_to_bottom(da, self.y_coord),
            )
            cglist.append(cg.dict())
        return cglist

    def _get_ds_var_attrs(self, da: xr.DataArray, attr: str) -> str:
        """Return var attributes.

        Args:
            da (xr.DataArray): _description_
            attr (str): _description_

        Returns:
            str: _description_
        """
        try:
            return da.attrs.get(attr)
        except KeyError:
            return "None"

    def _get_user_catparams(self, da: xr.DataArray):
        """Get CatParams from UserData."""
        cplist = []
        for _var in self.var:
            cp = CatParams(
                URL="",
                varname=_var,
                long_name=self._get_ds_var_attrs(da, "long_name"),
                T_name=self.t_coord,
                units=self._get_ds_var_attrs(da, "units"),
            )
            cplist.append(cp.dict())
        return cplist

    def prep_wght_data(self) -> WeightData:
        """Prepare and return WeightData for weight generation."""
        ds = self._get_xr_dataset()

        gdf_in = self._get_geodataframe()

        gdf_in.set_crs(self.proj_feature, inplace=True)

        gdf_bounds = _get_shp_bounds_w_buffer(
            gdf=gdf_in, ds=ds, crs=self.proj_ds, lon=self.x_coord, lat=self.y_coord
        )

        is_intersect, is_degrees, is_0_360 = _check_for_intersection_nc(
            ds=ds,
            x_name=self.x_coord,
            y_name=self.y_coord,
            proj=self.proj_ds,
            gdf=gdf_in,
        )

        if bool((not is_intersect) & is_degrees & (not is_0_360)):  # rotate
            print("rotating")
            ds.coords[self.x_coord] = (ds.coords[self.x_coord] + 180) % 360 - 180
            ds = ds.sortby(ds[self.x_coord])

        # calculate toptobottom (order of latitude coords)
        ttb = _get_top_to_bottom(ds, self.y_coord)

        subset_dict = build_subset(
            bounds=gdf_bounds,
            xname=self.x_coord,
            yname=self.y_coord,
            tname=self.t_coord,
            toptobottom=ttb,
            date_min=self.period[0],
        )

        print(subset_dict)

        data_ss_wght = ds.sel(**subset_dict)

        start = time.perf_counter()
        grid_poly = _get_cells_poly(
            xr_a=data_ss_wght,
            x=self.x_coord,
            y=self.y_coord,
            crs_in=self.proj_ds,
        )
        end = time.perf_counter()
        print(
            f"Generating grid-cell bounds finished in {round(end-start, 2)} second(s)"
        )
        return WeightData(
            feature=gdf_in, id_feature=self.id_feature, grid_cells=grid_poly
        )

    def _get_geodataframe(self):
        """Get GeoDataFrame."""
        if not isinstance(self.f_feature, gpd.GeoDataFrame):
            return gpd.read_file(self.f_feature)
        else:
            return self.f_feature

    def _get_xr_dataset(self):
        """Get xarray.Dataset."""
        if not isinstance(self.ds, xr.Dataset):
            ds = xr.open_dataset(self.ds)
        else:
            ds = self.ds
        return ds


class UserTiffData(UserData):
    """Instance of UserData for zonal stats processing of geotiffs."""

    def __init__(
        self,
        var: str,
        ds: Union[str, xr.Dataset],
        proj_ds: Any,
        x_coord: str,
        y_coord: str,
        bname: str,
        band: int,
        f_feature: Union[str, Path, gpd.GeoDataFrame],
        id_feature: str,
        proj_feature: Any,
    ) -> None:
        """__init__ Initialize UserTiffData.

        UserTiffData is a structure that aids calculating zonal stats.

        Args:
            var (str): _description_
            ds (Union[str, xr.Dataset]): _description_
            proj_ds (Any): _description_
            x_coord (str): _description_
            y_coord (str): _description_
            bname (str): _description_
            band (int): _description_
            f_feature (Union[str, Path, gpd.GeoDataFrame]): _description_
            id_feature (str): _description_
            proj_feature (Any): _description_
        """
        self.varname = var
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.bname = bname
        self.band = band
        self.toptobottom = None
        self._get_rxr_dataset(ds)
        self.proj_ds = proj_ds
        self._get_geodataframe(f_feature)
        self.id_feature = id_feature
        self.proj_feature = proj_feature
        self.f_feature = self.f_feature.sort_values(self.id_feature).dissolve(
            by=self.id_feature, as_index=False
        )
        self.f_feature.reset_index()

        self._check_xname()
        self._check_yname()
        self._check_band()
        self._check_crs()
        self._get_toptobottom()

    def get_vars(self) -> list[str]:
        """Return list of varnames."""
        return [self.varname]

    def get_feature_id(self) -> str:
        """Get Feature id."""
        return self.id_feature

    def prep_wght_data(self) -> WeightData:
        """Prepare data for weight generation."""
        pass

    def prep_agg_data(self, key: str) -> AggData:
        """Prepare data for aggregation or zonal stats."""
        bb_feature = _get_shp_bounds_w_buffer(
            gdf=self.f_feature,
            ds=self.ds,
            crs=self.proj_ds,
            lon=self.x_coord,
            lat=self.y_coord,
        )

        subset_dict = build_subset_tiff(
            bounds=bb_feature,
            xname=self.x_coord,
            yname=self.y_coord,
            toptobottom=self.toptobottom,
            bname=self.bname,
            band=self.band,
        )

        data_ss = self.ds.sel(**subset_dict)  # .rio.interpolate_na()
        # tstrt = time.perf_counter()
        # data_ss = data_ss.rio.interpolate_na(method='nearest')
        # tend = time.perf_counter()
        # print(f"fill missing data using nearest method in {tend - tstrt:0.4f} seconds")
        cplist = self._get_user_catparams(da=data_ss)
        cglist = self._get_user_catgrids(da=data_ss)
        param_dict = dict(zip([key], [cplist]))  # noqa B905
        grid_dict = dict(zip([key], [cglist]))  # noqa B905

        return AggData(
            variable=key,
            cat_param=CatParams(**param_dict.get(key)),
            cat_grid=CatGrids(**grid_dict.get(key)),
            da=data_ss,
            feature=self.f_feature,
            id_feature=self.id_feature,
            period=["None", "None"],
        )

    def _get_toptobottom(self):
        """Generate toptobottom."""
        yy = self.ds.coords[self.y_coord].values
        self.toptobottom = yy[0] <= yy[-1]

    def _check_xname(self):
        """Validate xname."""
        if self.x_coord not in self.ds.coords:
            raise ValueError(f"xname:{self.x_coord} not in {self.ds.coords}")

    def _check_yname(self):
        """Validate yname."""
        if self.y_coord not in self.ds.coords:
            raise ValueError(f"yname:{self.y_coord} not in {self.ds.coords}")

    def _check_band(self):
        """Validate band name."""
        if self.bname not in self.ds.coords:
            raise ValueError(f"band:{self.bname} not in {self.ds.coords}")

    def _check_crs(self):
        """Validate crs."""
        crs = CRS.from_user_input(self.proj_ds)
        if not isinstance(crs, CRS):
            raise ValueError(f"ds_proj:{self.proj_ds} not in valid")
        crs2 = CRS.from_user_input(self.proj_feature)
        if not isinstance(crs2, CRS):
            raise ValueError(f"ds_proj:{self.proj_feature} not in valid")

    def _get_rxr_dataset(self, ds: Union[str, xr.DataArray, xr.Dataset]):
        """Get xarray.Dataset."""
        if not isinstance(ds, (xr.Dataset, xr.DataArray)):
            self.ds = rxr.open_rasterio(ds)
        else:
            self.ds = ds

    def _get_geodataframe(self, f_feature: gpd.GeoDataFrame):
        """Get GeoDataFrame."""
        if not isinstance(f_feature, gpd.GeoDataFrame):
            self.f_feature = gpd.read_file(f_feature)
        else:
            self.f_feature = f_feature

    def _get_user_catgrids(self, da: xr.DataArray):
        """Get CatGrids from UserData."""
        cg = CatGrids(
            X_name=self.x_coord,
            Y_name=self.y_coord,
            proj=self.proj_ds,
            resX=max(np.diff(da[self.x_coord].values)),
            resY=max(np.diff(da[self.y_coord].values)),
            toptobottom=self.toptobottom,
        )
        return cg.dict()

    def _get_user_catparams(self, da: xr.DataArray):
        """Get CatParams from UserData."""
        cp = CatParams(
            URL="",
            varname=self.varname,
            long_name=self._get_ds_var_attrs(da, "long_name"),
            T_name="",
            units=self._get_ds_var_attrs(da, "units"),
        )
        return cp.dict()

    def _get_ds_var_attrs(self, da: xr.DataArray, attr: str) -> str:
        """Return var attributes.

        Args:
            da (xr.DataArray): _description_
            attr (str): _description_

        Returns:
            str: _description_
        """
        try:
            return da.attrs.get(attr)
        except KeyError:
            return "na"
