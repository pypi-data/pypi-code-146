# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graiax_bbot',
 'graiax_bbot.cli',
 'graiax_bbot.core',
 'graiax_bbot.function',
 'graiax_bbot.function.command',
 'graiax_bbot.function.command.admin',
 'graiax_bbot.function.command.configure',
 'graiax_bbot.function.command.menu',
 'graiax_bbot.function.command.subgroup',
 'graiax_bbot.function.command.up',
 'graiax_bbot.function.command.vip',
 'graiax_bbot.function.command.whitelist',
 'graiax_bbot.function.event',
 'graiax_bbot.function.pusher',
 'graiax_bbot.function.scheduler',
 'graiax_bbot.utils',
 'graiax_bbot.website',
 'graiax_bbot.website.api',
 'graiax_bbot.website.api.router']

package_data = \
{'': ['*'],
 'graiax_bbot': ['static/*', 'static/font/*'],
 'graiax_bbot.website': ['static/html/*', 'static/init/*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'bilireq>=0.2.3,<0.3.0',
 'fastapi>=0.88.0,<0.89.0',
 'graia-ariadne[standard]>=0.10.3,<0.11.0',
 'graiax-playwright>=0.2.1,<0.3.0',
 'passlib[bcrypt]>=1.7.4,<2.0.0',
 'peewee>=3.15.4,<4.0.0',
 'pillow>=9.4.0,<10.0.0',
 'psutil>=5.9.4,<6.0.0',
 'python-jose[cryptography]>=3.3.0,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pyyaml>=6.0,<7.0',
 'qrcode>=7.3.1,<8.0.0',
 'sentry-sdk>=1.12.1,<2.0.0',
 'uvicorn>=0.19.0,<0.20.0',
 'websockets>=10.4,<11.0']

entry_points = \
{'console_scripts': ['bbot = graiax_bbot.__main__:main']}

setup_kwargs = {
    'name': 'graiax-bbot',
    'version': '1.2.0b4',
    'description': '一个用于 QQ 群内高效推送哔哩哔哩 UP 动态及直播的机器人',
    'long_description': '<div align="center">\n\n![BBot-Graia](https://socialify.git.ci/djkcyl/BBot/image?description=1&font=Inter&logo=https%3A%2F%2Fgithub.com%2Fdjkcyl%2FBBot%2Fblob%2Fmaster%2Flogo.png%3Fraw%3Dtrue&owner=1&pattern=Circuit%20Board&theme=Dark)\n  \n# BBot for Ariadne\n![GitHub Repo stars](https://img.shields.io/github/stars/djkcyl/BBot?style=social)\n![GitHub forks](https://img.shields.io/github/forks/djkcyl/BBot?style=social)\n\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/djkcyl/BBot/prerelease.yml?branch=web)\n![GitHub release (latest by date)](https://img.shields.io/github/v/release/djkcyl/BBot?color=brightgreen)\n![GitHub all releases](https://img.shields.io/github/downloads/djkcyl/BBot/total)\n![Platform](https://img.shields.io/badge/platform-linux_%7C_windows-lightgrey)\n\n[![License](https://img.shields.io/github/license/djkcyl/BBot)](https://github.com/djkcyl/BBot/blob/master/LICENSE)\n[![wakatime](https://wakatime.com/badge/github/djkcyl/BBot.svg)](https://wakatime.com/badge/github/djkcyl/BBot)\n![QQ](https://img.shields.io/badge/Tencent_QQ-2948531755-ff69b4)\n\n![Python Version](https://img.shields.io/badge/python-3.9-blue)\n![Poetry Using](https://img.shields.io/badge/poetry-using-blue)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/djkcyl/bbot)\n\n![!](https://count.getloli.com/get/@BBot-Graia?theme=rule34)\n\n基于 [Graia-Ariadne](../../../../GraiaProject/Ariadne) 搭建的高效、高性能哔哩哔哩推送 [QQ](../../../../project-mirai/mirai-api-http) 机器人\n\n```text\nBBot\nB，是 26 个英文字母里的第二个，可意为我个人的第二个机器人\nB，也代表 BiliBili，这个 Bot 将专注于哔哩哔哩的推送等服务\n```\n\n</div>\n\n## BBot 现在能干什么\n\n- 订阅 UP 主 ~~废话~~\n- 推送直播（开播及下播）~~废话~~\n- 推送动态 ~~废话~~\n- 视频链接解析\n\n## 特色\n\n- 大量使用并发 **gRPC 接口**，推送效率远超使用 REST Api 的哔哩哔哩机器人且目前未见有风控（-421）风险\n- ~~使用登录和非登录两种方案，对于财大气粗的用户可以登录后再次提升效率~~ **不建议使用**\n- 动态使用 Web 端截图，虽然会吃那么点性能，~~但这都是值得的~~\n- 可自由配置是否在群内 @全体成员、对于直播和动态的分别控制等\n- 可针对不同群聊对订阅的 UP 主进行昵称替换\n- 可限制每个群可订阅的最大 UP 主数量\n\n## 使用\n\n**[BBot 使用文档](https://github.com/djkcyl/BBot/wiki)**\n\nDocker 部署请查看 [这里](https://github.com/djkcyl/BBot-Graia/wiki/Docker)\n\n## TODO\n\n- [x] 增加群内配置功能\n- [x] 增加菜单（/help 指令）\n- [x] 使用数据库存储推送记录\n- [x] 增加动态自动点赞功能\n- [x] 支持 up 全名搜索\n- [x] 增加可选的动态推送样式（App 样式）\n- [x] 定时刷新 token，防止过期\n- [x] 针对 Windows 和 Linux 平台，增加 Release 打包版本\n- [x] 增加非登录式的推送更新逻辑\n- [x] 更换 BiliBili 请求库为更成熟的 [BiliReq](../../../../SK-415/bilireq)\n- [x] 可能会增加不需要浏览器的动态截图获取方式\n- [x] 增加 Docker 部署方案\n- [x] 自定义动态页字体\n- [ ] **增加 Web 端管理界面**\n- [ ] 增加简单的推送数据分析及报告\n- [ ] 丰富管理员指令\n- [ ] 增加订阅组（同时订阅多个设定好的 up，如 `和谐有爱五人组`...）\n- [ ] ~~可能会增加其他平台的推送~~\n\n\nMore...\n\n## 感谢\n\n- [HarukaBot](../../../../SK-415/HarukaBot) 学习对象\n- [bilibili-API-collect](../../../../SocialSisterYi/bilibili-API-collect) 易姐收集的各种 BiliBili Api 及其提供的 gRPC Api 调用方案\n- [ABot-Graia](../../../../djkcyl/ABot-Graia) 永远怀念最好的 ABot 🙏\n- [Well404](https://space.bilibili.com/33138220/) 为本项目编写文档以及部署教程[视频](https://www.bilibili.com/video/BV16B4y137sx)\n- [八萬](https://space.bilibili.com/8027000) 项目 Logo 画师\n\n## Stargazers over time\n\n[![Stargazers over time](https://starchart.cc/djkcyl/BBot.svg)](https://starchart.cc/djkcyl/BBot)\n',
    'author': 'djkcyl',
    'author_email': 'cyl@cyllive.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/djkcyl/BBot-Graia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
