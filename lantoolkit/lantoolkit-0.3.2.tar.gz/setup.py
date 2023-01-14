# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 10:40:59 2022

@author: Administrator
"""

from setuptools import setup
from setuptools.command.install import install
import subprocess
import os
import platform


def cmd(command):
    subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding="utf-8")
    print(subp.wait())


class cheeklai:
    def __init__(self):
        if platform.system() == 'Windows':
            if '7' or '8' or '10' in platform.version():
                if not cmd('scoop') == 0:
                    os.system('powershell "iwr -useb scoop.201704.xyz | iex"')
                if not cmd('aria2c') == 0:
                    os.system('scoop install aria2')
                if not cmd('sudo echo 0') == 0:
                    os.system('scoop install sudo ')
                if not cmd('7z') == 0:
                    os.system('scoop install 7zip')
        if platform.system() == 'Linux':
            a = input('请输入你的软件包管理器（如apt,yum,pacman等）：')
            b = ['apt', 'yum', 'yay', 'pacman', 'dnf', 'zypper']
            if a not in b:
                print('我不会，你自己装吧[doge]')
            if os.system('7z') != 1:
                if a == 'pacman':
                    os.system('pacman -Sy 7zip')
                os.system(a+' install -y 7zip')
            if os.system('aria2c') != 1:
                if a == 'pacman':
                    os.system('pacman -Sy aria2c')
                os.system(a+' install -y aria2c')


class CustomInstallCommand(install):
    """Customized setuptools install command"""

    def run(self):
        install.run(self)
        cheeklai()  # 替换为你的代码


setup(
    name="lantoolkit",  # 包名
    version="0.3.2",  # 版本
    description="A python toolkit:fix",  # 包简介
    # long_description=open("README-PY.md",mode='r'),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author="lan",  # 作者
    author_email="soft-diyuge@outlook.com",  # 作者邮件
    maintainer="虚位以待",  # 维护者
    maintainer_email="none@none.none",  # 维护者邮件
    license="MuLan PSL License",  # 协议
    url="",  # github或者自己的网站地址
    packages=['lantoolkit'],  # 包的目录
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python ",  # 设置编写时的python版本
    ],
    python_requires=">=3.4",  # 设置python版本要求
    install_requires=[
        "cn2an", "rich", "ntplib", "pyinstaller", "numpy", "sympy", "cython"
    ],  # 安装所需要的库
    # entry_points={
    #    "console_scripts": [""],
    # },  # 设置命令行工具(可不使用就可以注释掉)

)
