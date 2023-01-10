# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gscode']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<1.0.0',
 'nonebot-adapter-onebot>=2.0.0b1',
 'nonebot2>=2.0.0a16']

setup_kwargs = {
    'name': 'nonebot-plugin-gscode',
    'version': '0.1.5',
    'description': 'Genshin live codes plugin for NoneBot2',
    'long_description': '<h1 align="center">NoneBot Plugin GsCode</h1></br>\n\n\n<p align="center">🤖 用于查询原神前瞻直播兑换码的 NoneBot2 插件</p></br>\n\n\n<p align="center">\n  <a href="https://github.com/monsterxcn/nonebot-plugin-gscode/actions">\n    <img src="https://img.shields.io/github/actions/workflow/status/monsterxcn/nonebot-plugin-gscode/publish.yml?branch=main&style=flat-square" alt="actions">\n  </a>\n  <a href="https://raw.githubusercontent.com/monsterxcn/nonebot-plugin-gscode/master/LICENSE">\n    <img src="https://img.shields.io/github/license/monsterxcn/nonebot-plugin-gscode?style=flat-square" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-gscode">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-gscode?style=flat-square" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue?style=flat-square" alt="python"><br />\n</p></br>\n\n\n| ![image](https://user-images.githubusercontent.com/22407052/204017447-84f300f4-0df2-44df-ac3e-4bc72a47d816.png) | ![image](https://user-images.githubusercontent.com/22407052/204016397-2c2063cb-9e0d-4060-808d-32b2bb84bc69.png) |\n|:--:|:--:|\n\n\n## 安装方法\n\n\n如果你正在使用 2.0.0.beta1 以上版本 NoneBot，推荐使用以下命令安装：\n\n\n```bash\n# 从 nb_cli 安装\npython -m nb_cli plugin install nonebot-plugin-gscode\n\n# 或从 PyPI 安装\npython -m pip install nonebot-plugin-gscode\n```\n\n\n## 使用说明\n\n\n插件响应 `gscode` / `兑换码`，返回一组包含兑换码信息的合并转发消息。\n\n\n经测试，兑换码接口返回与前瞻直播有 2 分钟左右延迟，应为正常现象，请耐心等待。\n\n\n插件依赖 [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的合并转发接口，如需启用私聊响应请务必安装 [v1.0.0-rc2](https://github.com/Mrs4s/go-cqhttp/releases/tag/v1.0.0-rc2) 以上版本的 go-cqhttp。\n\n\n## 特别鸣谢\n\n\n[@nonebot/nonebot2](https://github.com/nonebot/nonebot2/) | [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) | [@Le-niao/Yunzai-Bot](https://github.com/Le-niao/Yunzai-Bot)\n',
    'author': 'monsterxcn',
    'author_email': 'monsterxcn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/monsterxcn/nonebot-plugin-gscode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
