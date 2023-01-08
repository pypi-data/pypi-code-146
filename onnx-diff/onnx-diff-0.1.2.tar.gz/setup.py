# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onnx_diff']

package_data = \
{'': ['*']}

install_requires = \
['GraKeL>=0.1.9,<0.2.0',
 'colorama>=0.4.6,<0.5.0',
 'numpy>=1.24.1,<2.0.0',
 'onnx>=1.13.0,<2.0.0',
 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['onnxdiff = onnx_diff.run:run']}

setup_kwargs = {
    'name': 'onnx-diff',
    'version': '0.1.2',
    'description': 'Work in progress...',
    'long_description': None,
    'author': 'magnus',
    'author_email': 'contact@magnus.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/magnusmaynard/onnx-diff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
