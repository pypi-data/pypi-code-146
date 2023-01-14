# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dumbo_esse3', 'dumbo_esse3.utils']

package_data = \
{'': ['*']}

install_requires = \
['dateutils>=0.6.12,<0.7.0',
 'lxml>=4.9.2,<5.0.0',
 'rich>=13.1.0,<14.0.0',
 'selenium>=4.4.3,<5.0.0',
 'typeguard>=2.13.3,<3.0.0',
 'typer>=0.7.0,<0.8.0',
 'valid8>=5.1.2,<6.0.0']

setup_kwargs = {
    'name': 'dumbo-esse3',
    'version': '0.3.16',
    'description': 'Esse3 command line utility, to save my future time!',
    'long_description': 'None',
    'author': 'Mario Alviano',
    'author_email': 'mario.alviano@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
