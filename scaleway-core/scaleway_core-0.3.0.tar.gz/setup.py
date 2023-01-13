# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scaleway_core',
 'scaleway_core.bridge',
 'scaleway_core.profile',
 'scaleway_core.utils',
 'scaleway_core.validations']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'python-dateutil>=2.8.2,<3.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'scaleway-core',
    'version': '0.3.0',
    'description': 'Scaleway SDK for Python',
    'long_description': '# Scaleway Python SDK - Core\n',
    'author': 'Scaleway',
    'author_email': 'opensource@scaleway.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
