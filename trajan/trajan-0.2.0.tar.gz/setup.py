# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trajan', 'trajan.plot', 'trajan.scripts', 'trajan.skill']

package_data = \
{'': ['*']}

install_requires = \
['bottleneck>=1.3.0',
 'cartopy>=0.21',
 'click>=8.1.3,<9.0.0',
 'matplotlib>=3.5',
 'netCDF4>=1.6',
 'numpy>=1.23',
 'pyproj>=2.3',
 'scipy>=1.9',
 'xarray>=2022.6.0']

entry_points = \
{'console_scripts': ['trajanshow = trajan.scripts.trajanshow:main']}

setup_kwargs = {
    'name': 'trajan',
    'version': '0.2.0',
    'description': 'Trajectory analysis package for simulated and observed trajectories',
    'long_description': 'None',
    'author': 'Gaute Hope',
    'author_email': 'gauteh@met.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
