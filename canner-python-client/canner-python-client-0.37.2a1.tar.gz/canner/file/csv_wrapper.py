import csv
import pandas
from io import BytesIO

__all__ = ["CsvWrapper"]

class CsvWrapper(object):
    def __init__(
        self,
        content,
        encoding='utf-8'
    ):
        self.content = content
        self.encoding = encoding
    def to_list(self, delimiter=','):
        self.content_text = self.content.decode(self.encoding)
        cr = csv.reader(self.content_text.splitlines(), delimiter=delimiter)
        return list(cr)

    def to_pandas(self, *args, **kwargs):
        return pandas.read_csv(
            filepath_or_buffer=BytesIO(self.content),
            encoding=self.encoding,
            engine='python',
            *args,
            **kwargs
        )