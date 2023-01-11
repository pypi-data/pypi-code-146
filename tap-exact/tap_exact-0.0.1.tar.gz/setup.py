# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_exact', 'tap_exact.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.14.0,<0.15.0']

extras_require = \
{'s3': ['fs-s3fs>=1.1.1,<2.0.0']}

entry_points = \
{'console_scripts': ['tap-exact = tap_exact.tap:TapExactOnline.cli']}

setup_kwargs = {
    'name': 'tap-exact',
    'version': '0.0.1',
    'description': '`tap-exact` is a Singer tap for Exact Online, built with the Meltano Singer SDK.',
    'long_description': 'None',
    'author': 'Janick Otten',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
