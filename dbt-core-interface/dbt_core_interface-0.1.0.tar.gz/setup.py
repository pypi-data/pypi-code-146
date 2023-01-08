# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbt_core_interface']

package_data = \
{'': ['*']}

install_requires = \
['dbt-core>1.0.0,<1.4.0']

setup_kwargs = {
    'name': 'dbt-core-interface',
    'version': '0.1.0',
    'description': 'Dbt Core Interface',
    'long_description': "# Dbt Core Interface\n\n[![PyPI](https://img.shields.io/pypi/v/dbt-core-interface.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/dbt-core-interface.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/dbt-core-interface)][python version]\n[![License](https://img.shields.io/pypi/l/dbt-core-interface)][license]\n\n[![Read the documentation at https://dbt-core-interface.readthedocs.io/](https://img.shields.io/readthedocs/dbt-core-interface/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/z3z1ma/dbt-core-interface/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/z3z1ma/dbt-core-interface/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/dbt-core-interface/\n[status]: https://pypi.org/project/dbt-core-interface/\n[python version]: https://pypi.org/project/dbt-core-interface\n[read the docs]: https://dbt-core-interface.readthedocs.io/\n[tests]: https://github.com/z3z1ma/dbt-core-interface/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/z3z1ma/dbt-core-interface\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\nAn extremely simplified interface is provided to accomplish all of the following with no dependencies outside dbt-core:\n\n- Parse dbt project on disk loading dbt core classes into memory from a single class/interface\n\n- Automatic management of the adapter and thread-safe efficient connection pool reuse\n\n- Run SQL and get results in python fully independent of the dbt adapter which automatically enables support for many databases\n\n- Run SQL with dbt SQL from a single method call\n\n- Load macros at runtime enabling custom functionality in third party extensions without requiring the dbt packaging system to be managed in userland\n\n- Compile dbt jinja extremely fast and efficiently, thread-safe and stress tested at load via a fastapi server which live compiles SQL\n\n- Manage multiple dbt projects in a single process using the DbtProjectContainer class\n\n`dbt-core-interface` is a wrapper that allows developers to rapidly develop features and integrations for dbt. This project aims to serve as a place for the community to aggregate the best ways to interface with dbt. It is afforded a much faster iteration cycle and much more freedom due to it's independence from the dbt codebase. It is intended to act as an common library to dbt's existing APIs for developers. Implementations can land here and prove themselves out before landing in the dbt-core codebase and benefit all developers involved. Sqlfluff dbt templater, dbt-osmosis, dbt-fastapi which I am ripping out of dbt-osmosis, an impending metadata manager, a testing framework will all leverage this library. As dbt core evolves and stabilizes its python API, this project will evolve with it. This may manifest in simplification of certain methods but our goal is to maintain the API and focus on driving efficient, innovative/creative, and agile community driven integration patterns.\n\n## Requirements\n\n- The **only** requirement is dbt-core, tested with versions `1.0.*`, `1.1.*`, `1.2.*`, `1.3.*`\n\n## Installation\n\nYou can install _Dbt Core Interface_ via [pip] from [PyPI]:\n\n```console\n$ pip install dbt-core-interface\n```\n\n## Usage\n\nPlease see the [Api Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Dbt Core Interface_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/z3z1ma/dbt-core-interface/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/z3z1ma/dbt-core-interface/blob/main/LICENSE\n[contributor guide]: https://github.com/z3z1ma/dbt-core-interface/blob/main/CONTRIBUTING.md\n[api reference]: https://dbt-core-interface.readthedocs.io/en/latest/reference.html\n",
    'author': 'Alex Butler',
    'author_email': 'butler.alex2010@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/z3z1ma/dbt-core-interface',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
