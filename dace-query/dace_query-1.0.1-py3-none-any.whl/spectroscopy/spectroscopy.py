from __future__ import annotations

import json
import logging
from typing import Union, Optional

from astropy.coordinates import SkyCoord, Angle
from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass
from dace_query.dace import NoDataException

SPECTROSCOPY_DEFAULT_LIMIT = 10000


class SpectroscopyClass:
    """
    The spectroscopy class.
    Use to retrieve data from the spectroscopy module.

    **A spectroscopy instance is already provided, to use it:**

    >>> from dace_query.spectroscopy import Spectroscopy

    """
    ACCEPTED_FILE_TYPES = ['s1d', 's2d', 'ccf', 'bis', 'all']
    __OBS_API = 'obs-webapp'

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable spectroscopy object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.spectroscopy import SpectroscopyClass
        >>> spectroscopy_instance = SpectroscopyClass()
        """
        # Logging configuration
        self.log = logging.getLogger("Spectroscopy")
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
                       limit: Optional[int] = SPECTROSCOPY_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the spectroscopy database to retrieve data in the chosen format.

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

        >>> from dace_query.spectroscopy import Spectroscopy
        >>> values = Spectroscopy.query_database()

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OBS_API,
                endpoint='observation/search/spectroscopy',
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
                     limit: Optional[int] = SPECTROSCOPY_DEFAULT_LIMIT,
                     filters: Optional[dict] = None,
                     output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query a region, based on SkyCoord and Angle objects, in the spectroscopy database and retrieve data in the chosen format.

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

        >>> from dace_query.spectroscopy import Spectroscopy
        >>> from astropy.coordinates import SkyCoord, Angle
        >>> sky_coord, angle = SkyCoord("23h13m16s", "+57d10m06s", frame='icrs'), Angle('0.045d')
        >>> values = Spectroscopy.query_region(sky_coord=sky_coord, angle=angle)
        """
        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(limit=limit, filters=filters_with_coordinates, output_format=output_format)

    def download(self,
                 file_type: str,
                 filters: Optional[dict] = None,
                 output_directory: Optional[str] = None,
                 output_filename: Optional[str] = None):
        """
        Download Spectroscopy products (S1D, S2D, ...) and save it locally depending on the specified arguments.

        File type available are [ 's1d', 's2d', 'ccf', 'bis', 'guidance', 'all' ].

        Filters can be applied to the query via named arguments (see :doc:`query_options`).

        :param file_type: The type of files to download
        :type file_type: str
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]

        >>> from dace_query.spectroscopy import Spectroscopy
        >>> filters_to_use = {'file_rootpath': {'contains':['HARPS.2010-04-04T03:38:51.386.fits']}}
        >>> # Spectroscopy.download('s1d', filters=filters_to_use, output_filename='files.tar.gz')
        """
        if file_type not in self.ACCEPTED_FILE_TYPES:
            raise ValueError('file_type must be one of these values : ' + ','.join(self.ACCEPTED_FILE_TYPES))
        if filters is None:
            filters = {}

        spectroscopy_data = self.query_database(filters=filters, output_format='dict')
        files = spectroscopy_data['file_rootpath']
        download_response = self.dace.request_post(
            api_name=self.__OBS_API,
            endpoint='download/prepare/spectroscopy',
            data=json.dumps({
                'fileType': file_type,
                'files': files
            })
        )
        if not download_response:
            return None
        download_id = download_response['values'][0]

        self.dace.persist_file_on_disk(
            api_name=self.__OBS_API,
            obs_type='spectroscopy',
            download_id=download_id,
            output_directory=output_directory,
            output_filename=output_filename
        )

    def download_files(self,
                       files: list,
                       file_type: Optional[str] = 'all',
                       output_directory: Optional[str] = None,
                       output_filename: Optional[str] = None):
        """
        Download reduction products specified in argument for the list of raw files specified and save it locally.

        File type available are ['s1d', 's2d', 'ccf', 'bis', 'guidance', 'all']

        :param files: The raw files
        :param file_type: The type of files to download
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.spectroscopy import Spectroscopy
        >>> files_to_download = ['harps/DRS-3.5/reduced/2019-07-05/HARPS.2019-07-06T04:00:00.323.fits']
        >>> # Spectroscopy.download_files(files=files_to_download, file_type='all')
        """

        if files is None:
            raise NoDataException

        files = list(map(lambda file: f'{file}.fits' if not file.endswith('.fits') else file, files))
        # files = [file + '.fits' for file in files if '.fits' not in file]
        download_response = self.dace.request_post(
            api_name=self.__OBS_API,
            endpoint='download/prepare/spectroscopy',
            data=json.dumps(
                {'fileType': file_type, 'files': files}
            )
        )
        if not download_response:
            return None
        download_id = download_response['values'][0]

        self.dace.persist_file_on_disk(
            api_name=self.__OBS_API,
            obs_type='spectroscopy',
            download_id=download_id,
            output_directory=output_directory,
            output_filename=output_filename
        )

    def get_timeseries(self, target: str,
                       sorted_by_instrument: Optional[bool] = True,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Retrieve the spectroscopy time series data for a specified target in the chosen format.

        All available formats are defined in this section (see :doc:`output_format`).

        :param target: The target to retrieve data from.
        :type target: str
        :param sorted_by_instrument: Application of the instrument sorting
        :type sorted_by_instrument: Optional[bool]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.spectroscopy import Spectroscopy
        >>> target_to_search = "C15-0734"
        >>> values = Spectroscopy.get_timeseries(target=target_to_search)

        """
        spectroscopy_data = self.dace.request_get(
            api_name=self.__OBS_API,
            endpoint=f'observation/radialVelocities/{target}'
        )
        if not sorted_by_instrument:
            return self.dace.transform_to_format(spectroscopy_data, output_format=output_format)
        else:
            transformed_data = self.dace.transform_to_format(spectroscopy_data, output_format='numpy')
            return self.dace.order_spectroscopy_data_by_instruments(transformed_data)


Spectroscopy: SpectroscopyClass = SpectroscopyClass()
"""Spectroscopy instance"""
