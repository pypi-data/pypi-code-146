#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import numpy as np
from poppy.core.logger import logger

from roc.rpl.time import Time
from roc.idb.converters.cdf_fill import fill_records

from roc.rap.tasks.utils import sort_data
from roc.rap.tasks.lfr.utils import fill_asm, set_cwf, set_swf
from roc.rap.tasks.lfr.bp import convert_BP as bp_lib

__all__ = ['asm', 'bp1', 'bp2', 'cwf', 'swf']




class L1LFRNormalBurstError(Exception):
    """
    Errors for the L1 LFR ASM data
    """


# Numpy array dtype for LFR ASM L1 survey data
# Name convention is lower case
ASM = [
    ('epoch', 'uint64'),
    ('scet', 'float64'),
    ('acquisition_time', 'uint32', 2),
    ('synchro_flag', 'uint8'),
    ('quality_flag', 'uint8'),
    ('survey_mode', 'uint8'),
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
    ('asm_cnt', 'uint8'),
    ('asm', 'float32', (128, 25)),
    ('freq', 'uint8'),
]


def set_asm(fdata, freq):
    """
    Fill LFR ASM values

    :param fdata:
    :param freq:
    :return:
    """

    # number of blocks in the packets for the current freq
    nblk = fdata['PA_LFR_ASM_{0}_BLK_NR'.format(freq)]

    asm_blks = np.zeros([nblk.shape[0], np.max(nblk), 25], dtype=np.float32)
    asm_blks[:] = -1.0e31

    asm_blks[:] = np.dstack(
        list(fdata['PA_LFR_SC_ASM_{2}_{0}{1}'.format(i, j, freq)]
         for i in range(1, 6) for j in range(1, 6))
    ).reshape((nblk.shape[0], np.max(nblk), 25)).view('float32')
    data = fill_asm(fdata, freq, ASM, asm_blks)

    return data


def asm(f, task):
    # closure to compute the data
    def get_data(freq):
        # get the asm
        if ('TM_LFR_SCIENCE_NORMAL_ASM_F' + freq) in f['TM']:
            logger.info(
                'Getting data for TM_LFR_SCIENCE_NORMAL_ASM_F' + freq
            )

            # get data from the file
            fdata = f['TM']['TM_LFR_SCIENCE_NORMAL_ASM_F' + freq]['source_data']
            ddata = {
                name: fdata[name][...] for name in fdata.keys()
            }

            # set the data correctly
            data = set_asm(ddata, 'F' + freq)

            # set specific properties
            data['freq'][:] = int(freq)

            # set SURVEY_MODE
            data['survey_mode'][:] = 0

        else:
            data = np.empty(0, dtype=ASM)

        return data

    # get data
    data = [get_data(x) for x in '012']

    # concatenate both arrays
    return np.concatenate(tuple(data))


# Numpy array dtype for LFR BP1 L1 survey data
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
    ('pe', 'float64', 26),
    ('pb', 'float64', 26),
    ('nvec_v0', 'float32', 26),
    ('nvec_v1', 'float32', 26),
    ('nvec_v2', 'uint8', 26),
    ('ellip', 'float32', 26),
    ('dop', 'float32', 26),
    ('sx_rea', 'float64', 26),
    ('sx_arg', 'uint8', 26),
    ('vphi_rea', 'float64', 26),
    ('vphi_arg', 'uint8', 26),
    ('freq', 'uint8'),
    ('survey_mode', 'uint8'),
]

NB_MAP = {
    'NORMAL': 0,
    'BURST': 1,
}

BP_LIST = [
    ('NORMAL', '0'),
    ('NORMAL', '1'),
    ('NORMAL', '2'),
    ('BURST', '0'),
    ('BURST', '1'),
]


