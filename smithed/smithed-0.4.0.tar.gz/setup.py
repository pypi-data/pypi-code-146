# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'smithed'}

packages = \
['weld']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.82.1,<0.83.0',
 'click>=8.1.3,<9.0.0',
 'jsonpath-ng>=1.5.3,<2.0.0',
 'mecha>=0.59.2,<0.60.0']

entry_points = \
{'beet': ['commands = weld.commands'],
 'console_scripts': ['weld = weld.commands:weld']}

setup_kwargs = {
    'name': 'smithed',
    'version': '0.4.0',
    'description': "Smithed's Python client with CLI, weld and more",
    'long_description': '# smithed-python\n> The python package for Smithed. Including weld, cli, and libraries (via [`smithed-libraries`](https://github.com/Smithed-MC/Libraries)).\n> **HEAVY WIP**\n',
    'author': 'Smithed Team',
    'author_email': 'team@smithed.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
