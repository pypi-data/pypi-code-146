# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hcube',
 'hcube.api',
 'hcube.api.models',
 'hcube.backends',
 'hcube.backends.clickhouse']

package_data = \
{'': ['*']}

install_requires = \
['clickhouse-driver>=0.2.4,<0.3.0',
 'clickhouse-pool>=0.5.3,<0.6.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'python-decouple>=3.5,<4.0']

setup_kwargs = {
    'name': 'hcube',
    'version': '0.9.1',
    'description': 'HCube is a simple ORM for working with hyper-cube OLAP data stored in various backends.',
    'long_description': None,
    'author': 'Beda Kosata',
    'author_email': 'beda@bigdigdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.8,<4.0.0',
}


setup(**setup_kwargs)
