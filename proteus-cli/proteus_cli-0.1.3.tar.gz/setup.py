# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli',
 'cli.api',
 'cli.buckets',
 'cli.datasets',
 'cli.datasets.preprocessor',
 'cli.datasets.preprocessor.config',
 'cli.datasets.sources',
 'cli.debugger',
 'cli.jobs',
 'cli.simulations']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity>=1.12.0,<2.0.0',
 'azure-storage-blob>=12.8.1,<13.0.0',
 'boto3>=1.17.79,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'cryptography>=3.3.2,<4.0.0',
 'jwt>=1.2.0,<2.0.0',
 'markupsafe==2.0.1',
 'proteus-preprocessing>=0.1.9,<0.2.0',
 'proteus-runtime>=0.2,<0.3',
 'pycryptodome>=3.10.1,<4.0.0',
 'readchar>=3.0.4,<4.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.61.0,<5.0.0']

entry_points = \
{'console_scripts': ['proteus-do = cli.cli:main']}

setup_kwargs = {
    'name': 'proteus-cli',
    'version': '0.1.3',
    'description': '',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
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
