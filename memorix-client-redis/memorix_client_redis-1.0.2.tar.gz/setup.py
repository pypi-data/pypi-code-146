# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memorix_client_redis',
 'memorix_client_redis.features',
 'memorix_client_redis.features.api',
 'memorix_client_redis.features.api.cache',
 'memorix_client_redis.features.api.pubsub',
 'memorix_client_redis.features.api.task']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'redis>=4.3.4,<5.0.0']

entry_points = \
{'console_scripts': ['start = memorix_client_redis.start:start']}

setup_kwargs = {
    'name': 'memorix-client-redis',
    'version': '1.0.2',
    'description': '',
    'long_description': 'None',
    'author': 'Yuval Saraf',
    'author_email': 'unimonkiez@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
