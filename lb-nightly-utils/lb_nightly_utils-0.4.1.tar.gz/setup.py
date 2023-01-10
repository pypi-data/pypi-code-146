# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb', 'lb.nightly.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.22.13,<2.0.0',
 'lb-nightly-configuration>=0.3,<0.4',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'lb-nightly-utils',
    'version': '0.4.1',
    'description': 'Common utilities for LHCb Nightly and Continuous Integration Build System',
    'long_description': 'None',
    'author': 'Marco Clemencic',
    'author_email': 'marco.clemencic@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
