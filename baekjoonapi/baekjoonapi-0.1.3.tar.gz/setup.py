# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bojapi']

package_data = \
{'': ['*']}

install_requires = \
['bs4==0.0.1', 'lxml==4.9.2', 'random-user-agent==1.0.1', 'requests==2.28.1']

setup_kwargs = {
    'name': 'baekjoonapi',
    'version': '0.1.3',
    'description': 'BaekjoonAPI for Python',
    'long_description': '# BaekjoonAPI\n\nBaekjoonAPI for python\n\n## Installation\n\nInstall with pip (pip install baekjoonapi)\n',
    'author': 'MisileLaboratory',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/misilelab/baekjoonapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
