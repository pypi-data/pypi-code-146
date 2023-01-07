# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deck']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'cattrs>=1.7.1,<2.0.0',
 'dateutils>=0.6.12,<0.7.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'nextcloud-deck',
    'version': '0.2.0',
    'description': 'Python wrapper around Nextcloud Deck API',
    'long_description': '# Python Nextcloud Deck API\n\nSimple python based wrapper around the Nextcloud deck API\n\nBefore using this library you should get familiar with the [Offical REST API](https://deck.readthedocs.io/en/latest/API/)',
    'author': 'Kyle Prestel',
    'author_email': 'kprestel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kprestel/nextcloud-deck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
