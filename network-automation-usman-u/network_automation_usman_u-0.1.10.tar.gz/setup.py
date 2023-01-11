# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['net_automation']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'discord-webhook>=0.17.0,<0.18.0',
 'matplotlib>=3.6.2,<4.0.0',
 'netmiko>=4.1.2,<5.0.0',
 'pySMTP>=1.1.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'textfsm==1.1.2']

setup_kwargs = {
    'name': 'network-automation-usman-u',
    'version': '0.1.10',
    'description': 'An ansible-like network automation framework.',
    'long_description': 'None',
    'author': 'Usman',
    'author_email': 'unumer@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
