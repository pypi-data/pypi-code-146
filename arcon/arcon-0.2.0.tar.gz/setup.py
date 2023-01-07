# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcon']

package_data = \
{'': ['*']}

install_requires = \
['mergedeep>=1.3.4,<2.0.0', 'tomli>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'arcon',
    'version': '0.2.0',
    'description': 'Persistent runtime config',
    'long_description': 'arcon\n=====\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n.. image:: https://img.shields.io/pypi/v/arcon\n    :target: https://pypi.org/project/arcon/\n    :alt: PyPI\n.. image:: https://github.com/jshwi/arcon/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/arcon/actions/workflows/ci.yml\n    :alt: CI\n.. image:: https://results.pre-commit.ci/badge/github/jshwi/arcon/master.svg\n   :target: https://results.pre-commit.ci/latest/github/jshwi/arcon/master\n   :alt: pre-commit.ci status\n.. image:: https://github.com/jshwi/arcon/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/arcon/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://codecov.io/gh/jshwi/arcon/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/arcon\n    :alt: codecov.io\n.. image:: https://readthedocs.org/projects/arcon/badge/?version=latest\n    :target: https://arcon.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Black\n.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen\n    :target: https://github.com/PyCQA/pylint\n    :alt: pylint\n\nPersistent runtime config\n-------------------------\n\nChild class of ``argparse.ArgumentParser``\n\nIncludes version argument as a default\n\nDefault values are defined through pyproject.toml\n\nIncludes additional argument adding methods\n\n.. code-block:: python\n\n    >>> __version__ = "0.1.0"\n    >>> from arcon import ArgumentParser\n\nParsing comma separated list\n\n.. code-block:: python\n\n    >>> parser = ArgumentParser(__version__)\n    >>> parser.add_list_argument("-l", "--list")\n    >>> parser.parse_args(["--list", "comma,separated,list"])\n    Namespace(list=[\'comma\', \'separated\', \'list\'])\n\nParsing dict of comma separated lists\n\n.. code-block:: python\n\n    >>> parser = ArgumentParser(__version__)\n    >>> parser.add_dict_argument("-d", "--dict")\n    >>> parser.parse_args(["--dict", "key=comma,separated,list"])\n    Namespace(dict={\'key\': [\'comma\', \'separated\', \'list\']})\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': 'jshwi',
    'maintainer_email': 'stephen@jshwisolutions.com',
    'url': 'https://pypi.org/project/arcon/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
