from __future__ import annotations

import json
import logging
from typing import Optional

from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass
from dace_query.dace import NoDataException
from dace_query.spectroscopy import Spectroscopy

SUN_DEFAULT_LIMIT = 200000


class SunClass:
    """
    The sun class.
    Use to retrieve data from the sun module.

    **A sun instance is already provided, to use it :**

    >>> from dace_query.sun import Sun

    """

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable sun object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.sun import SunClass
        >>> sun_instance = SunClass()

        """
        # Logging configuration
        self.__OBS_API = 'obs-webapp'
        self.log = logging.getLogger("Sun")
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
                       limit: Optional[int] = SUN_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None):
        """
        Query the sun database to retrieve data in the chosen format.

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

        >>> from dace_query.sun import Sun
        >>> values = Sun.query_database()

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OBS_API,
                endpoint='sun/search',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }
            ), output_format=output_format
        )

    def get_timeseries(self, output_format: Optional[str] = None):
        """
        Get all sun timeseries.

        All available formats are defined in this section (see :doc:`output_format`).

        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format

        >>> from dace_query.sun import Sun
        >>> values = Sun.get_timeseries()
        """
        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OBS_API,
                endpoint='sun/radialVelocities',
            ), output_format=output_format
        )

    def download(self,
                 file_type: str,
                 filters: Optional[dict] = None,
                 output_directory: Optional[str] = None,
                 output_filename: Optional[str] = None) -> None:
        """
        Download Sun spectroscopy products (S1D, S2D, ...).

        Available file types are [ 's1d', 's2d', 'ccf', 'bis', 'all' ].

        :param file_type: The type of files to download
        :param filters: Filters to apply to the query
        :type filters: Optional[dict]
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.sun import Sun
        >>> filters_to_use = {'file_rootpath': {'contains': ['r.HARPN.2016-01-03T15-36-20.496.fits']}}
        >>> # Sun.download('s1d', filters=filters_to_use, output_directory='/tmp', output_filename='sun_spectroscopy_data.tar.gz')
        """

        if file_type not in Spectroscopy.ACCEPTED_FILE_TYPES:
            raise ValueError('file_type must be one of these values : ' + ','.join(Spectroscopy.ACCEPTED_FILE_TYPES))
        if filters is None:
            filters = {}

        sun_spectroscopy_data = self.query_database(filters=filters, output_format='dict')
        files = sun_spectroscopy_data['file_rootpath']
        download_response = self.dace.request_post(
            api_name=self.__OBS_API,
            endpoint='download/prepare/sun',
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
            obs_type='sun',
            download_id=download_id,
            output_directory=output_directory,
            output_filename=output_filename
        )

    def download_files(self,
                       file_type: Optional[str] = 's1d',
                       files: Optional[list[str]] = None,
                       output_directory: Optional[str] = None,
                       output_filename: Optional[str] = None) -> None:
        """
        Download reduction products specified in argument for the list of raw files specified and save it locally.

        Available file types are [ 's1d', 's2d', 'ccf', 'bis', 'all' ].

        :param file_type: The type of files to download
        :type file_type: Optional[str]
        :param files: The raw files
        :type files: list[str]
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.sun import Sun
        >>> files_to_retrieve = ['harpn/DRS-2.3.5/reduced/2016-01-03/r.HARPN.2016-01-03T15-36-20.496.fits']
        >>> # Sun.download_files('s1d', files=files_to_retrieve, output_directory='/tmp', output_filename='files.tar.gz')

        """
        if files is None:
            raise NoDataException

        files = list(map(lambda file: f'{file}.fits' if not file.endswith('.fits') else file, files))

        # files = [file + '.fits' for file in files if '.fits' not in file]

        download_response = self.dace.request_post(
            api_name=self.__OBS_API,
            endpoint='download/prepare/sun',
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
            obs_type='sun',
            download_id=download_id,
            output_directory=output_directory,
            output_filename=output_filename
        )

    def download_public_release_all(self,
                                    year: str,
                                    month: str,
                                    output_directory: Optional[str] = None,
                                    output_filename: Optional[str] = None) -> None:
        """
        Download public sun data of year and month specified in arguments.

        :param year: The year for sun data
        :type year: str
        :param month: The month for sun data
        :type month: str
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.sun import Sun
        >>> # Sun.download_public_release_all('2015','12', output_directory='/tmp', output_filename='release_all_2015-12.tar.gz')

        """
        year_and_month = str(year) + '-' + str(month)
        self.dace.download_file(
            api_name=self.__OBS_API,
            endpoint=f'sun/download/release/all/{year_and_month}',
            output_directory=output_directory,
            output_filename=output_filename
        )

    def download_public_release_ccf(self,
                                    year: str,
                                    output_directory: Optional[str] = None,
                                    output_filename: Optional[str] = None) -> None:
        """
        Download public ccf data realease of year specified in argument.

        :param year: The year for the ccf data
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.sun import Sun
        >>> # Sun.download_public_release_ccf('2015', output_directory='/tmp', output_filename='cff.tar.gz')
        """
        self.dace.download_file(
            api_name=self.__OBS_API,
            endpoint=f'sun/download/release/ccf/{year}',
            output_directory=output_directory,
            output_filename=output_filename
        )

    def download_public_release_timeseries(self,
                                           period: Optional[str] = '2015-2018',
                                           output_directory: Optional[str] = None,
                                           output_filename: Optional[str] = None) -> None:
        """
        Download public timeseries data release for a specified period and save it locally.

        The only available period is '2015-2018'.

        :param period: The period
        :type period: Optional[str]
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.sun import Sun
        >>> # Sun.download_public_release_timeseries(output_directory='/tmp', output_filename='public_release_timeseries.rdb')
        """
        self.dace.download_file(
            api_name=self.__OBS_API,
            endpoint=f'sun/download/release/timeseries/{period}',
            output_directory=output_directory,
            output_filename=output_filename
        )


Sun: SunClass = SunClass()
"""Sun instance"""
