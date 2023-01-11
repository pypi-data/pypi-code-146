# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algorithms_km_programs', 'algorithms_km_programs.algo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'algorithms-km-programs',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'SzymiYay',
    'author_email': 'szymoon09@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
