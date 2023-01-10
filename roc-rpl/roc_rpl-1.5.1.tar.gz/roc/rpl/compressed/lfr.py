#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the special handling of compressed data inside LFR packets.
"""

from roc.rpl.exceptions import RPLError
from roc.rpl.packet_parser.packet_parser import PacketParser
from .utils import get_base_packet

__all__ = []

def get_base_lfr(Packet):
    """
    Generate the base class to use for compressed packets in the case of LFR.
    """
    # base class for compressed packet
    Base = get_base_packet(Packet)

    # base class for the compressed packets of LFR
    class LFR(Base):
        """
        Base class for the compressed packets of LFR. Define the special
        behaviour of the treatment for those packets, that should mimic the non
        compressed (NC) ones.
        """
        def uncompressed_byte_size(self, data, values):
            """
            To get the size in bytes of the uncompressed data.
            """
            # get the number of blocks and return the size in bytes of the
            # uncompressed data
            if values[self.idx_nblocks] > self.nblocks.maximum:
                raise RPLError(
                    'The number of blocks is superior to authorized values' +
                    ' for packet {0}: {1} with maximum {2}'.format(
                        self.name,
                        values[self.idx_nblocks],
                        self.nblocks.maximum,
                    )
                )
            return values[self.idx_nblocks] * self.block_size

    return LFR


def create_packet(Packet):
    """
    Given the base class of the packets to use, add special methods into the
    new class to be able to treat the compressed packet as an existing one.
    """
    # get the base class for LFR
    LFR = get_base_lfr(Packet)

    # base class for the compressed packets of LFR
    class BurstCWFF2(LFR):
        DATA_START = 'PA_LFR_COMP_DATA_BLK'
        DATA_COUNT = 'PA_LFR_B_CWF_F2_C_BLK_NR'
        START = 'PA_LFR_COMPUTED_CRC'
        NBLOCK = 'PA_LFR_CWF_BLK_NR'
        NC_DATA_START = 'PA_LFR_SC_V_F2'

    BurstCWFF2('TM_LFR_SCIENCE_BURST_CWF_F2_C')

    class NormalCWFF3(LFR):
        DATA_START = 'PA_LFR_COMP_DATA_BLK'
        DATA_COUNT = 'PA_LFR_N_CWF_F3_C_BLK_NR'
        START = 'PA_LFR_COMPUTED_CRC'
        NBLOCK = 'PA_LFR_CWF3_BLK_NR'
        NC_DATA_START = 'PA_LFR_SC_V_F3'

    NormalCWFF3('TM_LFR_SCIENCE_NORMAL_CWF_F3_C')
    NormalCWFF3('TM_DPU_SCIENCE_BIAS_CALIB_C')

    class NormalCWFLongF3(NormalCWFF3):
        NBLOCK = 'PA_LFR_CWFL3_BLK_NR'

    NormalCWFLongF3('TM_LFR_SCIENCE_NORMAL_CWF_LONG_F3_C')
    NormalCWFLongF3('TM_DPU_SCIENCE_BIAS_CALIB_LONG_C')

    class NormalSWFF0(LFR):
        DATA_START = 'PA_LFR_COMP_DATA_BLK'
        DATA_COUNT = 'PA_LFR_N_SWF_F0_C_BLK_NR'
        START = 'PA_LFR_COMPUTED_CRC'
        NBLOCK = 'PA_LFR_SWF_BLK_NR'
        NC_DATA_START = 'PA_LFR_SC_V_F0'

    NormalSWFF0('TM_LFR_SCIENCE_NORMAL_SWF_F0_C')

    class NormalSWFF1(LFR):
        DATA_START = 'PA_LFR_COMP_DATA_BLK'
        DATA_COUNT = 'PA_LFR_N_SWF_F1_C_BLK_NR'
        START = 'PA_LFR_COMPUTED_CRC'
        NBLOCK = 'PA_LFR_SWF_BLK_NR'
        NC_DATA_START = 'PA_LFR_SC_V_F1'

    NormalSWFF1('TM_LFR_SCIENCE_NORMAL_SWF_F1_C')

    class NormalSWFF2(LFR):
        DATA_START = 'PA_LFR_COMP_DATA_BLK'
        DATA_COUNT = 'PA_LFR_N_SWF_F2_C_BLK_NR'
        START = 'PA_LFR_COMPUTED_CRC'
        NBLOCK = 'PA_LFR_SWF_BLK_NR'
        NC_DATA_START = 'PA_LFR_SC_V_F2'

    NormalSWFF2('TM_LFR_SCIENCE_NORMAL_SWF_F2_C')

    class SBM1CWFF1(LFR):
        DATA_START = 'PA_LFR_COMP_DATA_BLK'
        DATA_COUNT = 'PA_LFR_S1_CWF_F1_C_BLK_NR'
        START = 'PA_LFR_COMPUTED_CRC'
        NBLOCK = 'PA_LFR_CWF_BLK_NR'
        NC_DATA_START = 'PA_LFR_SC_V_F1'

    SBM1CWFF1('TM_LFR_SCIENCE_SBM1_CWF_F1_C')

    class SBM2CWFF2(LFR):
        DATA_START = 'PA_LFR_COMP_DATA_BLK'
        DATA_COUNT = 'PA_LFR_S2_CWF_F2_C_BLK_NR'
        START = 'PA_LFR_COMPUTED_CRC'
        NBLOCK = 'PA_LFR_CWF_BLK_NR'
        NC_DATA_START = 'PA_LFR_SC_V_F2'

    SBM2CWFF2('TM_LFR_SCIENCE_SBM2_CWF_F2_C')


# connect to the signal of the PacketParser to generate handlers of compressed packets
PacketParser.reseted.connect(create_packet)
