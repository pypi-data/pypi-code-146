# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abi_ds_utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.21.14,<2.0.0',
 'hurry.filesize>=0.9,<0.10',
 'psutil>=5.9.3,<6.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'pyspark==3.1.1']

setup_kwargs = {
    'name': 'abi-ds-utils',
    'version': '0.1.9',
    'description': 'Utility modules for working with spark, containers, aws and many more.',
    'long_description': None,
    'author': 'Martin Matousek',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.8',
}


setup(**setup_kwargs)
