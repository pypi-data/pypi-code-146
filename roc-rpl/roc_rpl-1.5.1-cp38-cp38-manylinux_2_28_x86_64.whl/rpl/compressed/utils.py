#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from roc.rpl.constants import INVALID_PACKET_CDATA
from roc.rpl.exceptions import RPLError
from roc.rpl.rice.rice import Compressor
from roc.rpl.packet_structure.data import header_foot_offset
from roc.rpl.packet_structure.data import Data

__all__ = ['find', 'find_index', 'get_base_packet']


def get_base_packet(Packet):
    """
    Generate the base class to use for compressed packets in the case of TDS.
    """
    # check if the class is already defined
    # base class for the compressed packets of LFR
    class BaseCompressed(Packet):
        """
        Base class for the compressed packets of LFR. Define the special
        behaviour of the treatment for those packets, that should mimic the non
        compressed (NC) ones.
        """
        # create an object allowing to do decompression of data
        compressor = Compressor()

        def __init__(self, name):
            # init the packet as the other
            super(BaseCompressed, self).__init__(name)

            # store the name of the non compressed packet
            if self.name.endswith('_C'):
                self.nc_name = self.name[:-2]
            else:
                # raise exception because the packet is not handled correctly
                raise RPLError(
                    (
                        'Trying to register {0} as compressed packet while ' +
                        'not following the name pattern'
                    ).format(self.name)
                )

            # get the associated NC packet
            self.nc_packet = Packet(self.nc_name)

            # and parameter marking start of the data block for the packet
            self.idx_data_start, self.data_start = find_index(
                self.parameters,
                self.DATA_START,
            )

            # same for the packet indicating the number of compressed packet
            self.idx_data_count, self.data_count = find_index(
                self.parameters,
                self.DATA_COUNT,
            )

            # same for the divergence with the NC packet
            self.idx_start, self.start = find_index(
                self.parameters,
                self.START,
            )

            # same for the NC packet
            self.nc_start = find(self.nc_packet.parameters, self.NC_DATA_START)

            # the index of the parameter with the number of blocks
            self.idx_nblocks, self.nblocks = find_index(
                self.parameters,
                self.NBLOCK,
            )

            # get the block size in byte to be able to know the size of the
            # data to decompress
            self.block_size = self.nc_start.block_size

            # compute the header offset (with know that it is TM packet)
            self.category = 0
            self.header_offset, _ = header_foot_offset(self.category)

            # the starting position for the compressed data
            self.start_position = self.data_start.byte + self.header_offset

            # no data reorganization by default
            self.is_compressed = True

            # valid packet flag
            self.is_valid = True


        def add(self):
            """
            Increment the number of packets of the NC packet because data will
            be added inside it.
            """
            self.nc_packet.add()

        def extract_data(self, data,
                         packet_length=None,
                         packet_data=None):
            """
            Extract the data as it was the NC packet. The hack is to modify the
            data buffer to reflect the structure of the NC packet.
            """
            try:
                # start by extracting the parameters until the divergence
                # between compressed and non compressed packets
                values, _ = data.extract_parameters(
                    self.header_offset,
                    self.parameters[:self.idx_data_start],
                )

                # get the compressed data part of the packet
                compressed_data = self.compressed_data(data, values)

                # get the number of bytes to uncompress
                size = self.uncompressed_byte_size(data, values)

                # get the uncompressed data by the method specified for each
                # instrument
                self.uncompressed = self.uncompressed_data(
                    compressed_data,
                    values,
                    size,
                )

                # check that the expected size for uncompressed data and the
                # extracted one from the compressed packet are the same
                if size != len(self.uncompressed):
                    raise RPLError(
                        (
                            "The uncompressed data for packet {0} doesn't" +
                            'have the same size as the expected one.\n' +
                            'Expected: {1} bytes\t Extracted: {2} bytes'
                        ).format(
                            self.name,
                            size,
                            len(self.uncompressed),
                        )
                    )

                # create the new data from the information
                new_data = self.data_substitution(data, self.uncompressed)

                # Set compressed status to 1
                packet_data['compressed'] = 1

                # extract the data as it is the NC packet
                self.nc_packet.extract_data(
                    new_data,
                    packet_length=new_data.data_size - 7,
                    packet_data=packet_data,
                )
            # If an exception is raised, set packet status to INVALID_PACKET_CDATA
            # and save error message
            except Exception as e:
                self.is_valid = False
                packet_data['status'] = INVALID_PACKET_CDATA
                packet_data['comment'] = e.message
            # gives the possibility to see a hole in data if something went
            # wrong
            finally:
                self.counter += 1

        def compressed_data(self, data, values):
            """
            Return the compressed data part of a compressed packet.
            """
            # get the size of compressed data and compare to the size
            # obtained from the position
            compressed_size = self.compressed_byte_size(values)

            # get the compressed data
            buf = data.to_bytes()[self.start_position:]

            # check the size of the data to what is expected from the
            # decommuted values of the compressed packet
            if compressed_size != len(buf):
                raise RPLError(
                    (
                        'The compressed data size is not coherent in the' +
                        ' packet parameters and from the bytes ' +
                        'themselves.\nFrom packet parameters: {0} bytes' +
                        '\nFrom data size: {1}'
                    ).format(
                        compressed_size,
                        len(buf),
                    )
                )

            # return the compressed data
            return Data(buf, len(buf))

        def uncompressed_data(self, compressed_data, values, size):
            """
            Return the uncompressed data from the data of the packet and the
            decommuted values of the compressed packet. Packets for LFR are
            special, because compressed data is organized by blocks of values.
            So we need to decompressed each block, then reorganize data
            according to the good structure as for the non compressed packet.
            """
            # initialize the offset when going though the compressed packet
            offset = 0

            # initialize the data buffer that will need to be transposed at the
            # end
            data = bytes()

            # compute the size in bytes of the uncompressed block
            uncompressed_block_size = size // self.nc_start.group

            # loop over the number of blocks of compressed data. This number is
            # directly the number of parameters inside a block of data for the
            # non compressed packet.
            for block in range(self.nc_start.group):
                # read the size of the block (16 bits)
                block_size = compressed_data.u16p(offset, 0, 16)

                # increment offset
                offset += 2

                # create a buffer for the compressed data with the good size
                buf = Data(
                    compressed_data.to_bytes()[offset:offset + block_size],
                    block_size,
                )

                # uncompress the data (and truncate to the size of expected
                # data because apparently the returned size can be superior to
                # the wanted size)
                data += self.compressor.uncompress(
                    buf,
                    uncompressed_block_size,
                ).to_bytes()[:uncompressed_block_size]

                # add the size of the compressed data
                offset += block_size

            # convert the concatenated byte array into a numpy array to be able
            # to transpose it and reorder correctly the data by sample
            data = np.frombuffer(data, dtype='uint8').view('uint16')
            data.shape = (
                self.nc_start.group,
                len(data) // self.nc_start.group
            )

            # transpose the data if a reorganization is needed and convert to
            # bytes
            return data.T.byteswap().tobytes()

        def data_substitution(self, data, uncompressed):
            """
            Create a new data bytes array in order to simulate an non
            compressed packet with the data from an uncompressed packet,
            allowing to decommute and store a compressed packet as an
            uncompressed one.
            """
            new_bytes = data.to_bytes()[:self.start.byte + self.header_offset]
            new_bytes += uncompressed
            new_data = Data(new_bytes, len(new_bytes))
            return new_data

        def compressed_byte_size(self, values):
            """
            Given the decommuted values of the packet before the data part,
            returns the size in bytes of the compressed data, as expected by
            the packet.
            """
            # check the maximal value of the block parameter
            if values[self.idx_data_count] > self.data_count.maximum:
                raise RPLError(
                    'The number of blocks is superior to authorized values ' +
                    'for compressed data of ' +
                    'packet {0}: {1} with maximum {2}'.format(
                        self.name,
                        values[self.idx_data_count],
                        self.data_count.maximum,
                    )
                )

            # return the value of the size of compressed data
            return values[self.idx_data_count] * self.data_start.block_size

    return BaseCompressed


def find(iterable, name):
    """
    Find the parameter with name in the list in argument.
    """
    for x in iterable:
        if x.name == name:
            return x

    raise ValueError(
        'Parameter {0} not found in list of parameters'.format(name)
    )


def find_index(iterable, name):
    """
    Find the parameter with name in the list in argument.
    """
    for index, x in enumerate(iterable):
        if x.name == name:
            return index, x

    raise ValueError(
        'Parameter {0} not found in list of parameters'.format(name)
    )
