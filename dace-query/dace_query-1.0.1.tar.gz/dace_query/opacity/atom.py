from __future__ import annotations

import json
import logging
from typing import Union, Optional

from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

ATOM_DEFAULT_LIMIT = 10000


class AtomClass:
    """
    The atom class
    Use to retrieve atom data from the opacity module.

    **An atom instance is already provided, to use it:**

    >>> from dace_query.opacity import Atom

    """

    def __init__(self, dace_instance: Optional[DaceClass] = None):
        """
        Create a configurable atom object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.opacity import AtomClass
        >>> atom_instance = AtomClass()

        """
        self.__OPACITY_API = 'opa-webapp'

        # Logging configuration
        self.log = logging.getLogger("Opacity")
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
                       limit: Optional[int] = ATOM_DEFAULT_LIMIT,
                       filters: Optional[dict] = None,
                       sort: Optional[dict] = None,
                       output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the atom database to retrieve data in the chosen format.

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
        :rtype:  dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.opacity import Atom
        >>> values = Atom.query_database()

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OPACITY_API,
                endpoint='atom/search',
                params={
                    'limit': str(limit),
                    'filters': json.dumps(filters),
                    'sort': json.dumps(sort)
                }
            ), output_format=output_format
        )

    def download(self,
                 atom: str, charge: str, line_list: str, version: str,
                 temperature_boundaries: tuple[int, int],
                 pressure_boundaries: tuple[float, float],
                 output_directory: Optional[str] = None,
                 output_filename: Optional[str] = None) -> None:
        """
        Download data for a specified atom.

        :param atom: The name of the atom to retrieve data from
        :type atom: str
        :param charge: The charge
        :type charge: str
        :param line_list: The line_list / data source
        :type line_list: str
        :param version: The version
        :type version: str
        :param temperature_boundaries: The temperature boundaries
        :type temperature_boundaries: tuple[int, int]
        :param pressure_boundaries: The pressure boundaries
        :type pressure_boundaries: tuple[float, float]
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.opacity import Atom
        >>> # Atom.download(atom='Lu', charge=0, line_list='Kurucz',version=1.0,temperature_boundaries=(2500, 2600),pressure_boundaries= (-8, -8),output_directory='/tmp',output_filename='test_atom.tar.gz')

        """
        self.dace.download_file(
            api_name=self.__OPACITY_API,
            endpoint=f'atom/download/{atom}/{charge}/{line_list}',
            params={
                'tMin': str(temperature_boundaries[0]),
                'tMax': str(temperature_boundaries[1]),
                'pMinExp': str(pressure_boundaries[0]),
                'pMaxExp': str(pressure_boundaries[1]),
                'version': str(version),
            },
            output_directory=output_directory,
            output_filename=output_filename
        )

    def get_data(self, atom: str, charge: str, line_list: str, version: str,
                 temperature: int, pressure_exponent: float,
                 output_format: Optional[str] = None) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Retrieve data from an atom in the chosen format.

        All available formats are defined in this section (see :doc:`output_format`).

        :param atom: The atom to retrieve data from
        :type atom: str
        :param charge: The charge
        :type charge: str
        :param line_list: The line list / data source
        :type line_list: str
        :param version: The version
        :type version: str
        :param temperature: The temperature
        :type temperature: int
        :param pressure_exponent: The pressure exponent
        :type pressure_exponent: float
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.opacity import Atom
        >>> values = Atom.get_data(atom='Lu', charge=0, line_list='Kurucz',version=1.0, temperature=2500, pressure_exponent=-8)

        """
        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OPACITY_API,
                endpoint=f'atom/data/{atom}/{charge}/{line_list}',
                params={
                    'temperature': str(temperature),
                    'pressureExp': str(pressure_exponent),
                    'version': str(version)
                }
            ), output_format=output_format
        )

    def get_high_resolution_data(self,
                                 atom: str, charge: str, line_list: str,
                                 version: str,
                                 temperature: int, pressure_exponent: float,
                                 wavenumber_boundaries: tuple[float, float],
                                 output_format: Optional[str] = None) -> Union[
        dict[str, ndarray], DataFrame, Table, dict]:
        """
        Retrieve high resolution data from an atom in the chosen format.

        All available formats are defined in this section (see :doc:`output_format`).

        :param atom: The atom to retrieve high resolution data from
        :type atom: str
        :param charge: The charge
        :type charge: str
        :param line_list: The line list / data source
        :type line_list: str
        :param version: The version
        :type version: str
        :param temperature: The temperature
        :param pressure_exponent: The pressure exponent
        :type pressure_exponent: float
        :param wavenumber_boundaries: The range min and max to extract from the binary high resolution file
        :type wavenumber_boundaries: tuple[float, float]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.opacity import Atom
        >>> values = Atom.get_high_resolution_data('Lu', 0, 'Kurucz', 1.0, 2500, -8, (1.01, 3.02))

        """
        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__OPACITY_API,
                endpoint=f'atom/highresolutiondata/{atom}/{charge}/{line_list}',
                params={
                    'temperature': str(temperature),
                    'pressureExp': str(pressure_exponent),
                    'wavenumberStart': str(wavenumber_boundaries[0]),
                    'wavenumberEnd': str(wavenumber_boundaries[1]),
                    'version': str(version)
                }
            ), output_format=output_format
        )

    def interpolate(self,
                    atom: str,
                    charge: str,
                    line_list: str,
                    version: str,
                    interpol_temperatures: list,
                    output_directory: Optional[str] = None,
                    output_filename: Optional[str] = None) -> None:
        """
        Compute interpolation for an atom.

        :param atom: The atom
        :type atom: str
        :param charge: The charge
        :type charge: str
        :param line_list: The line list / data sourcoe
        :type line_list: str
        :param version: The version
        :type version: str
        :param interpol_temperatures: The interpol temperatures
        :type interpol_temperatures: list
        :param output_directory: The directory where files will be saved
        :type output_directory: Optional[str]
        :param output_filename: The filename for the download
        :type output_filename: Optional[str]
        :return: None

        >>> from dace_query.opacity import Atom
        >>> # Atom.interpolate('Lu', 0, 'Kurucz', 1.0, [2510], output_directory='/tmp', output_filename='opacity_atom_interpolate.tar.gz')

        """
        download_response = self.dace.request_post(
            api_name=self.__OPACITY_API,
            endpoint=f'atom/interpolate/{atom}/{charge}/{line_list}',
            params={
                'version': str(version)
            },
            data=json.dumps({
                'interpol_temperatures': interpol_temperatures,
                'interpol_pressures': [1e-8 for _ in interpol_temperatures]
            })

        )
        if not download_response:
            return None
        download_id = download_response['values'][0]
        self.dace.download_file(
            api_name=self.__OPACITY_API,
            endpoint=f'atom/interpolate/{download_id}',
            output_directory=output_directory,
            output_filename=output_filename
        )


Atom: AtomClass = AtomClass()
"""Atom instance"""
