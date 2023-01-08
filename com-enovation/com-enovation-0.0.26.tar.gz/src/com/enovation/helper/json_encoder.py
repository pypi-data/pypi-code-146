import logging
from datetime import datetime
import json

from pandas import DataFrame, to_datetime, NaT, isnull


class JSONEncoder(json.JSONEncoder):

    _logger: logging.Logger = logging.getLogger(__name__)

    def default(self, obj):

        if isinstance(obj, DataFrame):
            return obj.to_dict()

        elif isinstance(obj, datetime):
            return obj.isoformat()

        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)
