""" Custom JSON encoder
"""
import datetime
from flask.json import JSONEncoder


class FlaskJSONEncoder(JSONEncoder):

    def default(self, o):
        try:
            if isinstance(o,
                          (datetime.datetime, datetime.date, datetime.time)):
                return o.isoformat()
            elif isinstance(o, datetime.timedelta):
                return o.total_seconds()
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, o)
