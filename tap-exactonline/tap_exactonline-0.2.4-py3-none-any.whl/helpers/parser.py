import re
from datetime import datetime
import time
import logging


class ODataParser:
    @staticmethod
    def parse_date(value):
        if type(value) == str:
            result = re.search("\/Date\((\d+)\)\/", value)
            if result and result.group(1):
                return datetime.fromtimestamp(round(int(result.group(1))/1000))
        return value

    @staticmethod
    def parse(value):
        return ODataParser.parse_date(value)

    @staticmethod
    def encode_date(value):
        return "/Date(%s)/" % round(time.mktime(datetime.fromisoformat(value).timetuple()))
