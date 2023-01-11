# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinygraphio']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tinygraphio',
    'version': '0.1.0',
    'description': '',
    'long_description': '# tinygraphio\n\nPython implementation of the tinygraphio graph data interchange file format https://tinygraph.org\n',
    'author': 'tinygraph',
    'author_email': 'hello@tinygraph.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
