# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from qrunner import __version__, __description__

try:
    long_description = open(os.path.join('qrunner', "README.md"), encoding='utf-8').read()
except IOError:
    long_description = ""

setup(
    name="qrunner",
    version=__version__,
    description=__description__,
    author="杨康",
    author_email="772840356@qq.com",
    url="https://gitee.com/bluepang2021/qrunner_new",
    platforms="Android,IOS,Web,Api",
    packages=find_packages(),
    long_description=long_description,
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ],
    include_package_data=True,
    package_data={
        r'': ['*.yml'],
    },
    install_requires=[
        'tidevice==0.6.1',
        'facebook-wda==1.4.6',
        'uiautomator2==2.16.13',
        'selenium==4.1.3',
        'webdriver-manager==3.5.2',
        'pytest==6.2.5',
        'pytest-rerunfailures==10.2',
        'pytest-ordering==0.6',
        'pytest-xdist==2.5.0',
        'pytest-dependency==0.5.1',
        'allure-pytest==2.9.45',
        'jmespath==0.9.5',
        'PyYAML==6.0',
        'PyMySQL==0.10.1',
        'pymongo==4.0.1',
        'yagmail==0.15.293',
        'jsonschema==4.17.0',
        'genson==1.2.2',
        'deepdiff==6.2.1',
        'easyocr==1.6.2',
        'opencv-python==4.6.0.66',
        'opencv-contrib-python==4.6.0.66',
        'opencv-python-headless==3.4.18.65'
    ],
    extras_require={
        "excel": ['pandas==1.3.4', 'openpyxl==3.0.9', 'XlsxWriter==3.0.2'],
        "jira": ['jira==3.1.1'],
        "encrypt": ['pycryptodome==3.14.1'],
    },
    entry_points={
        'console_scripts': [
            'qrunner = qrunner.cli:main'
        ]
    },
)
