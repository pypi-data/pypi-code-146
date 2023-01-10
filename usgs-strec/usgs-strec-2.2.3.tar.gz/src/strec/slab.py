# stdlib imports
import logging
import pathlib
import tarfile
import zipfile
from io import BytesIO

# third party imports
import numpy as np
import pandas as pd
import rasterio
import requests
from rasterio.windows import Window

MAX_INTERFACE_DEPTH = 70  # depth beyond which any tectonic regime has to be intraslab

# Slab 1.0 does not have depth uncertainty, so we make this a constant
DEFAULT_DEPTH_ERROR = 10

ITEM_TEMPLATE = "http://www.sciencebase.gov/catalog/file/get/[ITEMID]"
SEARCH_URL = "https://www.sciencebase.gov/catalog/items?s=Search&q=slab2&format=json"
KEYWORDS = ["subduction", "model", "slab2"]


def get_slab_grids(path):
    if not path.exists():
        path.mkdir(parents=True)
    response = requests.get(SEARCH_URL)
    jdict = response.json()
    for item in jdict["items"]:
        ititle = item["title"].lower()
        # is this the droid we're looking for?
        if not item["hasChildren"]:
            continue
        score = 0
        for keyword in KEYWORDS:
            if keyword in ititle:
                score += 1
        if score < 2:
            continue
        itemid = item["id"]
        item_url = ITEM_TEMPLATE.replace("[ITEMID]", itemid)
        response = requests.get(item_url)
        bytes = BytesIO(response.content)
        nfiles = 0
        with zipfile.ZipFile(bytes, "r") as myzip:
            for name in myzip.namelist():
                if not name.endswith("tar.gz"):
                    continue
                tarbytes = myzip.read(name)
                try:
                    my_tarfile = path / name
                    with open(my_tarfile, "wb") as tar:
                        tar.write(tarbytes)
                    with tarfile.open(my_tarfile, "r") as mytar:
                        for member_str in mytar.getnames():
                            if not member_str.endswith(".grd"):
                                continue
                            outfile = path / pathlib.Path(member_str).name
                            member = mytar.getmember(member_str)
                            logging.info(f"Unpacking slab grid {member_str}...")
                            with mytar.extractfile(member) as in_object:
                                with open(outfile, "wb") as out_object:
                                    out_object.write(in_object.read())
                                    nfiles += 1
                except Exception as e:
                    return (
                        False,
                        f"Unable to download Slab2 grids from {SEARCH_URL} - error {str(e)}.",
                    )
    return (True, f"Downloaded {nfiles} grid files from {SEARCH_URL} to {path}")


