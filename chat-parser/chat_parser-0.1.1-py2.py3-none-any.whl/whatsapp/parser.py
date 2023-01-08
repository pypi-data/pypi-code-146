import re
from datetime import datetime


class WParser:

    _avail_format = ["txt"]
    _name = "whatsapp parser"

    def __init__(self, file_path):
        self.is_file_supported(file_path)
        self.filepath = file_path
        self.fs = open(file_path, "r")
        self.regex_pattern = r'^\d{1,2}/\d{1,2}/\d{2}[ ,]+\d{1,2}[.:]\d{1,2}[ APM]* -'

    def __del__(self):
        try:
            self.fs.close()
        except AttributeError:
            pass

    def __is_head(self, line):
        return re.match(self.regex_pattern, line)

    def read_line(self):
        chunk_list = []
        line = self.fs.readline()
        counter = 0
        while line:
            if self.__is_head(line):
                counter += 1
                if counter == 2: #cursor is on end of message
                    self.fs.seek(pos) #undo position
                    break
                chunk_list.append(line)
            else:
                chunk_list.append(chunk_list.pop() + "\n" + line)
            pos = self.fs.tell()
            line = self.fs.readline()
        return ''.join(chunk_list)


    def extract_line(self, line):
        created_at = re.findall(r'(^\d{1,2}/\d{1,2}/\d{2}[ ,]+\d{1,2}[.:]\d{1,2}[ APM]*) -', line)[0]
        try:
            owner = re.findall(r'^\d{1,2}/\d{1,2}/\d{2}[ ,]+\d{1,2}[.:]\d{1,2}[ APM]* - ([^:]*):', line)[0]
        except IndexError: #unusual format (maybe an info)
            return None
        text = re.findall(r'^\d{1,2}/\d{1,2}/\d{2}[ ,]+\d{1,2}[.:]\d{1,2}[ APM]* - [^:]*: ([\w\W]*)', line)[0]
        return self.extract_datetime(created_at), owner, text.rstrip("\n")

    def extract_all_lines(self):
        self.fs.seek(0)
        line = self.read_line()
        while line:
            extracted = self.extract_line(line)
            line = self.read_line()
            if extracted:
                yield extracted
            else:
                continue

    def is_file_supported(self, path):
        file_ext = path.split(".")[-1]
        if file_ext not in self._avail_format:
            raise WhatsappParserError(f"{file_ext} format is not supported by {self._name}")

    @classmethod
    def extract_datetime(self, datestr):
        number = re.findall(r"\d+", datestr)
        m,d,y,H,M = map(int, number)
        if "." in datestr: #if d/m/y format
            t = d
            d = m
            m = t
        if "PM" in datestr:
                H += 12
        return datetime(year=y+2000, month=m, day=d, hour=H, minute=M)
    
class WhatsappParserError(Exception):
    pass