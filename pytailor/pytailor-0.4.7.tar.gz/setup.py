# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytailor',
 'pytailor.api',
 'pytailor.api.schema',
 'pytailor.api.schema.strategies',
 'pytailor.cli',
 'pytailor.clients',
 'pytailor.execution']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'genson>=1.2.2,<2.0.0',
 'httpx>=0.23.0,<0.24.0',
 'jsonpath-ng>=1.5.2,<2.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['tailor = pytailor.cli.main:cli']}

setup_kwargs = {
    'name': 'pytailor',
    'version': '0.4.7',
    'description': 'pyTailor orchestrates your existing python code as *workflows*',
    'long_description': 'None',
    'author': 'Audun Gravdal Johansen',
    'author_email': 'audun@entail.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/entailor/pytailor/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
