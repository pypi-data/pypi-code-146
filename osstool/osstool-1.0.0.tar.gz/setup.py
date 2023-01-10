#!/usr/bin/env python


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='osstool',
    version='1.0.0',
    description='OSS Python SDK',
    author='wangyingbin',
    author_email='869063218@qq.com',
    long_description=readme,
    packages=['oss'],
    install_requires=['requests!=2.9.0', 'crcmod>=1.7'],
    include_package_data=True,
    url='https://github.com/ybwang0211/oss-python-sdk'
)