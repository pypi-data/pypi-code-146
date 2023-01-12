from __future__ import annotations

import json
import logging
from typing import Union, Optional

from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

LOSSY_DEFAULT_LIMIT = 10000


class LossyClass:
    """
    The lossy class.
    Use to retrieve data from the lossy module.

    **A lossy instance is already provided, to use it :**

    >>> from dace_query.lossy import Lossy

    """

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable lossy object which uses a specified dace instance.

        :param dace_instance: Optional[DaceClass]

        >>> from dace_query.lossy import LossyClass
        >>> lossy_instance = LossyClass()

        """
        self.__LOSSY_API = 'lossy-webapp'
        # Logging configuration
        self.log = logging.getLogger("Population")
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
                       limit: Optional[int] = LOSSY_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the lossy database to retrieve data in the chosen format.

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

        >>> from dace_query.lossy import Lossy
        >>> values = Lossy.query_database()
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__LOSSY_API,
                endpoint='sample/search',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }), output_format=output_format)

    def get_sample(self,
                   sample_id: str,
                   output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Get the data for a specific sample.

        :param sample_id: The sample to retrieve data from.
        :type sample_id: str
        :param output_format: Type of data returns
        :type output_format: dict[str, ndarray] or DataFrame or Table or dict
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.lossy import Lossy
        >>> sample_id_to_retrieve = 'SAMPLE_Ice_LN2_11_20140221_000'
        >>> values = Lossy.get_sample(sample_id=sample_id_to_retrieve)
        """

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__LOSSY_API,
                endpoint=f'sample/{sample_id}'),
            output_format=output_format)


Lossy: LossyClass = LossyClass()
"""Lossy instance"""
