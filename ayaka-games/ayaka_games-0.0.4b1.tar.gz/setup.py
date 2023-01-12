# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka_games']

package_data = \
{'': ['*']}

install_requires = \
['ayaka>=0.0.0.4,<0.0.1.0', 'pypinyin>=0.47.1,<0.48.0']

setup_kwargs = {
    'name': 'ayaka-games',
    'version': '0.0.4b1',
    'description': 'ayaka小游戏合集',
    'long_description': '<div align="center">\n\n# Ayaka小游戏合集 - 0.0.4b1\n\n开发进度 10/10\n\n**特别感谢**  [@灯夜](https://github.com/lunexnocty/Meiri) 大佬的插件蛮好玩的~\n\n</div>\n\n得益于[ayaka](https://github.com/bridgeL/ayaka)，本插件可作为如下机器人框架的插件使用\n\n- [nonebot2](https://github.com/nonebot/nonebot2)(使用[onebot11](https://github.com/nonebot/adapter-onebot)适配器)\n- [hoshino](https://github.com/Ice-Cirno/HoshinoBot)\n- [nonebot1](https://github.com/nonebot/nonebot)\n\n也可将其作为console程序离线运行\n\n## 文档\n\nhttps://bridgel.github.io/ayaka_games/\n\n## 其他\n\n本插件的前身：[nonebot_plugin_ayaka_games](https://github.com/bridgeL/nonebot-plugin-ayaka-games)\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/ayaka_games',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
