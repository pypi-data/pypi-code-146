# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0', 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka',
    'version': '1.0.2',
    'description': '为nonebot插件开发提供状态机支持',
    'long_description': '<div align="center">\n\n# Ayaka - 为群聊插件开发提供状态机支持 - 1.0.2\n\n基于[nonebot2](https://github.com/nonebot/nonebot2)和[OnebotV11协议](https://github.com/botuniverse/onebot-11)，为群聊插件开发提供状态机支持\n\n<img src="https://img.shields.io/pypi/pyversions/nonebot-plugin-ayaka">\n\n单独安装本插件没有意义，本插件的意义在于帮助衍生插件实现功能\n\n</div>\n\n## 安装\n\n```\npip install nonebot-plugin-ayaka\n``` \n\n## 特性\n\n- 状态机\n- 数据缓存\n\n## 文档\n\nhttps://bridgel.github.io/ayaka_doc/\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bridgel.github.io/ayaka_doc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
