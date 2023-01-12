# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagbackup', 'tagbackup.commands']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'boto3>=1.26.48,<2.0.0',
 'humanize>=4.4.0,<5.0.0',
 'py-machineid>=0.2.1,<0.3.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['tagbackup = tagbackup.main:app']}

setup_kwargs = {
    'name': 'tagbackup',
    'version': '0.0.4',
    'description': '',
    'long_description': '# TagBackup\n',
    'author': 'TagBackup',
    'author_email': 'hello@tagbackup.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
