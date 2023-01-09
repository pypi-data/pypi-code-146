# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinyin_rhymer', 'pinyin_rhymer.data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pinyin-rhymer',
    'version': '0.1.8',
    'description': 'Generate pinyin rhymes based on rhyme schemes.',
    'long_description': None,
    'author': 'RCJacH',
    'author_email': 'RCJacH@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
