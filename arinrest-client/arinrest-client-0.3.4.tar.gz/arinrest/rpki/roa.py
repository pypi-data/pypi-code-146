from arinrest.common import exceptions
from datetime import datetime
import time
import ipaddress
from typing import Union
from base64 import b64encode


resource_classes = ["AR", "AP", "RN", "LN", "AF"]


class ROA(object):
    def __init__(
        self,
        name: str,
        origin_as: int,
        start_date: str,
        end_date: str,
        prefix: str,
        max_length: Union[int, str] = "",
    ):

        self.name = name
        self.timestamp = int(time.time())
        self.as_number = origin_as
        self.start_date = start_date
        self.end_date = end_date
        self.prefix = prefix
        self.resource_class = "AR"
        self.max_length = max_length

    @property
    def resource_class(self):
        return self.__resource_class

    @resource_class.setter
    def resource_class(self, resource_class: str):
        if resource_class not in resource_classes:
            raise exceptions.BadResourceClass(resource_class)
        self.__resource_class = resource_class

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date: str):
        try:
            self.__start_date = datetime.strptime(start_date, "%m-%d-%Y")
        except ValueError as e:
            raise e

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, end_date: str):
        try:
            self.__end_date = datetime.strptime(end_date, "%m-%d-%Y")
        except ValueError as e:
            raise e

    @property
    def prefix(self):
        return self.__prefix

    @prefix.setter
    def prefix(self, prefix: str):
        try:
            self.__prefix = ipaddress.ip_network(prefix)
        except ValueError as e:
            # reraise the exception
            raise e

    @property
    def max_length(self):
        """return max length allowed"""
        return self.__max_length

    @max_length.setter
    def max_length(self, max_length: int):
        # these values are dictated by internet norms and MANRS.
        if max_length == "":
            self.__max_length = max_length
            return

        if self.prefix.version == 4:
            max = 24
            min = 8
        elif self.prefix.version == 6:
            max = 48
            min = 16

        if min <= max_length <= max:
            self.__max_length = max_length
        else:
            raise ValueError(f"{max_length} needs to be between {min} and {max}")
            exit(1)

    @property
    def signature(self):
        return self.__signature

    @signature.setter
    def signature(self, signature):
        self.__signature = signature

    def to_xml(self):
        xml = f'<roa xmlns="http://www.arin.net/regrws/rpki/v1">\n\t<signature>{self.signature}</signature>\n\t<roaData>{str(self)}</roaData>\n</roa>'
        return xml

    def __str__(self):
        return f"1|{self.timestamp}|{self.name}|{self.as_number}|{self.start_date.strftime('%m-%d-%Y')}|{self.end_date.strftime('%m-%d-%Y')}|{str(self.prefix.network_address)}|{self.prefix.prefixlen}|{self.max_length}|"
