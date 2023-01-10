# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freighter', 'freighter.util']

package_data = \
{'': ['*']}

install_requires = \
['janus>=1.0.0,<2.0.0',
 'msgpack>=1.0.4,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'urllib3>=1.26.12,<2.0.0',
 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'synnax-freighter',
    'version': '0.2.6',
    'description': '',
    'long_description': 'None',
    'author': 'emiliano bonilla',
    'author_email': 'emilbon99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
