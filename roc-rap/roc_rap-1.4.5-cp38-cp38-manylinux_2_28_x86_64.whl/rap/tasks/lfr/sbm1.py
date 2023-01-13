#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import numpy as np
from poppy.core.logger import logger

from roc.rpl.time import Time
from roc.idb.converters.cdf_fill import fill_records

from roc.rap.tasks.utils import sort_data
from roc.rap.tasks.lfr.utils import set_cwf
from roc.rap.tasks.lfr.bp import convert_BP as bp_lib

__all__ = ['bp1', 'bp2', 'cwf']


class L1LFRSBM1Error(Exception):
    """
    Errors for L1 SBM1 LFR.
    """


# Numpy array dtype for LFR BP1 L1 SBM1 data
# Name convention is lower case
BP1 = [
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
    ('bias_on_off', 'uint8'),
    ('bw', 'uint8'),
    ('sp0', 'uint8'),
    ('sp1', 'uint8'),
    ('r0', 'uint8'),
    ('r1', 'uint8'),
    ('r2', 'uint8'),
    ('pe', 'float64', 22),
    ('pb', 'float64', 22),
    ('nvec_v0', 'float32', 22),
    ('nvec_v1', 'float32', 22),
    ('nvec_v2', 'uint8', 22),
    ('ellip', 'float32', 22),
    ('dop', 'float32', 22),
    ('sx_rea', 'float64', 22),
    ('sx_arg', 'uint8', 22),
    ('vphi_rea', 'float64', 22),
    ('vphi_arg', 'uint8', 22),
]


