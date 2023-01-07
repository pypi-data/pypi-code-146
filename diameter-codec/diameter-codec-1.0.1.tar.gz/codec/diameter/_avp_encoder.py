import binascii
import logging
import struct
from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Tuple, NamedTuple, Union
from urllib.parse import ParseResult, urlparse

from codec.diameter._diam_tools import _DiamTools
from codec.diameter.dictionary import DictionaryLayout, AvpDict


class Avp(NamedTuple):
    """Generic Avp data holder."""
    name: str
    data: any


class _AvpEncoder:
    def __init__(self, dictionary_layout: DictionaryLayout):
        """
        Constructor
        :type dictionary_layout: DictionaryLayout
        :param dictionary_layout: diameter dictionary layout
        """
        if not dictionary_layout:
            raise ValueError("dictionary_layout is None.")
        self.dictionary_layout = dictionary_layout

    def __encode_avp_grouped(self, application_id: int, avp_grouped_set: Tuple, buffer: bytes = b'') -> bytes:
        """
        Internal function for 'grouped' encoding
        :param application_id: application id
        :param avp_grouped_set: tuple of Avp
        :param buffer: accumulator used in recursion loop
        :return: grouped encoded as bytes
        """
        for avp_item in avp_grouped_set:  # list of single avp and group's (mix mode)
            is_grouped: bool = avp_item.data is tuple
            if not is_grouped:
                buffer += self.encode_avp(application_id, avp_item)
            else:
                return self.__encode_avp_grouped(application_id, avp_item, buffer)

        return buffer

    def __encode_octet_string_avp(self, avp_dict: AvpDict, data: Union[IPv4Address, IPv6Address, str, bytes]) -> bytes:
        """
        Encode to utf-8 octet string
        :param data: Union[IPv4Address, IPv6Address, str, bytes]
        :return: octet string encoded as bytes
        @rtype: bytes
        """
        encoded_data: bytes = b''

        if isinstance(data, (IPv4Address, IPv6Address)):
            encoded_data = data.packed
        elif isinstance(data, (str, bytes)) and _DiamTools.is_ip_v4_address(data):
            encoded_data = IPv4Address(data).packed
        elif isinstance(data, (str, bytes)) and _DiamTools.is_ip_v6_address(data):
            encoded_data = IPv6Address(data).packed
        elif avp_dict.content_type.lower() == "binary" and isinstance(data, str):   # hex-string expected
            encoded_data = bytes.fromhex(data.replace("0x", "", 1))
        elif isinstance(data, str):
            struct_format = f"!{len(data)}s"
            encoded_data = struct.pack(struct_format, data.encode("utf-8"))
        elif isinstance(data, int):
            encoded_data = bytes.fromhex(hex(data).replace("0x", "", 1))
        elif isinstance(data, bytes):
            encoded_data = data
        else:
            logging.warning(f"data={data}, type={type(data)} does not support encoding to octet string.")

        return encoded_data

    def __encode_ip_address_avp(self, data: Union[IPv4Address, IPv6Address, str, bytes]) -> bytes:
        """
        Encode IPv4 or IPv6 address
        sample AVPs:
        https://references.mobileum.com/DiaDict/Dictionary/MIP-Home-Agent-Address.html
        https://references.mobileum.com/DiaDict/Dictionary/Host-IP-Address.html
        :param data: data
        :return:
            IPv4 AVP = (2 bytes for Address Family Numbers [IANAADFAM] + 4 bytes for IPv4 address) = 6 bytes
            IPv6 AVP = (2 bytes for Address Family Numbers [IANAADFAM] + 16 bytes for IPv6 address) = 18 bytes
            @rtype: bytes
        """
        encoded_data: bytes = b''

        if isinstance(data, IPv4Address):
            encoded_data = b'\x00\x01' + data.packed
        elif isinstance(data, IPv6Address):
            encoded_data = b'\x00\x02' + data.packed
        elif _DiamTools.is_ip_v4_address(data):
            encoded_data = b'\x00\x01' + IPv4Address(data).packed
        elif _DiamTools.is_ip_v6_address(data):
            encoded_data = b'\x00\x02' + IPv6Address(data).packed
        else:
            logging.warning(f"data={data} is not proper IPv4/IPv6 address.")

        return encoded_data

    def encode_avp(self, application_id: int, avp: Avp) -> Optional[bytes]:
        """
        Converts Avp to bytes before sending to diameter server
        :param application_id: application id
        :param avp: avp (single or grouped)
        :return: bytes for diameter server
        """
        logging.debug(f"application_id={application_id}, avp={avp}")

        if application_id < 0:
            raise ValueError("application_id must be greater or equal to 0.")

        if not avp:
            raise ValueError("avp object is set to None.")

        if not avp.name:
            raise ValueError("avp.name is empty or None.")

        avp_dict: AvpDict = self.dictionary_layout.find_avp_by_name(application_id, avp.name.strip())
        if avp_dict is None:
            logging.warning(f"ENCODER: application_id={application_id}, avp name={avp.name} in diameter dictionary "
                            f"not found. It will be omitted!")
            return None

        bytes_4_code: bytes = avp_dict.code.to_bytes(4, "big")
        bytes_1_flags: bytes
        bytes_4_vendor_id: bytes
        bytes_3_length: bytes
        bytes_data: bytes = b''
        avp_buffer: bytes = b''
        avp_length: int

        if avp_dict.type.lower() == "unsigned32" and isinstance(avp.data, int):
            bytes_data = struct.pack(">I", int(avp.data))
        elif avp_dict.type.lower() == "unsigned64" and isinstance(avp.data, int):
            bytes_data = struct.pack(">Q", avp.data)
        elif avp_dict.type.lower() == "integer32" and isinstance(avp.data, int):
            bytes_data = struct.pack(">i", avp.data)
        elif avp_dict.type.lower() == "integer64" and isinstance(avp.data, int):
            bytes_data = struct.pack(">q", avp.data)
        elif avp_dict.type.lower() == "float32" and isinstance(avp.data, float):
            bytes_data = struct.pack(">f", avp.data)
        elif avp_dict.type.lower() == "float64" and isinstance(avp.data, float):
            bytes_data = struct.pack(">d", avp.data)
        elif avp_dict.type.lower() == "utf8string" and isinstance(avp.data, str):
            bytes_data = str(avp.data).encode("utf-8")
        elif avp_dict.type.lower() == "octetstring":
            bytes_data = self.__encode_octet_string_avp(avp_dict, avp.data)
        elif avp_dict.type.lower() == "diameteridentity" and isinstance(avp.data, str):
            bytes_data = str(avp.data).encode("utf-8")
        elif avp_dict.type.lower() == "grouped" and isinstance(avp.data, tuple):
            bytes_data = self.__encode_avp_grouped(application_id, avp.data)
        elif avp_dict.type.lower() == "address":
            bytes_data = self.__encode_ip_address_avp(avp.data)
        elif avp_dict.type.lower() == "time" and isinstance(avp.data, int):
            secs_between_1900_and_1970: int = (70 * 365 + 17) * 86400
            timestamp: int = int(avp.data) + secs_between_1900_and_1970
            bytes_data = struct.pack(">I", timestamp)
        elif avp_dict.type.lower() == "diameteruri" and isinstance(avp.data, ParseResult):
            bytes_data = avp.data.geturl().encode("utf-8")
        elif avp_dict.type.lower() == "diameteruri" and isinstance(avp.data, str):
            bytes_data = urlparse(str(avp.data)).geturl().encode("utf-8")
        elif avp_dict.type.lower() == "ipfilterrule" and isinstance(avp.data, str):
            bytes_data = str(avp.data).encode("utf-8")
        elif avp_dict.type.lower() == "enumerated" and isinstance(avp.data, str):
            for enum_value, enum_text in avp_dict.enums.items():
                if enum_text.strip() == avp.data.strip():
                    bytes_data = struct.pack(">i", enum_value)
                    break

            if not bytes_data:
                logging.warning(f"ENCODER: application_id={application_id}, {avp_dict.name}(code={avp_dict.code}) has "
                                f"unknown enumerated text={avp.data}")

        elif avp.data:  # unknown type, do best effort to encode
            logging.warning(f"ENCODER: application_id={application_id}, {avp_dict.name}(code={avp_dict.code}) has "
                            f"unknown data type={avp_dict.type}")

            bytes_data = str(avp.data).encode("utf-8")
        else:
            logging.warning(f"ENCODER: application_id={application_id}, {avp_dict.name}(code={avp_dict.code}) has no "
                            f"data!")

        has_vendor_id: bool = avp_dict.vendor_id > 0
        bytes_1_flags = _DiamTools.modify_flags_bit(bytes([0]), 7, has_vendor_id)
        bytes_1_flags = _DiamTools.modify_flags_bit(bytes_1_flags, 6, avp_dict.mandatory_flag)

        if has_vendor_id > 0:
            bytes_4_vendor_id = avp_dict.vendor_id.to_bytes(4, "big")
            avp_length = 12 + len(bytes_data)
            bytes_3_length = avp_length.to_bytes(3, "big")
            avp_buffer += bytes_4_code + bytes_1_flags + bytes_3_length + bytes_4_vendor_id + bytes_data
        else:
            avp_length = 8 + len(bytes_data)
            bytes_3_length = avp_length.to_bytes(3, "big")
            avp_buffer += bytes_4_code + bytes_1_flags + bytes_3_length + bytes_data

        padding: int = avp_length % 4
        if padding > 0:
            padding = 4 - padding
            avp_buffer += bytes(padding)

        logging.debug(f"ENCODER: application_id={application_id}, avp_dict={avp_dict}, avp_length={avp_length}, "
                      f"padding={padding}, avp_buffer={binascii.hexlify(avp_buffer)}")

        return avp_buffer
