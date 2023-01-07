# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['client', 'client.gui']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyQt6>=6.4.0,<7.0.0',
 'SQLAlchemy>=1.4.44,<2.0.0',
 'gb-pychat-common>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['client-gui = client.run_client:run']}

setup_kwargs = {
    'name': 'gb-pychat-client',
    'version': '0.1.1',
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
