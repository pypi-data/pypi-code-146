# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ishutils']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.0.1,<14.0.0']

setup_kwargs = {
    'name': 'ishutils',
    'version': '0.0.1',
    'description': 'My Shell Utils',
    'long_description': '# ishutils\n\nMy Shell Utils\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://liblaf.github.io/ishutils/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
