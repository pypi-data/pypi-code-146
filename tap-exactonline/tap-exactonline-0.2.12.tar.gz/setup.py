# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_exactonline', 'tap_exactonline.helpers', 'tap_exactonline.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.79,<2.0.0',
 'exactonline>=0.4.0,<0.5.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tap-exactonline = '
                     'tap_exactonline.tap:TapExactOnline.cli']}

setup_kwargs = {
    'name': 'tap-exactonline',
    'version': '0.2.12',
    'description': '`tap-exactonline` is a Singer tap for ExactOnline, built with the Meltano SDK for Singer Taps.',
    'long_description': 'None',
    'author': 'Hidde Stokvis',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
