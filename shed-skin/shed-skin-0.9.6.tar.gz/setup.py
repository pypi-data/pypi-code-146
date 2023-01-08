# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shedskin', 'shedskin.lib', 'shedskin.lib.os']

package_data = \
{'': ['*'], 'shedskin': ['templates/cpp/*'], 'shedskin.lib': ['builtin/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'blessings>=1.7,<2.0', 'progressbar2>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['shedskin = shedskin.__main__:run']}

setup_kwargs = {
    'name': 'shed-skin',
    'version': '0.9.6',
    'description': 'Shed Skin is a restricted-Python-to-C++ compiler.',
    'long_description': ".. image:: https://img.shields.io/travis/shedskin/shedskin.svg\n    :target: https://travis-ci.org/shedskin/shedskin\n\n.. image:: http://img.shields.io/badge/benchmarked%20by-asv-green.svg?style=flat\n    :target: http://shedskin.github.io/benchmarks\n\nShed Skin\n=========\n\nShed Skin is an experimental compiler, that can translate pure, but implicitly statically typed Python (3.8+) programs into optimized C++. It can generate stand-alone programs or extension modules that can be imported and used in larger Python programs.\n\nBesides the typing restriction, programs cannot freely use the Python standard library (although about 25 common modules, such as random and re, are currently supported). Also, not all Python features, such as nested functions and variable numbers of arguments, are supported (see the `documentation <https://shedskin.readthedocs.io/>`_ for details).\n\nFor a set of `75 non-trivial programs <https://github.com/shedskin/shedskin/tree/master/examples>`_ (at over 25,000 lines in total (sloccount)), measurements show a typical speedup of 2-200 times over CPython.\n\n\nUsage\n-----\n\n::\n    shedskin test.py\n    make\n    ./test\n\n\nRestrictions\n------------\n\nShed Skin only supports a restricted subset of Python, so one should not expect a given program to compile without any changes, if possible at all. See the `documentation <https://shedskin.readthedocs.io/>`_ for an overview of the limitations.\n\n\n\nInstallation\n------------\n\nShed Skin depends on some others projects, such as the `Boehm garbage collector <https://www.hboehm.info/gc/>`_. Please see the `documentation`_ on how to install these.\n\n\n\nComparison\n----------\n\nSome timings for the shedskin 'sieve' example (n=100000000) and several Python implementations/optimizers:\n\n::\n\n    cpython 3.10.6:   13.4 seconds\n    cpython 3.11.0:   11.4\n    nuitka 0.6.16:   11.4\n    pypy 3.9.12:     5.8\n    shedskin 0.9.6:  1.9\n\nScreenhots\n----------\n\nSome screenshots of the `example programs <https://github.com/shedskin/shedskin/tree/master/examples>`_ in action:\n\n.. image:: https://raw.githubusercontent.com/shedskin/shedskin/master/examples/screenshots/harm3.png\n  :width: 400\n\n.. image:: https://raw.githubusercontent.com/shedskin/shedskin/master/examples/screenshots/harm4.png\n  :width: 400\n\n.. image:: https://raw.githubusercontent.com/shedskin/shedskin/master/examples/screenshots/harm2.png\n  :width: 400\n\n.. image:: https://raw.githubusercontent.com/shedskin/shedskin/master/examples/screenshots/harm1.png\n  :width: 400\n\n\nContributors\n------------\n\nThe following people have contributed to Shed Skin development:\n\n::\n\n  Shakeeb Alireza\n  Hakan Ardo\n  Brian Blais\n  Paul Boddie\n  François Boutines\n  Djamel Cherif\n  James Coughlan\n  Mark Dewing\n  Mark Dufour\n  Artem Egorkine\n  Michael Elkins\n  Moataz Elmasry\n  Enzo Erbano\n  Ernesto Ferro\n  Salvatore Ferro\n  FFAO\n  Victor Garcia\n  Luis M. Gonzales\n  Fahrzin Hemmati\n  Folkert van Heusden\n  Karel Heyse\n  Johan Kristensen\n  Kousuke\n  Denis de Leeuw Duarte\n  Van Lindberg\n  David Marek\n  Douglas McNeil\n  Andy Miller\n  Jeff Miller\n  Danny Milosavljevic\n  Joaquin Abian Monux\n  John Nagle\n  Harri Pasanen\n  Brent Pedersen\n  Joris van Rantwijk\n  Retsyo\n  Pierre-Marie de Rodat\n  Jérémie Roquet\n  Mike Schrick\n  SirNotAppearingInThisTutorial\n  Paul Sokolevsky\n  Thomas Spura\n  Joerg Stippa\n  Dan Stromberg\n  Dave Tweed\n  Jaroslaw Tworek\n  Tony Veijalainen\n  Pavel Vinogradov\n  Jason Ye\n  Liu Zhenhai\n  Joris van Zwieten\n\n\n\n",
    'author': 'Mark Dufour and contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://shedskin.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
