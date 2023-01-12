# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paloma_sdk',
 'paloma_sdk.client',
 'paloma_sdk.client.lcd',
 'paloma_sdk.client.lcd.api',
 'paloma_sdk.core',
 'paloma_sdk.core.auth',
 'paloma_sdk.core.auth.data',
 'paloma_sdk.core.auth.msgs',
 'paloma_sdk.core.authz',
 'paloma_sdk.core.bank',
 'paloma_sdk.core.crisis',
 'paloma_sdk.core.distribution',
 'paloma_sdk.core.feegrant',
 'paloma_sdk.core.gov',
 'paloma_sdk.core.ibc',
 'paloma_sdk.core.ibc.data',
 'paloma_sdk.core.ibc.msgs',
 'paloma_sdk.core.ibc.proposals',
 'paloma_sdk.core.ibc_transfer',
 'paloma_sdk.core.params',
 'paloma_sdk.core.slashing',
 'paloma_sdk.core.staking',
 'paloma_sdk.core.staking.data',
 'paloma_sdk.core.upgrade',
 'paloma_sdk.core.upgrade.data',
 'paloma_sdk.core.wasm',
 'paloma_sdk.key',
 'paloma_sdk.util']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'attrs>=21.4.0,<22.0.0',
 'bech32>=1.2.0,<2.0.0',
 'betterproto==2.0.0b4',
 'bip32utils>=0.3.post4,<0.4',
 'boltons>=21.0.0,<22.0.0',
 'ecdsa>=0.17.0,<0.18.0',
 'furl>=2.1.3,<3.0.0',
 'mnemonic>=0.19,<0.20',
 'nest-asyncio>=1.5.4,<2.0.0',
 'protobuf>=3.19.1,<4.0.0',
 'terra-proto==2.1.0',
 'wrapt>=1.13.3,<2.0.0']

