from __future__ import annotations

import json
import logging
from typing import Union, Optional

from astropy.coordinates import SkyCoord, Angle
from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

PHOTOMETRY_DEFAULT_LIMIT = 10000


class PhotometryClass:
    """
    The photometry class.
    Use to retrieve data from the photometry database.

    **A photometry instance is already provided, to use it:**

    >>> from dace_query.photometry import Photometry
    """
    __ACCEPTED_FILE_TYPES = ['s1d', 's2d', 'ccf', 'bis', 'all']
    __OBS_API = 'obs-webapp'
    __OBSERVATION_ENDPOINT = __OBS_API + 'observation/'
    __PHOTOMETRY_ENDPOINT = __OBSERVATION_ENDPOINT + 'photometry/'

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable photometry object which uses a specified dace.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.photometry import PhotometryClass
        >>> photometry_instance = PhotometryClass()
        """
        # Logging configuration
        self.log = logging.getLogger("Photometry")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        elif isinstance(dace_instance, DaceClass):
            self.dace = dace_instance
        else:
            raise Exception("Dace instance is not valid")

    def query_database(self,
                       limit: Optional[int] = PHOTOMETRY_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:

        """
        Query the photometry database to retrieve data in the chosen format.

        Filters and sorting order can be applied to the query via named arguments (see :doc:`query_options`).

        All available formats are defined in this section (see :doc:`output_format`).

        :param limit: Maximum number of rows to return
        :type limit: Optional[int]
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param sort: Sort order to apply to the query
        :type sort: Optional[dict]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.photometry import Photometry
        >>> values =  Photometry.query_database()

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OBS_API,
                endpoint='observation/search/photometry',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }
            ), output_format=output_format
        )

    def query_region(self,
                     sky_coord: SkyCoord,
                     angle: Angle,
                     limit: Optional[int] = PHOTOMETRY_DEFAULT_LIMIT,
                     filters: Optional[dict] = None,
                     output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query a region, based on SkyCoord and Angle objects, in the photometry database and retrieve data in the chosen
        format.

        Filters can be applied to the query via named arguments (see :doc:`query_options`).

        All available formats are defined in this section (see :doc:`output_format`).

        :param sky_coord: Sky coordinates object from the astropy module
        :type sky_coord: SkyCoord
        :param angle: Angle object from the astropy module
        :type angle: Angle
        :param limit: Maximum number of rows to return
        :type limit: Optional[int]
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.photometry import Photometry
        >>> from astropy.coordinates import SkyCoord, Angle
        >>> sky_coord, angle = SkyCoord("11h01m04s", "+04d29m10s", frame='icrs'), Angle('0.045d')
        >>> values = Photometry.query_region(sky_coord=sky_coord, angle=angle)
        """

        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(limit=limit, filters=filters_with_coordinates, output_format=output_format)

    def get_timeseries(self, target: str) -> list:
        """
        Retrieve photometry timeseries for a specified target.

        :param target: The target to retrieve data from
        :type target: str
        :return: The desired data
        :rtype: list

        >>> from dace_query.photometry import Photometry
        >>> target_to_search = "EPIC201750173"
        >>> values = Photometry.get_timeseries(target=target_to_search)
        """
        result = self.dace.request_get(
            api_name=self.__OBS_API,
            endpoint=f'observation/photometry/{target}'
        )
        if not result:
            return None
        return result['observations']


Photometry: PhotometryClass = PhotometryClass()
"""A photometry instance"""
