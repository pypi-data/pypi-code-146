#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from poppy.core.logger import logger

from roc.rpl.time import Time
from roc.idb.converters.cdf_fill import fill_records

from roc.rap.tasks.utils import sort_data

__all__ = ['HIST1D', 'set_hist1d']

# Numpy array dtype for TDS histo1D L1 survey data
# Name convention is lower case

HIST1D = [
    ('epoch', 'uint64'),
    ('scet', 'float64'),
    ('acquisition_time', ('uint32', 2)),
    ('synchro_flag', 'uint8'),
    ('quality_flag', 'uint8'),
    ('quality_bitmask', 'uint8'),
    ('survey_mode', 'uint8'),
    ('bia_status_info', ('uint8', 6)),
    ('sampling_rate', 'float32'),
    ('rpw_status_info', ('uint8', 8)),
    ('channel_status_info', ('uint8', 4)),
    ('input_config', 'uint32'),
    ('snapshot_len', 'uint8'),
    ('hist1d_id', 'uint8'),
    ('hist1d_param', 'uint8'),
    ('hist1d_axis', 'uint8'),
    ('hist1d_col_time', 'uint16'),
    ('hist1d_out', 'uint16'),
    ('hist1d_bins', 'uint16'),
    ('hist1d_counts', ('uint16', 256)),
]

# TDS HIST1D sampling rate in Hz
SAMPLING_RATE_HZ = [65534.375, 131068.75, 262137.5, 524275., 2097100.]

def set_hist1d(l0, task):

    # name of the packet
    name = 'TM_TDS_SCIENCE_NORMAL_HIST1D'
    logger.debug('Get data for ' + name)

    # get the HIST1D packet data
    if name in l0['TM']:
        tm = l0['TM'][name]['source_data']
    else:
        # rest of the code inside the with statement will not be called
        return np.empty(
            0,
            dtype=HIST1D,
        )

    # Sort input packets by ascending acquisition times
    tm, __ = sort_data(tm, (
        tm['PA_TDS_ACQUISITION_TIME'][:,1],
        tm['PA_TDS_ACQUISITION_TIME'][:,0],
                    ))

    # get the number of packets
    size = tm['PA_TDS_ACQUISITION_TIME'].shape[0]

    # create the data array with good size
    data = np.zeros(size, dtype=HIST1D)
    fill_records(data)

    # set the data for stat, directly a copy of the content of parameters
    data['epoch'][:] = Time().obt_to_utc(tm['PA_TDS_ACQUISITION_TIME'][:, :2], to_tt2000=True)
    data['acquisition_time'][:, :] = tm['PA_TDS_ACQUISITION_TIME'][:, :2]
    data['synchro_flag'][:] = tm['PA_TDS_ACQUISITION_TIME'][:, 2]
    data['scet'][:] = Time.cuc_to_scet(data['acquisition_time'])
    data['survey_mode'][:] = 3

    # bias info
    data['bia_status_info'][:, :] = np.vstack(
        (
            tm['PA_BIA_ON_OFF'],
            tm['PA_BIA_MODE_BIAS3_ENABLED'],
            tm['PA_BIA_MODE_BIAS2_ENABLED'],
            tm['PA_BIA_MODE_BIAS1_ENABLED'],
            tm['PA_BIA_MODE_HV_ENABLED'],
            tm['PA_BIA_MODE_MUX_SET'],
        )
    ).T

    data['channel_status_info'][:, :] = np.vstack(
        (
        tm['PA_TDS_STAT_ADC_CH1'],
        tm['PA_TDS_STAT_ADC_CH2'],
        tm['PA_TDS_STAT_ADC_CH3'],
        tm['PA_TDS_STAT_ADC_CH4'],
        )
    ).T

    # rpw status
    data['rpw_status_info'][:, :] = np.vstack(
        (
            tm['PA_TDS_THR_OFF'],
            tm['PA_TDS_LFR_OFF'],
            tm['PA_TDS_ANT1_OFF'],
            tm['PA_TDS_ANT2_OFF'],
            tm['PA_TDS_ANT3_OFF'],
            tm['PA_TDS_SCM_OFF'],
            tm['PA_TDS_HF_ART_MAG_HEATER'],
            tm['PA_TDS_HF_ART_SCM_CALIB'],
        )
    ).T

    # input config
    data['input_config'] = tm['PA_TDS_SWF_HF_CH_CONF']

    # hist parameters
    data['snapshot_len'] = tm['PA_TDS_SNAPSHOT_LEN']
    data['hist1d_id'] = tm['PA_TDS_SC_HIST1D_ID']
    data['hist1d_param'] = tm['PA_TDS_SC_HIST1D_PARAM']
    data['hist1d_axis'] = tm['PA_TDS_SC_HIST1D_BINS']
    data['hist1d_col_time'] = tm['PA_TDS_SC_HIST1D_COLL_TIME']
    data['hist1d_out'] = tm['PA_TDS_SC_HIST1D_OUT']
    data['hist1d_bins'] = tm['PA_TDS_SC_HIST1D_NUM_BINS']

    for i in range(size):
        # sampling rate
        data['sampling_rate'][i] = SAMPLING_RATE_HZ[tm['PA_TDS_STAT_SAMP_RATE'][i]]
        # HIST1D count
        ncount = len(tm['PA_TDS_SC_HIST1D_COUNTS'][i, :])
        data['hist1d_counts'][i, 0:ncount] = tm['PA_TDS_SC_HIST1D_COUNTS'][i, :]

    return data
