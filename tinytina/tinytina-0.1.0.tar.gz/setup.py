# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinytina']

package_data = \
{'': ['*']}

install_requires = \
['beaupy>=3.2.0,<4.0.0',
 'ttwl-cli-saveedit>=1.0.0,<2.0.0',
 'userpaths>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['ttwl = tinytina.main:main']}

setup_kwargs = {
    'name': 'tinytina',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'arthur-trt',
    'author_email': 'atrouill@student.42.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
