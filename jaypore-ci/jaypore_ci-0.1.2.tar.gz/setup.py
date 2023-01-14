# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaypore_ci', 'jaypore_ci.executors', 'jaypore_ci.remotes']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'structlog>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'jaypore-ci',
    'version': '0.1.2',
    'description': '',
    'long_description': 'None',
    'author': 'arjoonn sharma',
    'author_email': 'arjoonn.94@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
