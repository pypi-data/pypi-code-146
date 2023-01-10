# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_oidc']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'requests-oidc',
    'version': '0.1.1',
    'description': '',
    'long_description': '# requests-oidc\n',
    'author': 'Tristan Sweeney',
    'author_email': 'tsweeney@dustidentity.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tsweeney-dust/requests-oidc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
