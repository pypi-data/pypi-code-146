import json
from ..data_extractor.utils import WordTools
import re
from datetime import datetime

class TelParser:
    _avail_format  = ["json"]
    _name = "telegram parser"

    def __init__(self, path):
        self.is_file_supported(path)
        self.path = path
    
    def extract_all_lines(self):
        with open(self.path) as f:
            json_object = json.loads(f.read())
            for o in json_object["messages"]:
                if not None in o:
                    yield self.__parse_dict(o)

    def __parse_dict(self, d: dict):
        #check type if 'message'
        if d.get("type") == "message" and d.get("text"):
            date = TelParser.extract_datetime(d.get("date"))
            owner = d.get("from")
            text = str(d.get("text"))
            return date, owner, text
        return (None,None, None)

    def is_file_supported(self, path):
        file_ext = path.split(".")[-1]
        if file_ext not in self._avail_format:
            raise TelegramParserError(f"{file_ext} format is not supported by {self._name}")

    @classmethod
    def extract_datetime(cls, datestr):
        number = re.findall(r"\d+", datestr)
        y,m,d,H,M,S = map(int, number)
        return datetime(year=y, month=m, day=d, hour=H, minute=M, second=S)

class TelegramParserError(Exception):
    pass