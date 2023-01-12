# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compose', 'compose.schema', 'compose.types']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pymongo[aws]>=4.3.3,<5.0.0']

setup_kwargs = {
    'name': 'pozalabs-compose',
    'version': '0.1.1',
    'description': 'Backend components for POZAlabs',
    'long_description': 'None',
    'author': 'pozalabs',
    'author_email': 'contact@pozalabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
