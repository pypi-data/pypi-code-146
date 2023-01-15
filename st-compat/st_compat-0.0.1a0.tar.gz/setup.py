# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['st_compat', 'st_compat.runtime']

package_data = \
{'': ['*']}

install_requires = \
['streamlit>=0.65']

setup_kwargs = {
    'name': 'st-compat',
    'version': '0.0.1a0',
    'description': 'Module to make it easier to build streamlit modules by implementing standard retro-compatiblity',
    'long_description': '# stqdm\n[![Tests](https://github.com/Wirg/st-compat/actions/workflows/tests.yml/badge.svg)](https://github.com/Wirg/st-compat/actions/workflows/tests.yml)\n[![CodeQL](https://github.com/Wirg/st-compat/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Wirg/st-compat/actions/workflows/codeql-analysis.yml)\n[![codecov](https://codecov.io/github/Wirg/st-compat/branch/main/graph/badge.svg?token=DSA23TOBWV)](https://codecov.io/github/Wirg/st-compat)\n\n`st-compat` is the simplest way to handle compatibility between streamlit versions when building utils and modules for the community!\n\n## How to install\n\n```sh\npip install st-compat\n```\n\n## How to use\n\n```python\nfrom st_compat import get_script_run_ctx\n\nctx = get_script_run_ctx()\n```\n',
    'author': 'Wirg',
    'author_email': 'Wirg@users.noreply.github.com',
    'maintainer': 'Wirg',
    'maintainer_email': 'Wirg@users.noreply.github.com',
    'url': 'https://github.com/Wirg/st_compat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
