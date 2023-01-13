# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zarr_checksum']

package_data = \
{'': ['*']}

install_requires = \
['boto3-stubs[s3]>=1.26.29,<2.0.0',
 'boto3>=1.26.29,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'zarr>=2.13.3,<3.0.0']

entry_points = \
{'console_scripts': ['zarrsum = zarr_checksum.cli:cli']}

setup_kwargs = {
    'name': 'zarr-checksum',
    'version': '0.1.1',
    'description': 'Checksum support for zarrs stored in various backends',
    'long_description': 'None',
    'author': 'Kitware, Inc.',
    'author_email': 'kitware@kitware.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.10,<4.0.0',
}


setup(**setup_kwargs)
