# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakemake_wrapper_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snakemake-wrapper-utils',
    'version': '0.5.2',
    'description': 'A collection of utils for Snakemake wrappers.',
    'long_description': 'None',
    'author': 'Johannes Köster',
    'author_email': 'johannes.koester@tu-dortmund.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
