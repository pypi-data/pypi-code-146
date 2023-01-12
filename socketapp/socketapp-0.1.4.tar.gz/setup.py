# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['socketapp']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'socketapp',
    'version': '0.1.4',
    'description': 'An opinionated library for creating websocket-based applications.',
    'long_description': '# socketapp\n An opinionated library for creating websocket-based applications.\n',
    'author': 'CircuitSacul',
    'author_email': 'circuitsacul@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
