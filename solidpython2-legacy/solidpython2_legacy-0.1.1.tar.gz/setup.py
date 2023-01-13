# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solid2_legacy',
 'solid2_legacy.examples',
 'solid2_legacy.examples.legacy',
 'solid2_legacy.examples.legacy.mazebox']

package_data = \
{'': ['*']}

install_requires = \
['euclid3>=0.1.0,<0.2.0',
 'prettytable==0.7.2',
 'pypng>=0.0.19,<0.0.20',
 'solidpython2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'solidpython2-legacy',
    'version': '0.1.1',
    'description': 'the legacy extension for SolidPython 2.x.x which provides some backwards compatibility to SolidPython 1.x.x',
    'long_description': 'None',
    'author': 'jeff',
    'author_email': '1105041+jeff-dh@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
