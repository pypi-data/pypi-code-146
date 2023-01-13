# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elektro']

package_data = \
{'': ['*']}

install_requires = \
['rath>=0.3.3', 'zarr>=2.11.1,<3.0.0']

extras_require = \
{'complete:python_version >= "3.9"': ['turms>=0.2.3,<0.3.0'],
 'turms:python_version >= "3.9"': ['turms>=0.2.3,<0.3.0']}

setup_kwargs = {
    'name': 'elektro',
    'version': '0.3.11',
    'description': 'electrophy for arkitekt',
    'long_description': 'None',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