def bp1(f, task):
    # name of the packet
    freq = 'F0'
    name = 'TM_LFR_SCIENCE_SBM1_BP1_' + freq
    logger.debug('Get data for ' + name)

    # get the sbm1 bp1 data
    if name in f['TM']:
        fdata = f['TM'][name]['source_data']
    else:
        # rest of the code inside the with statement will not be called
        return np.empty(
            0,
            dtype=BP1,
        )

    # Sort input packets by ascending acquisition times
    fdata, __ = sort_data(fdata, (
        fdata['PA_LFR_ACQUISITION_TIME'][:, 1],
        fdata['PA_LFR_ACQUISITION_TIME'][:, 0],
    ))

    # create an array for the data
    result = np.empty(
        fdata['PA_LFR_ACQUISITION_TIME'].shape[0],
        dtype=BP1,
    )
    fill_records(result)

    # Get number of packets and blocks
    shape = fdata['PA_LFR_SC_BP1_PE_' + freq].shape
    n = shape[1]

    # get the acquisition time and other data
    result['acquisition_time'] = fdata['PA_LFR_ACQUISITION_TIME'][:, :2]
    result['synchro_flag'] = fdata['PA_LFR_ACQUISITION_TIME'][:, 2]
    result['bias_mode_mux_set'] = fdata['PA_BIA_MODE_MUX_SET']
    result['bias_mode_hv_enabled'] = fdata['PA_BIA_MODE_HV_ENABLED']
    result['bias_mode_bias1_enabled'] = fdata['PA_BIA_MODE_BIAS1_ENABLED']
    result['bias_mode_bias2_enabled'] = fdata['PA_BIA_MODE_BIAS2_ENABLED']
    result['bias_mode_bias3_enabled'] = fdata['PA_BIA_MODE_BIAS3_ENABLED']
    result['bias_on_off'] = fdata['PA_BIA_ON_OFF']
    result['bw'] = fdata['SY_LFR_BW']
    result['sp0'] = fdata['SY_LFR_SP0']
    result['sp1'] = fdata['SY_LFR_SP1']
    result['r0'] = fdata['SY_LFR_R0']
    result['r1'] = fdata['SY_LFR_R1']
    result['r2'] = fdata['SY_LFR_R2']

    # Convert BP1 values (see convert_BP.py)
    struct = namedtuple('struct', ['nbitexp', 'nbitsig', 'rangesig_16',
                                   'rangesig_14', 'expmax', 'expmin'])
    bp_lib.init_struct(struct)

    result['pe'][:, :n] = bp_lib.convToFloat16(struct,
                                               fdata['PA_LFR_SC_BP1_PE_' + freq][:, :n])
    result['pb'][:, :n] = bp_lib.convToFloat16(struct,
                                               fdata['PA_LFR_SC_BP1_PB_' + freq][:, :n])
    # Compute n1 component of k-vector (normalized)
    result['nvec_v0'][:, :n] = bp_lib.convToFloat8(
        fdata['PA_LFR_SC_BP1_NVEC_V0_' + freq][:, :n])
    # Compute n2 component of k-vector (normalized)
    result['nvec_v1'][:, :n] = bp_lib.convToFloat8(
        fdata['PA_LFR_SC_BP1_NVEC_V1_' + freq][:, :n])

    # Store the 1b bit of the sign of n3 components k-vector in nvec_v2
    result['nvec_v2'][:, :n] = bp_lib.convToUint8(
        fdata['PA_LFR_SC_BP1_NVEC_' + freq][:, :n])

    result['ellip'][:, :n] = bp_lib.convToFloat4(
        fdata['PA_LFR_SC_BP1_ELLIP_' + freq][:, :n])

    result['dop'][:, :n] = bp_lib.convToFloat3(
        fdata['PA_LFR_SC_BP1_DOP_' + freq][:, :n])

    # Extract x-component of normalized Poynting flux...
    # sign (1 bit)...
    sx_sign = 1 - \
        (2 * bp_lib.Uint16ToUint8(fdata['PA_LFR_SC_BP1_SX_' +
                                        freq][:, :n], 15, 0x1).astype(float))

    # real value (14 bits)
    result['sx_rea'][:, :n] = sx_sign * bp_lib.convToFloat14(struct,
                                                             fdata['PA_LFR_SC_BP1_SX_' + freq][:, :n])

    # and arg (1 bit)
    result['sx_arg'][:, :n] = bp_lib.Uint16ToUint8(
        fdata['PA_LFR_SC_BP1_SX_' + freq][:, :n], 14, 0x1)

    # Extract velocity phase...

    # sign (1 bit)...
    vphi_sign = 1 - (2 * bp_lib.Uint16ToUint8(
        fdata['PA_LFR_SC_BP1_VPHI_' + freq][:, :n], 15, 0x1).astype(float))

    # real value (14 bits)
    result['vphi_rea'][:, :n] = vphi_sign * bp_lib.convToFloat14(struct,
                                                                 fdata['PA_LFR_SC_BP1_VPHI_' + freq][:, :n])

    # and arg (1 bit)
    result['vphi_arg'][:, :n] = bp_lib.Uint16ToUint8(
        fdata['PA_LFR_SC_BP1_VPHI_' + freq][:, :n], 14, 0x1)

    # Get TT2000 Epoch time
    result['epoch'] = Time().obt_to_utc(
        result['acquisition_time'], to_tt2000=True)

    # Get scet
    result['scet'] = Time.cuc_to_scet(result['acquisition_time'])

    return result

# Numpy array dtype for LFR BP2 L1 SBM1 data
# Name convention is lower case
BP2 = [
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
    ('bias_on_off', 'uint8'),
    ('bw', 'uint8'),
    ('sp0', 'uint8'),
    ('sp1', 'uint8'),
    ('r0', 'uint8'),
    ('r1', 'uint8'),
    ('r2', 'uint8'),
    ('auto', 'float64', (22, 5)),
    ('cross_re', 'float32', (22, 10)),
    ('cross_im', 'float32', (22, 10)),
]


