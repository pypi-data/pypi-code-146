# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firecore', 'firecore.torch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.0,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'rjsonnet>=0.4.5,<0.5.0',
 'structlog>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'firecore',
    'version': '0.2.1',
    'description': '',
    'long_description': '# firecore',
    'author': 'SunDoge',
    'author_email': '384813529@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
