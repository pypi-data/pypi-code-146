"""
Main diameter class for simple encoding and decoding.
"""
import logging
import random
from typing import Tuple, NamedTuple, Iterator

from codec.diameter._avp_decoder import _AvpDecoder
from codec.diameter._avp_encoder import _AvpEncoder
from codec.diameter._diam_tools import _DiamTools
from codec.diameter.dictionary import DictionaryLayout


class Avp(NamedTuple):
    """Generic Avp data holder."""
    name: str
    data: any


class DiameterHeader(NamedTuple):
    """Generic DiameterHeader data holder."""
    application_id: int
    command_code: int
    avp_set: Tuple[Avp] = ()
    hop_by_hop_identifier: int = random.getrandbits(32)
    end_to_end_identifier: int = random.getrandbits(32)
    command_flag_req: bool = False
    command_flag_proxy: bool = False
    command_flag_err: bool = False
    command_flag_ret: bool = False
    version: int = 1
    length: int = 0


class Diameter:
    """ Diameter class """
    def __init__(self, dictionary_layout: DictionaryLayout):
        """
        Constructor
        :param dictionary_layout: diameter dictionary layout.
        """
        self.avp_encoder = _AvpEncoder(dictionary_layout)
        self.avp_decoder = _AvpDecoder(dictionary_layout)

    def encode(self, header: DiameterHeader) -> bytes:
        """
        Encodes header and avp data for diameter server.
        :param header: diameter header
        :return: encoded header with avp data for diameter server.
        """
        logging.info(header)

        if header is None:
            raise ValueError("DiameterHeader is None.")

        if header.application_id < 0:
            raise ValueError(f'DiameterHeader.application_id={header.application_id} not greater than 0')

        if header.version != 1:
            raise ValueError(f'DiameterHeader.version={header.version} not equals 1')

        if header.command_code < 0:
            raise ValueError(f'DiameterHeader.command_code={header.command_code} not greater than 0')

        if header.end_to_end_identifier <= 0:
            raise ValueError(f'DiameterHeader.end_to_end_identifier={header.end_to_end_identifier} not greater or '
                             f'equal than 0')

        if header.hop_by_hop_identifier <= 0:
            raise ValueError(f'DiameterHeader.hop_by_hop_identifier={header.hop_by_hop_identifier} not greater or '
                             f'equal than 0')

        if not header.avp_set:
            raise ValueError('DiameterHeader.avp_set is None or empty.')

        bytes_4_application_id: bytes = header.application_id.to_bytes(4, "big")
        bytes_1_version: bytes = header.version.to_bytes(1, "big")
        bytes_3_command: bytes = header.command_code.to_bytes(3, "big")
        bytes_4_hop_by_hop_id: bytes = header.hop_by_hop_identifier.to_bytes(4, "big")
        bytes_4_end_to_end_id: bytes = header.end_to_end_identifier.to_bytes(4, "big")

        bytes_1_flags: bytes = _DiamTools.modify_flags_bit(bytes([0]), 7, header.command_flag_req)
        bytes_1_flags = _DiamTools.modify_flags_bit(bytes_1_flags, 6, header.command_flag_proxy)
        bytes_1_flags = _DiamTools.modify_flags_bit(bytes_1_flags, 5, header.command_flag_err)
        bytes_1_flags = _DiamTools.modify_flags_bit(bytes_1_flags, 4, header.command_flag_ret)

        avp_buffer_tp: tuple = tuple()
        for avp in header.avp_set:
            avp_buffer: bytes = self.avp_encoder.encode_avp(header.application_id, avp)
            if avp_buffer:
                avp_buffer_tp += (avp_buffer,)

        bytes_3_length: bytes = (20 + len(b''.join(avp_buffer_tp))).to_bytes(3, "big")
        buffer: bytes = \
            bytes_1_version \
            + bytes_3_length \
            + bytes_1_flags \
            + bytes_3_command \
            + bytes_4_application_id \
            + bytes_4_hop_by_hop_id \
            + bytes_4_end_to_end_id \
            + b''.join(avp_buffer_tp)

        return buffer

    def decode(self, buffer: bytes) -> DiameterHeader:
        """
        Decodes bytes from server to DiameterHeader instance.
        :return: DiameterHeader
        :rtype: DiameterHeader
        :param buffer: bytes from server
        """
        if buffer is None:
            raise ValueError("buffer is set to None.")

        if len(buffer) < 20:
            raise ValueError(f"diameter header size is {len(buffer)}, should be at least 20 bytes.")

        version: int = int.from_bytes(buffer[:1], "big")
        length: int = int.from_bytes(buffer[1:4], "big")
        command_flags: int = int.from_bytes(buffer[4:5], "big")
        command_code: int = int.from_bytes(buffer[5:8], "big")
        application_id: int = int.from_bytes(buffer[8:12], "big")
        hop_by_hop_identifier: int = int.from_bytes(buffer[12:16], "big")
        end_to_end_identifier: int = int.from_bytes(buffer[16:20], "big")
        avp_headers: bytes = buffer[20:]

        command_flag_req: bool = _DiamTools.is_flag_set(command_flags, 0)
        command_flag_proxy: bool = _DiamTools.is_flag_set(command_flags, 1)
        command_flag_err: bool = _DiamTools.is_flag_set(command_flags, 2)
        command_flag_ret: bool = _DiamTools.is_flag_set(command_flags, 3)

        avp_header_iter: Iterator[bytes] = _DiamTools.avp_headers_iterator(avp_headers)
        avp_set: Tuple[Avp] = tuple()

        #  avp_header - single avp or grouped avp !
        for avp_header in avp_header_iter:
            avp: Avp = self.avp_decoder.decode_avp(application_id, avp_header)
            avp_set += (avp,)

        header: DiameterHeader = DiameterHeader(application_id=application_id,
                                                command_code=command_code,
                                                avp_set=avp_set,
                                                hop_by_hop_identifier=hop_by_hop_identifier,
                                                end_to_end_identifier=end_to_end_identifier,
                                                command_flag_req=command_flag_req,
                                                command_flag_proxy=command_flag_proxy,
                                                command_flag_err=command_flag_err,
                                                command_flag_ret=command_flag_ret,
                                                version=version,
                                                length=length
                                                )

        logging.debug(f"decoded header={header}")

        return header
