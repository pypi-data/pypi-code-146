# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['continual',
 'continual.python',
 'continual.python.blob',
 'continual.python.cli',
 'continual.python.cli.tests',
 'continual.python.sdk',
 'continual.python.utils',
 'continual.rpc',
 'continual.rpc.graphql',
 'continual.rpc.management',
 'continual.rpc.management.v1',
 'continual.rpc.rpc',
 'continual.services']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.29',
 'click==8.0.4',
 'gitpython>=3.1.7',
 'google-cloud-storage>=1.33.0',
 'grpcio-tools>=1.43.0,<=1.48.1',
 'grpcio>=1.27.1',
 'grpcio_status>=1.31.0',
 'halo>=0.0.30',
 'humanize>=2.5.0',
 'numpy>=1.21.6',
 'omegaconf>=2.2.3',
 'pandas>=1.0.1',
 'protobuf==3.20.3',
 'pyyaml>=5.4',
 'requests>=2.28.1',
 'rich>=9.13.0',
 'scikit_learn>=1.1.2',
 'shortuuid>=1.0.9',
 'toml>=0.10.2',
 'typer==0.4.0']

entry_points = \
{'console_scripts': ['continual = continual.python.cli.cli:cli']}

setup_kwargs = {
    'name': 'continual',
    'version': '2.0.0a19',
    'description': 'Lifecyle Management for AI',
    'long_description': '# Python CLI and SDK for Continual\n\nContinual is lifecycle management for AI. Learn more at https://continual.ai.\n\n## Getting Started\n\nTo install the Continual AI CLI and SDK run:\n\n```\npip3 install continual\n```\n',
    'author': 'Continual',
    'author_email': 'support@continual.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
