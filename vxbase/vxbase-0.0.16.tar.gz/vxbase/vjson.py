import logging
from os import path
from six import string_types, binary_type
import simplejson


_logger = logging.getLogger(__name__)


def load_json(json, logger=True):
    """Loads a valid json string or file into a dictionary, returning the dict
    object.

    :param json: json string to convert.
    :type json: string or dict
    :param logger: when is False, it does not print the error logger. Default True
    :type logger: bool

    :returns: Returns the loaded dict or False if an error ocurred.
    :rtype: dict or bool

    :Example:

    .. code-block:: python

        json_dict = load_json(json_str)
        if isinstance(json_dict, dict):
            _logger.info("Everything OK")
        else:
            _logger.error("Something wrong")

    :Note: Don't check only using ``if json_dict: ...`` because ``"{}"`` is a
        valid json string and will return a valid object, but an empty object
        is considered `falsy` and the check will fail (unless that is what you
        want).
    """
    if isinstance(json, binary_type):
        json = json.decode()
    if isinstance(json, string_types):
        if path.isfile(json):
            return load_json_file(json, logger)
        return load_json_string(json, logger)
    if isinstance(json, dict):
        return json
    if logger:
        error_message = "Invalid type ({type})".format(type=type(json))
        _logger.error("Error loading json: %s", error_message)
    return False


def load_json_string(json, logger=True):
    """Loads a valid json string into a dictionary, returning the dict object.

    :param json: json string to convert.
    :type json: string
    :param logger: when is False, it does not print the error logger. Default True
    :type logger: bool

    :returns: Returns the loaded dict or False if an error ocurred.
    :rtype: dict or bool

    :Example:

    .. code-block:: python

        json_dict = load_json_string(json_str)
        if isinstance(json_dict, dict):
            _logger.info("Everything OK")
        else:
            _logger.error("Something wrong")

    :Note: Don't check only using ``if json_dict: ...`` because ``"{}"`` is a
        valid json string and will return a valid object, but an empty object
        is considered `falsy` and the check will fail (unless that is what you
        want).
    """
    _logger.debug(json)
    try:
        return simplejson.loads(json)
    except ValueError as error:
        if logger:
            _logger.error("Error loading json string: %s", str(error))
        return False


def load_json_file(json, logger=True):
    """Loads a valid json file into a dictionary, returning the dict object.

    :param json: json file to load.
    :type json: string
    :param logger: when is False, it does not print the error logger. Default True
    :type logger: bool

    :returns: Returns the loaded dict or False if an error ocurred.
    :rtype: dict or bool

    :Example:

    .. code-block:: python

        json_dict = load_json_file(json_file_name)
        if isinstance(json_dict, dict):
            _logger.info("Everything OK")
        else:
            _logger.error("Something wrong")

    :Note: Don't check only using ``if json_dict: ...`` because ``"{}"`` is a
        valid json string and will return a valid object, but an empty object
        is considered `falsy` and the check will fail (unless that is what you
        want).
    """
    try:
        with open(json) as json_file:
            return load_json_string(json_file.read(), logger)
    except IOError as error:
        if logger:
            _logger.error("Error loading json file %s: %s", json, str(error))
        return False


def save_json(info, filename, ensure_ascii=False):
    """Save info into Json file.

    :param info: Object to be saved
    :param filename: Name of Json file

    :returns: Absolute path of Json file
    :rtype: str
    """
    try:
        with open(filename, 'w') as fout:
            _logger.debug("Opening file %s", filename)
            simplejson.dump(info, fout, sort_keys=True, indent=4,
                            ensure_ascii=ensure_ascii, separators=(',', ':'))
            if not path.isabs(filename):
                filename = path.abspath(filename)
            _logger.debug("File saved")
    except IOError as error:
        _logger.error(error)
        return False
    return filename
