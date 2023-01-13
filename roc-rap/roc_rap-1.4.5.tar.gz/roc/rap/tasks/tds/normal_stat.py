#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from poppy.core.logger import logger

from roc.rpl.time import Time
from roc.idb.converters.cdf_fill import fill_records

from roc.rap.tasks.utils import sort_data


__all__ = ['STAT', 'set_stat']



# Numpy array dtype for TDS STAT L1 survey data
# Name convention is lower case

STAT = [
    ('epoch', 'uint64'),
    ('scet', 'float64'),
    ('acquisition_time', ('uint32', 2)),
    ('synchro_flag', 'uint8'),
    ('quality_flag', 'uint8'),
    ('quality_bitmask', 'uint8'),
    ('survey_mode', 'uint8'),
    ('bia_status_info', ('uint8', 6)),
    ('channel_status_info', ('uint8', 4)),
    ('sampling_rate', 'uint8'),
    ('rpw_status_info', ('uint8', 8)),
    ('input_config', 'uint32'),
    ('snapshot_len', 'uint8'),
    ('sn_nr_events', 'uint8'),
    ('sn_max_e', 'uint16'),
    ('sn_med_max_e', 'uint16'),
    ('sn_rms_e', 'uint16'),
    ('sn_threshold', 'uint16'),
    ('du_nr_impact', 'uint8'),
    ('du_med_imp', 'uint16'),
    ('wa_amp_max', 'uint16'),
    ('wa_amp_med', 'uint16'),
    ('wa_rms', 'uint16'),
    ('wa_nr_events', 'uint8'),
    ('wa_med_freq', 'uint8'),
]


def set_stat(l0, task):
    """
    Extract TM_TDS_SCIENCE_NORMAL_STAT data

    :param l0: h5py.h5 object containing the RPW TM/TC packets
    :param task: POPPy task
    :return: numpy array with TDS stat data
    """

    # name of the packet
    name = 'TM_TDS_SCIENCE_NORMAL_STAT'
    logger.debug('Get data for ' + name)

    # get the TDS STAT packet data
    if name in l0['TM']:
        tm = l0['TM'][name]['source_data']
    else:
        # rest of the code inside the with statement will not be called
        return np.empty(
            0,
            dtype=STAT,
        )

    # Sort input packets by ascending acquisition times
    tm, __ = sort_data(tm, (
        tm['PA_TDS_ACQUISITION_TIME'][:,1],
        tm['PA_TDS_ACQUISITION_TIME'][:,0],
                    ))

    # get the number of packets
    size = tm['PA_TDS_ACQUISITION_TIME'].shape[0]
    logger.debug('Number of packets: {0}'.format(size))

    # create the data array with good size
    data = np.zeros(size, dtype=STAT)
    fill_records(data)

    # set the data for stat, directly a copy of the content of parameters
    data['epoch'][:] = Time().obt_to_utc(tm['PA_TDS_ACQUISITION_TIME'][:, :2], to_tt2000=True)
    data['acquisition_time'][:, :] = tm['PA_TDS_ACQUISITION_TIME'][:, :2]
    data['synchro_flag'][:] = tm['PA_TDS_ACQUISITION_TIME'][:, 2]
    data['scet'][:] = Time.cuc_to_scet(data['acquisition_time'])
    data['survey_mode'][:] = 0

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

    # sampling rate
    data['sampling_rate'] = tm['PA_TDS_STAT_SAMP_RATE']

    # Channel status info
    data['channel_status_info'] = np.vstack(
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

    # stat parameters
    data['snapshot_len'] = tm['PA_TDS_SNAPSHOT_LEN']
    data['sn_nr_events'] = tm['PA_TDS_SC_STAT_SN_NR_EVENTS']
    data['sn_max_e'] = tm['PA_TDS_SC_STAT_SN_MAX_E']
    data['sn_med_max_e'] = tm['PA_TDS_SC_STAT_SN_MED_MAX_E']
    data['sn_rms_e'] = tm['PA_TDS_SC_STAT_SN_RMS_E']
    data['sn_threshold'] = tm['PA_TDS_SC_STAT_SN_THRESHOLD']
    data['du_nr_impact'] = tm['PA_TDS_SC_STAT_DU_NR_IMPACT']
    data['du_med_imp'] = tm['PA_TDS_SC_STAT_DU_MED_IMP']
    data['wa_amp_max'] = tm['PA_TDS_SC_STAT_WA_AMP_MAX']
    data['wa_amp_med'] = tm['PA_TDS_SC_STAT_WA_AMP_MED']
    data['wa_rms'] = tm['PA_TDS_SC_STAT_WA_RMS']
    data['wa_nr_events'] = tm['PA_TDS_SC_STAT_WA_NR_EVENTS']
    data['wa_med_freq'] = tm['PA_TDS_SC_STAT_WA_MED_FREQ']

    return data
