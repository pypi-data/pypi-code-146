# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kinetic_sdk',
 'kinetic_sdk.generated',
 'kinetic_sdk.generated.client',
 'kinetic_sdk.generated.client.api',
 'kinetic_sdk.generated.client.apis',
 'kinetic_sdk.generated.client.model',
 'kinetic_sdk.generated.client.models',
 'kinetic_sdk.helpers',
 'kinetic_sdk.models']

package_data = \
{'': ['*']}

install_requires = \
['bip-utils>=2.7.0,<3.0.0',
 'pybase64>=1.2.2,<2.0.0',
 'pybip39>=0.1.0,<0.2.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'solana>=0.27.2,<0.28.0',
 'solders==0.9.3']

setup_kwargs = {
    'name': 'kinetic-sdk',
    'version': '1.0.0rc13.post1',
    'description': '',
    'long_description': '# Kinetic Python SDK\n\nKinetic Python SDK is the official [python](https://www.python.org/) SDK for [Kinetic](https://github.com/kin-labs/kinetic) based on the [Kinetic SDK Standard](https://github.com/kin-labs/kinetic/discussions/317).\n\nThis SDK allows developers to rapidly integrate Kin and other SPL tokens in their app.\n\n## Usage\n\nIn order to use this SDK, please head over to the [Kinetic Pyrhon SDK](https://developer.kin.org/docs/developers/python) documentation.\n\n## Version\n\nThis SDK is built to work with `@kinetic/api@v1.0.0-rc.13`. Using it with other versions may lead to issues.\n\n## Contributing\n\nIf you want to contribute to this SDK, please follow the steps below to get it running locally:\n\n#### 1. Install the Poetry CLI on your local machine by visiting the link below:\n[Install Poetry](https://python-poetry.org/docs/#installation)\n\n#### 2. Install the OpenAPI Generator via NPM (for alternative installs visit: https://openapi-generator.tech)\n`$ npm install @openapitools/openapi-generator-cli -g`\n\n#### 3. Fetch the Kinetic Python repo\n`$ git clone https://github.com/kin-labs/kinetic-python-sdk`\n\n#### 4. Change into kinetic-python-sdk working directory\n`$ cd kinetic-python-sdk`\n\n#### 5. Run the tests\n`$ make test`\n\n#### 6. Generate OpenAPI Python client\n`$ make generate`\n\n## Directory labels\n- [generated](https://github.com/kin-labs/kinetic-python-sdk/tree/main/src/kinetic_sdk/generated) Contains all the generated Python client code based on the openapi spec.\n- [helpers](https://github.com/kin-labs/kinetic-python-sdk/tree/main/src/kinetic_sdk/helpers) Contains helper functions that simply calling the createAccount and makeTranfer sdk functions\n- [models](https://github.com/kin-labs/kinetic-python-sdk/tree/main/src/kinetic_sdk/models) Here you can find all reference to classes to-be created and what they override.\n\n## Contributing\nTo start contributing, take a look at the standard as this lays down the base for all clients.\nThis standard is subject to change so always review this before committing any meaningful work.\nYou can visit the standard [here](https://github.com/kin-labs/kinetic/discussions/317)\n\n## Troubleshooting\n\nIf you have issues with [coincurve](https://github.com/ofek/coincurve) dependency in Apple Silicon M1 run this:\n```\nxcode-select --install\nbrew install autoconf automake libffi libtool pkg-config python\n```\n',
    'author': 'Kin Foundation',
    'author_email': 'dev@kin.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kin-labs/kinetic-python-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
