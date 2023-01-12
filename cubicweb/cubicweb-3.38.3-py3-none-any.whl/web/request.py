from cubicweb_web.request import *  # noqa
from cubicweb_web.request import (  # noqa
    _parse_accept_header,
    _mimetype_sort_key,
    _mimetype_parser,
    _charset_sort_key,
)

from cubicweb.utils import warn_about_deprecated_web_module

warn_about_deprecated_web_module()
