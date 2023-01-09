# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dillo']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.4,<0.4.0', 'jsonpickle>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'dill-o',
    'version': '0.2.1',
    'description': 'Small dill wrapper with Metadata',
    'long_description': None,
    'author': 'Anubhav Mattoo',
    'author_email': 'anubhavmattoo@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
