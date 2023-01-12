from __future__ import annotations

import configparser
import json
import logging
import re
import urllib.parse
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Optional, Union

import numpy as np
import requests
from astropy.coordinates import SkyCoord, Angle
from astropy.table import Table
from pandas import DataFrame
from requests import RequestException, HTTPError

from dace_query.__version__ import __version__, __title__, __py_version__

COORDINATES_DB_COLUMN = 'obj_pos_coordinates_hms_dms'

MB_SIZE = 1048576


class NoDataException(Exception):
    """Raised when no data are provided"""


class DaceClass:
    """
    The dace class.
    When initializing an instance with this class, it loads the user .dacerc and config.ini files to authentify the
    current user and define which endpoints to use.

    The **.dacerc** file, (**you have to create it**), located by default in the home directory (~/.dacerc) and in TOML
    format, defines a user section with a key-value pair specifying the user's API key (see below).

    .. code-block:: cfg

        [user]
        key = apiKey:<xxx-xxx-xxx>

    To obtain an API key:

    1.  Login on dace (https://dace.unige.ch)
    2.  Go to the user profile
    3.  Click on [Generate a new API key]

    The **config.ini** file, in CFG format and already included in the dace package, defines default DACE endpoints
    to use (see below).

    .. code-block:: cfg

        [api]

        evo-webapp = https://evo-webapp.obsuksprd2.unige.ch/
        exo-webapp = https://exo-webapp.obsuksprd2.unige.ch/
        lossy-webapp = https://lossy-webapp.obsuksprd2.unige.ch/
        obs-webapp = https://obs-webapp.obsuksprd2.unige.ch/
        opa-webapp = https://opa-webapp.obsuksprd2.unige.ch/
        open-webapp = https://od-webapp.obsuksprd2.unige.ch/
        tess-webapp = https://tess-webapp.obsuksprd2.unige.ch/
        cheops-webapp = https://cheops-webapp.obsuksprd2.unige.ch/
        monitoring-webapp = https://pipe-webapp.obsuksprd2.unige.ch/

    **A dace instance is already provided, to use it :**

    >>> from dace_query import Dace


    """

    def __init__(self, dace_rc_config_path: Optional[Path] = None, config_path: Optional[Path] = None):
        """
        Create a configurable dace object which loads the user's .dacerc and the config file specified in arguments.

        :param dace_rc_config_path: The .dacerc filepath, used to authentify the user.
        :type dace_rc_config_path: Optional[Path]
        :param config_path: The config.ini filepath, defines which DACE endpoints to use.
        :type config_path: Optional[Path]

        >>> from dace_query import DaceClass
        >>> from pathlib import Path
        >>> dace_instance = DaceClass(dace_rc_config_path=Path.home(), config_path=Path('config.ini'))
        >>> type(DaceClass())
        <class 'dace.dace.DaceClass'>

        """
        # Logging configuration
        logger = logging.getLogger('dace')
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(ch)
        self.log = logger

        # Get dacerc and endpoints location
        dace_rc_config_path = Path(Path.home(), '.dacerc') if dace_rc_config_path is None else Path(dace_rc_config_path)
        endpoints_path = Path(Path(__file__).parent.resolve(), 'config.ini') if config_path is None else Path(
            config_path)

        self.__dace_rc_config = None
        # Load the dace resource file <.dacerc>
        if dace_rc_config_path.exists() and dace_rc_config_path.is_file():
            dace_rc_config = configparser.ConfigParser()
            dace_rc_config.read(dace_rc_config_path)
            self.__dace_rc_config = dace_rc_config
        else:
            self.log.warning(
                "File .dacerc not found. You are requesting data in public mode. "
                "To change this behaviour, create a .dacerc file in your home directory and fill it with your API key. "
                "More infos on https://dace.unige.ch")

        # Load the endpoint configuration file <config.ini>
        self.__cfg = None
        if endpoints_path.exists() and endpoints_path.is_file():
            endpoints_config = configparser.ConfigParser()
            endpoints_config.read(endpoints_path)
            self.__cfg = endpoints_config

    @staticmethod
    def transform_dict_to_encoded_json(dict_to_transform: Union[set, dict]) -> str:
        """Internal stuff"""
        return urllib.parse.quote_plus(json.dumps(dict_to_transform))

    @staticmethod
    def transform_coordinates_to_dict(sky_coord: SkyCoord, angle: Angle) -> dict:
        """Internal stuff"""
        return {COORDINATES_DB_COLUMN: {'ra': sky_coord.ra.degree, 'dec': sky_coord.dec.degree,
                                        'radius': angle.degree}}

    def transform_to_format(self, json_data: dict, output_format: Optional[str] = None):
        """Internal stuff"""
        data = self.parse_parameters(json_data)
        return self.convert_to_format(data, output_format)

    def parse_parameters(self, json_data: dict) -> dict[str, list]:
        """Internal stuff"""
        """
        Internally DACE data are provided using protobuf. The format is a list of parameters. Here we parse
        these data to give to the user something more readable and ignore the internal stuff
        """
        data = defaultdict(list)
        if 'parameters' not in json_data:
            return data
        parameters = json_data.get('parameters')
        for parameter in parameters:
            variable_name = parameter.get('variableName')
            double_values = parameter.get('doubleValues')
            # W/A for 'NaN' values
            if double_values is not None:
                double_values = list(map(float, double_values))
            float_values = parameter.get('floatValues')
            # W/A for 'NaN' values
            if float_values is not None:
                float_values = list(map(float, float_values))
            int_values = parameter.get('intValues')
            string_values = parameter.get('stringValues')
            bool_values = parameter.get('boolValues')
            occurrences = parameter.get('occurrences')

            # Only one type of values can be present. So we look for the next occurrence not None. Prevent not found
            # with an empty list to avoid having StopIteration exception
            values = next(
                (values_list for values_list in [double_values, float_values, int_values, string_values, bool_values] if
                 values_list is not None), [])
            if occurrences:
                data[variable_name].extend(self.__transform_values_with_occurrences(values, occurrences))
            else:
                data[variable_name].extend(values)

            error_values = parameter.get('minErrorValues')  # min or max is symmetric
            if error_values is not None:
                if occurrences:
                    data[variable_name + '_err'].extend(
                        self.__transform_values_with_occurrences(error_values, occurrences))
                else:
                    data[variable_name + '_err'].extend(error_values)
        return data

    @staticmethod
    def convert_to_format(data: dict, output_format: Optional[str]) -> Union[
        dict[str, np.ndarray], DataFrame, Table, dict]:
        """Internal stuff"""

        if output_format == 'pandas':
            return DataFrame.from_dict(data)
        elif output_format == 'astropy_table':
            return Table(data)
        elif output_format == 'dict':
            return data
        else:  # or output_format='numpy'
            np_data = {}
            for key, values in data.items():
                if any(map(lambda value: type(value) == list, values)):
                    np_data[key] = np.array(values, dtype='object')
                else:
                    np_data[key] = np.array(values)
            return np_data

    def persist_file_on_disk(self, api_name: str, obs_type: str, download_id: str,
                             params: Optional[dict] = None,
                             output_directory: Optional[str] = None,
                             output_filename: Optional[str] = None) -> None:
        """Internal stuff"""
        self.download_file(
            api_name=api_name,
            endpoint=f'download/{obs_type}/{download_id}',
            params=params,
            output_directory=output_directory,
            output_filename=output_filename
        )

    def request_get(self, api_name: str, endpoint: str, params: Optional[dict] = None,
                    raw_response: Optional[bool] = False) -> Union[bytes, dict]:
        """Internal stuff"""

        """
        This method does an HTTP get to DACE backend. If an apiKey has been found, it will be added in HTTP header
        :param endpoint: the DACE endpoint you want to query
        :return: the Json response containing data
        """
        headers = self.__prepare_request(raw_response)

        host = self.__cfg['api'][api_name] + endpoint
        try:
            response = requests.get(host, headers=headers, params=params)
            response.raise_for_status()

            if response.ok:
                if raw_response:
                    return response.content
                else:
                    return response.json()
            else:
                self.log.error("Status code %s when calling %s", response.status_code, host)
                raise RequestException
        except HTTPError as err_h:
            return self.__manage_http_errors(err_h)
        except RequestException as e:
            raise RequestException('Problem when calling {}'.format(host)) from e

    def request_post(self, api_name: str, endpoint: str,
                     json_data: Optional[dict] = None,
                     data: Optional[str] = None,
                     params: Optional[dict] = None) -> dict:

        """Internal stuff"""

        headers = self.__prepare_request()
        host = self.__cfg['api'][api_name] + endpoint

        try:
            response = requests.post(host, headers=headers, json=json_data, data=data, params=params)
            response.raise_for_status()
            if response.ok:
                return response.json()
            else:
                self.log.error("Status code %s when calling %s", response.status_code, host)
                raise RequestException
        except HTTPError as err_h:
            return self.__manage_http_errors(err_h)
        except RequestException as e:
            raise RequestException('Problem when calling {}'.format(host)) from e

    def download_file(self,
                      api_name: str,
                      endpoint: str,
                      params: Optional[dict] = None,
                      output_directory: Optional[str] = None,
                      output_filename: Optional[str] = None) -> None:
        """Internal stuff"""
        try:
            if output_directory is None:
                output_directory = Path.home()
            with requests.get(self.__cfg['api'][api_name] + endpoint,
                              params=params,
                              headers=self.__prepare_request(True),
                              stream=True) as response:
                response.raise_for_status()
                if output_filename is None:
                    output_filename = re.sub("attachment;\\s*filename\\s*=\\s*", '',
                                             response.headers['content-disposition']).replace('"', '')
                    if output_filename is None:
                        raise ValueError('Missing content-disposition. Please contact DACE support')
                output_full_file_path = Path(output_directory, output_filename)
                self.log.info("Downloading file on location : %s", output_full_file_path)
                self.write_stream(output_full_file_path, response)
                self.log.info('File downloaded on location : %s', output_full_file_path)
        except HTTPError as err_h:
            if err_h.response.status_code == 404:
                self.log.error('The file is not found on DACE')
            else:
                self.__manage_http_errors(err_h)

    @staticmethod
    def write_stream(output_filename: Union[Path, str], response: requests.Response) -> None:
        """Internal stuff"""

        with open(output_filename, 'wb') as f:
            chunk_total_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    chunk_total_size += 8192
                    if chunk_total_size % MB_SIZE == 0:
                        print("\r Download : " + str(chunk_total_size // MB_SIZE) + " MB", end="")
        print("\nDownload done")

    def __manage_http_errors(self, err_h) -> dict:
        """Internal stuff"""
        status_code = err_h.response.status_code
        if status_code == 404:
            self.log.error('No data found.')
        elif status_code == 401:
            self.log.error('Not authorized. You need to be logged on to access these data.')
        elif status_code == 403:
            self.log.error('Forbidden. You do not have the permission to access these data.')
        elif status_code == 405:
            self.log.error('Not Allowed. This method is deprecated. Please refer to the documentation.')
        else:
            self.log.error('Http error : ' + str(err_h))
            self.log.error('Please contact DACE support')
        return {}

    def __prepare_request(self, raw_response: Optional[bool] = False) -> dict:
        """Internal stuff"""
        headers = {'Accept': 'application/octet-stream'} if raw_response else {'Accept': 'application/json'}
        if self.__dace_rc_config is not None:
            headers['Authorization'] = self.__dace_rc_config['user']['key']
        headers['User-Agent'] = '/'.join([__title__, __version__, __py_version__])
        return headers

    @staticmethod
    def order_spectroscopy_data_by_instruments(data: dict[str, np.ndarray]) -> dict:
        """Internal stuff"""
        instruments_names = data.pop('ins_name', None)
        instruments_modes = data.pop('ins_mode', None)
        drs_versions = data.pop('drs_version', None)
        bib_codes = data.pop('pub_bibcode', None)

        data_by_instrument = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
        # Collect and group the data by ins_name / drs_version / ins_mode / parameter
        for i, ins_name in enumerate(instruments_names):
            for parameter, values in data.items():
                bibcode = bib_codes[i] if (bib_codes is not None and i < len(bib_codes)) else None
                drs_version = drs_versions[i] if (drs_versions is not None and i < len(drs_versions)) else None
                drs_or_bibcode = bibcode or drs_version or 'default'
                ins_mode = instruments_modes[i] if (
                        instruments_modes is not None and i < len(instruments_modes)) else 'default'
                # print('Value %s,  %s, %s' % (data[parameter][i], parameter, i))
                data_by_instrument[ins_name][drs_or_bibcode][ins_mode][parameter].append(data[parameter][i])

        numpy_data_by_instrument = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(partial(np.ndarray, 0)))))

        for ins_key, drs_list in data_by_instrument.items():
            for drs_key, mode_list in drs_list.items():
                for mode_key, parameter_list in mode_list.items():
                    for parameter_key, values in parameter_list.items():
                        numpy_data_by_instrument[ins_key][drs_key][mode_key][parameter_key] = np.array(values)

        return numpy_data_by_instrument

    @staticmethod
    def __transform_values_with_occurrences(values: list, occurrences: dict) -> list:
        """Internal stuff"""
        full_vector = []
        for i, occurrence in enumerate(occurrences):
            for j in range(0, occurrence):
                full_vector.append(values[i])

        return full_vector


Dace = DaceClass()
"""Dace instance"""
