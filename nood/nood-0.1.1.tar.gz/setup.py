# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nood', 'nood.api', 'nood.monitor', 'nood.objects']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.4,<1.11.0',
 'pytest>=7.2.0,<7.3.0',
 'requests>=2.28.1,<2.29.0']

setup_kwargs = {
    'name': 'nood',
    'version': '0.1.1',
    'description': 'All tools you need to interact with nood.',
    'long_description': '# nood \nNOtifications On Demand\n',
    'author': 'timreibe',
    'author_email': 'github@timreibe.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
