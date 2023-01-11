#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "cniptest",      #这里是pip项目发布的名称
    version = "3.0.2",  #版本号，数值大的会优先被pip
    keywords = ["pip", "ip", "ipv6", "cniptest", "pypi","bj","nj"],			# 关键字
    description = "一个可以获取ip地址的Python库",	# 描述
    long_description=open('README.md',encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    license = "MIT Licence",		# 许可证

    url = "https://gitee.com/codeqihan/cniptest",     #项目相关文件地址，一般是github项目地址即可
    author = "codeqihan",			# 作者
    author_email = "qh@codeqihan.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests"]          #这个项目依赖的第三方库
)