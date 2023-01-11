from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
import base64
import sys
from typing import Union


def decode(payload     )         :
    """
    Modified Base64 for URL variants exist, where the + and / characters of
    standard Base64 are respectively replaced by - and _.

    See https://en.wikipedia.org/wiki/Base64#URL_applications
    """

    if sys.version_info[0] < 3:
        # Base64 encode/decode does not accept `str` as input in python2
        # By running `future-fstrings-show`, it adds `unicode_literals` that
        # redefines some classes so the default behaviour changes
        def native_str_to_bytes(s, encoding=None):
            from future.types import newbytes  # pylint: disable=import-outside-toplevel
            return newbytes(s, encoding=encoding)
        payload = native_str_to_bytes(payload, encoding='utf-8')

    return base64.b64decode(payload, altchars=b'-_')


def encode(payload                   )         :
    """
    Modified Base64 for URL variants exist, where the + and / characters of
    standard Base64 are respectively replaced by - and _.

    See https://en.wikipedia.org/wiki/Base64#URL_applications
    """
    if isinstance(payload, str):
        payload = payload.encode('utf-8')

    return base64.b64encode(payload, altchars=b'-_')
