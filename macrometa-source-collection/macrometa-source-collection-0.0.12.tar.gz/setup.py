# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_source_collection']

package_data = \
{'': ['*']}

install_requires = \
['c8connector==0.0.11',
 'chardet==4.0.0',
 'idna==2.10',
 'numpy==1.21.6',
 'pandas==1.3.5',
 'pipelinewise-singer-python==1.2.0',
 'pulsar-client==2.10.1',
 'pyC8==0.17.3',
 'requests==2.25.1',
 'websocket-client==0.57.0']

entry_points = \
{'console_scripts': ['macrometa-source-collection = '
                     'macrometa_source_collection:main']}

setup_kwargs = {
    'name': 'macrometa-source-collection',
    'version': '0.0.12',
    'description': 'Pipelinewise tap for reading from GDN Collections',
    'long_description': 'None',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
