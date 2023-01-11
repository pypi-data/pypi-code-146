# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdncheck', 'cdncheck.tests']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cdncheck = cdncheck.cdncheck:main']}

setup_kwargs = {
    'name': 'cdncheck',
    'version': '1.0.0.34',
    'description': "A Python wrapper for ProjectDiscovery's cdncheck (https://github.com/projectdiscovery/cdncheck)",
    'long_description': '# `cdncheck-python`\n\n[![Tests](https://github.com/blacklanternsecurity/cdncheck-python/actions/workflows/tests.yml/badge.svg?branch=stable)](https://github.com/blacklanternsecurity/cdncheck-python/actions?query=workflow%3A"tests")\n\nThis is a Python wrapper around ProjectDiscovery\'s [cdncheck](https://github.com/projectdiscovery/cdncheck). It is useful for checking whether a given IP address belongs to a cloud provider, e.g. Google, Azure, etc. \n\nTests are run on a weekly schedule.\n\n## Installation\nIf you run into problems with installation, please make sure golang is installed on your system.\n```bash\n$ pip install cdncheck\n```\n\n## Usage (CLI)\n```bash\n$ cdncheck 1.2.3.4\n1.2.3.4 does not belong to a CDN\n\n$ cdncheck 168.62.20.37\n168.62.20.37 belongs to CDN "azure"\n```\n\n## Usage (Python)\n```python\n>>> from cdncheck import cdncheck\n# empty string == not belonging to a CDN\n>>> cdncheck(\'1.2.3.4\')\n\'\'\n>>> cdncheck(\'168.62.20.37\')\n\'azure\'\n```\n',
    'author': 'TheTechromancer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/blacklanternsecurity/cdncheck-python',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
