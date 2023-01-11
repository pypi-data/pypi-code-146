# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
import os
import re


with open('README.rst',encoding='utf-8') as f:
    readme = f.read()


def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

with open(os.path.join('vbmc', '__init__.py'), 'r', encoding='utf8') as f:
    version = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(f.read()).group(1)
setup(
    name='vbmc',
    version=version,
    license='MIT License',
    description='CPU version of Voxel-based Monte Carlo simulation',
    long_description=readme,
    long_description_content_type = 'text/x-rst',
    author='Kaname Miura',
    author_email='miukana21@gmail.com',
    install_requires=read_requirements(),
    url='https://github.com/Kaname21Miura/vbmc.git',
    packages=find_packages(exclude=('tests', 'docs')),
)
