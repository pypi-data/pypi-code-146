#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from copy import deepcopy

import numpy as np
import pandas as pd
from sqlalchemy import asc, and_
from sqlalchemy.orm.exc import NoResultFound

from poppy.core.db.connector import Connector
from poppy.core.logger import logger

from roc.rpl.time import Time
from roc.dingo.models.data import HfrTimeLog
from roc.dingo.tools import actual_sql

from roc.rap.constants import PIPELINE_DATABASE, UINT32_MAX_ENCODING

__all__ = ['get_hfr_time_log', 'get_hfr_delta_times',
           'merge_coarse_fine']


@Connector.if_connected(PIPELINE_DATABASE)
def get_hfr_time_log(mode, start_time, end_time,
                     model=HfrTimeLog):
    """
    Query pipeline.hfr_time_log table in database

    :param mode: Mode of HFR receiver (0=NORMAL, 1=BURST)
    :param start_time: minimal acquisition time to query (datetime object)
    :param end_time: maximal acquisition time to query (datetime object)
    :param model: database table class
    :return:
    """
    # get a database session
    session = Connector.manager[PIPELINE_DATABASE].session
    # Set filters
    logger.debug(f'Connecting {PIPELINE_DATABASE} database to retrieve entries from pipeline.hfr_time_log table ...')
    filters = []
    filters.append(model.mode == mode)  # Get data for current mode
    filters.append(model.acq_time >= str(start_time))
    filters.append(model.acq_time <= str(end_time))
    # Join query conditions with AND
    filters = and_(*filters)

    # Query database (returns results as a pandas.DataFrame object)
    try:
        query = session.query(model).filter(
            filters).order_by(asc(HfrTimeLog.acq_time))
        results = pd.read_sql(query.statement, session.bind)
    except NoResultFound:
        logger.exception(f'No result for {actual_sql(query)}')
        results = pd.DataFrame()

    return results


def get_hfr_delta_times(mode, acq_time_min,
                        duration=48):
    """
    Retrieve delta_times values in the pipeline.hfr_time_log table

    :param mode: HFR receiver mode (0=NORMAL, 1=BURST)
    :param acq_time_min: Minimal acquisition time to query (tuple with coarse and fine parts)
    :param duration: Time range to query will be [acq_start_time, acq_start_time + duration] with duration in hours. default is 24.
    :return: pandas.DataFrame with database query results
    """
    delta_times = [[], []]
    # Convert input acquisition time (coarse, fine) into
    # datetime object
    start_time = Time.cuc_to_datetime(acq_time_min)[0] - timedelta(minutes=1)
    end_time = start_time + timedelta(hours=duration)

    # Query database
    try:
        results = get_hfr_time_log(mode, start_time, end_time)
    except Exception as e:
        logger.exception('Cannot query pipeline.hfr_time_log table')
        raise e

    if results.shape[0] > 0:
        # If no empty dataframe, then make sure to have valid
        # delta times values
        results['delta_time1'] = results['delta_time1'].apply(valid_delta_time)
        results['delta_time2'] = results['delta_time2'].apply(valid_delta_time)

        # Add a variable containing merged coarse/fine parts of
        # acquisition time
        results['coarse_fine'] = results.apply(
            lambda row: merge_coarse_fine(
                row['coarse_time'], row['fine_time']),
            axis=1)

    return results


def valid_delta_time(delta_times):
    """
    Check if delta times values are valid for the input hfr_time_log row
    (i.e., first delta_time1 values for each record should be 0
        # and delta_times values should increase monotonically)

    :param delta_times1: hfr_time_log.delta_time 1 or 2 values to check
    :return: row with updates (if needed)
    """
    # Initialize output
    new_delta_times = deepcopy(delta_times)

    # Initialize byte offset
    offset = np.uint64(0)

    # Initialize previous value to compare
    prev_val = 0

    # Loop over packets
    for key, val in delta_times.items():
        # Loop over delta time values for current packet
        for j in range(0, len(val)):
            # Define index of value to compare
            if j > 0:
                prev_val = val[j - 1]

            # If previous delta time value is upper or equal than current value
            # then the increase is not monotone,
            # which indicates the max encoding value is reached
            if val[j] + offset < prev_val + offset:
                # In this case, increase offset
                offset += np.uint64(UINT32_MAX_ENCODING)
                logger.warning(f'Maximal encoding value reached for 32-bits delta time (offset={offset})')
            # Save delta time value with correct offset
            new_delta_times[key][j] = np.uint64(val[j]) + offset
            prev_val = val[j]

    return new_delta_times


def merge_coarse_fine(coarse, fine):
    """
    return input coarse and fine parts of CCSDS CUC time
    as an unique integer

    :param coarse: coarse part of CUC time
    :param fine: fine part of CUC time
    :return: resulting unique integer
    """
    return int(coarse * 100000 + fine)


def found_delta_time(group, delta_times, packet_times, i, message):
    """
    Get HF1 / HF2 delta times values for current HFR science packet

    :param group: h5.group containing HFR science packet source_data
    :param delta_times: pandas.DataFrame storing hfr_time_log table data
    :param packet_times: list of packet (creation) times (coarse, fine, sync)
    :param i: index of the current HFR science packet in the L0 file
    :param message: string containing HFR receiver mode ('normal' or 'burst')
    :return: delta_time1 and delta_time2 values found in delta_times for current packet
    """
    # Get row index where condition is fulfilled
    where_packet = (merge_coarse_fine(group['PA_THR_ACQUISITION_TIME'][i][0], group['PA_THR_ACQUISITION_TIME'][i][1]) ==
                    delta_times['coarse_fine'])
    # Must be only one row
    if delta_times[where_packet].shape[0] > 1:
        raise ValueError(f'Wrong number of hfr_time_log entries found for HFR {message} packet at {packet_times[i][:2]}: '
                         f'1 expected but {delta_times[where_packet].shape[0]} found! '
                         f'(acq. time is {group["PA_THR_ACQUISITION_TIME"][i][:2]})')
    # Must be at least one row
    elif delta_times[where_packet].shape[0] == 0:
        raise ValueError(f'No hfr_time_log entry found for HFR {message} packet #{i} at {packet_times[i][:2]} '
                         f'(acq. time is {group["PA_THR_ACQUISITION_TIME"][i][:2]})')
    else:
        # Else extract delta_time1 and delta_time2 values found
        delta_time1 = delta_times['delta_time1'][where_packet].reset_index(drop=True)[0][
            str(merge_coarse_fine(packet_times[i][0], packet_times[i][1]))]
        delta_time2 = delta_times['delta_time2'][where_packet].reset_index(drop=True)[0][
            str(merge_coarse_fine(packet_times[i][0], packet_times[i][1]))]

    return delta_time1, delta_time2
