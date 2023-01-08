# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycirclize', 'pycirclize.parser', 'pycirclize.utils']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'pycirclize',
    'version': '0.1.1',
    'description': 'Circular visualization in Python',
    'long_description': '# pyCirclize: Circular visualization in Python\n\n![Python3](https://img.shields.io/badge/Language-Python3-steelblue)\n![OS](https://img.shields.io/badge/OS-_Windows_|_Mac_|_Linux-steelblue)\n![License](https://img.shields.io/badge/License-MIT-steelblue)\n[![Latest PyPI version](https://img.shields.io/pypi/v/pycirclize.svg)](https://pypi.python.org/pypi/pycirclize)\n[![conda-forge](https://img.shields.io/conda/vn/conda-forge/pycirclize.svg?color=green)](https://anaconda.org/conda-forge/pycirclize)\n[![CI](https://github.com/moshi4/pyCirclize/actions/workflows/ci.yml/badge.svg)](https://github.com/moshi4/pyCirclize/actions/workflows/ci.yml)\n\n## Table of contents\n\n- [Overview](#overview)\n- [Installation](#installation)\n- [API Usage](#api-usage)\n- [Not Implemented Features](#not-implemented-features)\n\n## Overview\n\npyCirclize is a circular visualization python package implemented based on matplotlib.\nThis package is developed for the purpose of easily and beautifully plotting circular figure such as Circos Plot and Chord Diagram in Python.\nIn addition, useful genome and phylogenetic tree visualization methods for the bioinformatics field are also implemented.\npyCirclize was inspired by [circlize](https://github.com/jokergoo/circlize) and [pyCircos](https://github.com/ponnhide/pyCircos).\nMore detailed documentation is available [here](https://moshi4.github.io/pyCirclize/).\n\n![pyCirclize_gallery.png](https://raw.githubusercontent.com/moshi4/pyCirclize/main/docs/images/pyCirclize_gallery.png)  \n**Fig.1 pyCirclize example plot gallery**\n\n## Installation\n\n`Python 3.8 or later` is required for installation.\n\n**Install PyPI package:**\n\n    pip install pycirclize\n\n**Install conda-forge package:**\n\n    conda install -c conda-forge pycirclize\n\n## API Usage\n\nAPI usage is described in each of the following sections in the [document](https://moshi4.github.io/pyCirclize/).\n\n- [Getting Started](https://moshi4.github.io/pyCirclize/getting_started/)\n- [Plot API Example](https://moshi4.github.io/pyCirclize/plot_api_example/)\n- [Chord Diagram](https://moshi4.github.io/pyCirclize/chord_diagram/)\n- [Circos Plot (Genomics)](https://moshi4.github.io/pyCirclize/circos_plot/)\n- [Phylogenetic Tree](https://moshi4.github.io/pyCirclize/phylogenetic_tree/)\n\n## Not Implemented Features\n\nList of features implemented in other Circos plotting tools but not yet implemented in pyCirclize.\nI may implement them when I feel like it.\n\n- Plot histogram\n- Plot boxplot\n- Plot violin\n- Plot raster image\n- Label position auto adjustment\n',
    'author': 'moshi4',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://moshi4.github.io/pyCirclize/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
