"""Method for saving aggregation data."""
import warnings
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import pyproj
import xarray as xr
from shapely.geometry import Point

from gdptools.data.agg_gen_data import AggData


class AggDataWriter(ABC):
    """Abstract writer Template method."""

    def save_file(
        self: "AggDataWriter",
        agg_data: List[AggData],
        feature: gpd.GeoDataFrame,
        vals: List[npt.NDArray[Union[np.integer, np.double]]],
        p_out: str,
        file_prefix: str,
        append_date: Optional[bool] = False,
    ) -> None:
        """Abstract Template method for writing aggregation data.

        Args:
            agg_data (List[AggData]): _description_
            feature (gpd.GeoDataFrame): _description_
            vals (List[npt.NDArray[Union[int, np.double]]]): _description_
            p_out (str): _description_
            file_prefix (str): _description_
            append_date (Optional[bool], optional): _description_. Defaults to False.

        Raises:
            FileNotFoundError: _description_
        """
        self.agg_data = agg_data
        self.feature = feature
        self.vals = vals
        self.append_date = append_date
        self.fdate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.outpath = Path(p_out)
        if not self.outpath.exists():
            raise FileNotFoundError(f"Path: {p_out} does not exist")
        if self.append_date:
            self.fname = f"{self.fdate}_{file_prefix}"
        else:
            self.fname = f"{file_prefix}"

        self.create_out_file()

    @abstractmethod
    def create_out_file(self) -> None:
        """Abstract method for writing aggregation data."""
        pass


class CSVWriter(AggDataWriter):
    """Class for writing csv files."""

    def create_out_file(self) -> None:
        """Method for writing csv files."""
        # for idx in range(len(self.agg_data)):
        for idx, (_key, value) in enumerate(self.agg_data.items()):
            gdf = self.feature
            # gdf_idx = self.agg_data[idx].id_feature
            param_values = value.cat_param
            t_coord = param_values.T_name
            units = param_values.units
            varname = param_values.varname
            time = value.da.coords[t_coord].values
            # units = self.agg_data[idx].param_dict

            df_key = pd.DataFrame(data=self.vals[idx], columns=gdf.index.T.values)

            df_key.insert(0, "units", [units] * df_key.shape[0])
            df_key.insert(0, "varname", [varname] * df_key.shape[0])
            df_key.insert(0, "time", time)

            if idx == 0:
                df = df_key
            else:
                pd.concat([df, df_key])
        df.reset_index(inplace=True)
        path_to_file = self.outpath / f"{self.fname}.csv"
        print(f"Saving csv file to {path_to_file}")
        df.to_csv(path_to_file)


class NetCDFWriter(AggDataWriter):
    """NetCDF writer class."""

    def create_out_file(self) -> None:
        """Create NetCDF file from aggregation data."""
        # Suppres UserWarning from centroid calc - Here lat/lon centroid are
        # a convenience method.
        warnings.filterwarnings(action="ignore", category=UserWarning)
        dataset = []
        # for idx in range(len(self.agg_data)):
        for idx, (_key, value) in enumerate(self.agg_data.items()):
            gdf = self.feature
            gdf_idx = value.id_feature
            # param_values = list(self.agg_data[idx].param_dict.values())[idx]
            param_values = value.cat_param
            t_coord = param_values.T_name
            v_units = param_values.units
            v_varname = param_values.varname
            v_long_name = param_values.long_name
            time = value.da.coords[t_coord].values
            locs = gdf.index.values

            def getxy(pt: Point) -> Tuple[np.double, np.double]:
                """Return x y components of point."""
                return pt.x, pt.y

            centroid_series = gdf.geometry.centroid
            tlon, tlat = [
                list(t) for t in zip(*map(getxy, centroid_series))  # noqa B905
            ]
            crs_meta = pyproj.CRS(gdf.crs).to_cf()

            dsn = xr.Dataset(
                data_vars={
                    v_varname: (
                        ["time", gdf_idx],
                        self.vals[idx],
                        dict(
                            units=v_units,
                            long_name=v_long_name,
                            coordinates="time lat lon",
                            grid_mapping="crs",
                        ),
                    ),
                    "crs": (["one"], np.ones((1), dtype=np.double), crs_meta),
                },
                coords={
                    "time": time,
                    gdf_idx: ([gdf_idx], locs, {"feature_id": gdf_idx}),
                    "lat": (
                        [gdf_idx],
                        tlat,
                        {
                            "long_name": "Latitude of HRU centroid",
                            "units": "degrees_north",
                            "standard_name": "latitude",
                            "axis": "Y",
                        },
                    ),
                    "lon": (
                        [gdf_idx],
                        tlon,
                        {
                            "long_name": "Longitude of HRU centroid",
                            "units": "degrees_east",
                            "standard_name": "longitude",
                            "axis": "X",
                        },
                    ),
                },
            )

            dataset.append(dsn)
        # crs_cf = pyproj.CRS(gdf.crs).to_cf()
        # da = xr.DataArray(
        #     data=np.ones((1), dtype=np.double),
        #     attrs=crs_cf
        # )
        # data_array.append(da)
        ds = xr.merge(dataset)
        # ds = ds.assign(
        #     crs=(["one"], np.ones((1), dtype=np.double))
        # )
        # ds = ds.assign_coords(lat=tlat)
        # ds.lat.attrs = {
        #     "long_name": "Latitude of HRU centroid",
        #     "units": "degrees_north",
        #     "standard_name": "latitude",
        #     "axis": "Y"}

        # ds = ds.assign_coords(lon=tlon)
        # ds.lon.attrs = {
        #     "long_name": "Longitude of HRU centroid",
        #     "units": "degrees_east",
        #     "standard_name": "longitude",
        #     "axis": "X"}
        # ds.crs.attrs = crs_cf
        ds.attrs = {
            "Conventions": "CF-1.8",
            "featureType": "timeSeries",
            "history": (
                f"{self.fdate} Original filec created  by gdptools package: "
                "https://code.usgs.gov/wma/nhgf/toolsteam/gdptools \n"
            ),
        }
        path_to_file = self.outpath / f"{self.fname}.nc"
        print(f"Saving netcdf file to {path_to_file}")
        ds.to_netcdf(path_to_file)
