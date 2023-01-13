# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinygraphio', 'tinygraphio.proto', 'tinygraphio.scripts']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=4.21.12,<5.0.0']

entry_points = \
{'console_scripts': ['tinygraphio = tinygraphio.scripts.__main__:main']}

setup_kwargs = {
    'name': 'tinygraphio',
    'version': '1.0.0',
    'description': 'The tinygraphio graph data interchange file format',
    'long_description': '# tinygraphio\n\nPython implementation of the tinygraphio graph data interchange file format.\n\n\n## Installation\n\nInstall with `poetry`\n\n    poetry add tinygraphio\n\nInstall with `pip`\n\n    pip install tinygraphio\n\n\n## Usage\n\n- The `Tinygraph` class implements a compressed sparse row graph\n- The `TinygraphioReader` implements reading a graph from a binary file-like object\n- The `TinygraphioWriter` implements writing a graph to a binary file-like object\n\n```python3\nfrom tinygraphio.graph import Tinygraph, Node, Edge\nfrom tinygraphio.reader import TinygraphioReader\nfrom tinygraphio.writer import TinygraphioWriter\n```\n\nWriting\n\n```\ngraph = Tinygraph(offsets=[0, 2, 4, 5], targets=[1, 2, 0, 2, 1])\n\nwith open("berlin.tinygraph", "wb") as f:\n    writer = TinygraphioWriter(f)\n    writer.write(graph)\n```\n\nReading\n\n```\nwith open("berlin.tinygraph", "rb") as f:\n    reader = TinygraphioReader(f)\n    graph = reader.read()\n```\n\nNote: this library implements reading and writing a compressed sparse row graph in a \nThe use case tinygraphio covers is storing large graphs effectively and efficiently and sharing graphs in a portable way.\nWe do not provide a full-blown graph computation toolkit on purpose.\n\n## Development\n\n\n## License\n\nCopyright © 2023 tinygraph\n\nDistributed under the MIT License (MIT).\n',
    'author': 'tinygraph',
    'author_email': 'hello@tinygraph.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8,<=4',
}


setup(**setup_kwargs)
