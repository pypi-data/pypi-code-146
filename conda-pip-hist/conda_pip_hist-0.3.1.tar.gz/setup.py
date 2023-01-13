# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conda_pip_hist', 'conda_pip_hist.process_env']

package_data = \
{'': ['*'], 'conda_pip_hist': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['pipreqs>=0.4.11,<0.5.0',
 'pytest>=7.2.0,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['conda-pip-hist = conda_pip_hist.main:app']}

setup_kwargs = {
    'name': 'conda-pip-hist',
    'version': '0.3.1',
    'description': '',
    'long_description': '# conda-pip-hist\n\nThe awesome conda dependency export utility with build versions and primary pip dependencies.\n\nshare your conda project with environments that are easily reproducible.\n',
    'author': 'victor',
    'author_email': 'victor.ihuoma@danfoss.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.13,<4.0.0',
}


setup(**setup_kwargs)
