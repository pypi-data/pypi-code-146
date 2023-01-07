# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_mongodb_z', 'tap_mongodb_z.tests']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.8.2,<4.0.0',
 'pymongo[srv]>=4.3.3,<5.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['tap-mongodb = tap_mongodb_z.tap:TapMongoDB.cli']}

setup_kwargs = {
    'name': 'tap-mongodb-z',
    'version': '0.1.17',
    'description': '`tap-mongodb` is a Singer tap for MongoDB, built with the Meltano SDK for Singer Taps.',
    'long_description': 'None',
    'author': 'Alex Butler',
    'author_email': 'butler.alex2010@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
