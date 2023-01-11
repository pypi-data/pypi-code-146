# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tryton_analyzer']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=0.4.9,<0.5.0', 'lxml>=4.9.1,<5.0.0', 'pygls>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['tryton-lint = tryton_analyzer.tryton_lint:run',
                     'tryton-ls = tryton_analyzer.tryton_ls:run']}

setup_kwargs = {
    'name': 'tryton-analyzer',
    'version': '0.0.3',
    'description': 'A language server / linter for the Tryton framework',
    'long_description': '',
    'author': 'Jean Cavallo',
    'author_email': 'jean.cavallo@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
