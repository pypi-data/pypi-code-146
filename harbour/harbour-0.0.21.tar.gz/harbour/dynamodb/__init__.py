import datetime
import os

import boto3

from decimal import Decimal

def flatten(item, lkey='', sep='.'):
    """Flattens a dict to key1.key2.key3: value notation."""
    result = {}

    for rkey, val in item.items():

        key = lkey + rkey

        if isinstance(val, dict):

            result.update(flatten(val, key + sep))

        else:

            result[key] = val

    return result


class Table:

    def __init__(self, table, pk='id', *args, **kwargs):

        # Seek order: env defined then directly defined.
        table = os.getenv(table) or table

        self.pk = pk
        self.table = boto3.resource('dynamodb').Table(table)

    def format(self, obj, *args, **kwargs):
        """Default object formatter"""

        if isinstance(obj, datetime.datetime):

            return obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

        elif isinstance(obj, datetime.date):

            return obj.strftime('%Y-%m-%d')

        elif isinstance(obj, Decimal):

            return format(obj, '.8')

        elif isinstance(obj, bytes):

            return obj.decode(errors='ignore')

        elif isinstance(obj, datetime.timedelta):

            return str(obj)

        elif isinstance(obj, set):

            return ','.join(list(obj))

        elif isinstance(obj, list):

            return [self.format(i) for i in obj]

        elif isinstance(obj, dict):

            response = {}

            for k, v in obj.items():

                response[k] = self.format(v)

            return response

        else:

            return obj

    def get(self, pk, attributes=None, *args, **kwargs):
        """Returns the object"""

        payload = {
            'Key': {self.pk: pk},
            'ConsistentRead': True,
        }

        if attributes is not None:

            # Type checking and converting
            if isinstance(attributes, str):
                attributes = [attributes]

            elif isinstance(attributes, list):
                pass

            else:

                raise TypeError('attributes must be list or string')

            payload['ProjectionExpression'] = ', '.join(
                [f'#{a}' for a in attributes]
            )
            payload['ExpressionAttributeNames'] = {
                f'#{a}': a for a in attributes
            }

        response = self.table.get_item(**payload)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:

            # TODO: do this properly :)
            raise Exception('Deu ruim!')

        return response.get('Item', None)

    def update(self, pk, update, mode='PUT', *args, **kwargs):
        """Updates the entry on the DynamoDB"""

        if mode not in ['PUT', 'PATCH']:
            raise ValueError('Mode should be PUT or PATCH')

        payload = {
            'Key': {self.pk: pk},
            'ReturnValues': 'ALL_NEW'
        }

        # Injects the updated_at field
        update['updated_at'] = datetime.datetime.utcnow().isoformat()

        if mode == 'PUT':

            payload['UpdateExpression'] = 'SET ' + ', '.join(
                [f'#{k} = :{k}' for k in update.keys()]
            )

            payload['ExpressionAttributeNames'] = {
                f'#{k}': k for k in update.keys()
            }

            payload['ExpressionAttributeValues'] = {
                f':{k}': self.format(v) for k,v in update.items()
            }


        elif mode == 'PATCH':

            update = flatten(update)

            payload['UpdateExpression'] = 'SET ' + ', '.join(
                [f'#{k.replace(".", ".#")} = :{k.replace(".", "__")}' for k in update.keys()]
            )

            payload['ExpressionAttributeNames'] = {
                f'#{k}': k for x in update.keys() for k in x.split('.')
            }


            payload['ExpressionAttributeValues'] = {
                f':{k.replace(".", "__")}': self.format(v) for k,v in update.items()
            }


        response = self.table.update_item(**payload)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:

            # TODO: do this properly :)
            raise Exception('Deu ruim!')

        return response.get('Attributes', None)

    def delete(self, pk, *args, **kwargs):
        """Deletes a entry from DynamoDB"""

        response = self.table.delete_item(Key={self.pk: pk})

        return response

    def remove(self, pk, columns, *args, **kwargs):
        """Removes a column from DynamoDB entry"""

        payload = {
            'Key': {self.pk: pk},
            'ReturnValues': 'ALL_NEW',
        }

        if isinstance(columns, str):
            columns = [columns]

        elif isinstance(columns, list):
            pass

        else:
            raise TypeError('columns must be either string or list')

        payload['UpdateExpression'] = 'REMOVE ' + ', '.join(
            [f'#{c}' for c in columns]
        )

        payload['ExpressionAttributeNames'] = {
            f'#{c}': c for c in columns
        }

        response = self.table.update_item(**payload)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:

            # TODO: do this properly :)
            raise Exception('Deu ruim!')

        return response.get('Attributes', None)
