from __future__ import annotations

import logging
from typing import Optional, Union

from astropy.table import Table
from numpy import ndarray
from pandas import DataFrame

from dace_query import Dace, DaceClass

MONITORING_DEFAULT_LIMIT = 10000


class MonitoringClass:
    """
    The monitoring class.
    Use to retrieve data from the monitoring module.

    **A monitoring instance is already provided, to use it :**

    >>> from dace_query.monitoring import Monitoring

    """
    __MONITORING_API = 'monitoring-webapp'

    def __init__(self, dace_instance: DaceClass = None):
        """
        Create a configurable monitoring object which uses a specified dace instance.

        :param dace_instance: A dace object
        :type dace_instance: Optional[DaceClass]

        >>> from dace_query.monitoring import MonitoringClass
        >>> monitoring_instance = MonitoringClass()
        """

        # Logging configuration
        self.log = logging.getLogger("Monitoring")
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

    def query_transfer_by_night(self,
                                instrument: str, pipeline: str, night: str,
                                output_format: Optional[str] = None
                                ) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the monitoring database to retrieve data in the chosen format for the specified instrument, night and
        pipeline.

        All available formats are defined in this section (see :doc:`output_format`).

        Available pipeline names are:
            - ``TRANSFER``: From remote archive to Geneva archive (Transfer)
            - ``GENEVA``: From reduction in Geneva to DACE import (Reduction and import)
            - ``FULL``: From remote archive to DACE import (Transfer, reduction and import)

        The supported combinations are indicated below and described as ``(instrument name; date of the night; pipeline name)`` :

            - HARPS, NIGHT, [ TRANSFER, GENEVA, FULL ]
            - ESPRESSO, NIGHT, [ TRANSFER, GENEVA, FULL ]
            - CORALIE14, NIGHT, [ TRANSFER, GENEVA, FULL ]
            - ECAM, NIGHT, [ TRANSFER ]
            - HARPN, NIGHT, [ TRANSFER ]

        :param instrument: The instrument name
        :type instrument: str
        :param pipeline: The pipeline name
        :type pipeline: str
        :param night: The date of the night
        :type night: str
        :param output_format: Type of data returns
        :type output_format: Optional[strs]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.monitoring import Monitoring
        >>> values = Monitoring.query_transfer_by_night(instrument='HARPS', pipeline='FULL', night='2022-11-08')
        """

        complete_name = f"{instrument}_{pipeline}".upper()

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__MONITORING_API,
                endpoint=f'monitoring/{complete_name}/date/{night}'),
            output_format=output_format
        )

    def query_transfer_by_period(self, instrument: str, pipeline: str, period: tuple[str, str],
                                 output_format: Optional[str] = None
                                 ) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the monitoring database ot retrieve data in the chosen format for the specified instrument, period and
        period.

        All available formats are defined in this section (see :doc:`output_format`).


        Available pipeline names are:
            - ``TRANSFER``: From remote archive to Geneva archive (Transfer)
            - ``GENEVA``: From reduction in Geneva to DACE import (Reduction and import)
            - ``FULL``: From remote archive to DACE import (Transfer, reduction and import)

        The supported combinations are indicated below and described as ``(instrument name; period dates; pipeline name)``:

            - HARPS, PERIOD, [ TRANSFER, GENEVA, FULL ]
            - ESPRESSO, PERIOD, [TRANSFER, GENEVA, FULL]
            - CORALIE14, PERIOD, [TRANSFER, GENEVA, FULL]
            - ECAM, PERIOD, [ TRANSFER ]
            - HARPN, PERIOD, [ GENEVA ]

        :param instrument: The instrument name
        :type instrument: str
        :param pipeline: The pipeline name
        :type pipeline: str
        :param period: The periods
        :type period: tuple[str, str]
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.monitoring import Monitoring
        >>> values = Monitoring.query_transfer_by_period(instrument='HARPS', pipeline='FULL', period=('2022-11-07', '2022-11-09'))
        """

        complete_name = f"{instrument}_{pipeline}".upper()

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__MONITORING_API,
                endpoint=f'monitoring/{complete_name}/period/{period[0]}/{period[1]}'),
            output_format=output_format)

    def query_transfer_by_program(self, instrument: str, pipeline: str, program: str,
                                  output_format: Optional[str] = None
                                  ) -> Union[dict[str, ndarray], DataFrame, Table, dict]:
        """
        Query the monitoring database to retrieve data in the chosen format for the specified instrument, pipeline and
        program.

        All available formats are defined in this section (see :doc:`output_format`).


        Available pipeline names are:
            - ``TRANSFER``: From remote archive to Geneva archive (Transfer)
            - ``GENEVA``: From reduction in Geneva to DACE import (Reduction and import)
            - ``FULL``: From remote archive to DACE import (Transfer, reduction and import)


        The supported combinations are indicated below and described as ``(instrument name; program name; pipeline name)``:

            - HARPS, PROGRAM, [ TRANSFER, FULL ]
            - ESPRESSO, PROGRAM, [ TRANSFER, FULL ]


        :param instrument: The instrument name
        :type instrument: str
        :param pipeline: The pipeline name
        :type pipeline: str
        :param program: The program name
        :type program: str
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.monitoring import Monitoring
        >>> values = Monitoring.query_transfer_by_program(instrument='ESPRESSO', pipeline='TRANSFER', program='110.245W.001')

        """

        complete_name = f"{instrument}_{pipeline}".upper()

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__MONITORING_API,
                endpoint=f'monitoring/{complete_name}/program/{program}'),
            output_format=output_format)

    def query_transfer_by_target(self,
                                 instrument: str, pipeline: str, target: str,
                                 output_format: Optional[str] = None
                                 ):
        """
        Query the monitoring database to retrieve data in the chosen format for the specified instrument, pipeline and
        target.

        All available formats are defined in this section (see :doc:`output_format`).


        Available pipeline names are:
            - ``TRANSFER``: From remote archive to Geneva archive (Transfer)
            - ``GENEVA``: From reduction in Geneva to DACE import (Reduction and import)
            - ``FULL``: From remote archive to DACE import (Transfer, reduction and import)

        The supported combinations are indicated below and described as ``(instrument name; target name; pipeline name)``:

            - HARPS, TARGET, [ TRANSFER, FULL ]
            - ESPRESSO, TARGET, [ TRANSFER, FULL ]

        :param instrument: The instrument name
        :type instrument: str
        :param pipeline: The pipeline name
        :type pipeline: str
        :param target: The target name
        :type target: str
        :param output_format: Type of data returns
        :type output_format: Optional[str]
        :return: The desired data in the chosen output format
        :rtype: dict[str, ndarray] or DataFrame or Table or dict

        >>> from dace_query.monitoring import Monitoring
        >>> values = Monitoring.query_transfer_by_target(instrument='ESPRESSO', pipeline='TRANSFER', target='L 513-23')
        """

        complete_name = f"{instrument}_{pipeline}".upper()

        return self.dace.transform_to_format(
            self.dace.request_get(
                api_name=self.__MONITORING_API,
                endpoint=f'monitoring/{complete_name}/target/{target}'),
            output_format=output_format
        )


Monitoring: MonitoringClass = MonitoringClass()
"""
Monitoring instance
"""
