# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tomte']

package_data = \
{'': ['*']}

extras_require = \
{'bandit': ['bandit==1.7.4'],
 'black': ['black==22.12.0'],
 'darglint': ['darglint==1.8.1'],
 'docs': ['mkdocs==1.4.2',
          'mkdocs-material==9.0.4',
          'mkdocs-macros-plugin==0.7.0',
          'Markdown==3.3.7',
          'markdown-include==0.8.0',
          'pydoc-markdown==4.6.4',
          'pydocstyle==6.2.3',
          'pymdown-extensions==9.9.1',
          'bs4==0.0.1',
          'Pygments==2.14.0'],
 'flake8': ['flake8==3.9.2',
            'flake8-bugbear==23.1.14',
            'flake8-docstrings==1.6.0',
            'flake8-eradicate==1.4.0',
            'flake8-isort==6.0.0',
            'pydocstyle==6.2.3'],
 'isort': ['isort==5.11.4'],
 'mypy': ['mypy==0.991'],
 'pylint': ['pylint==2.13.9'],
 'safety': ['safety==2.3.5'],
 'tests': ['pytest==7.2.1',
           'pytest-asyncio==0.20.3',
           'pytest-cov==4.0.0',
           'pytest-randomly==3.12.0',
           'pytest-rerunfailures==11.0'],
 'tox': ['tox==3.28.0'],
 'vulture': ['vulture==2.7']}

setup_kwargs = {
    'name': 'tomte',
    'version': '0.2.1',
    'description': 'A library that wraps many useful tools (linters, analysers, etc) to keep Python code clean, secure, well-documented and optimised.',
    'long_description': 'None',
    'author': 'David Minarsch',
    'author_email': 'david.minarsch@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
