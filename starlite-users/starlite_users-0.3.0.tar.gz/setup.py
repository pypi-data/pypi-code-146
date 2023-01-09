# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlite_users', 'starlite_users.adapter.sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['cryptography', 'passlib', 'python-jose', 'sqlalchemy', 'starlite']

setup_kwargs = {
    'name': 'starlite-users',
    'version': '0.3.0',
    'description': 'Authentication and user management for Starlite',
    'long_description': '# starlite-users\n\nAuthentication, authorization and user management for the Starlite framework\n\n## _This package is not yet production ready._\n\n## Features\n\n- Supports Session, JWT and JWTCookie authentication backends\n- Authorization via role based guards\n- Pre-configured route handlers for:\n  - Authentication\n  - Registration\n  - Verification\n  - Password reset\n  - Administrative user management (read, update, delete)\n  - Administrative role management (read, update, delete)\n  - Assignment/revocation of roles to/from users\n\n## Getting started\n\n### Installation\n\n`pip install starlite-users`\n\n### Documentation\n\n[Read the documentation](https://lonelyvikingmichael.github.io/starlite-users/)\n\nOtherwise [check out the examples](https://github.com/LonelyVikingMichael/starlite-users/tree/main/examples)\n',
    'author': 'Michael Bosch',
    'author_email': 'michael@lonelyviking.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
