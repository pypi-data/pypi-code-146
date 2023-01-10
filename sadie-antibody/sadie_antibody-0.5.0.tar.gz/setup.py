# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sadie',
 'sadie.airr',
 'sadie.airr.airrtable',
 'sadie.airr.igblast',
 'sadie.airr.models',
 'sadie.cluster',
 'sadie.numbering',
 'sadie.receptor',
 'sadie.reference',
 'sadie.renumbering',
 'sadie.renumbering.aligners',
 'sadie.renumbering.clients',
 'sadie.typing',
 'sadie.utility']

package_data = \
{'': ['*'],
 'sadie.airr': ['bin/darwin/*',
                'bin/linux/*',
                'bin/windows/*',
                'data/germlines/*',
                'data/germlines/Ig/blastdb/clk/*',
                'data/germlines/Ig/blastdb/dog/*',
                'data/germlines/Ig/blastdb/human/*',
                'data/germlines/Ig/blastdb/macaque/*',
                'data/germlines/Ig/blastdb/mouse/*',
                'data/germlines/Ig/blastdb/rabbit/*',
                'data/germlines/Ig/blastdb/rat/*',
                'data/germlines/Ig/blastdb/se09/*',
                'data/germlines/Ig/internal_data/clk/*',
                'data/germlines/Ig/internal_data/dog/*',
                'data/germlines/Ig/internal_data/human/*',
                'data/germlines/Ig/internal_data/macaque/*',
                'data/germlines/Ig/internal_data/mouse/*',
                'data/germlines/Ig/internal_data/rabbit/*',
                'data/germlines/Ig/internal_data/rat/*',
                'data/germlines/Ig/internal_data/se09/*',
                'data/germlines/aux_db/imgt/*'],
 'sadie.reference': ['bin/darwin/*', 'bin/linux/*', 'bin/windows/*', 'data/*'],
 'sadie.renumbering': ['data/anarci/HMMs/*',
                       'data/hmms/*',
                       'data/stockholms/*']}

