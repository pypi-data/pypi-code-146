# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mercapi',
 'mercapi.models',
 'mercapi.models.item',
 'mercapi.models.profile',
 'mercapi.models.search',
 'mercapi.requests',
 'mercapi.util']

package_data = \
{'': ['*']}

install_requires = \
['ecdsa>=0.18.0,<0.19.0',
 'httpx>=0.23.0,<0.24.0',
 'python-jose[cryptography]>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'mercapi',
    'version': '0.2.1',
    'description': 'Python API for querying and browsing mercari.jp',
    'long_description': "# mercapi\n\n![PyPI](https://img.shields.io/pypi/v/mercapi)\n[![Tests](https://github.com/take-kun/mercapi/actions/workflows/check.yaml/badge.svg?branch=main)](https://github.com/take-kun/mercapi/actions/workflows/check.yaml)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mercapi)\n\n[API Documentation](https://take-kun.github.io/mercapi/)\n\n## What is Mercapi?\n\nMercapi is a Python wrapper for *mercari.jp* API.\nIt's capable of producing HTTP requests implementing security mechanisms employed in native *mercari.jp* web app.\nRequests and responses are mapped to custom classes with type-hinting and documentation.\n\n## Quickstart\n\nFirst, install the `mercapi` package using the package manager of your choice.\n\nAs an example, we want to run the search query `sharpnel`.\n\n```python\nfrom mercapi import Mercapi\n\n\nm = Mercapi()\nresults = await m.search('sharpnel')\n\nprint(f'Found {results.meta.num_found} results')\nfor item in results.items:\n    print(f'Name: {item.name}\\\\nPrice: {item.price}\\\\n')\n\n```\n\nWe can use a single result object to retrieve full details of the listing.\n```python\nitem = results.items[0]\nfull_item = await item.full_item()\n\nprint(full_item.description)\n```\n\nOr get it directly using an ID.\n```python\nitem = await m.item('m90925725213')\n\nprint(item.description)\n```\n\nRefer to `mercapi.mercapi.Mercapi` documentation for all implemented features.\n\n*Examples above are not executable. If you want to try them out, run `python example.py`.*",
    'author': 'take-kun',
    'author_email': '109226194+take-kun@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/take-kun/mercapi/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
