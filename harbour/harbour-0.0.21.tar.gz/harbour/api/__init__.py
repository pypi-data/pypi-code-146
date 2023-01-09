import json

from decimal import Decimal
from datetime import datetime, date

class Response:

    def __init__(self, code, body, *args, **kwargs):

        self.code = code
        self.body = body

    def format(self, obj, *args, **kwargs):
        """Default json formatter"""

        if isinstance(obj, datetime):

            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')

        elif isinstance(obj, date):

            return obj.strftime('%Y-%m-%d')

        elif isinstance(obj, Decimal):

            return format(obj, '.8')

        elif isinstance(obj, bytes):

            return obj.decode(errors='ignore')

        elif isinstance(obj, timedelta):

            return str(obj)

        elif isinstance(obj, set):

            return ','.join(list(obj))

        else:

            raise TypeError ("Type %s not serializable" % type(obj))

    def parse(self, *args, **kwargs):
        """Returns a parsed response"""

        if isinstance(self.body, (dict, list)):

            self.body = json.dumps(self.body, default=self.format)

        elif isinstance(self.body, (str)):
            pass

        elif self.body is None:
            self.body = json.dumps({})

        else:
            self.code = 500
            self.body = f'Invalid response format {type(self.body)}'

        response = {
            'statusCode': self.code,
            'body': self.body,
        }

        return response
