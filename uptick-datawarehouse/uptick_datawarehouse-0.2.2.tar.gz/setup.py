# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app',
 'uptick_datawarehouse',
 'uptick_datawarehouse.subscriptionmanager',
 'uptick_datawarehouse.subscriptionmanager.migrations',
 'uptick_datawarehouse.superblocks',
 'uptick_datawarehouse.superblocks.migrations',
 'uptick_datawarehouse.vitally',
 'uptick_datawarehouse.vitally.migrations',
 'uptick_datawarehouse.workforce',
 'uptick_datawarehouse.workforce.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<5.0.0']

setup_kwargs = {
    'name': 'uptick-datawarehouse',
    'version': '0.2.2',
    'description': '',
    'long_description': 'Datawarehousing models.\n',
    'author': 'william chu',
    'author_email': 'william.chu@uptickhq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
