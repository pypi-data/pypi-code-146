# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydpn', 'pydpn._api', 'pydpn._const', 'pydpn._utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'pycryptodome>=3.16.0,<4.0.0',
 'requests>=2.28.1,<3.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['dpn = pydpn.cli:main']}

setup_kwargs = {
    'name': 'pydpn',
    'version': '0.1.7',
    'description': 'python package for configuring a deeperNetwork device',
    'long_description': '# pydpn\n python package for configuring a deeperNetwork device\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
