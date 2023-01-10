from six import string_types, binary_type
from vxbase.vjson import load_json
import locale

try:
    locale.setlocale(locale.LC_ALL, '')
    CHARSET = locale.getlocale(locale.LC_CTYPE)[1]
except locale.Error:
    CHARSET = None
if CHARSET is None:
    CHARSET = 'ascii'


def is_iterable(obj):
    """ Method that verifies if an object is iterable and not a string, example:

        >>>vtypes.is_iterable(1)
        False
        >>> vtypes.is_iterable([1, 2, 3])
        True

    :param obj: Any object that will be tested if is iterable
    :return: True or False if the object can be iterated
    """
    return hasattr(obj, '__iter__') and not isinstance(obj, string_types + (binary_type,))


def decode(string, errors='replace'):
    if isinstance(string, binary_type) and not isinstance(string, string_types):
        return string.decode(encoding=CHARSET, errors=errors)
    return string


def encode(string, errors='replace'):
    if isinstance(string, string_types) and not isinstance(string, binary_type):
        return string.encode(encoding=CHARSET, errors=errors)
    return string


def get_error_message(exception_obj):
    """Get the message error from exception object or dict.

    :param exception_obj: the exception object or dict exception where get the message.
    :type: object, dict
    :return: A string containing the exception message.
    :rtype: str
    """
    error_attrs = ['stderr_output', 'explanation', 'msg', 'strerror',
                   'message', 'error_message', 'data', 'name']

    if isinstance(exception_obj, str):
        return str(exception_obj)
    for attr in error_attrs:
        if isinstance(exception_obj, dict) and exception_obj.get(attr):
            return exception_obj[attr]
        if not hasattr(exception_obj, attr):
            continue
        msg = getattr(exception_obj, attr)
        if not msg:
            continue
        msg = load_json(msg, False) or msg
        if isinstance(msg, dict):
            msg = msg.get("error") or msg.get("message") or msg
        if isinstance(msg, bytes):
            msg = msg.decode()
        return msg
    return repr(exception_obj)