class GridSlab(object):
    """Represents USGS Slab model grids for a given subduction zone."""

    def __init__(self, depth_file, dip_file, strike_file, error_file):
        """Construct GridSlab object from input files.

        Args:
            depth_file (str): Path to Slab depth grid file.
            dip_file (str): Path to Slab dip grid file.
            strike_file (str): Path to Slab strike grid file.
            error_file (str): Path to Slab depth error grid file (can be None).
        """
        self._depth_file = pathlib.Path(depth_file)
        self._dip_file = pathlib.Path(dip_file)
        self._strike_file = pathlib.Path(strike_file)
        self._error_file = pathlib.Path(error_file)

        # there may be a table of maximum slab depths in the same directory
        # as all of the slab grids.  Read it into a local dictionary if found,
        # otherwise we'll use the MAX_INTERFACE_DEPTH constant found above.
        table_file_name = (
            pathlib.Path(__file__).parent / "data" / "maximum_interface_depths.csv"
        )
        if table_file_name.is_file():
            self._slab_table = pd.read_csv(table_file_name)
        else:
            self._slab_table = None

    def getGridValue(self, grid, lat, lon):
        # rasterio does geo-referencing on grid-line basis, we do it on pixel basis
        # (half pixel down and to the right)
        xmax, _ = grid.xy(grid.height, grid.width)
        if xmax > 180:
            lon += 360
        row, col = grid.index(lon, lat)
        nrows, ncols = grid.shape
        if row < 0 or row > nrows - 1 or col < 0 or col > ncols - 1:
            return np.nan

        value = grid.read(1, window=Window(col, row, 1, 1))[0][0]
        return value

    def contains(self, lat, lon):
        """Check to see if input coordinates are contained inside Slab model.

        Args:
            lat (float):  Hypocentral latitude in decimal degrees.
            lon (float):  Hypocentral longitude in decimal degrees.
        Returns:
            bool: True if point falls inside minimum bounding box of slab model.
        """
        with rasterio.open(self._depth_file, "r") as dataset:
            xmin, ymax = dataset.xy(0, 0)
            xmax, ymin = dataset.xy(dataset.height, dataset.width)
            if xmax > 180:
                lon += 360
        if lat >= ymin and lat <= ymax and lon >= xmin and lon <= xmax:
            return True
        return False

    def getSlabInfo(self, lat, lon):
        """Return a dictionary with depth,dip,strike, and depth uncertainty.

        Args:
            lat (float):  Hypocentral latitude in decimal degrees.
            lon (float):  Hypocentral longitude in decimal degrees.
        Returns:
            dict: Dictionary containing keys:
                - region Three letter Slab model region code.
                - strike Slab model strike angle.
                - dip Slab model dip angle.
                - depth Slab model depth (km).
                - depth_uncertainty Slab model depth uncertainty.
        """
        slabinfo = {}
        if not self.contains(lat, lon):
            return slabinfo
        fname = self._depth_file.with_suffix("").name
        parts = fname.split("_")
        region = parts[0]

        with rasterio.open(self._depth_file, "r") as depth_grid:
            # slab grids are negative depth
            depth = -1 * self.getGridValue(depth_grid, lat, lon)

        with rasterio.open(self._dip_file, "r") as dip_grid:
            dip = self.getGridValue(dip_grid, lat, lon)

        with rasterio.open(self._strike_file, "r") as strike_grid:
            strike = self.getGridValue(strike_grid, lat, lon)
            if strike < 0:
                strike += 360

        error = DEFAULT_DEPTH_ERROR
        with rasterio.open(self._error_file, "r") as error_grid:
            error = self.getGridValue(error_grid, lat, lon)
            if np.isnan(strike):
                error = np.nan

        # get the maximum interface depth from table (if present)
        if self._slab_table is not None:
            df = self._slab_table
            max_int_depth = df[df["zone"] == region].iloc[0]["interface_max_depth"]
        else:
            max_int_depth = MAX_INTERFACE_DEPTH

        slabinfo = {
            "region": region,
            "strike": strike,
            "dip": dip,
            "depth": depth,
            "maximum_interface_depth": max_int_depth,
            "depth_uncertainty": error,
        }
        return slabinfo


class SlabCollection(object):
    def __init__(self, datafolder):
        """Object representing a collection of SlabX.Y grids.

        This object can be queried with a latitude/longitude to see if that point is
        within a subduction slab - if so, the slab information is returned.

        Args:
            datafolder (str): String path where grid files and GeoJSON file reside.
        """
        datafolder = pathlib.Path(datafolder)
        self._depth_files = datafolder.glob("*_dep*.grd")

    def getSlabInfo(self, lat, lon, depth):
        """Query the entire set of slab models and return a SlabInfo object, or None.

        Args:
            lat (float):  Hypocentral latitude in decimal degrees.
            lon (float):  Hypocentral longitude in decimal degrees.
            depth (float): Hypocentral depth in km.

        Returns:
            dict: Dictionary containing keys:
                - region Three letter Slab model region code.
                - strike Slab model strike angle.
                - dip Slab model dip angle.
                - depth Slab model depth (km).
                - depth_uncertainty Slab model depth uncertainty.
        """

        deep_depth = 99999999999
        slabinfo = {}
        # loop over all slab regions, return keep all slabs found
        for depth_file in self._depth_files:
            dip_file = pathlib.Path(str(depth_file).replace("dep", "dip"))
            strike_file = pathlib.Path(str(depth_file).replace("dep", "str"))
            error_file = pathlib.Path(str(depth_file).replace("dep", "unc"))
            if not error_file.is_file():
                error_file = None
            gslab = GridSlab(depth_file, dip_file, strike_file, error_file)
            tslabinfo = gslab.getSlabInfo(lat, lon)
            if not len(tslabinfo):
                continue
            else:
                depth = tslabinfo["depth"]
                if depth < deep_depth:
                    slabinfo = tslabinfo.copy()
                    deep_depth = depth
                elif np.isnan(depth) and "depth" not in slabinfo:
                    slabinfo = tslabinfo.copy()

        return slabinfo
