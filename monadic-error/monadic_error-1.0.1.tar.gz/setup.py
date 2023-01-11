# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monadic_error']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'monadic-error',
    'version': '1.0.1',
    'description': 'Monads used for handling Errors. Contains Either and Option.',
    'long_description': '# Monadic Error\n\nThis contains code for handling errors in Python in\na monadic way. This works with Python Pattern Matching.',
    'author': 'Ian Kollipara',
    'author_email': 'ian.kollipara@cune.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
