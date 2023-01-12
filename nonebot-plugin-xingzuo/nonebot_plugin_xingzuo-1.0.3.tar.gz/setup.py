# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_xingzuo']

package_data = \
{'': ['*']}

install_requires = \
['httpx==0.23.0', 'nonebot2>=2.0.0rc1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-xingzuo',
    'version': '1.0.3',
    'description': '一个nonebot插件，可以查询星座运势',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://zsy.juncikeji.xyz/i/img/mxy.png" width="150" height="150" alt="API管理系统"></a>\n</p>\n<div align="center">\n    <h1 align="center">✨萌新源API管理系统</h1>\n</div>\n<p align="center">\n<!-- 插件名称 -->\n<img src="https://img.shields.io/badge/插件名称-星座运势-blue" alt="python">\n<!-- Python版本 -->\n<img src="https://img.shields.io/badge/-Python3-white?style=flat-square&logo=Python">\n<!-- 插件名称 -->\n<img src="https://img.shields.io/badge/Python-3.8+-blue" alt="python">\n<a style="margin-inline:5px" target="_blank" href="http://blog.juncikeji.xyz/">\n\t<img src="https://img.shields.io/badge/Blog-个人博客-FDE6E0?style=flat&logo=Blogger" title="萌新源的小窝">\n</a>\n<a style="margin-inline:5px" target="_blank" href="https://github.com/mengxinyuan638/mxy-api-system">\n\t<img src="https://img.shields.io/badge/github-萌新源API管理系统-FDE6E0?style=flat&logo=github" title="萌新源API管理系统">\n</a>\n<a style="margin-inline:5px" target="_blank" href="https://gitee.com/meng-xinyuan-mxy/mxy-api">\n\t<img src="https://img.shields.io/badge/gitee-萌新源API管理系统-FDE6E0?style=flat&logo=gitee" title="萌新源API管理系统">\n</a>\n<!-- 萌新源API -->\n<a style="margin-inline:5px" target="_blank" href="https://api.juncikeji.xyz/">\n\t<img src="https://img.shields.io/badge/API-萌新源-blue?style=flat&logo=PHP" title="萌新源API">\n</a>\n<!-- CSDN博客 -->\n<a style="margin-inline:5px" target="_blank" href="https://blog.csdn.net/m0_66648798">\n\t<img src="https://img.shields.io/badge/CSDN-博客-c32136?style=flat&logo=C" title="CSDN博客主页">\n</a>\n<!-- QQ群 -->\n<a style="margin-inline:5px" target="_blank" href="https://jq.qq.com/?_wv=1027&k=5Ot4AUXh">\n\t<img src="https://img.shields.io/badge/QQ群-934541995-0cedbe?style=flat&logo=Tencent QQ" title="QQ">\n</a>\n<img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT">\n</p>\n\n\n# 使用教程\n\n## 命令：#星座 + 想要查询的星座\n',
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
