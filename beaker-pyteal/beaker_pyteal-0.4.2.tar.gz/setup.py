# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beaker',
 'beaker.client',
 'beaker.lib',
 'beaker.lib.inline',
 'beaker.lib.iter',
 'beaker.lib.math',
 'beaker.lib.storage',
 'beaker.lib.strings',
 'beaker.sandbox',
 'beaker.testing']

package_data = \
{'': ['*']}

install_requires = \
['py-algorand-sdk>=1.16.1', 'pyteal>=0.20.1,<0.21.0']

setup_kwargs = {
    'name': 'beaker-pyteal',
    'version': '0.4.2',
    'description': 'A Framework for building PyTeal Applications',
    'long_description': 'Beaker\n------\n<img align="left" src="beaker.png" margin="10px" >\n\nBeaker is a smart contract development framework for [PyTeal](https://github.com/algorand/pyteal).\n\n\nWith Beaker, we build a class that represents our entire application including state and routing.\n\n\n&nbsp;\n\n&nbsp;\n\n\n\n## WARNING\n\n :warning: *Mostly Untested - Expect Breaking Changes*  :warning:\n\n **Please file issues or prs and get any contracts audited**\n\n## Hello, Beaker\n\n\n```py\nfrom pyteal import *\nfrom beaker import *\n\n# Create a class, subclassing Application from beaker\nclass HelloBeaker(Application):\n    # Add an external method with ABI method signature `hello(string)string`\n    @external\n    def hello(self, name: abi.String, *, output: abi.String):\n        # Set output to the result of `Hello, `+name\n        return output.set(Concat(Bytes("Hello, "), name.get()))\n\n\n# Create an Application client\napp_client = client.ApplicationClient(\n    # Get sandbox algod client\n    client=sandbox.get_algod_client(),\n    # Instantiate app with the program version (default is MAX_TEAL_VERSION)\n    app=HelloBeaker(version=6),\n    # Get acct from sandbox and pass the signer\n    signer=sandbox.get_accounts().pop().signer,\n)\n\n# Deploy the app on-chain\napp_id, app_addr, txid = app_client.create()\nprint(\n    f"""Deployed app in txid {txid}\n    App ID: {app_id} \n    Address: {app_addr} \n"""\n)\n\n# Call the `hello` method\nresult = app_client.call(HelloBeaker.hello, name="Beaker")\nprint(result.return_value)  # "Hello, Beaker"\n\n```\n\n## Install\n\n    Beaker currently requires Python >= 3.10\n\nYou can install from pip:\n\n`pip install beaker-pyteal`\n\nOr from github directly (no promises on stability): \n\n`pip install git+https://github.com/algorand-devrel/beaker`\n\n\n# Dev Environment \n\nRequires a local [sandbox](https://github.com/algorand/sandbox) with latest stable tag minimum.\n\n```sh\n$ git clone git@github.com:algorand/sandbox.git\n$ cd sandbox\n$ sandbox up source\n```\n\n## Front End \n\nSee [Beaker TS](https://github.com/algorand-devrel/beaker-ts) to generate a front end client for a Beaker App.\n\n## Testing\n\nYou can run tests from the root of the project using `pytest`\n\n## Use\n\n[Examples](/examples/)\n\n[Docs](https://beaker.algo.xyz)\n\n*Please feel free to file issues/prs*',
    'author': 'Ben Guidarelli',
    'author_email': 'ben@algorand.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://beaker.algo.xyz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
