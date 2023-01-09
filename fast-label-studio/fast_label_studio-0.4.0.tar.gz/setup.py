# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_label_studio']

package_data = \
{'': ['*']}

install_requires = \
['fastai>=2.7.10,<3.0.0',
 'label-studio-ml>=1.0.8,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'fast-label-studio',
    'version': '0.4.0',
    'description': '',
    'long_description': '# Fast-label-studio\n## Set of utilities for working with label studio and fastai\n\n',
    'author': 'Glaadiss',
    'author_email': 'bartekgladys@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
