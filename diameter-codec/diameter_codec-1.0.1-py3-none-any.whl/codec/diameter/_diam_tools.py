import re
import copy
from ipaddress import IPv4Address, IPv6Address
from typing import Iterator, Union


class AvpHeaderIterator:
    """ AvpHeaderIterator """

    def __init__(self, avp_headers: bytes):
        """
        Iterator.
        :param avp_headers: avp headers
        """
        if avp_headers is None:
            raise ValueError("avp_headers is None.")

        if len(avp_headers) == 0:
            raise ValueError("avp_headers is empty.")

        self.avp_headers = copy.deepcopy(avp_headers)
        self.next_pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.avp_headers) < 8:
            raise StopIteration

        length: int = int.from_bytes(self.avp_headers[5:8], "big")
        padding: int = length % 4
        if padding > 0:
            padding = 4 - padding
        self.next_pos = length + padding
        if self.next_pos <= len(self.avp_headers):  # prevent infinite loop !
            avp_header_this: bytes = self.avp_headers[:self.next_pos]
            self.avp_headers = self.avp_headers[self.next_pos:]  # for __next__ iteration (remember this step)
            return avp_header_this

        raise StopIteration


class _DiamTools:

    @staticmethod
    def avp_headers_iterator(buffer: bytes) -> Iterator[bytes]:
        """
        Avp bytes iterator.
        :rtype: Iterator
        :param buffer: avp headers
        :return: avp bytes iterator
        """
        clazz = AvpHeaderIterator(buffer)
        return iter(clazz)

    @staticmethod
    def modify_flags_bit(source: bytes, position: int, flag: bool) -> bytes:
        """
        https://www.geeksforgeeks.org/modify-bit-given-position/amp/
        :param source: bytes to process
        :param position: index position (0 - 7)
        :param flag: True | False
        :return: shifted bytes
        """
        mask: int = 1 << position
        int_flags: int = int.from_bytes(source, "big")
        int_shifted: int = (int_flags & ~mask) | ((int(flag) << position) & mask)

        return int_shifted.to_bytes(1, "big")

    @staticmethod
    def is_flag_set(source: any, position: int) -> bool:
        """
        Check request flag.
        :param position: flag position (0 - 7)
        :param source: bytes(1 byte) or int
        :return: True|False
        """
        if position < 0 or position > 7:
            raise ValueError("position value must be in range 0 - 7")

        if isinstance(source, bytes):
            return int.from_bytes(source, "big") & position + 1 != 0

        if isinstance(source, int):
            return source & position + 1 != 0

        return False

    @staticmethod
    def is_ip_v4_address(address: Union[IPv4Address, str, int, bytes]) -> bool:
        """
        IPv4 regex pattern took from https://uibakery.io/regex-library/ip-address-regex-python
        :param address: IPv4 address
        :return: True|False
        """
        if address is None:
            return False

        if isinstance(address, IPv4Address):
            return True

        if isinstance(address, str) and address:
            ipv4_pattern = "^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(" \
                           "?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

            return re.match(ipv4_pattern, address) is not None

        try:
            return IPv4Address(address).exploded is not None
        except ValueError:
            return False

    @staticmethod
    def is_ip_v6_address(address: Union[IPv6Address, str, int, bytes]) -> bool:
        """
        IPv6 regex pattern took from https://uibakery.io/regex-library/ip-address-regex-python
        :param address: IPv6 address
        :return: True|False
        """
        if address is None:
            return False

        if isinstance(address, IPv6Address):
            return True

        if isinstance(address, str) and address:
            ipv6_pattern = "^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1," \
                           "4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{" \
                           "1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1," \
                           "4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1," \
                           "4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1," \
                           "}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3," \
                           "3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{" \
                           "0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$"

            return re.match(ipv6_pattern, address) is not None

        try:
            return IPv6Address(address).exploded is not None
        except ValueError:
            return False