def set_bp1(fdata, freq, task):
    """
    Fill LFR BP1 values

    :param fdata:
    :param freq:
    :param task:
    :return:
    """

    # Sort input packets by ascending acquisition times
    fdata, __ = sort_data(fdata, (
        fdata['PA_LFR_ACQUISITION_TIME'][:,1],
        fdata['PA_LFR_ACQUISITION_TIME'][:,0],
                    ))

    # create a record array with the good dtype and good length
    result = np.zeros(
        fdata['PA_LFR_ACQUISITION_TIME'].shape[0],
        dtype=BP1,
    )
    fill_records(result)

    # add common properties
    result['acquisition_time'] = fdata['PA_LFR_ACQUISITION_TIME'][:, :2]
    result['synchro_flag'] = fdata['PA_LFR_ACQUISITION_TIME'][:, 2]
    result['bias_mode_mux_set'] = fdata['PA_BIA_MODE_MUX_SET']
    result['bias_mode_hv_enabled'] = fdata['PA_BIA_MODE_HV_ENABLED']
    result['bias_mode_bias1_enabled'] = fdata[
        'PA_BIA_MODE_BIAS1_ENABLED'
    ]
    result['bias_mode_bias2_enabled'] = fdata[
        'PA_BIA_MODE_BIAS2_ENABLED'
    ]
    result['bias_mode_bias3_enabled'] = fdata[
        'PA_BIA_MODE_BIAS3_ENABLED'
    ]
    result['bias_on_off'] = fdata['PA_BIA_ON_OFF']
    result['bw'] = fdata['SY_LFR_BW']
    result['sp0'] = fdata['SY_LFR_SP0']
    result['sp1'] = fdata['SY_LFR_SP1']
    result['r0'] = fdata['SY_LFR_R0']
    result['r1'] = fdata['SY_LFR_R1']
    result['r2'] = fdata['SY_LFR_R2']

    # get the shape of the data
    # (required since number of blocks are not the same in the normal/burst F0/F1/F2 packets)
    shape = fdata['PA_LFR_SC_BP1_PE_' + freq].shape
    n = shape[1]

    # Convert BP1 values (see convert_BP.py)
    struct = namedtuple('struct', ['nbitexp', 'nbitsig', 'rangesig_16',\
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
    result['nvec_v2'][:, :n] = bp_lib.convToUint8(fdata['PA_LFR_SC_BP1_NVEC_' + freq][:, :n])

    result['ellip'][:, :n] = bp_lib.convToFloat4(
        fdata['PA_LFR_SC_BP1_ELLIP_' + freq][:, :n])

    result['dop'][:, :n] = bp_lib.convToFloat3(
        fdata['PA_LFR_SC_BP1_DOP_' + freq][:, :n])

    # Extract x-component of normalized Poynting flux...
    # sign (1 bit)...
    sx_sign = 1 - (2 * bp_lib.Uint16ToUint8(fdata['PA_LFR_SC_BP1_SX_' + freq][:, :n], 15, 0x1).astype(float))

    # real value (14 bits)
    result['sx_rea'][:, :n] = sx_sign * bp_lib.convToFloat14(struct,
                                                           fdata['PA_LFR_SC_BP1_SX_' + freq][:, :n])

    # and arg (1 bit)
    result['sx_arg'][:, :n] = bp_lib.Uint16ToUint8(fdata['PA_LFR_SC_BP1_SX_' + freq][:, :n], 14, 0x1)

    # Extract velocity phase...

    # sign (1 bit)...
    vphi_sign = 1 - (2 * bp_lib.Uint16ToUint8(fdata['PA_LFR_SC_BP1_VPHI_' + freq][:, :n], 15, 0x1).astype(float))

    # real value (14 bits)
    result['vphi_rea'][:, :n] = vphi_sign * bp_lib.convToFloat14(struct,
                                                   fdata['PA_LFR_SC_BP1_VPHI_' + freq][:, :n])

    # and arg (1 bit)
    result['vphi_arg'][:, :n] = bp_lib.Uint16ToUint8(fdata['PA_LFR_SC_BP1_VPHI_' + freq][:, :n], 14, 0x1)


    # Get TT2000 Epoch time
    result['epoch'] = Time().obt_to_utc(result['acquisition_time'], to_tt2000=True)

    # Get scet
    result['scet'] = Time.cuc_to_scet(result['acquisition_time'])

    return result


def bp1(f, task):
    # define the function to get the data
    def get_data(mode, freq):
        # get the packet name
        name = 'TM_LFR_SCIENCE_{0}_BP1_F{1}'.format(mode, freq)
        logger.debug('Get data for ' + name)

        # get the sbm2 bp1 data
        if name in f['TM']:
            # get data from the file
            fdata = f['TM'][name]['source_data']

            # set common parameters with other frequencies
            data = set_bp1(fdata, 'F' + freq, task)

            # set some specific properties
            data['freq'][:] = int(freq)
            data['survey_mode'] = NB_MAP[mode]

        else:
            data = np.empty(0, dtype=BP1)

        return data

    # get the data
    data = [get_data(mode, freq) for mode, freq in BP_LIST]

    # concatenate both arrays
    return np.concatenate(data)


# Numpy array dtype for LFR BP2 L1 survey data
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
    ('auto', 'float64', (26, 5)),
    ('cross_re', 'float32', (26, 10)),
    ('cross_im', 'float32', (26, 10)),
    ('freq', 'uint8'),
    ('survey_mode', 'uint8'),
]


def set_bp2(fdata, freq, task):

    # Sort input packets by ascending acquisition times
    fdata, __ = sort_data(fdata, (
        fdata['PA_LFR_ACQUISITION_TIME'][:,1],
        fdata['PA_LFR_ACQUISITION_TIME'][:,0],
                    ))

    # create a record array with the good dtype and good length
    data = np.zeros(
        fdata['PA_LFR_ACQUISITION_TIME'].shape[0],
        dtype=BP2,
    )
    fill_records(data)

    # get the acquisition time and other data common
    data['acquisition_time'] = fdata['PA_LFR_ACQUISITION_TIME'][:, :2]
    data['synchro_flag'] = fdata['PA_LFR_ACQUISITION_TIME'][:, 2]
    data['bias_mode_mux_set'] = fdata['PA_BIA_MODE_MUX_SET']
    data['bias_mode_hv_enabled'] = fdata['PA_BIA_MODE_HV_ENABLED']
    data['bias_mode_bias1_enabled'] = fdata[
        'PA_BIA_MODE_BIAS1_ENABLED'
    ]
    data['bias_mode_bias2_enabled'] = fdata[
        'PA_BIA_MODE_BIAS2_ENABLED'
    ]
    data['bias_mode_bias3_enabled'] = fdata[
        'PA_BIA_MODE_BIAS3_ENABLED'
    ]
    data['bias_on_off'] = fdata['PA_BIA_ON_OFF']
    data['bw'] = fdata['SY_LFR_BW']
    data['sp0'] = fdata['SY_LFR_SP0']
    data['sp1'] = fdata['SY_LFR_SP1']
    data['r0'] = fdata['SY_LFR_R0']
    data['r1'] = fdata['SY_LFR_R1']
    data['r2'] = fdata['SY_LFR_R2']

    # get the shape of the data
    shape = fdata['PA_LFR_SC_BP2_AUTO_A0_' + freq].shape
    n = shape[1]

    # more specific parameters
    auto = np.dstack(
        list(
            fdata['PA_LFR_SC_BP2_AUTO_A{0}_{1}'.format(x, freq)]
            for x in range(5)
        )
    )[:, :, :]
    cross_re = np.dstack(
        list(
            fdata['PA_LFR_SC_BP2_CROSS_RE_{0}_{1}'.format(x, freq)]
            for x in range(10)
        )
    )[:, :, :]
    cross_im = np.dstack(
        list(
            fdata['PA_LFR_SC_BP2_CROSS_IM_{0}_{1}'.format(x, freq)]
            for x in range(10)
        )
    )[:, :, :]

    # Convert AUTO, CROSS_RE an CROSS_IM (see convert_BP.py)
    struct = namedtuple('struct', ['nbitexp', 'nbitsig', 'rangesig_16', 'rangesig_14', \
                                   'expmax', 'expmin'])
    bp_lib.init_struct(struct)

    data['auto'][:, :n, :] = bp_lib.convToAutoFloat(struct, auto)
    data['cross_re'][:, :n, :] = bp_lib.convToCrossFloat(cross_re)
    data['cross_im'][:, :n, :] = bp_lib.convToCrossFloat(cross_im)

    # WARNING, IF NAN or INF, put FILLVAL
    # TODO - Optimize this part
    data['auto'][np.isinf(data['auto'])] = -1e31
    data['auto'][np.isnan(data['auto'])] = -1e31
    data['cross_re'][np.isinf(data['cross_re'])] = -1e31
    data['cross_re'][np.isnan(data['cross_re'])] = -1e31
    data['cross_im'][np.isinf(data['cross_im'])] = -1e31
    data['cross_im'][np.isnan(data['cross_im'])] = -1e31

    # Get TT2000 Epoch time
    data['epoch'] = Time().obt_to_utc(data['acquisition_time'], to_tt2000=True)

    # Get scet
    data['scet'] = Time.cuc_to_scet(data['acquisition_time'])

    return data


def bp2(f, task):
    # define the function to get the data
    def get_data(mode, freq):
        # get the packet name
        name = 'TM_LFR_SCIENCE_{0}_BP2_F{1}'.format(mode, freq)
        logger.info('Get data for ' + name)

        # get the sbm2 bp1 data
        if name in f['TM']:
            # get data from the file
            fdata = f['TM'][name]['source_data']

            # set common parameters with other frequencies
            data = set_bp2(fdata, 'F' + freq, task)

            # set some specific properties
            data['freq'][:] = int(freq)
            data['survey_mode'] = NB_MAP[mode]

        else:
            data = np.empty(0, dtype=BP2)

        return data

    # get the data
    data = [get_data(mode, freq) for mode, freq in BP_LIST]

    # concatenate both arrays
    return np.concatenate(data)

# Numpy array dtype for LFR CWF L1 survey data
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
    ('v', 'int16'),
    ('e', 'int16', 2),
    ('b', 'int16', 3),
    ('freq', 'uint8'),
    ('sampling_rate', 'float32'),
    ('survey_mode', 'uint8'),
    ('type', 'uint8'),
]


