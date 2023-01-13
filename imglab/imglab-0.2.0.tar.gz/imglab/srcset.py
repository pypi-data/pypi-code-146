from .url import url
from .sequence import sequence
from .utils import srcset as utils

DEFAULT_DPRS = [1, 2, 3, 4, 5, 6]
DEFAULT_WIDTHS = sequence(100, 8192)


def srcset(source, path, **params):
    """Returns a formatted srcset string for a source, with a path and optional arguments

    :Examples:
        >>> import imglab
        >>> imglab.srcset("assets", "example.jpeg", width=500, dpr=[1, 2, 3])
        'https://assets.imglab-cdn.net/example.jpeg?width=500&dpr=1 1x,\\nhttps://assets.imglab-cdn.net/example.jpeg?width=500&dpr=2 2x,\\nhttps://assets.imglab-cdn.net/example.jpeg?width=500&dpr=3 3x'
        >>> imglab.srcset("assets", "example.jpeg", width=[400, 800, 1200], format="webp")
        'https://assets.imglab-cdn.net/example.jpeg?width=400&format=webp 400w,\\nhttps://assets.imglab-cdn.net/example.jpeg?width=800&format=webp 800w,\\nhttps://assets.imglab-cdn.net/example.jpeg?width=1200&format=webp 1200w'

    :param source: A source name as string or :class:`imglab.Source` object
    :type source: str, class:`imglab.Source`
    :param path: The path where the resource is located
    :type path: str
    :param params: The query parameters that we want to use as keyword argument list
    :type params: list, optional
    :raises ValueError: When some params fluid combinations are not allowed
    :return: A string with the generated srcset value
    :rtype: str
    """
    params = utils.normalize_params(params)

    width, height, dpr = [params.get(key) for key in ["width", "height", "dpr"]]

    if _is_fluid(width):
        if _is_fluid(dpr):
            raise ValueError("dpr as %s is not allowed when width is list or range" % type(dpr).__name__)

        return _srcset_width(source, path, params)
    elif width or height:
        if _is_fluid(height):
            raise ValueError("height as %s is not allowed when width is not a list or range" % type(height).__name__)

        return _srcset_dpr(source, path, {**params, **{"dpr": _dprs(params)}})
    else:
        if _is_fluid(dpr):
            raise ValueError("dpr as %s is not allowed without specifying width or height" % type(dpr).__name__)

        return _srcset_width(source, path, {**params, **{"width": DEFAULT_WIDTHS}})


def _dprs(params):
    if _is_fluid(params.get("dpr")):
        return params["dpr"]
    else:
        return DEFAULT_DPRS


def _is_fluid(value):
    return isinstance(value, (list, range))


def _srcset_dpr(source, path, params):
    return ",\n".join(
        "%s %dx" % (url(source, path, **split_params), split_params["dpr"])
        for split_params in utils.split_params_dpr(params)
    )


def _srcset_width(source, path, params):
    return ",\n".join(
        "%s %dw" % (url(source, path, **split_params), split_params["width"])
        for split_params in utils.split_params_width(params)
    )
