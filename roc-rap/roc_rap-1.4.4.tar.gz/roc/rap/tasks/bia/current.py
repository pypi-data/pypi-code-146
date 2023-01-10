#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime

from poppy.core.logger import logger
from roc.rap.tasks.utils import decode

from roc.rpl.time import Time
from roc.rpl.packet_parser import raw_to_eng
from roc.rpl.constants import TIME_ISO_STRFORMAT

# Numpy array dtype for BIAS current data
# Name convention is lower case
from roc.rap import MetadataException

CURRENT_DTYPE = [
    ('epoch', 'uint64'),
    ('ibias_1', 'float32'),
    ('ibias_2', 'float32'),
    ('ibias_3', 'float32'),
]

# Number of antennas (3)
ANT_NUM = 3

# SRDB ID of the transfer function TF_CP_BIA_P011 (or TF_CP_BIA_0011 in ICD)
# NOTES: SRDB_ID is CIWP0075TC and not CIWP0040TC as indicated in the ICD)
TF_CP_BIA_P011_SRDB_ID = 'CIWP0075TC'

def set_current(l0, task):
    """
    Set Bias current values from TC_DPU_SET_BIAi

    :param l0: input l0 files
    :return:
    """

    from roc.idb.converters.cdf_fill import fill_records

    # Get/create time instance
    time = Time()

    # Get number of TC_DPU_SET_BIAS1/2/3 packets in L0
    # (One packet == one record)
    sizes = np.zeros(ANT_NUM, dtype=np.uint32)
    for i in range(ANT_NUM):
        tc_name = 'TC_DPU_SET_BIAS{0}'.format(i + 1)
        if tc_name in l0['TC']:
            ack_exe_state = decode(l0['TC'][tc_name]['tc_ack_state'][:, 1])
            where_exe_passed = ack_exe_state[ack_exe_state == 'PASSED']
            sizes[i] = where_exe_passed.shape[0]
        else:
            logger.warning(f'No {tc_name} in input L0 file!')


    # Get number of output records (one by TC_DPU_SET_BIAS1/2/3 packets)
    nrec = np.sum(sizes)
    # And initialize the output numpy array for BIAS current L1 data
    data = np.empty(nrec, dtype=CURRENT_DTYPE)
    if nrec > 0:
        # create a record array with the good dtype and good length
        fill_records(data)
    else:
        # if no data, return empty array
        return data

    # Fill the data numpy array
    counter = 0
    for i in range(ANT_NUM):
        tc_name = 'TC_DPU_SET_BIAS{0}'.format(i + 1)
        if tc_name not in l0['TC']:
            continue
        else:
            ack_exe_state = decode(l0['TC'][tc_name]['tc_ack_state'][:, 1])
            where_exe_passed = ack_exe_state == 'PASSED'

        # If not 'passed' TC, then continue
        if not where_exe_passed.any():
            continue
        else:
            ibias = l0['TC'][tc_name]['application_data']['CP_BIA_SET_BIAS{0}'.format(i + 1)][where_exe_passed]
            utc_time = decode(l0['TC'][tc_name]['utc_time'][where_exe_passed])
            idb_source = decode(l0['TC'][tc_name]['idb'][where_exe_passed, 0][0])
            idb_version = decode(l0['TC'][tc_name]['idb'][where_exe_passed, 1][0])
            size = len(ibias)

        # Else store the bias current intensity values found in the output sample array
        # TODO - See how to deal if IDB version change in the output sample array
        data['ibias_{0}'.format(i+1)][counter:counter + size] = raw_to_na(ibias,
                                                                          idb_source=idb_source,
                                                                          idb_version=idb_version)

        # And corresponding TC execution time (UTC in input L0)
        data['epoch'][counter:counter + size] = [time.utc_to_tt2000(datetime.strptime(current_time[:-4],
                                                                                      TIME_ISO_STRFORMAT[:-1]))
                                                 for current_time in utc_time]

        # Increment counter
        counter += size

    return data

def raw_to_na(raw_values,
              idb_source='MIB',
              idb_version=None):
    """
    Convert input raw values of bias current into physical units (nA)

    :param raw_values: numpy array with raw values of Bias current
    :param idb_version: string with idb version
    :param idb_source: string with idb_source
    :return: values in physical units (nA)
    """

    # Retrieve engineering values in uA and return them in nA
    return raw_to_eng(raw_values, TF_CP_BIA_P011_SRDB_ID,
                    idb_source=idb_source, idb_version=idb_version) * 1000
