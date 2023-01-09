# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teiphy']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.9.1,<5.0.0',
 'numpy>=1.23.2,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.4,<2.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['teiphy = teiphy.main:app']}

setup_kwargs = {
    'name': 'teiphy',
    'version': '0.1.4',
    'description': 'Converts TEI XML collations to NEXUS and other formats',
    'long_description': '.. start-badges\n\n.. image:: https://raw.githubusercontent.com/jjmccollum/teiphy/main/docs/img/teiphy-logo.svg\n\n|license badge| |testing badge| |coverage badge| |docs badge| |black badge| |git3moji badge| \n|iqtree badge| |raxml badge| |mrbayes badge| |stemma badge| |joss badge| |doi badge|\n\n.. |license badge| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat\n    :target: https://choosealicense.com/licenses/mit/\n\n.. |testing badge| image:: https://github.com/jjmccollum/teiphy/actions/workflows/testing.yml/badge.svg\n    :target: https://github.com/jjmccollum/teiphy/actions/workflows/testing.yml\n\n.. |docs badge| image:: https://github.com/jjmccollum/teiphy/actions/workflows/docs.yml/badge.svg\n    :target: https://jjmccollum.github.io/teiphy\n    \n.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    \n.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/jjmccollum/62997df516f95bbda6eaefa02b9570aa/raw/coverage-badge.json\n    :target: https://jjmccollum.github.io/teiphy/coverage/\n\n.. |git3moji badge| image:: https://img.shields.io/badge/git3moji-%E2%9A%A1%EF%B8%8F%F0%9F%90%9B%F0%9F%93%BA%F0%9F%91%AE%F0%9F%94%A4-fffad8.svg\n    :target: https://robinpokorny.github.io/git3moji/\n\n.. |iqtree badge| image:: https://github.com/jjmccollum/teiphy/actions/workflows/iqtree.yml/badge.svg\n    :target: https://github.com/jjmccollum/teiphy/actions/workflows/iqtree.yml\n\n.. |raxml badge| image:: https://github.com/jjmccollum/teiphy/actions/workflows/raxml.yml/badge.svg\n    :target: https://github.com/jjmccollum/teiphy/actions/workflows/raxml.yml\n\n.. |mrbayes badge| image:: https://github.com/jjmccollum/teiphy/actions/workflows/mrbayes.yml/badge.svg\n    :target: https://github.com/jjmccollum/teiphy/actions/workflows/mrbayes.yml\n\n.. |stemma badge| image:: https://github.com/jjmccollum/teiphy/actions/workflows/stemma.yml/badge.svg\n    :target: https://github.com/jjmccollum/teiphy/actions/workflows/stemma.yml\n\n.. |joss badge| image:: https://joss.theoj.org/papers/e0a813f4cdf56e9f6ae5d555ce6ed93b/status.svg\n    :target: https://joss.theoj.org/papers/e0a813f4cdf56e9f6ae5d555ce6ed93b\n    \n.. |doi badge| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7455638.svg\n   :target: https://doi.org/10.5281/zenodo.7455638\n\n.. end-badges\n\n.. start-about\n\nA Python package for converting TEI XML collations to NEXUS and other formats.\n\nTextual scholars have been using phylogenetics to analyze manuscript traditions since the early 1990s.\nMany standard phylogenetic software packages accept as input the `NEXUS file format <https://doi.org/10.1093/sysbio/46.4.590>`_.\nThe ``teiphy`` program takes a collation of texts encoded using the `Text Encoding Initiative (TEI) guidelines <https://tei-c.org/release/doc/tei-p5-doc/en/html/TC.html>`_\nand converts it to a NEXUS format so that it can be used for phylogenetic analysis.\nIt can also convert to other formats as well.\n\n\n.. end-about\n\n\n.. start-quickstart\n\nInstallation\n============\n\nThe software can be installed using ``pip``:\n\n.. code-block:: bash\n\n    pip install teiphy\n\nAlternatively, you can install the package by cloning this repository and installing it with poetry:\n\n.. code-block:: bash\n\n    git clone https://github.com/jjmccollum/teiphy.git\n    cd teiphy\n    poetry install\n\nOnce the package is installed, you can run all unit tests via the command\n\n.. code-block:: bash\n\n    poetry run pytest\n\nUsage\n============\n\nTo use the software, run the ``teiphy`` command line tool:\n\n.. code-block:: bash\n\n    teiphy <input TEI XML> <output file>\n\n``teiphy`` can export to NEXUS, Hennig86 (TNT), PHYLIP (in the relaxed form used by RAxML), FASTA, CSV, TSV, Excel and STEMMA formats. \n``teiphy`` will try to infer the file format to export to from the extension of the output file. Accepted file extensions are:\n".nex", ".nexus", ".nxs", ".ph", ".phy", ".fa", ".fasta", ".tnt", ".csv", ".tsv", ".xlsx".\n\nTo explicitly say which format you wish to export to, use the ``--format`` option. For example:\n\n.. code-block:: bash\n\n    teiphy <input TEI XML> <output file> --format nexus\n\nFor more information about the other options, see the help with:\n\n.. code-block:: bash\n\n    teiphy --help\n\nOr see the documentation with explanations about `advanced usage <https://jjmccollum.github.io/teiphy/advanced.html>`_.\n\nThe software can also be used in Python directly. \nSee `API Reference <https://jjmccollum.github.io/teiphy/reference.html>`_ in the documentation for more information.\n\n.. end-quickstart\n\nCredits\n============\n\n.. start-credits\n\n``teiphy`` was designed by Joey McCollum (Australian Catholic University) and Robert Turnbull (University of Melbourne).\nWe received additional help from Stephen C. Carlson (Australian Catholic University).\n\nIf you use this software, please cite the paper: Joey McCollum and Robert Turnbull, "``teiphy``: A Python Package for Converting TEI XML Collations to NEXUS and Other Formats," *JOSS* 7.80 (2022): 4879, DOI: 10.21105/joss.04879.\n\n.. code-block:: bibtex\n\n    @article{McCollum2022, \n        author = {Joey McCollum and Robert Turnbull}, \n        title = {{teiphy: A Python Package for Converting TEI XML Collations to NEXUS and Other Formats}}, \n        journal = {Journal of Open Source Software},\n        year = {2022}, \n        volume = {7}, \n        number = {80}, \n        pages = {4879},\n        publisher = {The Open Journal}, \n        doi = {10.21105/joss.04879}, \n        url = {https://doi.org/10.21105/joss.04879}\n    }\n\n\n.. end-credits\n',
    'author': 'Joey McCollum and Robert Turnbull',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jjmccollum/teiphy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
