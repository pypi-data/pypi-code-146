# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fsai_grpc_api',
 'fsai_grpc_api.protos',
 'fsai_grpc_api.protos.protoc_gen_validate']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.10.4,<0.11.0',
 'google>=3.0.0,<4.0.0',
 'grpcio-tools>=1.47.0,<2.0.0',
 'grpcio>=1.47.0,<2.0.0',
 'jsonlines>=3.0.0,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'marshmallow>=3.17.1,<4.0.0',
 'protobuf>=4.21.11,<5.0.0',
 'pydash>=5.1.0,<6.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'fsai-grpc-api',
    'version': '0.0.104',
    'description': 'Auto-generate library for use with GRPC API.',
    'long_description': '# Development\n\nTo re-generate the proto library, run `make proto-gen`\n',
    'author': 'Michael Mohamed',
    'author_email': 'michael@foundationstack.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fsai-dev/fsai-cli-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