def cwf(f, task):
    """LFR CWF packet data."""
    if 'TM_LFR_SCIENCE_NORMAL_CWF_F3' in f['TM']:
        # get data from the file
        logger.info('Get data for TM_LFR_SCIENCE_NORMAL_CWF_F3')
        fdata = f['TM']['TM_LFR_SCIENCE_NORMAL_CWF_F3']['source_data']

        ddata = {
            name: fdata[name][...] for name in fdata.keys()
        }

        # create data with common
        data = set_cwf(ddata, 'F3', CWF, False, task)

        # specific parameters
        data['freq'][:] = 3
        data['type'][:] = 0
        data['survey_mode'][:] = 0

    else:
        data = np.empty(0, dtype=CWF)

    if 'TM_LFR_SCIENCE_NORMAL_CWF_LONG_F3' in f['TM']:
        # get data from the file
        logger.info('Get data for TM_LFR_SCIENCE_NORMAL_CWF_LONG_F3')
        fdata = f['TM']['TM_LFR_SCIENCE_NORMAL_CWF_LONG_F3']['source_data']

        ddata = {
            name: fdata[name][...] for name in fdata.keys()
        }

        # create data with common
        data1 = set_cwf(ddata, 'LONG_F3', CWF, True, task)

        # specific parameters
        data1['freq'][:] = 3
        data1['type'][:] = 1
        data1['survey_mode'][:] = 0

    else:
        data1 = np.empty(0, dtype=CWF)

    if 'TM_LFR_SCIENCE_BURST_CWF_F2' in f['TM']:
        # get data from the file
        logger.info('Get data for TM_LFR_SCIENCE_BURST_CWF_F2')
        fdata = f['TM']['TM_LFR_SCIENCE_BURST_CWF_F2']['source_data']

        ddata = {
            name: fdata[name][...] for name in fdata.keys()
        }

        # create data with common
        data2 = set_cwf(ddata, 'F2', CWF, True, task)

        # specific parameters
        data2['freq'][:] = 2
        data2['type'][:] = 0
        data2['survey_mode'][:] = 1

    else:
        data2 = np.empty(0, dtype=CWF)

    # concatenate both arrays
    return np.concatenate((data, data1, data2))

