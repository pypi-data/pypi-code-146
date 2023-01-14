# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_mc_server_status']

package_data = \
{'': ['*']}

install_requires = \
['mcstatus>=10.0.0,<11.0.0',
 'nonebot-adapter-onebot>=2.0.0,<3.0.0',
 'nonebot2>=2.0.0-rc.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mc-server-status',
    'version': '0.2.0',
    'description': 'Nonebot2查询MC服务器在线信息插件',
    'long_description': '# nonebot_plugin_mc_server_status\n[![nonebot2](https://img.shields.io/static/v1?label=nonebot&message=v2rc1%2B&color=green)](https://v2.nonebot.dev/)[![python](https://img.shields.io/static/v1?label=python+&message=3.9%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nNonebot2查询MC服务器在线信息插件  \n支持Java和Bedrock服务器  \n\n### 安装\n\n使用nb-cli安装\n```bash\nnb plugin install nonebot_plugin_mc_server_status\n```\n\n或者  \n直接把插件clone下来放进去plugins文件夹，记得把依赖装上 pip install mcstatus  \n\n### 使用\n\n添加了服务器信息后，会在bot根目录下的data目录创建一个mc_status_data.json文件，用于存储插件信息  \n在bot对应的.env文件修改\n\n```bash\n# 机器人的QQ号（由于开发者多gocq连接，所以有这个设置）\nmc_status_bot_qqnum = 114514\n# 管理员的QQ号（别问我为什么要另外写）\nmc_status_admin_qqnum = 114514\n```\n\n### 插件命令  \n| 指令 | 说明 |\n|:-----:|:----:|\n| 信息|所有人都能使用，查看当前群添加的服务器状态|\n| 添加服务器|字面意思，bot超级管理员用|\n| 删除服务器|字面意思，bot超级管理员用|\n| 信息数据|查看已添加的群和服务器信息，bot超级管理员用|\n\n### 使用截图\n<img width="300" src="https://raw.githubusercontent.com/nikissXI/nonebot_plugins/main/nonebot_plugin_mc_server_status/readme_img/xinxi.jpg"/>\n\n### 定制\n\n自己看代码改啦！',
    'author': 'nikissXI',
    'author_email': '1299577815@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nikissXI/nonebot_plugins/tree/main/nonebot_plugin_mc_server_status',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
