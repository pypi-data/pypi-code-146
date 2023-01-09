# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.cadquery']

package_data = \
{'': ['*'],
 'sphinxcontrib.cadquery': ['static/dist/vtk-lite.js',
                            'static/dist/vtk-lite.js',
                            'static/dist/vtk-lite.js.LICENSE.txt',
                            'static/dist/vtk-lite.js.LICENSE.txt']}

install_requires = \
['Sphinx>=5.3.0,<6.0.0', 'ipython>=8.0.0,<9.0.0']

setup_kwargs = {
    'name': 'sphinxcontrib-cadquery',
    'version': '0.2.0',
    'description': 'Sphinx extension for rendering CadQuery models.',
    'long_description': '======================\nsphinxcontrib-cadquery\n======================\n\n|docs-status|\n\n\nA `Sphinx`_ extension for rendering `CadQuery`_ models.\n\n**Development Status :: 2 - Pre-Alpha**\n\n.. _Sphinx: https://www.sphinx-doc.org/\n.. _CadQuery: https://cadquery.readthedocs.io/\n\n.. |docs-status| image:: https://readthedocs.org/projects/sphinxcontrib-cadquery/badge/?version=latest\n    :target: https://sphinxcontrib-cadquery.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation status\n',
    'author': 'Seth Fischer',
    'author_email': 'seth@fischer.nz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sethfischer/sphinxcontrib-cadquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
