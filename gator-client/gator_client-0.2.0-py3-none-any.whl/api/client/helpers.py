"""API helpers."""
import json
from typing import Any, Optional
from urllib.parse import ParseResult, parse_qsl, unquote, urlencode, urlparse


def add_url_params(url: str, params: Optional[dict] = None, **kwargs: Any) -> str:
    """Add GET params to provided URL being aware of existing.

    Args:
        url: target URL to add params to
        params: dict of key:value pairs to be added as params
        kwargs: key:value pairs to be added as params as keyword arguments

    Remarks:
        If both params and kwargs are provided, the two are merged with kwargs
        taking precedence.

    Returns:
        URL with added params.

    Examples:
        >>> new_params = {'answers': False, 'data': ['some','values']}
        >>> add_url_params('https://foo.com', new_params)
        'https://foo.com?answers=false&data=some&data=values'
        >>> add_url_params('https://bar.com/hello', name='world')
        'https://bar.com/hello?name=world'
    """
    # Merge params and kwargs into one dict, with kwargs taking precedence
    params = params or {}
    params.update(kwargs)

    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))
    # Merging URL arguments dict with new params
    parsed_get_args.update(params)

    # Bool and Dict values should be converted to json-friendly values
    # you may throw this part away if you don't like it :)
    parsed_get_args.update(
        {k: json.dumps(v) for k, v in parsed_get_args.items()
         if isinstance(v, (bool, dict))}
    )

    # Converting URL argument to proper query string
    encoded_get_args = urlencode(parsed_get_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()

    return new_url
