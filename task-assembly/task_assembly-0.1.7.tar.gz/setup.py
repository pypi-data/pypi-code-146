# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task_assembly']

package_data = \
{'': ['*']}

install_requires = \
['api-client>=1.3.1,<2.0.0', 'boto3>=1.26.0,<2.0.0', 'larry>=0.2.12,<0.3.0']

entry_points = \
{'console_scripts': ['task-assembly = task_assembly.cli:main']}

setup_kwargs = {
    'name': 'task-assembly',
    'version': '0.1.7',
    'description': 'SDK and CLI for using the Task Assembly crowdwork service',
    'long_description': '# Task Assembly Client\nTools for working with the Task Assembly service for managing crowdwork projects.\n',
    'author': 'Dave Schultz',
    'author_email': 'dave@daveschultzconsulting.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
