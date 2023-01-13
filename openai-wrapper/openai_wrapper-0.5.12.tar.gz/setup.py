# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openai_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'configobj>=5.0.6,<6.0.0',
 'dnspython>=2.2.1,<3.0.0',
 'motor>=3.1.1,<4.0.0',
 'openai>=0.26.0,<0.27.0',
 'pymongo>=4.2.0,<5.0.0',
 'typeguard>=2.13.3,<3.0.0']

setup_kwargs = {
    'name': 'openai-wrapper',
    'version': '0.5.12',
    'description': "A wrapper for OpenAI's python API which wraps around the openAI functions and stores the request, response and metadata to MongoDB. The stored data can be used to fine tune GPT-3 models or HuggingFace models.",
    'long_description': 'None',
    'author': 'AI Team',
    'author_email': 'datascience@prosus.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
