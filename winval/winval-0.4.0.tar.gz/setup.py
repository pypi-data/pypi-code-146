# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['winval', 'winval.antlr']

package_data = \
{'': ['*'], 'winval': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['antlr4-python3-runtime==4.10',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'winval',
    'version': '0.4.0',
    'description': 'Workflow inputs validation',
    'long_description': None,
    'author': 'doron',
    'author_email': 'doron.shemtov@ultimagen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
