from __future__ import annotations

import json
import logging
from typing import Union, Optional

from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

POPULATION_DEFAULT_LIMIT = 10000


class PopulationClass:
    """
    The population class.
    Use to retrieve data from the population module.

    **A population instance is already provided, to use it:**

    >>> from dace_query.population import Population
    """

    SNAPSHOTS_DEFAULT_COLUMN = ['system_id', 'planet_id', 'total_mass', 'semi_major_axis']
    """Snapshot parameters retrieved by default"""
    SIMULATIONS_DEFAULT_COLUMN = ['total_mass', 'semi_major_axis']
    """Simulation parameters retrieved by default"""
    __POPULATION_API = 'evo-webapp'

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable population object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.population import PopulationClass
        >>> population_instance = PopulationClass()
        """
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
                       limit: Optional[int] = POPULATION_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the population database to retrieve data (population descriptions) in the chosen format.

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

        >>> from dace_query.population import Population
        >>> values = Population.query_database()

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__POPULATION_API,
                endpoint='population/search',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }
            ), output_format=output_format
        )

    def get_columns(self, population_id: str, output_format: Optional[str] = None) \
            -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Get the available columns for the specified population.

        All available formats are defined in this section (see :doc:`output_format`).

        :param population_id: The population id
        :type population_id: str
        :param output_format: Type of data returns
        :type output_format: str
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.population import Population
        >>> population_to_search = 'ng96'
        >>> values = Population.get_columns('ng96')
        """

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__POPULATION_API,
                endpoint=f'population/{population_id}/variables'
            ), output_format=output_format
        )

    def get_snapshots(self,
                      population_id: str,
                      years: str,
                      columns: Optional[list[str]] = None,
                      output_format: Optional[str] = None) \
            -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Get snapshots data for a specific population at a specific age.

        All available formats are defined in this section (see :doc:`output_format`).

        :param population_id: The population id to get snapshots from
        :type population_id: str
        :param years: The specific age of the snapshot
        :type years: str
        :param columns: A list of parameters to retrieve
        :type columns: Optional[list[str]]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.population import Population
        >>> population_id = 'ng96'
        >>> years = '5000000'
        >>> columns_to_retrieve = ['system_id', 'planet_id', 'total_mass']
        >>> values = Population.get_snapshots(population_id=population_id, years=years, columns=columns_to_retrieve)
        """
        if columns is None:
            columns = self.SNAPSHOTS_DEFAULT_COLUMN
        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__POPULATION_API,
                endpoint=f'population/{population_id}/snapshots/{str(years)}',
                params={'col': columns}
            ), output_format=output_format
        )

    @staticmethod
    def get_snapshot_ages() -> list[str]:
        """
        Use to get all snapshot ages.

        :return: All existing ages
        :rtype: list[str]

        >>> from dace_query.population import Population
        >>> ages = Population.get_snapshot_ages()
        """

        snapshot_ages = []
        for exp in range(5, 10):
            for base in range(1, 10):
                age = base * 10.0 ** exp
                snapshot_ages.append(age)
        snapshot_ages.append(1E10)
        snapshot_ages = list(map(lambda v: str(int(v)), snapshot_ages))
        return snapshot_ages

    def get_track(self,
                  population_id: str,
                  system_id: int,
                  planet_id: int,
                  columns: Optional[list[str]] = None,
                  output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Retrieve tracks for a specific population, system id and planet id.

        All available formats are defined in this section (see :doc:`output_format`).

        :param population_id: The population id to retrieve tracks from
        :type population_id: str
        :param system_id: The system id
        :type system_id: int
        :param planet_id: The planet id
        :type planet_id: int
        :param columns: The parameters to retrieve
        :type columns: Optional[list[str]]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.population import Population
        >>> pop_id, planet_id, system_id = 'ng96', 1, 1
        >>> parameters_to_retrieve = ['time_yr', 'total_mass']
        >>> values = Population.get_track(population_id=pop_id, system_id=system_id, planet_id=planet_id, columns=parameters_to_retrieve)

        """
        if columns is None:
            columns = self.SIMULATIONS_DEFAULT_COLUMN
        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__POPULATION_API,
                endpoint=f'population/{population_id}/{system_id}/{planet_id}/simulations',
                params={'col': columns}
            ), output_format=output_format
        )


Population: PopulationClass = PopulationClass()
"""Population instance"""
