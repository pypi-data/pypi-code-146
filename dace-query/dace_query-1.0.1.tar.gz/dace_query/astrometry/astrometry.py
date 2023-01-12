from __future__ import annotations

import json
import logging
from typing import Optional
from typing import Union

from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

ASTROMETRY_DEFAULT_LIMIT = 10000


class AstrometryClass:
    """
    The astrometry class.
    Use to retrieve data from the astrometry module.

    **An astrometry instance is already provided, to use it :**

    >>> from dace_query.astrometry import Astrometry

    """

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable astrometry object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.astrometry import AstrometryClass
        >>> astrometry_instance = AstrometryClass()

        """

        # Logging configuration
        self.__OBSERVATION_API = 'obs-webapp'
        self.log = logging.getLogger("Astrometry")
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
                       limit: Optional[int] = ASTROMETRY_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) \
            -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the astrometry database to retrieve data in the chosen format.

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

        >>> from dace_query.astrometry import Astrometry
        >>> values = Astrometry.query_database()
        """

        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OBSERVATION_API,
                endpoint='observation/search/astrometry',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }), output_format=output_format)

    def get_gaia_timeseries(self,
                            target: str,
                            output_format: Optional[str] = None) \
            -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Get timeseries from Gaia astrometry for the specified target.

        All available formats are defined in this section (see :doc:`output_format`).

        :param target: The target name to retrieve astrometry data from
        :type target: str
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.astrometry import Astrometry
        >>> target_to_search = 'your-target'
        >>> values = Astrometry.get_gaia_timeseries(target=target_to_search)

        """

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OBSERVATION_API,
                endpoint=f'observation/astrometry/{target}'),
            output_format=output_format)


Astrometry: AstrometryClass = AstrometryClass()
"""
Astrometry instance
"""
