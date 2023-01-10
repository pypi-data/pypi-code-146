# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bite', 'bite.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bite-parser',
    'version': '0.2.1',
    'description': 'Asynchronous parser taking incremental bites out of your byte input stream.',
    'long_description': '.. image:: https://github.com/jgosmann/bite-parser/actions/workflows/ci.yml/badge.svg\n  :target: https://github.com/jgosmann/bite-parser/actions/workflows/ci.yml\n  :alt: CI and release pipeline\n.. image:: https://codecov.io/gh/jgosmann/bite-parser/branch/main/graph/badge.svg?token=O4M05YWNQK\n  :target: https://codecov.io/gh/jgosmann/bite-parser\n  :alt: Codecov coverage\n.. image:: https://img.shields.io/pypi/v/bite-parser\n  :target: https://pypi.org/project/bite-parser/\n  :alt: PyPI\n.. image:: https://img.shields.io/pypi/pyversions/bite-parser\n  :target: https://pypi.org/project/bite-parser/\n  :alt: PyPI - Python Version\n.. image:: https://img.shields.io/pypi/l/bite-parser\n  :target: https://pypi.org/project/bite-parser/\n  :alt: PyPI - License\n\nWelcome to bite-parser\n======================\n\n   Asynchronous parser taking incremental bites out of your byte input stream.\n\nThe bite-parser is a parser combinator library for Python.\nIt is similar to `PyParsing <https://github.com/pyparsing/pyparsing>`_\nin that it allows the construction of grammars for parsing\nfrom simple building blocks in pure Python.\nThis approach is also known as `Parsing Expression Grammar (PEG)\n<https://en.wikipedia.org/wiki/Parsing_expression_grammar>`_.\nWhile PyParsing\n(and many other Python parsing libraries)\nonly support string,\nbite-parser operates on bytes.\nIn addition,\nbite-parser makes use of `asyncio`\nand can asynchronously generate parsed items\nfrom an input stream.\n\nA typical use-case would be the parsing of a network protocol\nlike IMAP.\nIn fact,\nI wrote this library for the IMAP implementation of my\n`dmarc-metrics-exporter <https://github.com/jgosmann/dmarc-metrics-exporter>`_.\n\n.. note::\n   I have implemented the fundamental set of parsers,\n   which should allow constructing most or all grammars\n   recognizable by this type of parser.\n   However, many convenience or higher level parsers are not yet implemented.\n\n   Other areas that still need improvement are:\n\n   * Abilitiy to debug the parsing.\n   * Better error messages.\n   * Performance: Currently, only a basic recursive descent parser is\n     implemented which can exhibit exponential worst case performance.\n     This could be improved by implementing a packrat parser.\n\nImportant links\n---------------\n\n* `Documentation <https://jgosmann.github.io/bite-parser/docs/en/main/>`_\n* `GitHub repository <https://github.com/jgosmann/bite-parser>`_\n',
    'author': 'Jan Gosmann',
    'author_email': 'jan@hyper-world.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jgosmann/bite-parser/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
