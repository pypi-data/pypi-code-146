# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goog_stats']

package_data = \
{'': ['*']}

install_requires = \
['logging>=0.4.9.6,<0.5.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'typer>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'goog-stats',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Project to push stats to google analytics\n\n# <i> example',
    'author': 'Yash Jagdale',
    'author_email': 'jagdale0210@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.10.8',
}


setup(**setup_kwargs)
