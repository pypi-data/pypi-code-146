# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chime_frb_api',
 'chime_frb_api.backends',
 'chime_frb_api.core',
 'chime_frb_api.modules',
 'chime_frb_api.stations',
 'chime_frb_api.tests',
 'chime_frb_api.workflow',
 'chime_frb_api.workflow.daemons']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'click>=7',
 'pydantic>=1.10.2,<2.0.0',
 'pyjwt>=2,<3',
 'python-dateutil>=2,<3',
 'requests>=2,<3']

extras_require = \
{'docs': ['mkdocs-material>=8',
          'pytkdocs[numpy-style]>=0.10',
          'mkdocstrings[python]>=0.18']}

entry_points = \
{'console_scripts': ['frb-api = chime_frb_api.cli:cli',
                     'workflow = chime_frb_api.workflow.cli:cli']}

setup_kwargs = {
    'name': 'chime-frb-api',
    'version': '2.3.3',
    'description': 'CHIME/FRB API',
    'long_description': '# CHIME/FRB API\n\n|   **`Testing`**   | **`Coverage`**  |  **`Release`**  |   **`Style`**   |\n|-----------------|-----------------|-----------------|-----------------|\n| [![Continuous Integration](https://github.com/CHIMEFRB/frb-api/actions/workflows/ci.yml/badge.svg)](https://github.com/CHIMEFRB/frb-api/actions/workflows/ci.yml) | [![Coverage Status](https://coveralls.io/repos/github/CHIMEFRB/frb-api/badge.svg?t=uYdqsa)](https://coveralls.io/github/CHIMEFRB/frb-api) | [![PyPI version](https://img.shields.io/pypi/v/chime-frb-api.svg)](https://pypi.org/project/chime-frb-api/) | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)\n\n--------\n\n`chime-frb-api` is a python library to access CHIME/FRB backend. This library enables you interact with resources such as databases, event headers, calibration products, cluster jobs etc.\n\nCheck out the **[documentation](https://chimefrb.github.io/frb-api/)** for more details.\n\n## Installation\n\nThe latest stable version is available on [PyPI](https://pypi.org/project/chime-frb-api/).\nTo install `chime-frb-api` simply run,\n\n```bash\npip install --upgrade chime-frb-api\n```\n\nTo add `chime-frb-api` to your project,\n\n```bash\npoetry add chime-frb-api\n```\n\n## Documentation\n\nFor further reading, please refer to the [documentation](https://chimefrb.github.io/frb-api/).\n',
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CHIMEFRB/frb-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
