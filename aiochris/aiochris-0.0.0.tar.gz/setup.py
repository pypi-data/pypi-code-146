# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chris', 'chris.common', 'chris.cube', 'chris.store']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'pyserde==0.8.3']

setup_kwargs = {
    'name': 'aiochris',
    'version': '0.0.0',
    'description': 'ChRIS client built on aiohttp',
    'long_description': '# aiochris\n\n[![Tests](https://github.com/FNNDSC/aiochris/actions/workflows/test.yml/badge.svg)](https://github.com/FNNDSC/chris_plugin/actions/workflows/test.yml)\n[![PyPI](https://img.shields.io/pypi/v/aiochris)](https://pypi.org/project/aiochris/)\n[![License - MIT](https://img.shields.io/pypi/l/aiochris)](https://github.com/FNNDSC/aiochris/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[_ChRIS_](https://chrisproject.org) Python client library built on\n[aiohttp](https://github.com/aio-libs/aiohttp) (async HTTP client) and\n[pyserde](https://github.com/yukinarit/pyserde)\n([dataclasses](https://docs.python.org/3/library/dataclasses.html) deserializer).\n\n## Developing\n\nRequires [Poetry](https://python-poetry.org/) version 1.3.1.\n\n### Setup\n\n```shell\ngit clone git@github.com:FNNDSC/aiochris.git\ncd aiochris\npoetry install --with=dev\n```\n\n### Testing\n\n1. Start up [miniCHRIS](https://github.com/FNNDSC/miniChRIS-docker)\n2. `poetry run pytest`\n\n### Code Formatting\n\n```shell\npoetry run pre-commit run --all-files\n```\n',
    'author': 'FNNDSC',
    'author_email': 'dev@babyMRI.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
