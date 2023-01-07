import ipaddress
import logging
import socket
import struct
from typing import Tuple, Iterator, NamedTuple, Optional
from urllib.parse import urlparse

from codec.diameter._diam_tools import _DiamTools
from codec.diameter.dictionary import AvpDict, DictionaryLayout


class Avp(NamedTuple):
    """Generic Avp data holder."""
    name: str
    data: any


class _AvpHeader(NamedTuple):
    code: int
    flags: int
    length: int
    padding: int
    end_pos: int
    data_bytes: bytes
    avp_dict: AvpDict


class _AvpDecoder:
    def __init__(self, dictionary_layout: DictionaryLayout):
        """
        Constructor.
        :type dictionary_layout: DictionaryLayout
        :param dictionary_layout: diameter dictionary layout
        """
        if not dictionary_layout:
            raise ValueError("dictionary_layout is None.")
        self.dictionary_layout = dictionary_layout

    def __extract_avp_header(self, application_id: int, avp_header: bytes) -> _AvpHeader:
        """
        Read and extract avp header field values
        :param application_id: application id
        :param avp_header: avp header with data
        :return: _AvpHeader
        :rtype: _AvpHeader as NamedTuple
        """
        code: int = int.from_bytes(avp_header[:4], "big")
        flags: int = int.from_bytes(avp_header[4:5], "big")
        length: int = int.from_bytes(avp_header[5:8], "big")
        padding: int = length % 4
        if padding > 0:
            padding = 4 - padding
        next_pos: int = length + padding
        data_bytes: bytes = avp_header[8: length]  # single avp or grouped avp

        if flags >= 128:
            vendor_id: int = int.from_bytes(avp_header[8:12], "big")
            if vendor_id >= 0:
                data_bytes = avp_header[12: length]  # single avp or grouped avp

        avp_dict: AvpDict = self.dictionary_layout.find_avp_by_code(application_id, code)

        return _AvpHeader(code, flags, length, padding, next_pos, data_bytes, avp_dict)

    def __decode_avp_grouped(self, application_id: int, avp_grouped: bytes) -> Tuple[Avp]:
        """
        Decodes grouped avp using recursion.
        :rtype: object
        :param application_id: application id
        :param avp_grouped: single avp or grouped avp
        :return: grouped decoded as Tuple
        """
        my_tuple: Tuple = tuple()
        avp_header_iter: Iterator[bytes] = _DiamTools.avp_headers_iterator(avp_grouped)
        for avp_header in avp_header_iter:
            avp_item: _AvpHeader = self.__extract_avp_header(application_id, avp_header)
            avp_sub_header_iter: Iterator[bytes] = _DiamTools.avp_headers_iterator(avp_item.data_bytes)
            for avp_sub_header in avp_sub_header_iter:
                avp: Avp = self.decode_avp(application_id, avp_sub_header)
                my_tuple += (avp,)

        return my_tuple

    def __decode_octet_string_avp(self, avp_dict: AvpDict, data: bytes) -> any:
        if avp_dict.content_type.lower() == "binary":
            return bytes.hex(data).replace("0x", "", 1)

        if _DiamTools.is_ip_v4_address(data) or _DiamTools.is_ip_v6_address(data):
            struct_format = f"!{len(data)}s"
            unpacked_bytes_data: bytes = struct.unpack(struct_format, data)[0]
            return ipaddress.ip_address(unpacked_bytes_data).exploded

        try:
            return data.decode('utf-8')
        except UnicodeDecodeError as err:
            logging.error(f"data={data}, type={type(data)} does not support decoding to octet string.", err)

        return bytes.hex(data).replace("0x", "", 1)

    def __decode_ip_address_avp(self, data: bytes) -> Optional[str]:
        value = None

        try:
            address_type: int = int.from_bytes(data[:2], byteorder="big")
            if address_type == 1:
                value = socket.inet_ntoa(data[2:])
            elif address_type == 2:
                value = socket.inet_ntop(socket.AF_INET6, data[2:])
            else:
                logging.warning(f"data={data} is not proper IPv4/IPv6 address.")
        except ValueError as err:
            logging.error(f"data={data} is not proper IPv4/IPv6 address.", err)

        return value

    def decode_avp(self, application_id: int, avp_header: bytes) -> Optional[Avp]:
        """
        Avp headers only !
        :param avp_header: avp header without diameter header --> buffer[20:]
        :param application_id: application id
        :return: Avp object
        """
        code: int = int.from_bytes(avp_header[:4], "big")
        flags: int = int.from_bytes(avp_header[4:5], "big")
        length: int = int.from_bytes(avp_header[5:8], "big")
        data: bytes = b''
        decode_data: any = None
        #   ----------------------------------------------------

        if flags >= 128:
            vendor_id: int = int.from_bytes(avp_header[8:12], "big")
            if vendor_id > 0:
                data = avp_header[12: length]
        else:
            data = avp_header[8: length]

        avp_dict: AvpDict = self.dictionary_layout.find_avp_by_code(application_id, code)
        if avp_dict is None:
            logging.warning(f"DECODER: application_id={application_id}, avp code={code} in diameter dictionary not "
                            f"found!")
            return None

        if len(data) == 0:
            logging.warning(f"DECODER: application_id={application_id}, {avp_dict.name}(code={code}) has no data!")
            return Avp(avp_dict.name, None)

        if avp_dict.type.lower() == "unsigned32":
            decode_data = struct.unpack(">I", data)[0]
        elif avp_dict.type.lower() == "unsigned64":
            decode_data = struct.unpack(">Q", data)[0]
        elif avp_dict.type.lower() == "integer32":
            decode_data = struct.unpack(">i", data)[0]
        elif avp_dict.type.lower() == "integer64":
            decode_data = struct.unpack(">q", data)[0]
        elif avp_dict.type.lower() == "float32":
            decode_data = struct.unpack(">f", data)[0]
        elif avp_dict.type.lower() == "float64":
            decode_data = struct.unpack(">d", data)[0]
        elif avp_dict.type.lower() == "utf8string":
            decode_data = data.decode("utf-8")
        elif avp_dict.type.lower() == "octetstring":
            decode_data = self.__decode_octet_string_avp(avp_dict, data)
        elif avp_dict.type.lower() == "diameteridentity":
            decode_data = urlparse(data.decode("utf-8")).geturl()
        elif avp_dict.type.lower() == "grouped":
            decode_data = self.__decode_avp_grouped(application_id, avp_header)
        elif avp_dict.type.lower() == "address":
            decode_data = self.__decode_ip_address_avp(data)
        elif avp_dict.type.lower() == "time":
            secs_between_1900_and_1970: int = (70 * 365 + 17) * 86400
            timestamp = struct.unpack(">I", data)[0]
            decode_data = timestamp - secs_between_1900_and_1970
        elif avp_dict.type.lower() == "diameteruri":
            decode_data = urlparse(data.decode("utf-8")).geturl()
        elif avp_dict.type.lower() == "ipfilterrule":
            decode_data = data.decode("utf-8")
        elif avp_dict.type.lower() == "enumerated":
            value = struct.unpack(">i", data)
            for enum_value, enum_text in avp_dict.enums.items():
                if int(enum_value) == int(value[0]):  # e.g value=(6, )
                    decode_data = enum_text
                    break

            if not decode_data:
                logging.warning(f"DECODER: application_id={application_id}, {avp_dict.name}(code={code}) has unknown "
                                f"enumerated value='{value}'")
        else:
            decode_data = data.decode("utf-8")

        return Avp(avp_dict.name, decode_data)
