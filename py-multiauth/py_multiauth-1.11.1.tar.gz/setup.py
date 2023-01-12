# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multiauth',
 'multiauth.entities',
 'multiauth.entities.providers',
 'multiauth.providers',
 'multiauth.static']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=1.1.0,<2.0.0',
 'PyJWT>=2.6.0,<3.0.0',
 'graphql-core>=3.2.3,<4.0.0',
 'jsonschema>=4.17.3,<5.0.0',
 'pycognito>=2022.11.2,<2023.0.0',
 'pydash>=5.1.2,<6.0.0']

entry_points = \
{'console_scripts': ['multiauth = multiauth:cli']}

setup_kwargs = {
    'name': 'py-multiauth',
    'version': '1.11.1',
    'description': 'Python package to interact with multiple authentication services',
    'long_description': "# py-multiauth ![PyPI](https://img.shields.io/pypi/v/py-multiauth) [![CI](https://github.com/Escape-Technologies/py-multiauth/actions/workflows/ci.yaml/badge.svg)](https://github.com/Escape-Technologies/py-multiauth/actions/workflows/ci.yaml) [![CD](https://github.com/Escape-Technologies/py-multiauth/actions/workflows/cd.yaml/badge.svg)](https://github.com/Escape-Technologies/py-multiauth/actions/workflows/cd.yaml) [![codecov](https://codecov.io/gh/Escape-Technologies/py-multiauth/branch/main/graph/badge.svg?token=NL148MNKAE)](https://codecov.io/gh/Escape-Technologies/py-multiauth)\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-multiauth)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/py-multiauth)\n\n## Installation\n\n```bash\npip install py-multiauth\n```\n\n## Supported methods\n\n|Name     |Authenticate|Refresh|Extra    |\n|---------|:----------:|:-----:|---------|\n|`API_KEY`|✓           |       |         |\n|`AWS`    |✓           |✓      |Signature|\n|`BASIC`  |✓           |       |         |\n|`REST`   |✓           |✓      |         |\n|`DIGEST` |✓           |       |         |\n|`GRAPHQL`|✓           |       |         |\n|`HAWK`   |✓           |       |         |\n|`MANUAL` |✓           |       |         |\n|`OAUTH`  |✓           |✓      |         |\n\n## Usage\n\n### Loading a configuration file\n\nCurrently, we support 4 way of loading a configuration file.\n\n```python\n\n# Using constructor argument\nMultiAuth(authrc_file='path.json')\n\n# Using environment variable\nos.environ['AUTHRC'] = 'path.json'\n\n# Using autodection\nos.paths.exists('.authrc')?\n\n# Using autodection from user home directory\nos.path.exists(os.path.expanduser('~/.multiauth/.authrc'))?\n```\n\n### Managing authentication flow\n\n**MultiAuth supports context singleton.\nFrom that, you can instanciate MultiAuth and re-use the same class in another package as far it is sharing the same context.**\n\n```python\nauth = MultiAuth(auths=.., users=.., authrc=.., logger=..)\n\n# Sending the requests to get the correct headers\nauth.authenticate_users()\n\n# Getting the header before sending a HTTP request\nauth_headers = auth.reauthenticate(username=.., additional_headers=.., no_auth=..)\nr = requests.get('https://example.com', headers=auth_headers[0])\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License ![PyPI - License](https://img.shields.io/pypi/l/py-multiauth)\n\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Escape Technologies SAS',
    'author_email': 'ping@escape.tech',
    'maintainer': 'Antoine Carossio',
    'maintainer_email': 'antoine@escape.tech',
    'url': 'https://escape.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
