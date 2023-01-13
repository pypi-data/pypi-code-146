from time import struct_time
from datetime import datetime
from calendar import timegm
from urllib.parse import urlparse

WEB_URI_SCHEMES = ["https", "http"]


def normalize_path(path):
    """Returns a normalized path where suffix and prefix slashes are removed

    :Examples:
        >>> from imglab.utils import url as utils
        >>> utils.normalize_path("/example.jpeg")
        'example.jpeg'
        >>> utils.normalize_path("/example.jpeg/")
        'example.jpeg'
        >>> utils.normalize_path("/subfolder/example.jpeg/")
        'subfolder/example.jpeg'

    :param path: A path string to be normalized
    :type path: str
    :return: A string with the normalized path
    :rtype: str
    """
    return path.strip("/")


def normalize_params(params):
    """Returns a dict of normalized params, transforming keys with underscores to hyphens and expires values with
    struct_time or datetime instances to timestamps

    :Examples:
        >>> from imglab.utils import url as utils
        >>> utils.normalize_params({"trim": "color", "trim_color": "orange"})
        {'trim': 'color', 'trim-color': 'orange'}
        >>> import time
        >>> utils.normalize_params({"width": 200, "height": 300, "expires": time.gmtime(1464096368)})
        {'width': 200, 'height': 300, 'expires': 1464096368}

    :param params: A dict with params to be normalized
    :type params: dict
    :return: A dict with the normalized params
    :rtype: dict
    """
    return dict(_normalize_param(_dasherize(key), value) for key, value in params.items())


def is_web_uri(uri):
    """Returns if the specified uri is a valid Web URI with https or https schema or not

    :Examples:
        >>> from imglab.utils import url as utils
        >>> utils.is_web_uri("https://imglab.io")
        True
        >>> utils.is_web_uri("http://imglab.io")
        True
        >>> utils.is_web_uri("imglab.io")
        False
        >>> utils.is_web_uri("ftp://imglab.io")
        False

    :param uri: A string with the URI
    :type uri: str
    :return: `True` if the specified uri is a valid Web URI, `False` otherwise
    :rtype: bool
    """
    try:
        return urlparse(uri).scheme in WEB_URI_SCHEMES
    except Exception:
        return False


def _dasherize(value):
    return value.replace("_", "-")


def _normalize_param(key, value):
    if key == "expires" and isinstance(value, struct_time):
        return (key, timegm(value))
    elif key == "expires" and isinstance(value, datetime):
        return (key, timegm(value.timetuple()))
    elif value == None:
        return (key, "")
    else:
        return (key, value)
