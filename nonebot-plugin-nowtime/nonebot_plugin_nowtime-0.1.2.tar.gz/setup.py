# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_nowtime']

package_data = \
{'': ['*'], 'nonebot_plugin_nowtime': ['config/*', 'resource/*']}

install_requires = \
['aiofiles>=0.7.0',
 'httpx>=0.19.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1',
 'nonebot-plugin-apscheduler>=0.2.0,<0.3.0',
 'nonebot2>=2.0.0-beta.1',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-nowtime',
    'version': '0.1.2',
    'description': 'Nonebot2 plugin for telling the time per hour',
    'long_description': '<div align="center">\n\n<a href="https://v2.nonebot.dev/store"><img src="https://img.zcool.cn/community/014c9a55420cdc0000019ae952d851.jpg@1280w_1l_2o_100sh.jpg" width="180" height="180" alt="NoneBotPluginLogo"></a>\n\n</div>\n\n<div align="center">\n\n# nonebot-plugin-nowtime\n\n_⭐基于Nonebot2的一款整点报时的插件⭐_\n\n\n</div>\n\n\n## ⭐ 介绍\n\n让机器人为你整点报时吧，\n由于本人第一次创建，有不足的地方还请指出\n\n## 💿 安装\n\n<details>\n<summary>nb-cli安装</summary>\n\n在项目目录文件下运行\n\n```\nnb plugin install nonebot_plugin_nowtime\n```\n</details>\n\n<details>\n<summary>pip安装</summary>\n\n```\npip install nonebot-plugin-nowtime\n```\n\n</details>\n\n## ⚙️ 配置\n\n无需额外配置\n\n\n## ⭐ 使用\n\n### 指令：\n| 指令 | 需要@ | 范围 | 说明 |\n|:-----:|:----:|:----:|:----:|\n|北京时间|否|私聊、群聊|查看现在时间|\n|开启、关闭整点报时|否|群聊|开启或关闭群聊的整点报时|\n|查看整点报时列表|否|群聊|查看已开启整点报时的群聊|\n\n如：\n```\n    /开启整点报时\n```    \n**注意**\n\n默认情况下, 您应该在指令前加上命令前缀, 通常是 /\n\n## 🌙 未来todo\n\n- [√]添加语音整点报时\n- [ ]优化整点报时词库\n- [ ]图片整点报时\n',
    'author': 'Cvadia',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Cvandia/nonebot_plugin_nowtime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
