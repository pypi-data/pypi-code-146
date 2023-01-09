# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_security_cookie']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.89.0,<0.90.0', 'itsdangerous>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'fastapi-security-cookie',
    'version': '0.1.2',
    'description': 'Simple security cookie for FastAPI',
    'long_description': '',
    'author': 'Arian Ventura Rodríguez',
    'author_email': 'arianventura94@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ventura94/FastAPICookie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
