# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uva', 'uva.commands', 'uva.localdb']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'html5lib>=1.1,<2.0',
 'pickledb>=0.9.2,<0.10.0',
 'requests>=2.28.1,<3.0.0',
 'timeago>=1.0.16,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['uva = uva.main:app']}

setup_kwargs = {
    'name': 'uva',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Uva Command Line Tool\n\nThis is an Uva Command line tool that can help with Uva online judge problem submissions.',
    'author': 'Aleksandar Markovic',
    'author_email': 'aleksamarkoni@gmail.com',
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
