# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dhcomp']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21,<2.0', 'pandas']

setup_kwargs = {
    'name': 'dhcomp',
    'version': '0.3.1',
    'description': 'Simple utility to composite drill hole data in python',
    'long_description': '# dhcomp\n\n## Rationale\nThere does not seem to be any permissively licenced drill hole compositing software in python.\ndhcomp is a MIT licenced open source one function utility that (currently) composites geophysical data to a set of intervals.\n\n\n## Installation\nInstallation\n```pip install dhcomp```\n\n## Usage\n\n',
    'author': 'Ben',
    'author_email': 'ben@fractalgeoanalytics.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
