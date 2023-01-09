# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deltafi']

package_data = \
{'': ['*']}

install_requires = \
['json-logging==1.3.0',
 'minio==7.1.12',
 'pydantic==1.10.2',
 'redis==4.3.4',
 'requests==2.28.1',
 'urllib3==1.26.12']

setup_kwargs = {
    'name': 'deltafi',
    'version': '0.99.8',
    'description': 'SDK for DeltaFi plugins and actions',
    'long_description': '# DeltaFi Action Kit\n\nThis project provides a Python implementation of the DeltaFi Action Kit. The DeltaFi Action Kit is a setup of modules which simplify the creation of a DeltaFi Plugin.\n',
    'author': 'DeltaFi',
    'author_email': 'deltafi@systolic.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
