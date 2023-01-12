# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bblocks',
 'bblocks.analysis_tools',
 'bblocks.cleaning_tools',
 'bblocks.dataframe_tools',
 'bblocks.import_tools',
 'bblocks.import_tools.debt',
 'bblocks.other_tools']

package_data = \
{'': ['*'], 'bblocks.import_tools': ['stored_data/*', 'stored_data/wfp_raw/*']}

install_requires = \
['PyPDF2>=2.11.2,<3.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'camelot-py>=0.10.1,<0.11.0',
 'country-converter>=0.8.0,<0.9.0',
 'numpy>=1.24.1,<2.0.0',
 'opencv-python>=4.7.0,<5.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pyarrow>=10.0.1,<11.0.0',
 'pyjstat>=2.3.0,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'wbgapi<1.1',
 'weo>=0.7.4,<0.8.0']

setup_kwargs = {
    'name': 'bblocks',
    'version': '0.5.1',
    'description': 'A package with tools to download and analyse international development data.',
    'long_description': 'The bblocks package\n===================\n\n|pypi| |python| |Documentation| |codecov|\n\n\n**bblocks** is a python package with tools to download and analyse\ndevelopment data. These tools are meant to be the *building blocks* of\nfurther analysis.\n\n**bblocks** is currently in active development. Functionality and APIs\nare very likely to change. We welcome feedback, feature requests, and\ncollaboration. We hope that this will be a valuable resource for\norganisations working with sustainable development data.\n\n-  Documentation: https://bblocks.readthedocs.io/\n-  GitHub: https://github.com/ONECampaign/bblocks\n-  PyPI: https://pypi.org/project/bblocks/\n-  Free software: MIT\n\nInstallation\n------------\n\nbblocks can be installed from PyPI: from the command line:\n\n.. code-block:: python\n\n   pip install bblocks\n\nAlternatively, the source code is available on\n`GitHub <https://github.com/ONECampaign/bblocks>`__.\n\nBasic usage\n-----------\n\nbblocks is in active development. Check back regularly for new features.\nWe will be adding example jupyter notebooks for some of the main\nfeatures. Be sure to check the issues or projects section to learn more\nabout the features that we are planning to add.\n\nQuestions?\n----------\n\nPlease feel free to reach out via GitHub or at data at one.org\n\n.. |pypi| image:: https://img.shields.io/pypi/v/bblocks.svg\n   :target: https://pypi.org/project/bblocks/\n.. |python| image:: https://img.shields.io/pypi/pyversions/bblocks.svg\n   :target: https://pypi.org/project/bblocks/\n.. |codecov| image:: https://codecov.io/gh/ONECampaign/bblocks/branch/main/graph/badge.svg?token=YN8S1719NH\n   :target: https://codecov.io/gh/ONECampaign/bblocks\n.. |Documentation| image:: https://readthedocs.org/projects/bblocks/badge/?version=latest\n   :target: https://bblocks.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n',
    'author': 'The ONE Campaign',
    'author_email': 'data@one.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ONECampaign/bblocks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
