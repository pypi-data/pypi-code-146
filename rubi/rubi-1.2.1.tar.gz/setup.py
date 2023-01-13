# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rubi',
 'rubi.book',
 'rubi.contracts',
 'rubi.contracts.helper',
 'rubi.data',
 'rubi.data.processing',
 'rubi.data.sources',
 'rubi.data.sources.helper']

package_data = \
{'': ['*'], 'rubi.contracts.helper': ['abis/*']}

install_requires = \
['attributedict>=0.3.0,<0.4.0',
 'eth-abi>=3.0.1,<4.0.0',
 'eth-tester>=0.8.0b1,<0.9.0',
 'eth-utils>=2.1.0,<3.0.0',
 'hexbytes>=0.3.0,<0.4.0',
 'py-evm>=0.6.1a1,<0.7.0',
 'pytest>=7.2.0,<8.0.0',
 'subgrounds>=1.0.3,<2.0.0',
 'web3>=6.0.0b,<7.0.0']

extras_require = \
{':extra == "docs"': ['sphinx>=5.3.0,<6.0.0']}

setup_kwargs = {
    'name': 'rubi',
    'version': '1.2.1',
    'description': 'a python SDK for the Rubicon Protocol',
    'long_description': '# rubi\nrubi is a python SDK for the Rubicon Protocol and has a variety of functionality for interacting with the protocol. documentation related to rubi and its functionality can be found [here](https://rubi.readthedocs.io/en/latest/#). \n\n### Design Goals\nthe underlying goal of the design of rubi is to decrease user friction when interacting with the protocol, and when interacting with the sdk. we want to enable the user\nas much access as possible without requiring any input from the user. for example, by breaking up the contract functionality into read and write classes, we enable the user to\nuse the sdk to read from the protocol without passing in any keys. within the data classes, we aim to provide as much information as possible to the user without requiring any \nadditional input such as api keys. when it is clearly useful, we will add higher level classes that provide additional functionality to the user by requiring additional input. \n\n### SDK Disclaimer\n\nThis codebase is in Alpha and could contain bugs or change significantly between versions. Contributing through Issues or Pull Requests is welcome!\n\n### Protocol Disclaimer\n\nPlease refer to [this](https://docs.rubicon.finance/docs/protocol/rubicon-pools/risks) for information on the risks associated to the Rubicon Protocol.',
    'author': 'denver',
    'author_email': 'denver@rubicon.finance',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
