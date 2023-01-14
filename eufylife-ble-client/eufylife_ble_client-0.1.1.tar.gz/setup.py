# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eufylife_ble_client']

package_data = \
{'': ['*']}

install_requires = \
['bleak-retry-connector>=2.3.0', 'bleak>=0.19.0']

setup_kwargs = {
    'name': 'eufylife-ble-client',
    'version': '0.1.1',
    'description': 'A library to communicate with EufyLife Bluetooth devices.',
    'long_description': '# EufyLife BLE Client\n\nThis is a library for parsing data from Eufy smart scales that use the EufyLife mobile app.\n\n# Supported Models\n\n| Model | Name               |\n| ----- | ------------------ |\n| T9140 | Smart Scale        |\n| T9146 | Smart Scale C1     |\n| T9147 | Smart Scale P1     |\n| T9148 | Smart Scale P2     |\n| T9149 | Smart Scale P2 Pro |\n\n## Installation\n\nInstall this via pip:\n\n`pip install eufylife-ble-client`\n',
    'author': 'Brandon Rothweiler',
    'author_email': 'brandonrothweiler@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
