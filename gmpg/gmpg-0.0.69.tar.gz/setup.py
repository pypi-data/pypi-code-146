# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gmpg', 'gmpg._pkg', 'gmpg._pkg.licensing']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.12.0',
 'isort>=5.11.4',
 'pendulum>=2.1.2',
 'pydeps>=1.10.24',
 'pyright>=1.1.288',
 'pytest-cov>=4.0.0',
 'pytest-gevent>=1.1.0',
 'pytest-pep8>=1.0.6',
 'pytest>=7.1.3',
 'radon>=5.1.0',
 'responses>=0.22.0',
 'toml>=0.10.2',
 'txtint>=0.0.0']

entry_points = \
{'console_scripts': ['gmpg = gmpg.__main__:main']}

setup_kwargs = {
    'name': 'gmpg',
    'version': '0.0.69',
    'description': 'tools for metamodern software development',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/gmpg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11',
}


setup(**setup_kwargs)
