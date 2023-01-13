from itertools import zip_longest

from ..sequence import sequence, DEFAULT_SIZE as SEQUENCE_DEFAULT_SIZE

NORMALIZE_KEYS = ["dpr", "width"]

SPLIT_DPR_KEYS = ["dpr", "quality"]
SPLIT_WIDTH_KEYS = ["width", "height", "quality"]


def normalize_params(params):
    """Returns a dict of normalized params, rejecting values with keys includes in normalized keys and with empty lists

    :Examples:
        >>> from imglab.utils import srcset as utils
        >>> utils.normalize_params({"width": [], "dpr": [], "format": "png"})
        {'format': 'png'}
        >>> utils.normalize_params({"width": [100, 200], "dpr": [], "format": "png"})
        {'width': [100, 200], 'format': 'png'}

    :param params: A dict with params to be normalized
    :type params: dict
    :return: A dict with the normalized params
    :rtype: dict
    """
    return {key: value for key, value in params.items() if not (key in NORMALIZE_KEYS and value == [])}


def split_params_dpr(params):
    """Returns a list with the parameters to use in different URLs for a srcset split by dpr parameter

    :Examples:
        >>> from imglab.utils import srcset as utils
        >>> utils.split_params_dpr({"width": 100, "dpr": [1, 2], "format": "png"})
        [{'width': 100, 'dpr': 1, 'format': 'png'}, {'width': 100, 'dpr': 2, 'format': 'png'}]
        >>> utils.split_params_dpr({"width": 100, "blur": 100, "dpr": range(1, 2), "format": "webp"})
        [{'width': 100, 'blur': 100, 'dpr': 1, 'format': 'webp'}, {'width': 100, 'blur': 100, 'dpr': 2, 'format': 'webp'}]

    :param params: A dict with params to be split by dpr
    :type params: dict
    :return: A list of dicts with parameters to be used for every URL in a srcset
    :rtype: list
    """
    return list(
        _merge_params(params, {"dpr": dpr, "quality": quality})
        for dpr, quality in _split_values(params, SPLIT_DPR_KEYS, _split_size_dpr(params["dpr"]))
    )


def split_params_width(params):
    """Returns a list with the parameters to use in different URLs for a srcset split by width parameter

    :Examples:
        >>> from imglab.utils import srcset as utils
        >>> utils.split_params_width({"width": [100, 200], "format": "png"})
        [{'width': 100, 'format': 'png'}, {'width': 200, 'format': 'png'}]
        >>> utils.split_params_width({"width": [100, 200], "height": [300], "quality": [75], "format": "png"})
        [{'width': 100, 'height': 300, 'quality': 75, 'format': 'png'}, {'width': 200, 'height': None, 'quality': None, 'format': 'png'}]

    :param params: A dict with params to be split by width
    :type params: dict
    :return: A list of dicts with parameters to be used for every URL in a srcset
    :rtype: list
    """
    return list(
        _merge_params(params, {"width": width, "height": height, "quality": quality})
        for width, height, quality in _split_values(params, SPLIT_WIDTH_KEYS, _split_size_width(params["width"]))
    )


def _split_size_dpr(value):
    if isinstance(value, range):
        return len(value) + 1
    else:
        return len(value)


def _split_size_width(value):
    if isinstance(value, range):
        return SEQUENCE_DEFAULT_SIZE
    else:
        return len(value)


def _split_values(params, keys, size):
    return list(zip_longest(*[_split_value(key, params.get(key), size) for key in keys]))


def _split_value(key, value, size):
    if key == "dpr" and isinstance(value, range):
        return list(range(value.start, value.stop + 1))
    elif isinstance(value, range):
        return sequence(value.start, value.stop, size)
    elif isinstance(value, list):
        return value
    else:
        return [value] * size


def _merge_params(params, merge_params):
    return {**params, **{key: value for key, value in merge_params.items() if key in params}}