def bp2(f, task):
    # name of the packet
    name = 'TM_LFR_SCIENCE_SBM1_BP2_F0'
    logger.debug('Get data for ' + name)
    # get the sbm1 bp2 data
    if name in f['TM']:
        data = f['TM'][name]['source_data']
    else:
        return np.empty(
            0,
            dtype=BP2,
        )

    # Sort input packets by ascending acquisition times
    data, __ = sort_data(data, (
        data['PA_LFR_ACQUISITION_TIME'][:, 1],
        data['PA_LFR_ACQUISITION_TIME'][:, 0],
    ))

    # create an array for the data
    result = np.empty(
        data['PA_LFR_ACQUISITION_TIME'].shape[0],
        dtype=BP2,
    )
    fill_records(result)

    # get the acquisition time and other data
    result['acquisition_time'] = data['PA_LFR_ACQUISITION_TIME'][:, :2]
    result['synchro_flag'] = data['PA_LFR_ACQUISITION_TIME'][:, 2]
    result['bias_mode_mux_set'] = data['PA_BIA_MODE_MUX_SET']
    result['bias_mode_hv_enabled'] = data['PA_BIA_MODE_HV_ENABLED']
    result['bias_mode_bias1_enabled'] = data['PA_BIA_MODE_BIAS1_ENABLED']
    result['bias_mode_bias2_enabled'] = data['PA_BIA_MODE_BIAS2_ENABLED']
    result['bias_mode_bias3_enabled'] = data['PA_BIA_MODE_BIAS3_ENABLED']
    result['bias_on_off'] = data['PA_BIA_ON_OFF']
    result['bw'] = data['SY_LFR_BW']
    result['sp0'] = data['SY_LFR_SP0']
    result['sp1'] = data['SY_LFR_SP1']
    result['r0'] = data['SY_LFR_R0']
    result['r1'] = data['SY_LFR_R1']
    result['r2'] = data['SY_LFR_R2']

    auto = np.dstack(
        list(
            data['PA_LFR_SC_BP2_AUTO_A{0}_F0'.format(x)]
            for x in range(5)
        )
    )
    cross_re = np.dstack(
        list(
            data['PA_LFR_SC_BP2_CROSS_RE_{0}_F0'.format(x)]
            for x in range(10)
        )
    )
    cross_im = np.dstack(
        list(
            data['PA_LFR_SC_BP2_CROSS_IM_{0}_F0'.format(x)]
            for x in range(10)
        )
    )

    # Get number of packets and blocks
    shape = data['PA_LFR_SC_BP2_AUTO_A0_F0'].shape
    n = shape[1]

    # Convert AUTO, CROSS_RE an CROSS_IM (see convert_BP.py)
    struct = namedtuple('struct', ['nbitexp', 'nbitsig', 'rangesig_16', 'rangesig_14',
                                   'expmax', 'expmin'])
    bp_lib.init_struct(struct)

    result['auto'][:, :n, :] = bp_lib.convToAutoFloat(struct, auto)
    result['cross_re'][:, :n, :] = bp_lib.convToCrossFloat(cross_re)
    result['cross_im'][:, :n, :] = bp_lib.convToCrossFloat(cross_im)

    # WARNING, IF NAN or INF, put FILLVAL
    # TODO - Optimize this part
    result['auto'][np.isinf(result['auto'])] = -1e31
    result['auto'][np.isnan(result['auto'])] = -1e31
    result['cross_re'][np.isinf(result['cross_re'])] = -1e31
    result['cross_re'][np.isnan(result['cross_re'])] = -1e31
    result['cross_im'][np.isinf(result['cross_im'])] = -1e31
    result['cross_im'][np.isnan(result['cross_im'])] = -1e31

    # Get Epoch in nanoseconds
    result['epoch'] = Time().obt_to_utc(
        result['acquisition_time'], to_tt2000=True)

    # Get scet
    result['scet'] = Time.cuc_to_scet(result['acquisition_time'])

    return result

# Numpy array dtype for LFR CWF L1 SBM1 data
# Name convention is lower case
CWF = [
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
    ('bias_on_off', 'uint8'),
    ('bw', 'uint8'),
    ('sp0', 'uint8'),
    ('sp1', 'uint8'),
    ('r0', 'uint8'),
    ('r1', 'uint8'),
    ('r2', 'uint8'),
    ('freq', 'uint8'),
    ('sampling_rate', 'float32'),
    ('v', 'int16'),
    ('e', 'int16', 2),
    ('b', 'int16', 3),
]


def cwf(f, task):
    # name of the packet
    name = 'TM_LFR_SCIENCE_SBM1_CWF_F1'
    logger.debug('Get data for ' + name)

    # get the sbm1 bp1 data
    if name in f['TM']:
        fdata = f['TM'][name]['source_data']
    else:
        return np.empty(
            0,
            dtype=CWF,
        )

    in_data = {
        name: fdata[name][...] for name in fdata.keys()
    }

    # get the data for cwf
    out_data = set_cwf(in_data, 'F1', CWF, True, task)

    # specific parameters
    out_data['freq'][:] = 1

    return out_data
