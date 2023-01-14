# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'build', 'google': 'build/google'}

packages = \
['arg_services', 'google']

package_data = \
{'': ['*']}

install_requires = \
['grpc-stubs>=1.24.11,<2.0.0',
 'grpcio-reflection>=1.51.1,<2.0.0',
 'grpcio>=1.51.1,<2.0.0',
 'protobuf>=4.21.12,<5.0.0']

setup_kwargs = {
    'name': 'arg-services',
    'version': '1.0.5',
    'description': 'gRPC definitions for microservice-based argumentation machines',
    'long_description': '# Argumentation Microservices\n\nThis project contains Protobuf definitions for building complex argumentation machines.\nThe idea is to facilitate a microservice-oriented architecture where individual parts can be swapped out easily.\nAlong with the Protobuf files, the project also contains code for generating libraries for multiple programming languages that are released as packages in their respective registries:\n\n- [Python](https://pypi.org/project/arg-services/)\n- [TypeScript](https://www.npmjs.com/package/arg-services)\n\nDocumentation can be found at the [Buf Schema Registry](https://buf.build/recap/arg-services).\n',
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://recap.uni-trier.de',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
