# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gui',
 'roentgen',
 'roentgen.absorption',
 'roentgen.lines',
 'roentgen.tests',
 'roentgen.util']

package_data = \
{'': ['*'],
 'gui': ['templates/*'],
 'roentgen': ['data/README.rst',
              'data/README.rst',
              'data/README.rst',
              'data/README.rst',
              'data/README.rst',
              'data/README.rst',
              'data/README.rst',
              'data/compounds_mixtures.csv',
              'data/compounds_mixtures.csv',
              'data/compounds_mixtures.csv',
              'data/compounds_mixtures.csv',
              'data/compounds_mixtures.csv',
              'data/compounds_mixtures.csv',
              'data/compounds_mixtures.csv',
              'data/compounds_mixtures/*',
              'data/cxro/*',
              'data/electron_binding_energies.csv',
              'data/electron_binding_energies.csv',
              'data/electron_binding_energies.csv',
              'data/electron_binding_energies.csv',
              'data/electron_binding_energies.csv',
              'data/electron_binding_energies.csv',
              'data/electron_binding_energies.csv',
              'data/elements.csv',
              'data/elements.csv',
              'data/elements.csv',
              'data/elements.csv',
              'data/elements.csv',
              'data/elements.csv',
              'data/elements.csv',
              'data/elements/*',
              'data/emission_energies.csv',
              'data/emission_energies.csv',
              'data/emission_energies.csv',
              'data/emission_energies.csv',
              'data/emission_energies.csv',
              'data/emission_energies.csv',
              'data/emission_energies.csv',
              'data/emission_lines.csv',
              'data/emission_lines.csv',
              'data/emission_lines.csv',
              'data/emission_lines.csv',
              'data/emission_lines.csv',
              'data/emission_lines.csv',
              'data/emission_lines.csv',
              'data/siegbahn_to_iupac.csv',
              'data/siegbahn_to_iupac.csv',
              'data/siegbahn_to_iupac.csv',
              'data/siegbahn_to_iupac.csv',
              'data/siegbahn_to_iupac.csv',
              'data/siegbahn_to_iupac.csv',
              'data/siegbahn_to_iupac.csv']}

install_requires = \
['astropy>=5.1,<6.0', 'numpy>=1.23.3,<2.0.0', 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'roentgen',
    'version': '2.1.0',
    'description': 'A Python package for the quantitative analysis of the interaction of energetic x-rays with matter. This package is named after one of the discoverers of X-rays, Wilhelm Rontgen.',
    'long_description': '========\nOverview\n========\n\n.. start-badges\n\n.. list-table::\n    :stub-columns: 1\n\n    * - docs\n      - |docs|\n    * - build status\n      - |testing| |codestyle| |coverage|\n    * - package\n      - |version| |downloads| |wheel|\n\n.. |docs| image:: https://readthedocs.org/projects/roentgen/badge/?version=latest\n    :target: https://roentgen.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. |testing| image:: https://github.com/ehsteve/roentgen/actions/workflows/testing.yml/badge.svg\n    :target: https://github.com/ehsteve/roentgen/actions/workflows/testing.yml\n    :alt: Build Status\n\n.. |codestyle| image:: https://github.com/ehsteve/roentgen/actions/workflows/codestyle.yml/badge.svg\n    :target: https://github.com/ehsteve/roentgen/actions/workflows/codestyle.yml\n    :alt: Black linting\n\n.. |coverage| image:: https://codecov.io/gh/ehsteve/roentgen/branch/master/graph/badge.svg?token=feNCnYTjB3\n    :alt: Test coverage on codecov\n    :target: https://codecov.io/gh/ehsteve/roentgen\n\n.. |version| image:: https://img.shields.io/pypi/v/roentgen.svg?style=flat\n    :alt: PyPI Package latest release\n    :target: https://pypi.python.org/pypi/roentgen\n\n.. |downloads| image:: https://img.shields.io/pypi/dm/roentgen.svg?style=flat\n    :alt: PyPI Package monthly downloads\n    :target: https://pypi.python.org/pypi/roentgen\n\n.. |wheel| image:: https://img.shields.io/pypi/wheel/roentgen.svg?style=flat\n    :alt: PyPI Wheel\n    :target: https://pypi.python.org/pypi/roentgen\n\n.. end-badges\n\n.. image:: https://raw.githubusercontent.com/ehsteve/roentgen/main/docs/logo/roentgen_logo.svg\n    :height: 150\n    :width: 150\n\nA Python package for the quantitative analysis of the interaction of energetic x-rays with matter.\nThis package is named after one of the discoverers of X-rays, `Wilhelm Röntgen <https://en.wikipedia.org/wiki/Wilhelm_Röntgen>`_.\n\nInstallation\n============\n\n::\n\n    pip install roentgen\n\nThis project makes use of `Poetry <https://python-poetry.org>`_ for dependency management. To install this project for development, clone the repository and then run the following command inside the package directory\n\n::\n\n    poetry install --with dev,docs,gui\n\n\nDocumentation\n=============\n\nhttp://roentgen.readthedocs.io/en/stable/\n\nGUI\n===\nThis package provides a gui interface to quickly investigate the absorption and transmission of x-rays through different materials.\nIt is based on `bokeh <https://docs.bokeh.org/en/stable/>`_. To run it locally use the following command\n\n::\n\n   bokeh serve --show <roengten_directory>/gui\n\n\nData Sources\n============\nThis package includes on a number of data files which were translated and imported from a few key sources.\nThe package developers would like to thank the following data providers\n\n* The U.S National Institute of Standards and Technology (NIST)\n* The Center for X-ray Optics and Advanced Light Source at the Lawrence Berkeley National Laboratory\n\nFor more information see the `README <roentgen/data/README.rst>`_ in data directory.\n\nContributing\n============\n\nContributions are welcome, and they are greatly appreciated!\nEvery little bit helps, and credit will always be given.\nHave a look at the `great guide <https://docs.sunpy.org/en/latest/dev_guide/contents/newcomers.html>`__ from the `sunpy project <https://sunpy.org>`__ which provides advice for new contributors.\n\nCode of Conduct\n===============\n\nWhen you are interacting with members of this community, you are asked to follow the SunPy `Code of Conduct <https://sunpy.org/coc>`__.\n',
    'author': 'Steven Christe',
    'author_email': 'ehsteve@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ehsteve/roentgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
