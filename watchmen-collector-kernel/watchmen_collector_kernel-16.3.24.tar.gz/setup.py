# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['watchmen_collector_kernel',
 'watchmen_collector_kernel.common',
 'watchmen_collector_kernel.connector',
 'watchmen_collector_kernel.lock',
 'watchmen_collector_kernel.model']

package_data = \
{'': ['*']}

install_requires = \
['watchmen-pipeline-kernel==16.3.24']

extras_require = \
{'mongodb': ['watchmen-storage-mongodb==16.3.24'],
 'mssql': ['watchmen-storage-mssql==16.3.24'],
 'mysql': ['watchmen-storage-mysql==16.3.24'],
 'oracle': ['watchmen-storage-oracle==16.3.24'],
 'oss': ['watchmen-storage-oss==16.3.24'],
 'postgresql': ['watchmen-storage-postgresql==16.3.24'],
 's3': ['watchmen-storage-s3==16.3.24']}

setup_kwargs = {
    'name': 'watchmen-collector-kernel',
    'version': '16.3.24',
    'description': '',
    'long_description': 'None',
    'author': 'botlikes',
    'author_email': '75356972+botlikes456@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
