from urllib.parse import ParseResult, quote, urlencode

from .source import Source
from .signature import generate as generate_signature
from .utils import url as utils


def url(source, path, **params):
    """Returns a formatted URL string for a source, with a path and optional arguments

    :Examples:
        >>> import imglab
        >>> imglab.url("assets", "example.jpeg")
        'https://assets.imglab-cdn.net/example.jpeg'
        >>> imglab.url(imglab.Source("assets"), "example.jpeg", width=500, height=600)
        'https://assets.imglab-cdn.net/example.jpeg?width=500&height=600'

    :param source: A source name as string or :class:`imglab.Source` object
    :type source: str, class:`imglab.Source`
    :param path: The path where the resource is located
    :type path: str
    :param params: The query parameters that we want to use as a keyword argument list
    :type params: list, optional
    :raises ValueError: When the specified source is not a string or a :class:`imglab.Source` object
    :return: A string with the generated URL
    :rtype: str
    """
    if isinstance(source, str):
        return _url_for_source(Source(source), path, params)
    elif isinstance(source, Source):
        return _url_for_source(source, path, params)
    else:
        raise ValueError("Invalid source name or source. A string or a %s instance is expected." % Source.__name__)


def _url_for_source(source, path, params):
    normalized_path = utils.normalize_path(path)
    normalized_params = utils.normalize_params(params)

    return ParseResult(
        scheme=source.scheme(),
        netloc=_netloc(source),
        path=source.path(_encode_path(normalized_path)),
        params=None,
        query=_encode_params(source, normalized_path, normalized_params),
        fragment=None,
    ).geturl()


def _netloc(source):
    if source.port:
        return ":".join([source.host, str(source.port)])
    else:
        return source.host


def _encode_path(path):
    if utils.is_web_uri(path):
        return _encode_path_component(path)
    else:
        return "/".join(map(_encode_path_component, path.split("/")))


def _encode_path_component(path_component):
    return quote(path_component, safe=[])


def _encode_params(source, path, params):
    if source.is_secure():
        params.update(signature=generate_signature(source, path, urlencode(params)))

    return urlencode(params)
