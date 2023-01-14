# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postr', 'postr.model']

package_data = \
{'': ['*']}

install_requires = \
['coincurve>=18.0.0,<19.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'websocket-client>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'postr',
    'version': '0.1.0a0',
    'description': 'Small python nostr client',
    'long_description': '# postr\nSmall python nostr client\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
