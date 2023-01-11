# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgfp_nfl']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'onetoonemap>=1.0.0,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'tgfp-nfl',
    'version': '5.2.0',
    'description': 'Python extraction of NFL scores schedule data from abstracted data source',
    'long_description': 'None',
    'author': 'John Sturgeon',
    'author_email': 'john.sturgeon@me.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
