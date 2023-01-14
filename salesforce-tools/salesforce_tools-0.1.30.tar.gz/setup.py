# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['salesforce_tools', 'salesforce_tools.async_sf']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.1,<3.0.0',
 'PyJWT>=2.4.0,<3.0.0',
 'authlib>=1.1.0,<2.0.0',
 'cryptography>=38.0.3,<39.0.0',
 'flatten-json>=0.1.13,<0.2.0',
 'httpx>=0.23.3,<0.24.0',
 'pandas>=1.4.3,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests-oauthlib>=1.3.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'salesforce-tools',
    'version': '0.1.30',
    'description': 'Salesforce API tools',
    'long_description': 'None',
    'author': 'David Manuel',
    'author_email': 'david@dcmanjr.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dacmanj/salesforce-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
