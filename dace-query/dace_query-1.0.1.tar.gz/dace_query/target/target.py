from __future__ import annotations

import json
import logging
from typing import Optional, Union

from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

TARGET_DEFAULT_LIMIT = 10000


class TargetClass:
    """
    The target class.
    Use to retrieve data from the target module.

    **A target instance is already provided, to use it :**

    >>> from dace_query.target import Target
    """
    __OBS_API = 'obs-webapp'

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable target object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.target import TargetClass
        >>> target_instance = TargetClass()

        """
        # Logging configuration
        self.log = logging.getLogger("Target")
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
                       limit: Optional[int] = TARGET_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the target database to retrieve data in the chosen format.

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

        >>> from dace_query.target import Target
        >>> values = Target.query_database()
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}
        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OBS_API,
                endpoint='target',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }
            ), output_format=output_format
        )


Target: TargetClass = TargetClass()
"""Target instance"""
