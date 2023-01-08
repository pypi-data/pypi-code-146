# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_admin_cli']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2,<4.0.0', 'asyncclick>=8.1.3.4,<9.0.0.0']

entry_points = \
{'console_scripts': ['flask-admin = flask_admin_cli.cli:the_cli']}

setup_kwargs = {
    'name': 'flask-admin-cli',
    'version': '0.1.3',
    'description': 'A CLI application to create Flask Admin instances.',
    'long_description': '# flask admin cli\nA CLI application to create Flask Admin instances.  \n\n## Installation\n```bash\npip install flask-admin-cli\n```',
    'author': 'Mario Hernandez',
    'author_email': 'mariofix@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mariofix.github.io/flask-admin-cli/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
