import json
import pandas
from io import BytesIO

__all__ = ["JsonWrapper"]


class JsonWrapper(object):
    def __init__(self, content, encoding="utf-8"):
        self.content = content
        self.encoding = encoding

    def to_json(self):
        self.content_text = self.content.decode(self.encoding)
        return json.loads(self.content_text)

    def to_pandas(self, *args, **kwargs):
        return pandas.read_json(path_or_buf=BytesIO(self.content), *args, **kwargs)
