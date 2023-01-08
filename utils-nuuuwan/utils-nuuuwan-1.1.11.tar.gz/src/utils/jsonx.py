"""JSON utils."""
import base64
import json

from utils import filex


def read(file_name):
    """Read JSON from file.

    Args:
        file_name (str): file name

    Returns:
        Parsed JSON data

    """
    return json.loads(filex.read(file_name))


def write(file_name, data):
    """Write data as JSON to file.

    Args:
        file_name (str): file name
        data: data as serializable object

    """
    filex.write(file_name, json.dumps(data, indent=2))


def serialize(data):
    if isinstance(data, bytes):
        return {
            'type': 'bytes',
            'data': base64.b64encode(data).decode('ascii'),
        }

    return {
        'type': None,
        'data': data,
    }


def deserialize(data):
    data_type = data['type']
    data_data = data['data']

    if data_type == 'bytes':
        return base64.b64decode(data_data)

    return data_data
