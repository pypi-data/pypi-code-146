# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dateparse', 'dateparse._parse_util']

package_data = \
{'': ['*']}

install_requires = \
['datetime>=4.9,<5.0']

setup_kwargs = {
    'name': 'dateparse',
    'version': '0.10.1a0',
    'description': 'A pure Python library for parsing natural language time expressions, with minimal dependencies',
    'long_description': '# Dateparse\nA python library for parsing natural language time descriptions\n',
    'author': 'keagud',
    'author_email': 'keagud@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
