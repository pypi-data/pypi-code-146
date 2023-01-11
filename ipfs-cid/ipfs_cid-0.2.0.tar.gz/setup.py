# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipfs_cid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ipfs-cid',
    'version': '0.2.0',
    'description': 'A library for building IPFS CID v1 compatible content identifiers using fixed encoding parameters.',
    'long_description': '# ipfs-cid\n\n[![pypi](https://img.shields.io/pypi/v/ipfs-cid)](https://pypi.org/project/ipfs-cid/)\n[![test](https://github.com/thunderstore-io/ipfs-cid/workflows/Test/badge.svg)](https://github.com/thunderstore-io/ipfs-cid/actions)\n[![codecov](https://codecov.io/gh/thunderstore-io/ipfs-cid/branch/master/graph/badge.svg?token=6lS3pEHvIw)](https://codecov.io/gh/thunderstore-io/ipfs-cid)\n[![python-versions](https://img.shields.io/pypi/pyversions/ipfs-cid.svg)](https://pypi.org/project/ipfs-cid/)\n\nA library for building IPFS CID v1 compatible content identifiers using fixed\nencoding parameters.\n\n## Usage\n\n### Get CID from bytes\n\nAll at once\n\n```python\nfrom ipfs_cid import cid_sha256_hash\n\ndata = b"Hello world"\nresult = cid_sha256_hash(data)\nassert result == "bafkreide5semuafsnds3ugrvm6fbwuyw2ijpj43gwjdxemstjkfozi37hq"\n```\n\nIn chunks with a generator\n\n```python\nfrom typing import Iterable\nfrom io import BytesIO\nfrom ipfs_cid import cid_sha256_hash_chunked\n\ndef as_chunks(stream: BytesIO, chunk_size: int) -> Iterable[bytes]:\n    while len((chunk := stream.read(chunk_size))) > 0:\n        yield chunk\n\nbuffer = BytesIO(b"Hello world")\nresult = cid_sha256_hash_chunked(as_chunks(buffer, 4))\nassert result == "bafkreide5semuafsnds3ugrvm6fbwuyw2ijpj43gwjdxemstjkfozi37hq"\n```\n\n### Wrap an existing SHA 256 checksum as a CID\n\n```python\nfrom hashlib import sha256\nfrom ipfs_cid import cid_sha256_wrap_digest\n\ndata = b"Hello world"\ndigest = sha256(data).digest()\nresult = cid_sha256_wrap_digest(digest)\nassert result == "bafkreide5semuafsnds3ugrvm6fbwuyw2ijpj43gwjdxemstjkfozi37hq"\n```\n\n## Encoding Format\n\n[The CID spec](https://github.com/multiformats/cid) supports multiple different\nencodings and hashing algorithms.\n\nThe resulting CID string is composed of the following components:\n\n```\n{multibase prefix} + multibase_encoded({cid version} + {content type} + {multihash})\n```\n\nThis library always uses the following encoding parameters:\n\n| multibase | CID version | Content Type | Multihash |\n| --------- | ----------- | ------------ | --------- |\n| base32    | cidv1       | raw          | sha2-256  |\n\nMore details about the formats below:\n\n### Multibase\n\n| encoding | code | description                           |\n| -------- | ---- | ------------------------------------- |\n| base32   | b    | rfc4648 case-insensitive - no padding |\n\n### Multicodec\n\n| name     | code | description                  |\n| -------- | ---- | ---------------------------- |\n| cidv1    | 0x01 | CID v1                       |\n| sha2-256 | 0x12 | sha2-256 with 256 bit digest |\n| raw      | 0x55 | raw binary                   |\n',
    'author': 'Mythic',
    'author_email': 'mythic@thunderstore.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thunderstore-io/ipfs-cid',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
