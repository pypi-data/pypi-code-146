# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['play_integrity']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.72.0,<3.0.0', 'google-auth>=2.16.0,<3.0.0']

setup_kwargs = {
    'name': 'play-integrity',
    'version': '0.1.1',
    'description': 'Python library to verify Play Integrity API',
    'long_description': None,
    'author': 'Yves Tumushimire',
    'author_email': 'yvestumushimire@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
