# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_xingzuo']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0rc1,<3.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-xingzuo',
    'version': '1.0.2',
    'description': '一个nonebot插件，可以查询星座运势',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://zsy.juncikeji.xyz/i/img/mxy.png" width="150" height="150" alt="API管理系统"></a>\n</p>\n<div align="center">\n    <h1 align="center">✨萌新源API管理系统</h1>\n</div>\n<p align="center">\n<!-- 插件名称 -->\n<img src="https://img.shields.io/badge/插件名称-星座运势-blue" alt="python">\n<!-- Python版本 -->\n<img src="https://img.shields.io/badge/-Python3-white?style=flat-square&logo=Python">\n<!-- 插件名称 -->\n<img src="https://img.shields.io/badge/Python-3.8+-blue" alt="python">\n<a href="https://blog.juncikeji.xyz">\n<img src="https://img.shields.io/badge/博客-萌新源-red">\n</a>\n</p>\n\n# 使用教程\n\n## 命令：#星座 + 想要查询的星座\n',
    'author': 'mengxinyuan',
    'author_email': '1648576390@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
