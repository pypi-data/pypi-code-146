# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['schatsi',
 'schatsi.jobs',
 'schatsi.models',
 'schatsi.processor',
 'schatsi.reader']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF>=1.20.2,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'dask[diagnostics,distributed]>=2022.10.0,<2023.0.0',
 'docx2python==2.0.4',
 'loguru>=0.6.0,<0.7.0',
 'nltk>=3.7,<4.0',
 'pandas>=1.5.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['schatsi = schatsi.cli:cli']}

setup_kwargs = {
    'name': 'schatsi',
    'version': '0.1.20',
    'description': '',
    'long_description': '# (f)SCHA.T.S.I\n\n(f)SCHA.T.S.I - An abbreviation for \'**f**aster **SCH**eduling *A*lgorithm for **T**ext **S**each **I**ntelligence\'.\n\n\n## Getting Started\nhttps://python-poetry.org/\n```\npip install poetry\npoetry lock\n.venv\\Scripts\\activate\npoetry config virtualenvs.in-project true\npoetry install\n```\n\nGenerate documentation\n----------------------\n\nTheme documentation: https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html\napidoc documentation: https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html\n\n\nos.environ["SPHINX_APIDOC_OPTIONS"]="members,show-inheritance"\n\nWindows\n\n```shell\ncd docs\nsphinx-apidoc -lfM -d 0 -o drg_analytic/ ../src/drg_analytic\n.\\make.bat html\n```\n\nMac/Linux\n\n```shell\ncd docs\nsphinx-apidoc -lfM -d 0 -o drg_analytic/ ../src/drg_analytic\nmake html\n```',
    'author': 'robnoflop',
    'author_email': 'info@robertkasseck.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/robnoflop/Schatsi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.8,<4.0.0',
}


setup(**setup_kwargs)
