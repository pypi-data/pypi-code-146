from setuptools import setup, find_packages
import os
import platform
from urllib import request, parse

setup(
    name='crisppy',
    version='1.0.2',
    license='MIT',
    author="",
    author_email='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='crisp utils',
    install_requires=[
          'scikit-learn',
          'requests',
      ],
)
