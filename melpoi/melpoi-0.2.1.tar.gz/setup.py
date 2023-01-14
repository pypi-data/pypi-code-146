# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melpoi', 'melpoi.dataframe', 'melpoi.sql']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.20.1,<0.21.0', 'ipython>=8.6.0,<9.0.0', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'melpoi',
    'version': '0.2.1',
    'description': '',
    'long_description': '# melpoi\n[![PyPI Latest Release](https://img.shields.io/pypi/v/melpoi.svg)](https://pypi.org/project/melpoi/)\n[![release](https://github.com/la0bing/melpoi/actions/workflows/release.yml/badge.svg?branch=master)](https://github.com/la0bing/melpoi/actions/workflows/release.yml)\n\nmelpoi is a python library to mainly to speed up data discovery, data analyzing, etc.\n\n# Get Started\n```\npip install melpoi\n```\n\n# Categories\n- [SQL](https://github.com/la0bing/melpoi/tree/master/melpoi/sql)\n- [DataFrame](https://github.com/la0bing/melpoi/tree/master/melpoi/dataframe)\n\n\n# Work in progress\n- Dataset auto analyzer\n- AutoML\n',
    'author': 'Melvin Low',
    'author_email': 'la0bing07148@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
