# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rivian']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0.0', 'yarl>=1.6.0']

setup_kwargs = {
    'name': 'rivian-python-client',
    'version': '0.1.8',
    'description': 'Rivian API Client (Unofficial)',
    'long_description': '# Python: Rivian API Client\n\nCurrently a Work In Progress\n\n## Dependencies\n\n[Poetry](https://python-poetry.org/docs/)\n\n```\ncurl -sSL https://install.python-poetry.org | python3 -\n```\n\n## Setup\n\nInstall project dependencies into the poetry virtual environment.\n\n```\npoetry install\n```\n\n## Run Tests\n\n```\npoetry run pytest\n```\n',
    'author': 'Brian Retterer',
    'author_email': 'bretterer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
