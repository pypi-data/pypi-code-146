from __future__ import annotations

import json
import logging
from typing import Union, Optional

from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

OPENDATA_DEFAULT_LIMIT = 10000


class OpenDataClass:
    """
    The opendata class.
    Use to retrieve data from the opendata module.

    **An opendata instance is already provided, to use it:**

    >>> from dace_query.opendata import OpenData
    """

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable opendata object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.opendata import OpenDataClass
        >>> opendata_instance = OpenDataClass()
        """

        self.__OPEN_DATA_API = 'open-webapp'
        self.__OPENDATA_AVAILABLE_FILE_TYPES = ['readme', 'archive']
        self.__ADS_URL = 'https://ui.adsabs.harvard.edu/abs/'
        self.__DOI_URL = 'https://doi.org/'

        # Logging configuration
        self.log = logging.getLogger("OpenData")
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
                       limit: Optional[int] = OPENDATA_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the open database to retrieve data in the chosen format.

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

        >>> from dace_query.opendata import OpenData
        >>> values =  OpenData.query_database()
        """

        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        data = self.dace.parse_parameters(
            self.dace.request_get(
                api_name=self.__OPEN_DATA_API,
                endpoint='publication/search',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }
            )
        )

        data['ads_link'] = [f'{self.__ADS_URL}{bibcode}' for bibcode in data['pub_bibcode']]
        data['doi_link'] = [f'{self.__DOI_URL}{doi}' for doi in data['pub_doi']]
        data['data_external_repositories'] = [json.loads(data_external_repositories) for data_external_repositories in
                                              data['data_external_repositories']]

        # Convert list of major into list of boolean values
        data['pub_major'] = list(
            map(lambda vector_major:
                list(
                    map(
                        lambda value: value.lower() == 'true', vector_major)),
                map(lambda record: record.split(','),
                    data['pub_major'])))

        return self.dace.convert_to_format(data, output_format=output_format)

    def download(self, dace_data_id: str,
                 file_type: str,
                 output_directory: Optional[str] = None,
                 output_filename: Optional[str] = None) -> None:
        """
        Download a publication specified by its dace_data_id, depending on the specified file type it downloads the archive
        or the readme file.

        Available file types are [ 'readme', 'archive' ].

        :param dace_data_id: The publication's data id
        :type bibcode: str
        :param file_type: The file to download
        :type file_type: str
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.opendata import OpenData
        >>> # OpenData.download('2019MNRAS.483.5534S', 'archive', output_directory='/tmp', output_filename='opendata.tar.gz')

        """

        if file_type not in self.__OPENDATA_AVAILABLE_FILE_TYPES:
            raise ValueError('file_type must be : ' + ','.join(self.__OPENDATA_AVAILABLE_FILE_TYPES))

        self.dace.download_file(
            api_name=self.__OPEN_DATA_API,
            endpoint=f'publication/{file_type}/{dace_data_id}',
            output_directory=output_directory,
            output_filename=output_filename
        )


OpenData: OpenDataClass = OpenDataClass()
"""OpenData instance"""
