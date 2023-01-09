# -*- coding: utf-8 -*-
# @Time : 2022/12/27 17:36
# @Author : jh
# @File : setup.py


from setuptools import setup, find_packages

setup(name='jhsi',
      version='0.0.1',
      description='use for test',
      author='jh',
      author_email='jhdyxa@163.com',
      requires=['ahocorasick'],
      packages=['mark'],
      zip_safe=True,
)

