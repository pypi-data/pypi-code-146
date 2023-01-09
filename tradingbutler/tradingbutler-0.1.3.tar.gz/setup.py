# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tradingbutler', 'tradingbutler.tests']

package_data = \
{'': ['*'], 'tradingbutler': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'tradingbutler',
    'version': '0.1.3',
    'description': '',
    'long_description': '# tradingbutler\n\norganizes data from trades and turn into statistics',
    'author': 'Robin Huo',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Robinhuo1/tradingbutler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
