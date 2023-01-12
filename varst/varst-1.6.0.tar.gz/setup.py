# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['varst', 'varst.utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['varst = varst.cli:main']}

setup_kwargs = {
    'name': 'varst',
    'version': '1.6.0',
    'description': 'Replace substitutions in rst files with variables.',
    'long_description': '==============================\nvarST(var ➡️ reStructuredText)\n==============================\n\n|PyPI version| |Github Actions| |pre-commit.ci status| |GitHub Workflow Status| |Documentation Status|\n\nReplace substitutions in rst files with variables.\n\nGetting Started\n===============\n\ncli\n-------\n\n   See |Quickstart Documentation Page|_.\n\n.. code:: bash\n\n   $ pip install varst\n   $ varst -h  # --help\n\nGithub Actions\n--------------\n\nvarST can be integrated with ``Github Actions``.\nPlease refer to this link_ and apply it to your own workflows.\n\nContributing\n============\n\nContribution Guideline\n----------------------\n\nPlease read the |contributing guidelines|_ to learn how to contribute to this project.\n\nReporting Issues\n----------------\n\nIf you have any questions, suggestions, or bug reports, please feel free to report them to the issue.\n\nCode of Conduct\n---------------\n\nThis project is governed by the |code of conduct|_.\n\nLicense\n=======\n\n`MIT\nLicense <https://github.com/junghoon-vans/varst/blob/main/LICENSE>`__\n\n.. |Quickstart Documentation Page| replace:: quickstart documentation\n.. _Quickstart Documentation Page: https://varst.readthedocs.io/en/latest/index.html#quickstart\n\n.. |PyPI version| image:: https://img.shields.io/pypi/v/varst\n   :target: https://pypi.org/project/varst/\n.. |Github Actions| image:: https://img.shields.io/badge/Actions-black?logo=github\n   :target: https://github.com/marketplace/actions/rst-substitution\n.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/junghoon-vans/varst/main.svg\n   :target: https://results.pre-commit.ci/latest/github/junghoon-vans/varst/main\n.. |GitHub Workflow Status| image:: https://img.shields.io/github/actions/workflow/status/junghoon-vans/varst/python-publish.yml?branch=v1.6.0\n.. |Documentation Status| image:: https://readthedocs.org/projects/varst/badge/?version=latest\n    :target: https://varst.readthedocs.io/en/latest/?badge=latest\n\n.. _link: https://github.com/marketplace/actions/rst-substitution\n\n.. |contributing guidelines| replace:: contributing guidelines\n.. _contributing guidelines: ./CONTRIBUTING.md\n.. |code of conduct| replace:: Code of Conduct\n.. _Code Of Conduct: ./CODE_OF_CONDUCT.md\n',
    'author': 'junghoon-vans',
    'author_email': 'junghoon.ban@gmail.com',
    'maintainer': 'junghoon-vans',
    'maintainer_email': 'junghoon.ban@gmail.com',
    'url': 'https://github.com/junghoon-vans/varst',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
