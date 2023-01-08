from .whatsapp.parser import WParser, WhatsappParserError
from .telegram.parser import TelParser, TelegramParserError
import pandas as pd

class FileParser():
    """Parsing file into date, owner, text columns pandas dataframe"""

    _time_format = ["hour","day", "day_name", "month", "year", "iso-datetime"]
    data_columns = ["date","owner","text"]

    def __init__(self):
        pass


    def whatsapp_create_frame(self, path):
        """Parse whatsapp file chat"""
        self.parser = WParser(path)
        self.frame = pd.DataFrame([l for l in self.parser.extract_all_lines()])
        self.__config_frame()
        
    def telegram_create_frame(self, path):
        self.parser = TelParser(path)
        self.frame = pd.DataFrame([l for l in self.parser.extract_all_lines()])
        self.__config_frame()
        
    
    def generator_create_frame(self,data_gen):
        self.frame = pd.DataFrame([c for c in data_gen])
        self.__config_frame()
        self.parser = "custom parser"

    def reframe_bydate(self, date):
        sdates = date.split("/")
        if len(sdates) == 1:
            self.frame = self.frame[self.frame.year == int(sdates[0])]
        elif len(sdates) == 2:
            self.frame = self.frame[self.frame.year == int(sdates[0])][self.frame.month == sdates[1]]
        elif len(sdates) == 3:
            self.frame = self.frame[self.frame.year == int(sdates[0])][self.frame.month == sdates[1]][self.frame.day==int(sdates[2])]

    def row_dict_list(self, frame=None):
        if type(frame) == pd.DataFrame:
            date = [d.strftime("%Y-%m-%d %H:%m") for d in frame["date"]]
            owner = frame["owner"].values
            text = frame["text"].values
            data = []
            for i in range(len(date)):
                d = {
                    "date": date[i],
                    "owner": owner[i],
                    "text": text[i]
                }
                data.append(d)
            return data
        else:
            return self.row_dict_list(self.frame)

    def __config_frame(self):
        self.frame = self.frame.dropna()
        self.frame.columns = self.data_columns
        self.frame[self._time_format[0]] = [t.hour for t in self.frame["date"]]
        self.frame[self._time_format[1]] = [t.day for t in self.frame["date"]]
        self.frame[self._time_format[2]] = [t.day_name() for t in self.frame["date"]]
        self.frame[self._time_format[3]] = [t.month_name() for t in self.frame["date"]]
        self.frame[self._time_format[4]] = [t.year for t in self.frame["date"]]



