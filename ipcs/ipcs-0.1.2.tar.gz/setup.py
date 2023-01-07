# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipcs']

package_data = \
{'': ['*']}

install_requires = \
['orjson==3.8.3', 'websockets==10.4']

entry_points = \
{'console_scripts': ['ipcs-server = ipcs.__main__:main']}

setup_kwargs = {
    'name': 'ipcs',
    'version': '0.1.2',
    'description': 'Simple IPC server/client',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/ipcs)](https://pypi.org/project/ipcs/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ipcs) ![PyPI - Downloads](https://img.shields.io/pypi/dm/ipcs) ![PyPI - License](https://img.shields.io/pypi/l/ipcs) [![Documentation Status](https://readthedocs.org/projects/ipcs/badge/?version=latest)](https://ipcs.readthedocs.io/en/latest/?badge=latest) [![Buy Me a Coffee](https://img.shields.io/badge/-tasuren-E9EEF3?label=Buy%20Me%20a%20Coffee&logo=buymeacoffee)](https://www.buymeacoffee.com/tasuren)\n# ipcs\nA library for Python for IPC.  \n(Although it is written as IPC, it can also be used for communication with an external server.)\n\n**WARNING** This library is currently in preview.\n\n## Installation\n`$ pip install ipcs`\n\n## Examples\nRun `ipcs-server` and run following code.\n### Client A\n```python\n# Client A\n\nfrom ipcs import Client, Request\n\nclient = Client("a")\n\n@client.route()\nasync def hello(request: Request, word: str):\n    print("Hello, %s!" % word)\n\nclient.run("ws://localhost/", port=8080)\n```\n### Client B\n```python\n# Client B\n\nfrom ipcs import Client\n\nclient = Client("b")\n\n@client.listen()\nasync def on_ready():\n    # Run client a\'s hello str to say greetings to world.\n    await client.request("a", "hello", "World")\n    # or `await client.connections.a.request("hello", "World")`\n\nclient.run("ws://localhost/", port=8080)\n```\n\n## License\nThe license is MIT and details can be found [here](https://github.com/tasuren/ipcs/blob/main/LICENSE).\n\n## Documentation\nDocumentation is avaliable [here](https://ipcs.readthedocs.io/en/latest/).',
    'author': 'Takagi Tasuku',
    'author_email': 'tasuren@outlook.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
