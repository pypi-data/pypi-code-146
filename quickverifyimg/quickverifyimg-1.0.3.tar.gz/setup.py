import sys

import pkg_resources
from setuptools import find_packages, setup


# Package meta-data.
NAME = 'quickverifyimg'
DESCRIPTION = 'quick verify img'
URL = ''
EMAIL = 'fengzhiyuan@yy.com'
AUTHOR = 'Zhiyuan Feng'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.3'


# Setting.
def parse_requirements(filename):
    """ load requirements from a pip requirements file. (replacing from pip.req import parse_requirements)"""
    lineiter = (line.strip() for line in open(filename))
    reqs = [line for line in lineiter if line and not line.startswith("#")]
    return reqs



setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    license="MIT"
)
