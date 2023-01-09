# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grai_client',
 'grai_client.endpoints',
 'grai_client.endpoints.v1',
 'grai_client.schemas',
 'grai_client.testing',
 'grai_client.utilities']

package_data = \
{'': ['*']}

install_requires = \
['multimethod==1.9',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'grai-client',
    'version': '0.1.16',
    'description': '',
    'long_description': 'None',
    'author': 'Ian Eaves',
    'author_email': 'ian@grai.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
