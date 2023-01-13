#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

from poppy.core.generic.metaclasses import Singleton
from poppy.core.db.connector import Connector
from poppy.core.logger import logger

from roc.rap.constants import PIPELINE_DATABASE, TC_HFR_LIST_PAR

__all__ = ['HfrListMode']


class HfrListMode(object, metaclass=Singleton):

    def __init__(self):
        self._hfr_list_data = None

    @property
    def hfr_list_data(self):
        if self._hfr_list_data is None:
            self._hfr_list_data = self.load_hfr_list_data()
        return self._hfr_list_data

    @hfr_list_data.setter
    def hfr_list_data(self, value):
        self._hfr_list_data = value

    @Connector.if_connected(PIPELINE_DATABASE)
    def load_hfr_list_data(self):
        """
        Query ROC database to get the data from hfr_freq_list table.

        :return: query result
        """
        from sqlalchemy import asc, or_
        from roc.dingo.models.packet import TcLog
        # get a database session
        session = Connector.manager[PIPELINE_DATABASE].session
        # Set filters
        logger.debug(f'Connecting {PIPELINE_DATABASE} database to retrieve entries from pipeline.tc_log table ...')
        filters = [TcLog.palisade_id == current_tc
                   for current_tc in TC_HFR_LIST_PAR]
        filters = or_(*filters)

        # Query database (returns results as a pandas.DataFrame object)
        results = pd.read_sql(session.query(TcLog).filter(
            filters).order_by(asc(TcLog.utc_time)).statement, session.bind)

        return results

    def get_freq(self, utc_time, band, mode, get_index=False):
        """
        Get the list of frequencies (kHz) in HFR LIST mode for a given band (HF1 or HF2)

        :param utc_time: datetime object containing the UTC time for which the frequency list must be returned
        :param band: string giving the name of the HFR band (HF1 or HFR2)
        :param mode: string giving the mode (0=NORMAL, 1=BURST)
        :param get_index: If True return the index of the frequencies instead of value
        :return:
        """
        # Get lists of frequencies in HFR LIST mode stored in database
        hfr_list_data = self.hfr_list_data

        # Expected TC name
        band_index = int(band[-1])
        if mode == 1:
            tc_name = f'TC_THR_LOAD_BURST_PAR_{band_index + 1}'
            param_name = f'SY_THR_B_SET_HLS_FREQ_HF{band_index}'
        else:
            tc_name = f'TC_THR_LOAD_NORMAL_PAR_{band_index + 1}'
            param_name = f'SY_THR_N_SET_HLS_FREQ_HF{band_index}'

        # Get list of frequencies from the last TC executed on board
        try:
            latest_hfr_list_data = hfr_list_data[(
                hfr_list_data.palisade_id == tc_name) & (hfr_list_data.utc_time <= utc_time)].iloc[-1]
        except:
            logger.warning(f'No valid frequency list found for {tc_name} at {utc_time}!')
            frequency_list = []
        else:
            # Get indices of frequencies for current utc_time, mode and band
            frequency_list = latest_hfr_list_data.data[param_name].copy()
            logger.debug(f'Frequency values found for {tc_name} on {latest_hfr_list_data.utc_time}: {frequency_list}')

        if not get_index:
            # Compute frequency values in kHz
            frequency_list = [compute_hfr_list_freq(current_freq)
                              for current_freq in frequency_list]

        return frequency_list


def compute_hfr_list_freq(freq_index):
    """
    In HFR LIST mode, return frequency value in kHz giving its
    index

    :param freq_index: index of the frequency
    :return: Value of the frequency in kHz
    """
    return 375 + 50 * (int(freq_index) - 436)
