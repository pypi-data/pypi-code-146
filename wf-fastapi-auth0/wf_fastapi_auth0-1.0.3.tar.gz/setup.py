# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wf_fastapi_auth0', 'wf_fastapi_auth0.wf_permissions']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=3.24.0,<4.0.0',
 'cachetools>=5.2.1,<6.0.0',
 'fastapi>=0.89.1,<0.90.0',
 'python-jose>=3.3.0,<4.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'wf-fastapi-auth0',
    'version': '1.0.3',
    'description': 'Library to simplify adding Auth0 support to FastAPI',
    'long_description': '# Wildflower FastAPI/Auth0 integration\n\nBasic token verification for FastAPI and Auth0.  Also includes support for the Wildflower Permissions API, which provides centralized Role/Domain based access control.\n\n## Environment Configuration\n\n`AUTH0_DOMAIN` Domain to auth against within Auth0\n\n`API_AUDIENCE` Audience the tokens should target\n\n`CLIENT_ID` Client ID for machine-to-machine authenticatio for checking user Profiles\n\n`CLIENT_SECRET` Client Secret for machine-to-machine authenticatio for checking user Profiles\n\n\n### For permissions-api integration (optional)\n\n`TOKEN_EMAIL_DOMAIN` Domain to add to client_credentials for email address for `wf_permissions` integration\n\n`TOKEN_DOMAIN` Domain to add to client_credentials for `wf_permissions` integration\n\n`PERMS_API_URI` URI for permissions API\n\n`PERMS_API_AUD` Audience to auth against with machine-to-machine tokens\n',
    'author': 'Paul DeCoursey',
    'author_email': 'paul.decoursey@wildflowerschools.org',
    'maintainer': 'Benjamin Jaffe-Talberg',
    'maintainer_email': 'ben.talberg@wildflowerschools.org',
    'url': 'https://github.com/WildflowerSchools/wf-fastapi-auth0',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
