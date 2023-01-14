# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d_oss']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.3', 'oss2>=2.15.0,<3.0.0', 'rich==12.4.2', 'typer[all]==0.6.1']

entry_points = \
{'console_scripts': ['oss = d_oss.main:app']}

setup_kwargs = {
    'name': 'd-oss',
    'version': '0.2.1',
    'description': '迪的OSS存储',
    'long_description': 'None',
    'author': 'good-as-water',
    'author_email': '790990241@qq.com',
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
