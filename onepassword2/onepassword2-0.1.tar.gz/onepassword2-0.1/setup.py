# -*- coding: utf-8 -*-
#!/usr/bin/python

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='onepassword2',
    version='0.1',
    description='A python wrapper for onepassword cli version 2',
    long_description=long_description,
    long_description_content_type="text/markdown",      
    url='https://github.com/krezreb/onepassword2',
    author='krezreb',
    author_email='josephbeeson@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    #install_requires=[
    #    'redis',
    #],
    zip_safe=False)





