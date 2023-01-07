# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_admin_cli']

package_data = \
{'': ['*']}

install_requires = \
['asyncclick>=8.1.3.4,<9.0.0.0']

setup_kwargs = {
    'name': 'flask-admin-cli',
    'version': '0.1.2',
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
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