install_requires = \
['Levenshtein>=0.20.5,<0.21.0',
 'PyYAML>=6.0,<7.0',
 'biopython>=1.79',
 'click>=7.0',
 'filetype>=1.1.0,<2.0.0',
 'ipython>=8.5.0,<9.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.0,<1.5.0',
 'pyarrow>=6.0.1',
 'pydantic>=1.9.0,<2.0.0',
 'pyhmmer>=0.5.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'semantic-version>=2.10.0,<3.0.0',
 'yarl>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['sadie = sadie.app:sadie']}

setup_kwargs = {
    'name': 'sadie-antibody',
    'version': '0.5.0',
    'description': '"The Complete Antibody Library"',
    'long_description': '<!-- markdownlint-disable -->\n<h2 align="center" style="font-family:verdana;font-size:150%"> <b>S</b>equencing <b>A</b>nalysis and <b>D</b>ata Library for <b>I</b>mmunoinformatics <b>E</b>xploration</h2>\n<div align="center">\n  <img src="https://sadiestaticcrm.s3.us-west-2.amazonaws.com/Sadie.svg" alt="SADIE" style="margin:0.5em;width:50%">\n</div>\n\n<div class="flex-container" align="center">\n    <img src="https://github.com/jwillis0720/sadie/workflows/Linux%20Build%20and%20Test/badge.svg"\n         alt="Linux Build">\n    <a href="https://github.com/jwillis0720/sadie/workflows/MacOS%20Build%20and%20Test/badge.svg">\n    <img src="https://github.com/jwillis0720/sadie/workflows/MacOS%20Build%20and%20Test/badge.svg"\n         alt="Mac Build">\n    <a href="https://github.com/jwillis0720/sadie/actions/workflows/pyright.yml/badge.svg">\n    <img src="https://github.com/jwillis0720/sadie/actions/workflows/pyright.yml/badge.svg"\n         alt="Static Type">\n    <a href="https://img.shields.io/badge/Python-3.7%7C3.8%7C3.9%7C3.10-blue">\n    <img src="https://img.shields.io/badge/Python-3.7%7C3.8%7C3.9%7C3.10-blue"\n        alt="Python Version">\n    <a href="https://github.com/psf/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg"\n        alt="Format Version">\n    <a href="https://codecov.io/gh/jwillis0720/sadie">\n    <img src="https://codecov.io/gh/jwillis0720/sadie/branch/main/graph/badge.svg?token=EH9QEX4ZMP"\n        alt="Code Coverage">\n    <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"\n        alt="pre commit">\n    <a href="https://pypi.org/project/sadie-antibody">\n    <img src="https://img.shields.io/pypi/v/sadie-antibody?color=blue"\n        alt=\'pypi\'>\n    <a href="https://app.netlify.com/sites/sadie-docs/overview">\n    <img src="https://api.netlify.com/api/v1/badges/59ff956c-82d9-4900-83c7-758ed21ccb34/deploy-status"\n        alt="Documentation">\n    </a>\n</div>\n<!-- markdownlint-restore -->\n\n## About\n\n---\n\n<!-- use a href so you can use _blank to open new tab -->\n\n**Documentation**: <a href="https://sadie.jordanrwillis.com" target="_blank">https://sadie.jordanrwillis.com</a>\n\n**Source Code**: <a href="https://github.com/jwillis0720/sadie" target="_blank">https://github.com/jwillis0720/sadie</a>\n\n**Colab**: [https://colab.research.google.com/github/jwillis0720/sadie](https://colab.research.google.com/github/jwillis0720/sadie/blob/main/notebooks/airr_c/SADIE_DEMO.ipynb)\n\n---\n\nSADIE is the **S**equencing **A**nalysis and **D**ata library for **I**mmunoinformatics **E**xploration. The key feautures include:\n\n- Provide pre-built **command line applications** for popular immunoinformatics applications.\n\n- Provide a **low-level API framework** for immunoinformatics developers to build higher level tools.\n\n- Provide a **testable** and **reusable** library that WORKS!\n\n- Provide a **customizable** and **verified** germline reference library.\n\n- Maintain data formats consistent with standards governed by the [**AIRR community**](https://docs.airr-community.org/en/stable/#table-of-contents)\n\n- **Portability** ready to use out the box.\n\nSADIE is billed as a "**complete antibody library**", not because it aims to do everything, but because it aims to meet the needs of all immunoinformatics users. SADIE contains both low, mid and high level functionality for immunoinformatics tools and workflows. You can use SADIE as a framework to develop your own tools, use many of the prebuilt contributed tools, or run it in a notebook to enable data exploration. In addition, SADIE aims to port all code to python because relies heavily on the [Pandas](https://www.pandas.org) library, the workhorse of the data science/machine learning age.\n\n## Installation\n\n---\n\nInstallation is handled using the python package installer `pip`\n\n```console\n$ pip install sadie-antibody\n```\n\n### Development installation.\n\nPull requests are highly encouraged [here](https://github.com/jwillis0720/sadie/pulls). The development installation uses [pre-commit](https://pre-commit.com/), [flake8](https://flake8.pycqa.org/en/latest/) linting and [black](https://github.com/psf/black) style formatting to maintain code readability and reausability.\n\n```console\n$ git clone git@github.com/jwillis0720/sadie.git\n$ pip install poetry\n$ poetry install --with dev\n```\n\n## The Littlest Usage\n\nConsult the [documentation](https://sadie.jordanrwillis.com) for complete usage\n\n### Command Line Usage\n\nAnnotate antibody sequences only from functional human imgt antibodies to a gzip output\n\n```console\n$ airr -q my_sequecnes.fasta -s human -d imgt\n```\n\n### API\n\n```python\nfrom sadie.airr import Airr\n# define a single sequence\npg9_seq = """\n    CAGCGATTAGTGGAGTCTGGGGGAGGCGTGGTCCAGCCTGGGTCGTCCCTGAGACTCTCCTGTGCAGCGT\n    CCGGATTCGACTTCAGTAGACAAGGCATGCACTGGGTCCGCCAGGCTCCAGGCCAGGGGCTGGAGTGGGT\n    GGCATTTATTAAATATGATGGAAGTGAGAAATATCATGCTGACTCCGTATGGGGCCGACTCAGCATCTCC\n    AGAGACAATTCCAAGGATACGCTTTATCTCCAAATGAATAGCCTGAGAGTCGAGGACACGGCTACATATT\n    TTTGTGTGAGAGAGGCTGGTGGGCCCGACTACCGTAATGGGTACAACTATTACGATTTCTATGATGGTTA\n    TTATAACTACCACTATATGGACGTCTGGGGCAAAGGGACCACGGTCACCGTCTCGAGC""".replace(\n    "\\n", ""\n)\n\n# initialize the api\nair_api = Airr("human")\n\n# run single sequence\nairr_table = air_api.run_single("PG9", pg9_seq)\n```\n\n## License\n\n[![License](https://img.shields.io/github/license/jwillis0720/sadie)](https://opensource.org/licenses/MIT)\n\n- Copyright © Jordan R. Willis and Troy M. Sincomb\n',
    'author': 'Jordan R. Willis',
    'author_email': 'jwillis0720@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sadie.jordanrwillis.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
