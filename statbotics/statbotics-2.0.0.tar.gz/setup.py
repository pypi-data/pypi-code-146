# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statbotics']

package_data = \
{'': ['*']}

install_requires = \
['cachecontrol>=0.12.11,<0.13.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'statbotics',
    'version': '2.0.0',
    'description': 'Modernizing FRC Data Analytics',
    'long_description': "# Statbotics API\n\nStatbotics.io aims to modernize FRC data analytics through developing and distributing cutting-edge metrics and analysis. This Python API makes Expected Points Added (EPA) statistics just a few Python lines away! Currently we support queries on teams, years, events, and matches. Read below for usage and documentation.\n\nVisit https://statbotics.io for more content!\n\n## Usage\n\nWith Python>=3.8 and pip installed, run\n\n```\npip install statbotics\n```\n\nThen in a Python file, create a Statbotics object and get started!\n\n```\nimport statbotics\n\nsb = statbotics.Statbotics()\nprint(sb.get_team(254))\n\n>> {'team': 254, 'name': 'The Cheesy Poofs', 'offseason': False, 'state': 'CA', 'country': 'USA', 'district': None, 'rookie_year': 1999, 'active': True, 'norm_epa': 1961.0, 'norm_epa_recent': 1956.0, 'norm_epa_mean': 1896.0, 'norm_epa_max': 2114.0, ... }\n```\n\nRead below for more methods!\n\n## API Reference\n\nVisit https://statbotics.readthedocs.io/en/latest/\n\n## Contribute\n\nIf you are interested in contributing, reach out to Abhijit Gupta (avgupta456@gmail.com)\n\n## Support\n\nIf you are having issues, please let us know. We welcome issues and pull requests.\n\n## License\n\nThe project is licensed under the MIT license.\n",
    'author': 'Abhijit Gupta',
    'author_email': 'avgupta456@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://statbotics.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
