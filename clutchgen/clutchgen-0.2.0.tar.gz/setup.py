# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clutchGen', 'clutchGen.handlers']

package_data = \
{'': ['*'], 'clutchGen': ['templates/*']}

install_requires = \
['Mako>=1.1.6,<2.0.0', 'PyYAML>=6.0,<7.0', 'click>=8.0.4,<9.0.0']

entry_points = \
{'console_scripts': ['clutchGen = clutchGen.__main__:cli']}

setup_kwargs = {
    'name': 'clutchgen',
    'version': '0.2.0',
    'description': '',
    'long_description': 'ClutchGen is CLI tool for generating new projects structures. Developed on python.\nUsing `.yaml` config files you can create structures any complexity\n\nFor example with config like:\n\n```yaml\n$root:\n  - app:\n    - src:\n      - services:\n          - some_service.py\n      - settings.py\n    - main.py\n  - Makefile\n  - README.md\n```\n\nYou will get structure like this:\n\n![img.png](docs/images/example_of_project.png)\n\nMore info about usage you can find on [WIKI pages](https://gitlab.com/AlexeyReket/clutchgen/-/wikis/home)\n',
    'author': 'alexey.reket',
    'author_email': 'alexey.reket@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/AlexeyReket/clutchgen/-/wikis/home',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
