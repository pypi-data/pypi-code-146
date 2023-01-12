#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os 
from setuptools import setup, find_packages

MAJOR =1
MINOR =1
PATCH =5
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"

def get_install_requires():
    reqs = [
            'requests==2.28.1'
            ]
    return reqs
setup(
	name = "PdfSplitLogin",
	version = VERSION,
    author ="wangweidong",
    author_email = "17891967090@163.com",
    description='Dynamsoft Barcode Reader Python project',
    long_description_content_type="text/markdown",
	url = 'https://mail.163.com/js6/main.jsp?sid=PAlGWIYldfIQjfQTFYllFVEyKXidwtNk&df=mail163_letter#module=welcome.WelcomeModule%7C%7B%7D',
	long_description = open('README.md',encoding="utf-8").read(),
    python_requires=">=3.7",
    install_requires=get_install_requires(),
	packages = find_packages(),
 	license = 'Apache',
   	classifiers = [
       'License :: OSI Approved :: Apache Software License',
       'Natural Language :: English',
       'Operating System :: OS Independent',
       'Programming Language :: Python',
       'Topic :: Software Development :: Libraries :: Python Modules',

    ],
    #包含的类型
    package_data={'': ['*.csv', '*.txt','.toml', "*.pyd",'*.exe']}, #这个很重要
    include_package_data=True #也选上

)