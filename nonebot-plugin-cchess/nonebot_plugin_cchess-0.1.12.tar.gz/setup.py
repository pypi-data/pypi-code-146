# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_cchess']

package_data = \
{'': ['*'], 'nonebot_plugin_cchess': ['resources/images/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-datastore>=0.4.0,<0.5.0',
 'nonebot2>=2.0.0-rc.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-cchess',
    'version': '0.1.12',
    'description': 'Nonebot2 象棋插件',
    'long_description': '## nonebot-plugin-cchess\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的象棋插件。\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_cchess\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_cchess\n```\n\n\n人机功能 需要使用遵循 [UCCI协议](https://www.xqbase.com/protocol/cchess_ucci.htm) 的引擎\n\n需要在 `.env` 文件中添加 引擎的可执行文件的路径\n\n```\ncchess_engine_path=/path/to/your/engine\n```\n\n经试用可用的引擎：\n\n - [Fairy-Stockfish](https://github.com/ianfab/Fairy-Stockfish/releases)\n\n注意，Fairy-Stockfish 支持多种游戏，需要选择支持 `Xiangqi` 的发行版，即需要选带有 `largeboard` 的版本\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n@我 + “象棋人机”或“象棋对战”开始一局游戏；\n\n可使用“lv1~8”指定AI等级，如“象棋人机lv5”，默认为“lv4”；\n\n发送 中文纵线格式如“炮二平五” 或 起始坐标格式如“h2e2”下棋；\n\n发送“结束下棋”结束当前棋局；\n\n发送“显示棋盘”显示当前棋局；\n\n发送“悔棋”可进行悔棋（人机模式可无限悔棋；对战模式只能撤销自己上一手下的棋）；\n\n\n或者使用 `cchess` 指令：\n\n可用选项：\n\n - `-e`, `--stop`, `--end`: 停止下棋\n - `-v`, `--show`, `--view`: 显示棋盘\n - `--repent`: 悔棋\n - `--reload`: 重新加载已停止的游戏\n - `--battle`: 对战模式，默认为人机模式\n - `--black`: 执黑，即后手\n - `-l <LEVEL>`, `--level <LEVEL>`: 人机等级，可选 1~8，默认为 4\n\n\n### 示例\n\n<div align="left">\n    <img src="https://s2.loli.net/2022/04/30/RztCnIkFQqWKsUe.jpg" width="500" />\n</div>\n\n\n### 特别感谢\n\n- [niklasf/python-chess](https://github.com/niklasf/python-chess) A chess library for Python\n- [StevenBaby/chess](https://github.com/StevenBaby/chess) 基于 Pyside2 和 UCCI 引擎的中国象棋程序\n- [walker8088/cchess](https://github.com/walker8088/cchess) cchess是一个Python版的中国象棋库\n- [ianfab/Fairy-Stockfish](https://github.com/ianfab/Fairy-Stockfish) chess variant engine supporting Xiangqi and many more\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/noneplugin/nonebot-plugin-cchess',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
