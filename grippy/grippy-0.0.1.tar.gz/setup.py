# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grippy']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.51.1,<2.0.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'grippy',
    'version': '0.0.1',
    'description': '',
    'long_description': '# grippy\n\nBuild gRPC services using type annotations.\n',
    'author': 'Erik Hasse',
    'author_email': 'erik.g.hasse@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
