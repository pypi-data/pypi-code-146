# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_package']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['my_package = '
                     'poetry_demo_victorio.my_package.msg:say_hello']}

setup_kwargs = {
    'name': 'poetry-demo-victorio',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Victorio',
    'author_email': 'victorio.lazaro15@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
