# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygpeg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pygpeg',
    'version': '0.1.0',
    'description': 'Another PEG parser for Python',
    'long_description': "pygpeg\n======\n\n**pygpeg** (/pig'peg/) is a parsing expression grammar (PEG) library for\nPython. It allows you to generate a parser that allows you to parse\ncontext-free grammars into whatever structures you want.\n\n**pygpeg** combines the PEG syntax with the terse callback semantics found in\ntraditional parser generators like yacc or bison. \n",
    'author': 'Curtis Schlak',
    'author_email': 'foss@schlak.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://realistschuckle.gitlab.io/pygpeg',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
