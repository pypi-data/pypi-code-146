# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mppsolar',
 'mppsolar.devices',
 'mppsolar.inout',
 'mppsolar.libs',
 'mppsolar.outputs',
 'mppsolar.ports',
 'mppsolar.protocols']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML', 'bleak', 'paho-mqtt', 'pyserial>3']

entry_points = \
{'console_scripts': ['jkbms = mppsolar:main',
                     'mpp-solar = mppsolar:main',
                     'powermon = mppsolar.powermon:main']}

setup_kwargs = {
    'name': 'mppsolar',
    'version': '0.15.1',
    'description': 'Package to communicate with Solar inverters and BMSs',
    'long_description': None,
    'author': 'John Blance',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
