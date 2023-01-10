# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['git_tag_bump']
install_requires = \
['typer[all]>=0.7']

entry_points = \
{'console_scripts': ['git-bump = git_tag_bump:main']}

setup_kwargs = {
    'name': 'git-tag-bump',
    'version': '0.1',
    'description': '',
    'long_description': 'None',
    'author': 'Dmitry Voronin',
    'author_email': 'dimka665@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
