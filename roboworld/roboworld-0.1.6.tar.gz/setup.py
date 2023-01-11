# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
    ['roboworld']

install_requires = \
    ['matplotlib', 'numpy']

package_data = \
    {'': ['*']}

keywords = ['education', 'gamification', 'cellular automaton', 'roboter', 'learning', 'beginners', 'computational thinking']

#long_description=long_description,
#long_description_content_type='text/x-rst',

long_description="""
``roboworld`` is an educational ``Python`` package designed for students to learn basic programming concepts, such as,

+ variables,
+ function calls,
+ conditionals,
+ loops and
+ recursion.

Students must navigate ``Robo`` (a robot) through different two-dimensional discrete ``Worlds``.
``Robo`` represents a very simplistic machine that can only deal with elementary instructions, i.e., method calls.
Therefore, students have to extend the missing functionality step by step.
Through this process they learn

1. to divide a problem into smaller pieces,
2. to abstract,
3. to recognize patterns, and
4. to design and implement algorithms.


The documentation can be found here: https://robo-world-doc.readthedocs.io/en/latest/index.html
"""

setup_kwargs = {
    'name': 'roboworld',
    'version': '0.1.6',
    'description': 'Educational roboter world to learn basic programming concepts.',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'author': 'Benedikt Zoennchen',
    'author_email': 'benedikt.zoennchen@web.de',
    'maintainer': 'BZoennchen',
    'maintainer_email': 'benedikt.zoennchen@web.de',
    'url': 'https://github.com/BZoennchen/robo-world',
    'packages': packages,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
    'keywords': keywords
}

setup(**setup_kwargs)
