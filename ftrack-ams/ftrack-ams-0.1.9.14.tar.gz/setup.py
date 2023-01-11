# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ftrack_ams']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'ftrack-python-api>=2.3.1,<3.0.0', 'pick>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['ftrack-ams = ftrack_ams.console:main']}

setup_kwargs = {
    'name': 'ftrack-ams',
    'version': '0.1.9.14',
    'description': '',
    'long_description': 'None',
    'author': 'Lucas Selfslagh',
    'author_email': 'lucas@animotions.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
