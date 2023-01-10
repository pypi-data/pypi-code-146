# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synnax',
 'synnax.channel',
 'synnax.cli',
 'synnax.cli.console',
 'synnax.cli.flow',
 'synnax.config',
 'synnax.framer',
 'synnax.ingest',
 'synnax.io',
 'synnax.user']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.5.0,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'keyring>=23.9.3,<24.0.0',
 'mypy>=0.971,<0.972',
 'pandas>=1.4.3,<2.0.0',
 'pick>=2.0.2,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'synnax-freighter>=0.2.6,<0.3.0',
 'websockets>=10.3,<11.0']

entry_points = \
{'console_scripts': ['synnax = synnax.cli.synnax:synnax']}

setup_kwargs = {
    'name': 'synnax',
    'version': '0.2.10',
    'description': 'Synnax Client Library',
    'long_description': 'None',
    'author': 'emiliano bonilla',
    'author_email': 'emilbon99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://synnaxlabs.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
