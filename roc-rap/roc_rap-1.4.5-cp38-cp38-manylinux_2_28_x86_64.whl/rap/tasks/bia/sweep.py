#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from poppy.core.logger import logger

from roc.rpl.time import Time

from roc.idb.converters.cdf_fill import fill_records

# Numpy array dtype for BIAS sweep data
# Name convention is lower case
from roc.rap.tasks.utils import sort_data

SWEEP_DTYPE = [
    ('epoch', 'uint64'),
    ('scet', 'float64'),
    ('acquisition_time', 'uint32', 2),
    ('synchro_flag', 'uint8'),
    ('quality_flag', 'uint8'),
    ('quality_bitmask', 'uint8'),
    ('bias_mode_mux_set', 'uint8'),
    ('bias_mode_hv_enabled', 'uint8'),
    ('bias_mode_bias1_enabled', 'uint8'),
    ('bias_mode_bias2_enabled', 'uint8'),
    ('bias_mode_bias3_enabled', 'uint8'),
    ('bias_mode_bypass_probe1', 'uint8'),
    ('bias_mode_bypass_probe2', 'uint8'),
    ('bias_mode_bypass_probe3', 'uint8'),
    ('bias_on_off', 'uint8'),
    ('ant_flag', 'uint8'),
    ('bw', 'uint8'),
    ('sp0', 'uint8'),
    ('sp1', 'uint8'),
    ('r0', 'uint8'),
    ('r1', 'uint8'),
    ('r2', 'uint8'),
    ('sampling_rate', 'float32'),
    ('v', 'float32', 3),
    ('bias_sweep_current', 'float32', 3),
]

# Factor to convert LFR Bias sweep data voltage into volts, i.e., V_TM ~ V_Volt * 8000 * 1/17
# Provided by Yuri
BIA_SWEEP_TM2V_FACTOR = 1.0 / (8000 * 1.0 / 17.0)

# F3 = 16Hz
CWF_SAMPLING_RATE = 16.0


def set_sweep(l0, task, freq):
    # Get/create time instance
    time_instance = Time()

    # Get the number of packets
    size = l0['PA_LFR_ACQUISITION_TIME'].shape[0]

    if freq == 'F3':
        blk_nr = l0['PA_LFR_CWF3_BLK_NR'][:]
    elif freq == 'LONG_F3':
        blk_nr = l0['PA_LFR_CWFL3_BLK_NR'][:]
        freq = freq[-2:]
    else:
        logger.warning(f'Unknown frequency label {freq}')
        return np.empty(size, dtype=SWEEP_DTYPE)

    # Sort input packets by ascending acquisition times
    l0, __ = sort_data(l0, (
        l0['PA_LFR_ACQUISITION_TIME'][:, 1],
        l0['PA_LFR_ACQUISITION_TIME'][:, 0],
    ))

    # Total number of samples
    nsamps = np.sum(blk_nr)

    # Sampling rate
    samp_rate = CWF_SAMPLING_RATE

    # Cadence in nanosec
    delta_t = 1.0e9 / samp_rate

    # create a record array with the good dtype and good length
    data = np.empty(nsamps, dtype=SWEEP_DTYPE)
    fill_records(data)

    # Loop over packets
    i = 0
    for packet in range(size):
        # Get the number of samples for the current packet
        nsamp = blk_nr[packet]

        # get the acquisition time and time synch. flag
        data['acquisition_time'][i:i + nsamp, :] = \
            l0['PA_LFR_ACQUISITION_TIME'][packet, :2]
        data['synchro_flag'][i:i + nsamp] = \
            l0['PA_LFR_ACQUISITION_TIME'][packet, 2]

        # Compute corresponding Epoch time
        epoch0 = time_instance.obt_to_utc(
            l0['PA_LFR_ACQUISITION_TIME'][packet, :2].reshape([1, 2]),
            to_tt2000=True)

        data['epoch'][i:i + nsamp] = epoch0 + np.uint64(delta_t * np.arange(0, nsamp, 1))

        data['scet'][i:i + nsamp] = Time.cuc_to_scet(data['acquisition_time'][i:i + nsamp, :])

        data['bias_mode_mux_set'][i:i + nsamp] = \
            l0['PA_BIA_MODE_MUX_SET'][packet]
        data['bias_mode_hv_enabled'][i:i + nsamp] = \
            l0['PA_BIA_MODE_HV_ENABLED'][packet]
        data['bias_mode_bias1_enabled'][i:i + nsamp] = \
            l0['PA_BIA_MODE_BIAS1_ENABLED'][packet]
        data['bias_mode_bias2_enabled'][i:i + nsamp] = \
            l0['PA_BIA_MODE_BIAS2_ENABLED'][packet]
        data['bias_mode_bias3_enabled'][i:i + nsamp] = \
            l0['PA_BIA_MODE_BIAS3_ENABLED'][packet]
        data['bias_on_off'][i:i + nsamp] = l0['PA_BIA_ON_OFF'][packet]
        data['bw'][i:i + nsamp] = l0['SY_LFR_BW'][packet]
        data['sp0'][i:i + nsamp] = l0['SY_LFR_SP0'][packet]
        data['sp1'][i:i + nsamp] = l0['SY_LFR_SP1'][packet]
        data['r0'][i:i + nsamp] = l0['SY_LFR_R0'][packet]
        data['r1'][i:i + nsamp] = l0['SY_LFR_R1'][packet]
        data['r2'][i:i + nsamp] = l0['SY_LFR_R2'][packet]

        # Fill sampling rate
        data['sampling_rate'][i:i + nsamp] = CWF_SAMPLING_RATE

        # Electrical potential on each antenna 1, 2 and 3 (just need to be reshaped)
        data['v'][i:i + nsamp, 0] = raw_to_volts(l0['PA_LFR_SC_V_' + freq][packet, :])
        data['v'][i:i + nsamp, 1] = raw_to_volts(l0['PA_LFR_SC_E1_' + freq][packet, :])
        data['v'][i:i + nsamp, 2] = raw_to_volts(l0['PA_LFR_SC_E2_' + freq][packet, :])

        i += nsamp

    return data


def raw_to_volts(raw_value):
    """
    Convert LFR V raw value to Volts units.

    Comment from Bias team:
    'for DC single(which we have for mux=4, BIAS_1-3), and BIAS+LFR,
    the conversion should be _approximately_ V_TM = V_Volt * 8000 * 1/17'

    :param raw_value: LFR F3 V value in count. Can be a scalar or a numpy array
    :return: value in Volts
    """
    return raw_value * BIA_SWEEP_TM2V_FACTOR
