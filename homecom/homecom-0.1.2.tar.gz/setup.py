# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['homecom']

package_data = \
{'': ['*']}

install_requires = \
['StrEnum>=0.4.8,<0.5.0',
 'aiohttp>=3.8.1,<4.0.0',
 'lxml>=4.9.1,<5.0.0',
 'pyppeteer>=1.0.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'homecom',
    'version': '0.1.2',
    'description': '',
    'long_description': 'None',
    'author': 'neugartf',
    'author_email': 'fabianneugart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