setup_kwargs = {
    'name': 'paloma-sdk',
    'version': '3.0.14',
    'description': 'The Python SDK for Paloma',
    'long_description': '<br/>\n<br/>\n\n<h1>The Python SDK for Paloma</h1>\n<br/>\n\n<p><sub>(Unfamiliar with Paloma?  <a href="https://docs.palomachain.com">Check out the Paloma Docs</a>)</sub></p>\n\n  \n\n<p>\n  <a href="https://docs.palomachain.com"><strong>Explore the Docs »</strong></a>\n  ·\n  <a href="https://github.com/palomachain/paloma.py">GitHub Repository</a>\n</p></div>\n\nThe Paloma Software Development Kit (SDK) in Python is a simple library toolkit for building software that can interact with the Paloma blockchain and provides simple abstractions over core data structures, serialization, key management, and API request generation.\n\n## Features\n\n- Written in Python with extensive support libraries\n- Versatile support for key management solutions\n- Exposes the Paloma API through LCDClient\n\n<br/>\n\n# Table of Contents\n\n- [API Reference](#api-reference)\n- [Getting Started](#getting-started)\n  - [Requirements](#requirements)\n  - [Installation](#installation)\n  - [Dependencies](#dependencies)\n  - [Tests](#tests)\n  - [Code Quality](#code-quality)\n- [Usage Examples](#usage-examples)\n  - [Getting Blockchain Information](#getting-blockchain-information)\n    - [Async Usage](#async-usage)\n  - [Building and Signing Transactions](#building-and-signing-transactions)\n    - [Example Using a Wallet](#example-using-a-wallet-recommended)\n- [Contributing](#contributing)\n  - [Reporting an Issue](#reporting-an-issue)\n  - [Requesting a Feature](#requesting-a-feature)\n  - [Contributing Code](#contributing-code)\n  - [Documentation Contributions](#documentation-contributions)\n- [License](#license)\n\n<br/>\n\n# API Reference\n\nAn intricate reference to the APIs on the Paloma SDK can be found <a href="https://docs.palomachain.com">here</a>.\n\n<br/>\n\n# Getting Started\n\nA walk-through of the steps to get started with the Paloma SDK alongside a few use case examples are provided below. git ad\n\n## Requirements\n\nPaloma SDK requires <a href="https://www.python.org/downloads/">Python v3.7+</a>.\n\n## Installation\n\n<sub>**NOTE:** _All code starting with a `$` is meant to run on your terminal (a bash prompt). All code starting with a `>>>` is meant to run in a python interpreter, like <a href="https://pypi.org/project/ipython/">ipython</a>._</sub>\n\nPaloma SDK can be installed (preferably in a `virtual environment` from PyPI using `pip`) as follows:\n  \n```\n$ pip install -U paloma_sdk\n```\n\n<sub>_You might have `pip3` installed instead of `pip`; proceed according to your own setup._<sub>\n  \n❗ If you want to communicate with Paloma Classic, use paloma-sdk==2.x\n  \n## Dependencies\n\nPaloma SDK uses <a href="https://python-poetry.org/">Poetry</a> to manage dependencies. To get set up with all the required dependencies, run:\n\n```\n$ pip install poetry\n$ poetry install\n```\n\n## Tests\n\nPaloma SDK provides extensive tests for data classes and functions. To run them, after the steps in [Dependencies](#dependencies):\n\n```\n$ make test\n```\n\n## Code Quality\n\nPaloma SDK uses <a href="https://black.readthedocs.io/en/stable/">Black</a>, <a href="https://isort.readthedocs.io/en/latest/">isort</a>, and <a href="https://mypy.readthedocs.io/en/stable/index.html">Mypy</a> for checking code quality and maintaining style. To reformat, after the steps in [Dependencies](#dependencies):\n\n```\n$ make qa && make format\n```\n\n<br/>\n\n# Usage Examples\n\nPaloma SDK can help you read block data, sign and send transactions, deploy and interact with contracts, and many more.\nThe following examples are provided to help you get started. Use cases and functionalities of the Paloma SDK are not limited to the following examples and can be found in full <a href="https://paloma-money.github.io/paloma.py/index.html">here</a>.\n\nIn order to interact with the Paloma blockchain, you\'ll need a connection to a Paloma node. This can be done through setting up an LCDClient (The LCDClient is an object representing an HTTP connection to a Paloma LCD node.):\n\n```\n>>> from paloma_sdk.client.lcd import LCDClient\n>>> paloma = LCDClient(chain_id="<CHECK DOCS FOR LATEST TESTNET>", url="https://testnet.palomaswap.com")\n```\n\n## Getting Blockchain Information\n\nOnce properly configured, the `LCDClient` instance will allow you to interact with the Paloma blockchain. Try getting the latest block height:\n\n```\n>>> paloma.tendermint.block_info()[\'block\'][\'header\'][\'height\']\n```\n\n`\'1687543\'`\n\n### Async Usage\n\nIf you want to make asynchronous, non-blocking LCD requests, you can use AsyncLCDClient. The interface is similar to LCDClient, except the module and wallet API functions must be awaited.\n\n<pre><code>\n>>> import asyncio \n>>> from paloma_sdk.client.lcd import AsyncLCDClient\n\n>>> async def main():\n      <strong>paloma = AsyncLCDClient("https://testnet.palomaswap.com", "<CHECK DOCS FOR LATEST TESTNET>")</strong>\n      total_supply = await paloma.bank.total()\n      print(total_supply)\n      <strong>await paloma.session.close # you must close the session</strong>\n\n>>> asyncio.get_event_loop().run_until_complete(main())\n</code></pre>\n\n## Building and Signing Transactions\n\nIf you wish to perform a state-changing operation on the Paloma blockchain such as sending tokens, swapping assets, withdrawing rewards, or even invoking functions on smart contracts, you must create a **transaction** and broadcast it to the network.\nPaloma SDK provides functions that help create StdTx objects.\n\n### Example Using a Wallet (_recommended_)\n\nA `Wallet` allows you to create and sign a transaction in a single step by automatically fetching the latest information from the blockchain (chain ID, account number, sequence).\n\nUse `LCDClient.wallet()` to create a Wallet from any Key instance. The Key provided should correspond to the account you intend to sign the transaction with.\n  \n<sub>**NOTE:** *If you are using MacOS and got an exception \'bad key length\' from MnemonicKey, please check your python implementation. if `python3 -c "import ssl; print(ssl.OPENSSL_VERSION)"` returns LibreSSL 2.8.3, you need to reinstall python via pyenv or homebrew.*</sub>\n\n```\n>>> from paloma_sdk.client.lcd import LCDClient\n>>> from paloma_sdk.key.mnemonic import MnemonicKey\n\n>>> mk = MnemonicKey(mnemonic=MNEMONIC)\n>>> paloma = LCDClient("https://testnet.palomaswap.com", "<CHECK DOCS FOR LATEST TESTNET>")\n>>> wallet = paloma.wallet(mk)\n```\n\nOnce you have your Wallet, you can simply create a StdTx using `Wallet.create_and_sign_tx`.\n\n```\n>>> from paloma_sdk.core.fee import Fee\n>>> from paloma_sdk.core.bank import MsgSend\n>>> from paloma_sdk.client.lcd.api.tx import CreateTxOptions\n\n>>> tx = wallet.create_and_sign_tx(CreateTxOptions(\n        msgs=[MsgSend(\n            wallet.key.acc_address,\n            RECIPIENT,\n            "1000000ugrain"    # send 1 grain\n        )],\n        memo="test transaction!",\n        fee=Fee(200000, "120000ugrain")\n    ))\n```\n\nYou should now be able to broadcast your transaction to the network.\n\n```\n>>> result = paloma.tx.broadcast(tx)\n>>> print(result)\n```\n\n<br/>\n\n# Contributing\n\nCommunity contribution, whether it\'s a new feature, correction, bug report, additional documentation, or any other feedback is always welcome. Please read through this section to ensure that your contribution is in the most suitable format for us to effectively process.\n\n<br/>\n\n## Reporting an Issue\n\nFirst things first: **Do NOT report security vulnerabilities in public issues!** Please disclose responsibly by submitting your findings to the [Paloma Bugcrowd submission form](https://www.paloma.money/bugcrowd). The issue will be assessed as soon as possible.\nIf you encounter a different issue with the Python SDK, check first to see if there is an existing issue on the <a href="https://github.com/paloma-money/paloma-sdk-python/issues">Issues</a> page, or if there is a pull request on the <a href="https://github.com/paloma-money/paloma-sdk-python/pulls">Pull requests</a> page. Be sure to check both the Open and Closed tabs addressing the issue.\n\nIf there isn\'t a discussion on the topic there, you can file an issue. The ideal report includes:\n\n- A description of the problem / suggestion.\n- How to recreate the bug.\n- If relevant, including the versions of your:\n  - Python interpreter\n  - Paloma SDK\n  - Optionally of the other dependencies involved\n- If possible, create a pull request with a (failing) test case demonstrating what\'s wrong. This makes the process for fixing bugs quicker & gets issues resolved sooner.\n  </br>\n\n## Requesting a Feature\n\nIf you wish to request the addition of a feature, please first check out the <a href="https://github.com/paloma-money/paloma-sdk-python/issues">Issues</a> page and the <a href="https://github.com/paloma-money/paloma-sdk-python/pulls">Pull requests</a> page (both Open and Closed tabs). If you decide to continue with the request, think of the merits of the feature to convince the project\'s developers, and provide as much detail and context as possible in the form of filing an issue on the <a href="https://github.com/paloma-money/paloma-sdk-python/issues">Issues</a> page.\n\n<br/>\n\n## Contributing Code\n\nIf you wish to contribute to the repository in the form of patches, improvements, new features, etc., first scale the contribution. If it is a major development, like implementing a feature, it is recommended that you consult with the developers of the project before starting the development to avoid duplicating efforts. Once confirmed, you are welcome to submit your pull request.\n</br>\n\n### For new contributors, here is a quick guide:\n\n1. Fork the repository.\n2. Build the project using the [Dependencies](#dependencies) and [Tests](#tests) steps.\n3. Install a <a href="https://virtualenv.pypa.io/en/latest/index.html">virtualenv</a>.\n4. Develop your code and test the changes using the [Tests](#tests) and [Code Quality](#code-quality) steps.\n5. Commit your changes (ideally follow the <a href="https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit">Angular commit message guidelines</a>).\n6. Push your fork and submit a pull request to the repository\'s `main` branch to propose your code.\n\nA good pull request:\n\n- Is clear and concise.\n- Works across all supported versions of Python. (3.7+)\n- Follows the existing style of the code base (<a href="https://pypi.org/project/flake8/">`Flake8`</a>).\n- Has comments included as needed.\n- Includes a test case that demonstrates the previous flaw that now passes with the included patch, or demonstrates the newly added feature.\n- Must include documentation for changing or adding any public APIs.\n- Must be appropriately licensed (MIT License).\n  </br>\n\n## Documentation Contributions\n\nDocumentation improvements are always welcome. The documentation files live in the [docs](./docs) directory of the repository and are written in <a href="https://docutils.sourceforge.io/rst.html">reStructuredText</a> and use <a href="https://www.sphinx-doc.org/en/master/">Sphinx</a> to create the full suite of documentation.\n</br>\nWhen contributing documentation, please do your best to follow the style of the documentation files. This means a soft limit of 88 characters wide in your text files and a semi-formal, yet friendly and approachable, prose style. You can propose your improvements by submitting a pull request as explained above.\n\n### Need more information on how to contribute?\n\nYou can give this <a href="https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution">guide</a> read for more insight.\n\n<br/>\n\n# License\n\nThis software is licensed under the MIT license. See [LICENSE](./LICENSE) for full disclosure.\n\n© 2021 Paloma\n\n<hr/>\n',
    'author': 'Paloma',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/palomachain/paloma.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
