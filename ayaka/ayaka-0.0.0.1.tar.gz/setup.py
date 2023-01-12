# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka', 'ayaka.adapters', 'ayaka.adapters.nonebot2']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'ayaka',
    'version': '0.0.0.1',
    'description': '猫猫，猫猫！',
    'long_description': '<div align="center">\n\n# Ayaka - 猫猫，猫猫！ - 0.0.0.1\n\n</div>\n\n## 安装\n\n```\npip install ayaka\n```\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bridgel.github.io/ayaka/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
