# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['server', 'server.gui', 'server.migrations', 'server.migrations.versions']

package_data = \
{'': ['*']}

install_requires = \
['PyQt6>=6.4.0,<7.0.0',
 'SQLAlchemy>=1.4.44,<2.0.0',
 'alembic>=1.8.1,<2.0.0',
 'gb-pychat-common>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['server-cli = server.run_server_cli:run',
                     'server-gui = server.run_server_gui:run']}

setup_kwargs = {
    'name': 'gb-pychat-server',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'DashViolin',
    'author_email': 'mymail@srv.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
