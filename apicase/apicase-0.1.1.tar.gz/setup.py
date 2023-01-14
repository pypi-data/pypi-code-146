# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apicase', 'apicase.client', 'apicase.common', 'apicase.script']

package_data = \
{'': ['*']}

install_requires = \
['allure-pytest>=2.12.0,<3.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['apicase = apicase.script.cli:main']}

setup_kwargs = {
    'name': 'apicase',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'guowenhe',
    'author_email': '18538570410@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
