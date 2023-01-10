#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
It is aimed to get rid of repetitive lines of code by integrating tools
that use multiple APIs for FastApi and facilitate repetitive operations.

Details will be shared at
https://www.ibrahimcorut.com/tr/projects/pypi-corut_fastapi_tools.
"""

import importlib_metadata

__all__ = (
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
)

__copyright__ = "Copyright 2023 ibrahim CÖRÜT"
metadata = importlib_metadata.metadata("corut_fastapi_tools")
__title__ = metadata["name"]
__summary__ = metadata["summary"]
__uri__ = metadata["home-page"]
__version__ = metadata["version"]
__author__ = metadata["author"]
__email__ = metadata["author-email"]
__license__ = metadata["license"]

if __name__ == '__main__':
    for _ in __all__:
        print(f'{_}'.ljust(13), ':', globals().get(_))
