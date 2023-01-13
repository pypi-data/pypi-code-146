# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ratio_svenbarray']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ratio-svenbarray',
    'version': '0.1.0',
    'description': 'My first poetry file',
    'long_description': 'In terminal:\npip install -r requirements.txt\npython main.py',
    'author': 'SvenBarray',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '==3.10.4',
}


setup(**setup_kwargs)
