import base64
import hashlib
import os

import boto3

from dynamodb import Table
from storage import Bucket
from api import Response
from datetime import datetime

def handler(event, context):
    """Registers a code as job"""

    method = event['httpMethod']
    resource = event['resource']

    key = (event.get('pathParameters') or {}).get('id', None)
    body = event.get('body', {})

    functions = {
        'GET': {
            '/register/{id}': detail,
            '/register': list,
        },
        'POST': {
            '/register/{id}': create,
        },
        'DELETE': {
            '/register/{id}': delete,
        },
        'PATCH': {
            '/register/{id}': update,
        },
    }

    handler = functions.get(method, {}).get(resource)

    return handler(key=key, body=body)


def detail(key, *args, **kwargs):
    """Describes a entry"""

    table = Table('REGISTRY_TABLE_NAME')

    response = Response(200, table.get(key))

    return response.parse()

def list(*args, **kwargs):
    """Lists all entries"""
    pass

def delete(key, *args, **kwargs):
    """Deletes a entry"""
    pass

def update(key, body, *args, **kwargs):
    """Updates (patches) a entry"""
    pass

def create(key, body, *args, **kwargs):
    """Creates a entry"""

    # Creates the S3 client
    client = boto3.client('s3')
    bucket = Bucket('REGISTRY_BUCKET_NAME')
    table = Table('REGISTRY_TABLE_NAME')

    # Generates the file md5
    hash = hashlib.md5(key.encode()).digest().hex()

    # Gets the content of the payload
    filename = os.path.join('/tmp', f'{hash}.zip')
    filekey = f'build/artifacts/{hash}'

    with open(filename, 'wb+') as file:
        file.write(base64.b64decode(body))

    # Writes the content to S3
    bucket.upload(filename, filekey, delete=True)

    # Returns the object id
    object = {
        'name': key,
        'status': 'UPLOADED',
        'created_at': datetime.utcnow().isoformat(),
        'location': f's3://{bucket.name}/{filekey}',
    }

    table.update(hash, object)

    response = Response(200, {'id': hash, 'object': object})

    return response.parse()
