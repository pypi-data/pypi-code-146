# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ario3s_aiva']

package_data = \
{'': ['*']}

install_requires = \
['tomli>=2.0.1,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['aiva = ario3s_aiva.main:app']}

setup_kwargs = {
    'name': 'ario3s-aiva',
    'version': '0.2.0',
    'description': '',
    'long_description': '# aiva cli tool\n\n<p>a tool to connect to server using ssh</p>\n<p>it creates a SOCKS proxy on provided port default to 4321</p>',
    'author': 'ario',
    'author_email': 'cybera.3s@gmail.com',
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
