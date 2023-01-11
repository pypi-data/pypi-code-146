# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipfs_cid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ipfs-cid',
    'version': '0.1.1',
    'description': 'Library for generating IPFS v1 CIDs',
    'long_description': '# ipfs-cid\n\n[![pypi](https://img.shields.io/pypi/v/ipfs-cid)](https://pypi.org/project/ipfs-cid/)\n[![test](https://github.com/thunderstore-io/ipfs-cid/workflows/Test/badge.svg)](https://github.com/thunderstore-io/ipfs-cid/actions)\n[![codecov](https://codecov.io/gh/thunderstore-io/ipfs-cid/branch/master/graph/badge.svg?token=6lS3pEHvIw)](https://codecov.io/gh/thunderstore-io/ipfs-cid)\n\nA library for building IPFS CID v1 compatible content identifiers using fixed\nencoding parameters.\n\n## Usage\n\n```python\nfrom ipfs_cid import encode_cid_v1\n\ndata = b"Hello world"\nresult = encode_cid_v1(data)\n# result is now "bafkreide5semuafsnds3ugrvm6fbwuyw2ijpj43gwjdxemstjkfozi37hq"\n```\n\n## Encoding Format\n\n[The CID spec](https://github.com/multiformats/cid) supports multiple different\nencodings and hashing algorithms.\n\nThe resulting CID string is composed of the following components:\n\n```\n{multibase prefix} + multibase_encoded({cid version} + {content type} + {multihash})\n```\n\nThis library always uses the following encoding parameters:\n\n| multibase | CID version | Content Type | Multihash |\n| --------- | ----------- | ------------ | --------- |\n| base32    | cidv1       | raw          | sha2-256  |\n\nMore details about the formats below:\n\n### Multibase\n\n| encoding | code | description                           |\n| -------- | ---- | ------------------------------------- |\n| base32   | b    | rfc4648 case-insensitive - no padding |\n\n### Multicodec\n\n| name     | code | description                  |\n| -------- | ---- | ---------------------------- |\n| cidv1    | 0x01 | CID v1                       |\n| sha2-256 | 0x12 | sha2-256 with 256 bit digest |\n| raw      | 0x55 | raw binary                   |\n',
    'author': 'Mythic',
    'author_email': 'mythic@thunderstore.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
