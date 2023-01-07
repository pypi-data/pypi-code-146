# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nvd_api', 'nvd_api.api', 'nvd_api.apis', 'nvd_api.model', 'nvd_api.models']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2022.12.7,<2023.0.0',
 'frozendict>=2.3.4,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'setuptools>=65.6.3,<66.0.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'urllib3>=1.26.13,<2.0.0']

entry_points = \
{'console_scripts': ['push = tools.push:main',
                     'release = tools.release:main',
                     'sbom = tools.sbom:main',
                     'sphinx = tools.sphinx:main']}

setup_kwargs = {
    'name': 'nvd-api',
    'version': '0.3.3',
    'description': 'NVD API 2.0 Python API',
    'long_description': '=================\nnvd-api\n=================\n\nNVD API 2.0 client\n\n.. image:: https://badge.fury.io/py/nvd-api.svg\n    :target: https://badge.fury.io/py/nvd-api\n\n.. image:: https://github.com/kannkyo/nvd-api/actions/workflows/python-ci.yml/badge.svg\n    :target: https://github.com/kannkyo/nvd-api/actions/workflows/python-ci.yml\n\n.. image:: https://codecov.io/gh/kannkyo/nvd-api/branch/main/graph/badge.svg?token=ASYLVG3X9O\n    :target: https://codecov.io/gh/kannkyo/nvd-api\n\n.. image:: https://github.com/kannkyo/nvd-api/actions/workflows/scorecards.yml/badge.svg\n    :target: https://github.com/kannkyo/nvd-api/actions/workflows/scorecards.yml\n\n.. image:: https://bestpractices.coreinfrastructure.org/projects/6051/badge\n    :target: https://bestpractices.coreinfrastructure.org/projects/6051\n\n',
    'author': 'kannkyo',
    'author_email': '15080890+kannkyo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kannkyo/nvd-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
