# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twothousand_forty_eight', 'twothousand_forty_eight.board']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['start = twothousand_forty_eight.app:main']}

setup_kwargs = {
    'name': 'twothousand-forty-eight',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Elias Eskelinen',
    'author_email': 'pgp@eliaseskelinen.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
