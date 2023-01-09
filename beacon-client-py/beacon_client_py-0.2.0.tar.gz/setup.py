# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beacon_client', 'beacon_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['bitstring>=3.1.9,<4.0.0',
 'dacite>=1.6.0,<2.0.0',
 'multiaddr>=0.0.9,<0.0.10',
 'requests>=2.28.1,<3.0.0',
 'sseclient-py>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'beacon-client-py',
    'version': '0.2.0',
    'description': 'A Python Client for interacting with the Ethereum Beacon Chain API',
    'long_description': '# beacon-client-py\nA Python client for interacting with the Ethereum Beacon Chain API\n\n[Beacon Chain API Reference](https://ethereum.github.io/beacon-APIs)\n\n[Ethereum Consensus Specification](https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md)\n\n[Ethereum Consensus Specification Annotated](https://eth2book.info/altair/part3)\n\nThis implementation also leans on types implemented [here](https://github.com/ralexstokes/beacon-api-client)\n\n## Installation\n```bash\npip install beacon-client-py\n```\n\n## Simple Example\n\n```python\nfrom beacon_client.api import BeaconChainAPI\n\nclient = BeaconChainAPI("http://localhost:5052")\nclient.get_headers_from_block_id(block_id="head")\n```\n\n## Streaming Example\n```python\nfor event in client.stream_events(head=True, block=True, attestation=True):\n    match event.event:\n        case "head":\n            print(client.parse_head(event.data))\n        case "block":\n            print(client.parse_block(event.data))\n        case "attestation":\n            print(client.parse_attestation(event.data))\n        case other:\n            pass\n```\n\n## Development\n\nRun the docs locally \n\n```bash\npoetry run mkdocs serve\n```\n\nFormatter\n```bash\npoetry run black .\n```\n\nTests\n```bash\npoetry run pytest -vv\n```\n\nlinter\n```bash\npoetry run flake8\n```\n\n_note_: requires poetry version 1.2.x or higher\n',
    'author': 'Benedict Brady',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
