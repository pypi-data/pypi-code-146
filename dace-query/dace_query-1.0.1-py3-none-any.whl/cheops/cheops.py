from __future__ import annotations

import json
import logging
from typing import Union, Optional

from astropy.coordinates import SkyCoord, Angle
from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

CHEOPS_DEFAULT_LIMIT = 10000


class CheopsClass:
    """
    The cheops class.
    Use to retrieve data from the cheops module.

    **A cheops instance is already provided, to use it :**
    """
    __ACCEPTED_FILE_TYPES = ['lightcurves', 'images', 'reports', 'full', 'sub', 'all']
    __ACCEPTED_CATALOGS = ['planet', 'stellar']

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable cheops object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.cheops import CheopsClass
        >>> cheops_instance = CheopsClass()

        """
        # Logging configuration
        self.__CHEOPS_API = 'cheops-webapp'
        self.log = logging.getLogger("Cheops")
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
                       limit: Optional[int] = CHEOPS_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the cheops database to retrieve available visits in the chosen format.

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

        >>> from dace_query.cheops import Cheops
        >>> values = Cheops.query_database()
        """

        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__CHEOPS_API,
                endpoint='search',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }
            ), output_format=output_format)

    def query_catalog(self,
                      catalog: str,
                      limit: Optional[int] = CHEOPS_DEFAULT_LIMIT,
                      filters: Optional[dict] = None,
                      sort: Optional[dict] = None,
                      output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the cheops, either stellar or planet, catalogs.

        Available catalogs are [ 'planet', 'stellar' ].

        Filters and sorting order can be applied to the query via named arguments (see :doc:`query_options`).

        All available formats are defined in this section (see :doc:`output_format`).

        :param catalog: The catalog name
        :type catalog: str
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

        >>> from dace_query.cheops import Cheops
        >>> catalog_to_search = 'planet'
        >>> values = Cheops.query_catalog(catalog_to_search)
        """

        if catalog not in self.__ACCEPTED_CATALOGS:
            raise ValueError('catalog must be one of these values : ' + ','.join(self.__ACCEPTED_CATALOGS))

        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__CHEOPS_API,
                endpoint=f'catalog/{catalog}',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }), output_format=output_format)

    def query_region(self,
                     sky_coord: SkyCoord,
                     angle: Angle,
                     limit: Optional[int] = CHEOPS_DEFAULT_LIMIT,
                     filters: Optional[dict] = None,
                     output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query a region, based on SkyCoord and Angle objects, in the Cheops database and retrieve data in the chosen
        format.

        Filters and sorting order can be applied to the query via named arguments (see :doc:`query_options`).

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


        >>> from dace_query.cheops import Cheops
        >>> from astropy.coordinates import SkyCoord, Angle
        >>> sky_coord, angle = SkyCoord("22h23m29s", "+32d27m34s", frame='icrs'), Angle('0.045d')
        >>> values = Cheops.query_region(sky_coord=sky_coord, angle=angle)

        """

        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(limit=limit, filters=filters_with_coordinates, output_format=output_format)

    def get_lightcurve(self,
                       target: str,
                       aperture: Optional[str] = 'default',
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Get the photometry data (from Cheops) in the chosen format for a specified target.

        Aperture types available are [ 'default', 'optimal, 'rinf', 'rsup' ].

        Filters and sorting order can be applied to the query via named arguments (see :doc:`query_options`).

        All available formats are defined in this section (see :doc:`output_format`).

        :param target: The target to retrieve light curve from
        :type target: str
        :param aperture: Aperture type
        :type aperture: Optional[str]
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param sort: Sort order to apply to the query
        :type sort: Optional[dict]
        :param output_format: The desired data in the chosen output format
        :type output_format: Optional[str]
        :return: The desired data in the chosen format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.cheops import Cheops
        >>> values = Cheops.get_lightcurve('WASP-8')
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        # a = 'photometry/' + target + '?aperture=' + aperture + '&filters=' +
        # self.dace.transform_dict_to_encoded_json(filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__CHEOPS_API,
                endpoint=f'photometry/{target}',
                params={
                    'aperture': str(aperture),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }), output_format=output_format
        )

    def download(self,
                 file_type: str,
                 filters: Optional[dict] = None,
                 output_directory: Optional[str] = None,
                 output_filename: Optional[str] = None) -> None:
        """
        Download CHEOPS products (FITS, PDF,...) for specific visits and save it locally depending on the specified
        arguments.

        Filters can be applied to the query via named arguments (see :doc:`query_options`).

        File types available are [ 'lightcurves', 'images', 'reports', 'full', 'sub', 'all' ].

        All available formats are defined in this section (see :doc:`output_format`).

        :param file_type: The type of files to download
        :type file_type: str
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.cheops import Cheops
        >>> filters_to_use = {'file_key': {'contains': 'CH_PR300001_TG000301_V0000'}}
        >>> # Cheops.download('all', filters_to_use, output_directory='/tmp', output_filename='cheops.tar.gz')

        """
        if file_type not in self.__ACCEPTED_FILE_TYPES:
            raise ValueError('file_type must be one of these values : ' + ','.join(self.__ACCEPTED_FILE_TYPES))
        if filters is None:
            filters = {}

        cheops_data = self.query_database(filters=filters, output_format='dict')

        files = []
        if 'file_rootpath' in cheops_data:
            files = cheops_data['file_rootpath']

        download_id = self.dace.request_post(
            api_name=self.__CHEOPS_API,
            endpoint='download',
            data=json.dumps({'fileType': file_type, 'files': files})
        )
        if not download_id:
            return None

        self.dace.persist_file_on_disk(
            api_name=self.__CHEOPS_API,
            obs_type='photometry',
            download_id=download_id['key'],
            output_directory=output_directory,
            output_filename=output_filename
        )

    def download_diagnostic_movie(self,
                                  file_key: str,
                                  aperture: Optional[str] = 'default',
                                  output_directory: Optional[str] = None,
                                  output_filename: Optional[str] = None) -> None:
        """
        Download diagnostic movie for a Cheops file_key.

        Aperture types available are [ 'default', 'optimal, 'rinf', 'rsup' ].

        :param file_key: The cheops visit file key
        :type file_key: str
        :param aperture: Apertures types
        :type aperture: Optional[str]
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename:  The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.cheops import Cheops
        >>> # Cheops.download_diagnostic_movie(file_key='CH_PR100018_TG027204_V0200', output_directory='/tmp', output_filename='cheops_movie.mp4')

        """
        self.dace.download_file(
            api_name=self.__CHEOPS_API,
            endpoint=f'diagnosticMovie/{file_key}',
            params={
                'aperture': str(aperture)
            },
            output_directory=output_directory,
            output_filename=output_filename
        )


Cheops: CheopsClass = CheopsClass()
"""
Cheops instance
"""
