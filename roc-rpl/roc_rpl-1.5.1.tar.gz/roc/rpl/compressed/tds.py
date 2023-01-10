#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct

from roc.rpl.exceptions import RPLError
from roc.rpl.packet_parser.packet_parser import PacketParser
from .utils import find_index
from .utils import get_base_packet
from roc.rpl.packet_structure.data import Data

__all__ = []


def get_base_tds(Packet):
    """
    Generate the base class to use for compressed packets in the case of TDS.
    """
    # base class for compressed packet
    Base = get_base_packet(Packet)

    # base class for the compressed packets of LFR
    class TDS(Base):
        """
        Base class for the compressed packets of LFR. Define the special
        behaviour of the treatment for those packets, that should mimic the non
        compressed (NC) ones.
        """
        def __init__(self, name):
            # init the packet as the other
            super(TDS, self).__init__(name)

            # the index of the parameter with the number of blocks
            self.idx_nchannels, self.nchannels = find_index(
                self.parameters,
                self.NCHANNEL,
            )

        def data_substitution(self, data, uncompressed):
            """
            Create a new data bytes array in order to simulate an non
            compressed packet with the data from an uncompressed packet,
            allowing to decommute and store a compressed packet as an
            uncompressed one. Different from the base one since we need to add
            the parameter indicating the number of blocks used in the packet,
            not present in the compressed packet.
            """
            new_bytes = data.to_bytes()[:self.start.byte + self.header_offset]
            new_bytes += struct.pack(
                ">H",
                len(uncompressed) // self.block_size,
            )
            new_bytes += uncompressed
            new_data = Data(new_bytes, len(new_bytes))
            return new_data

        def uncompressed_byte_size(self, data, values):
            # check number of samples
            if values[self.idx_nblocks] > self.nblocks.maximum:
                raise RPLError(
                    "The number of samples is superior to authorized values" +
                    " for packet {0}: {1} with maximum {2}".format(
                        self.name,
                        values[self.idx_nblocks],
                        self.nblocks.maximum,
                    )
                )

            # check number of channels
            if values[self.idx_nchannels] > self.nchannels.maximum:
                raise RPLError(
                    "The number of samples is superior to authorized values" +
                    " for packet {0}: {1} with maximum {2}".format(
                        self.name,
                        values[self.idx_nchannels],
                        self.nchannels.maximum,
                    )
                )
            return (
                values[self.idx_nblocks] * values[self.idx_nchannels] *
                self.block_size
            )

    return TDS


def create_packet(Packet):
    """
    Given the base class of the packets to use, add special methods into the
    new class to be able to treat the compressed packet as an existing one.
    """
    # get the base class for TDS packets
    TDS = get_base_tds(Packet)

    # TM_TDS_SCIENCE_NORMAL_RSWF
    class NormalRSWF(TDS):
        DATA_START = "PA_TDS_COMP_DATA_BLK"
        DATA_COUNT = "PA_TDS_N_RSWF_C_BLK_NR"
        START = "PA_TDS_COMPUTED_CRC"
        NBLOCK = "PA_TDS_SAMPS_PER_CH"
        NCHANNEL = "PA_TDS_NUM_CHANNELS"
        NC_DATA_START = "PA_TDS_RSWF_DATA_BLK"

    NormalRSWF("TM_TDS_SCIENCE_NORMAL_RSWF_C")

    # TM_TDS_SCIENCE_SBM1_RSWF
    class SBM1RSWF(NormalRSWF):
        DATA_COUNT = "PA_TDS_S1_RSWF_C_BLK_NR"

    SBM1RSWF("TM_TDS_SCIENCE_SBM1_RSWF_C")

    # TM_TDS_SCIENCE_NORMAL_TSWF
    class NormalTSWF(TDS):
        DATA_START = "PA_TDS_COMP_DATA_BLK"
        DATA_COUNT = "PA_TDS_N_TSWF_C_BLK_NR"
        START = "PA_TDS_COMPUTED_CRC"
        NBLOCK = "PA_TDS_SAMPS_PER_CH"
        NCHANNEL = "PA_TDS_NUM_CHANNELS"
        NC_DATA_START = "PA_TDS_TSWF_DATA_BLK"

    NormalTSWF("TM_TDS_SCIENCE_NORMAL_TSWF_C")

    # TM_TDS_SCIENCE_SBM2_TSWF
    class SBM2TSWF(NormalTSWF):
        DATA_COUNT = "PA_TDS_S2_TSWF_C_BLK_NR"

    SBM2TSWF("TM_TDS_SCIENCE_SBM2_TSWF_C")

    # TM_TDS_SCIENCE_NORMAL_MAMP
    class NormalMAMP(TDS):
        DATA_START = "PA_TDS_COMP_DATA_BLK"
        DATA_COUNT = "PA_TDS_MAMP_C_DATA_BLK_NR"
        START = "PA_TDS_COMPUTED_CRC"
        NBLOCK = "PA_TDS_MAMP_SAMP_PER_CH"
        NCHANNEL = "PA_TDS_MAMP_NUM_CH"
        NC_DATA_START = "PA_TDS_MAMP_DATA_BLK"

    NormalMAMP("TM_TDS_SCIENCE_NORMAL_MAMP_C")

    # TM_TDS_SCIENCE_LFM_CWF
    class LFMCWF(TDS):
        DATA_START = "PA_TDS_COMP_DATA_BLK"
        DATA_COUNT = "PA_TDS_LFM_CWF_C_BLK_NR"
        START = "PA_TDS_COMPUTED_CRC"
        NBLOCK = "PA_TDS_LFR_CWF_SAMPS_PER_CH"
        NCHANNEL = "PA_TDS_LFM_CWF_CH_NR"
        NC_DATA_START = "PA_TDS_LFM_CWF_DATA_BLK"

    LFMCWF("TM_TDS_SCIENCE_LFM_CWF_C")

    # TM_TDS_SCIENCE_LFM_RSWF
    class LFMRSWF(TDS):
        DATA_START = "PA_TDS_COMP_DATA_BLK"
        DATA_COUNT = "PA_TDS_LFM_RSWF_C_BLK_NR"
        START = "PA_TDS_COMPUTED_CRC"
        NBLOCK = "PA_TDS_LFR_SAMPS_PER_CH"
        NCHANNEL = "PA_TDS_LFM_RSWF_CH_NR"
        NC_DATA_START = "PA_TDS_LFM_RSWF_DATA_BLK"

    LFMRSWF("TM_TDS_SCIENCE_LFM_RSWF_C")


# connect to the signal of the PacketParser to generate handlers of compressed packets
PacketParser.reseted.connect(create_packet)
