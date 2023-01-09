# -*- coding: utf-8 -*-
# @Time : 2022/12/27 17:36
# @Author : jh
# @File : setup.py


from setuptools import setup, find_packages

setup(name='jhsan',
      version='0.0.1',
      description='use for test',
      author='jh',
      author_email='jhdyxa@163.com',
      requires=['ahocorasick'],
      packages=find_packages(),     # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      # packages=['代码1','代码2','__init__']   # 指定目录中需要打包的py文件，注意，不需要写后缀
      # license=''    # 支持的开源协议
       )
