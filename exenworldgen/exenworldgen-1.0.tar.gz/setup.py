# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['exenworldgen']

package_data = \
{'': ['*']}

install_requires = \
['exencolor>=1.0,<2.0']

setup_kwargs = {
    'name': 'exenworldgen',
    'version': '1.0',
    'description': 'Cool world generator',
    'long_description': '# ExenWorldGen\nModule for quicks maze-like 2D world generations <br>\n![https://github.com/Exenifix/worldgen/blob/master.github/res/maze.png](https://github.com/Exenifix/worldgen/blob/master/.github/res/maze.png)\n\n## Installation\nLibrary is available on PyPI:\n```shell\n$ pip install exenworldgen\n```\n\n## Code Usage\n```python\nfrom exenworldgen import World\n\nworld = World((25, 25))\ndata = world.generate()  # data can also be obtained via world.data\nworld.print()  # print the world\n```\n\n## CLI Usage\n```shell\npython -m exenworldgen 25x25      # one world of size 25x25\npython -m exenworldgen 10x10 30   # 30 worlds of size 10x10\n```\n',
    'author': 'Exenifix',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Exenifix/worldgen',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
