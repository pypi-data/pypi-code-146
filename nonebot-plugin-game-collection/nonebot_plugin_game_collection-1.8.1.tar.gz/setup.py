from setuptools import setup,find_namespace_packages

setup(
name='nonebot_plugin_game_collection',
version='1.8.1',
description='改自nonebot_plugin_russian合并了nonebot_plugin_horserace还有一些自编玩法的小游戏合集。',
#long_description=open('README.md','r').read(),
author='karisaya',
author_email='1048827424@qq.com',
license='MIT license',
include_package_data=True,
packages=find_namespace_packages(include=["nonebot_plugin_game_collection","nonebot_plugin_game_collection.*"]),
platforms='all',
install_requires=["nonebot2","nonebot-adapter-onebot","nonebot_plugin_apscheduler","nonebot_plugin_imageutils","mplfinance","seaborn"],
url='https://github.com/KarisAya/nonebot_plugin_game_collection',
)