# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['steggi']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.6.0.66,<5.0.0.0',
 'pillow>=9.3.0,<10.0.0',
 'tk>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['steggi = steggi.steggi:main']}

setup_kwargs = {
    'name': 'steggi',
    'version': '0.2.1',
    'description': 'Stegsolve like GUI program for steganographic purposes.',
    'long_description': '# steggi\n\nStegsolve like GUI program in python with opencv and tkinter.\n',
    'author': 'Aquib',
    'author_email': 'aquibjavedt007@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tamton-aquib/steggi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
