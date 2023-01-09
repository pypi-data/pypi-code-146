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
    'version': '1.0.0.4',
    'description': "A Python wrapper for ProjectDiscovery's cdncheck (https://github.com/projectdiscovery/cdncheck)",
    'long_description': "# `cdncheck-python`\n\nThis is a Python wrapper around ProjectDiscovery's [cdncheck](https://github.com/projectdiscovery/cdncheck). Given an IP address it will identify which cloud provider, if any, it belongs to.\n\n## Installation\n```bash\n$ pip install cdncheck\n```\n\n## Usage (CLI)\n```bash\n$ cdncheck 1.2.3.4\n1.2.3.4 does not belong to a CDN\n\n$ cdncheck 168.62.20.37\n168.62.20.37 belongs to CDN azure\n```\n\n## Usage (Python)\n```python\n>>> from cdncheck import cdncheck\n>>> cdncheck.cdncheck('1.2.3.4')\n''\n>>> cdncheck('168.62.20.37')\n'azure'\n```\n",
    'author': 'TheTechromancer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/blacklanternsecurity/cdncheck-python',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
