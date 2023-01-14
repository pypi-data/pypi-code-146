# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['binformat']
setup_kwargs = {
    'name': 'binformat',
    'version': '1.0.1',
    'description': 'Implementation of the Permuatio wire format',
    'long_description': None,
    'author': 'Arcade Wise',
    'author_email': 'l3gacy.b3ta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/Patpine/binformat-py',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
