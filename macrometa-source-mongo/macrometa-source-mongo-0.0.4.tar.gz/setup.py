# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'macrometa_source_mongo'}

packages = \
['macrometa_source_mongo',
 'macrometa_source_mongo.sync_strategies',
 'sync_strategies']

package_data = \
{'': ['*']}

install_requires = \
['c8connector==0.0.10',
 'dnspython>=2.1.0,<2.2.0',
 'pipelinewise-singer-python==1.2.0',
 'pymongo>=3.12.0,<3.13.0',
 'terminaltables>=3.1.0,<3.2.0',
 'tzlocal>=2.1.0,<2.2.0']

entry_points = \
{'console_scripts': ['macrometa-source-mongo = macrometa_source_mongo:main']}

setup_kwargs = {
    'name': 'macrometa-source-mongo',
    'version': '0.0.4',
    'description': 'Macrometa Source for extracting data from MongoDB',
    'long_description': 'None',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