# Numpy array dtype for LFR SWF L1 survey data
# Name convention is lower case
SWF = [
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
    ('v', 'int16', 2048),
    ('e', 'int16', (2, 2048)),
    ('b', 'int16', (3, 2048)),
    ('freq', 'uint8'),
    ('sampling_rate', 'float32'),
    ('survey_mode', 'uint8'),
]


def swf(f, task):
    # closure for getting the data for several packets
    def get_data(freq):
        if 'TM_LFR_SCIENCE_NORMAL_SWF_F' + freq in f['TM']:
            # get data from the file
            logger.info('Get data for TM_LFR_SCIENCE_NORMAL_SWF_F' + freq)
            fdata = f['TM']['TM_LFR_SCIENCE_NORMAL_SWF_F' + freq]['source_data']

            # copy data from file to numpy
            ddata = {
                name: fdata[name][...] for name in fdata.keys()
            }

            # create data with common
            data = set_swf(ddata, 'F' + freq, SWF, task)

            # specific parameters
            data['freq'][:] = int(freq)
            data['survey_mode'][:] = 0

        else:
            data = np.empty(0, dtype=SWF)

        return data

    # get the data
    data = [get_data(x) for x in '012']


    x = np.concatenate(tuple(data))

    # concatenate both arrays
    return np.concatenate(tuple(data))
