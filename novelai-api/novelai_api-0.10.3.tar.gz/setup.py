# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['novelai_api', 'novelai_api.tokenizers']

package_data = \
{'': ['*'],
 'novelai_api': ['presets/presets_2.7B/*',
                 'presets/presets_6B_v4/*',
                 'presets/presets_euterpe_v2/*',
                 'presets/presets_genji_jp_6b_v2/*',
                 'presets/presets_genji_python_6b/*',
                 'presets/presets_hypebot/*',
                 'presets/presets_infillmodel/*',
                 'presets/presets_krake_v2/*',
                 'schemas/*',
                 'templates/*']}

install_requires = \
['PyNaCl>=1.5.0,<2.0.0',
 'aiohttp[speedups]>=3.8.3,<4.0.0',
 'argon2-cffi>=21.3.0,<22.0.0',
 'ftfy>=6.1.1,<7.0.0',
 'jsonschema>=4.17.0,<5.0.0',
 'regex>=2022.10.31,<2023.0.0',
 'tokenizers>=0.13.1,<0.14.0']

setup_kwargs = {
    'name': 'novelai-api',
    'version': '0.10.3',
    'description': 'Python API for the NovelAI REST API',
    'long_description': '# novelai-api\nPython API for the NovelAI REST API\n\nThis module is intended to be used by developers as a helper for using NovelAI\'s REST API.\n\n[TODO]: # (Add Quality Checking workflows and badges)\n\n| Category         | Badges                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |\n|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| Pypi             | [![PyPI](https://img.shields.io/pypi/v/novelai-api)](https://pypi.org/project/novelai-api) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/novelai-api)](https://pypi.org/project/novelai-api) [![PyPI - License](https://img.shields.io/pypi/l/novelai-api)](https://pypi.org/project/novelai-api/) [![PyPI - Format](https://img.shields.io/pypi/format/novelai-api)](https://pypi.org/project/novelai-api/)                                                                                                                                                                                                                                                                                               |\n| Quality checking | [![Python package](https://github.com/Aedial/novelai-api/actions/workflows/python-package.yml/badge.svg)](https://github.com/Aedial/novelai-api/actions/workflows/python-package.yml) [![Python package](https://github.com/Aedial/novelai-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Aedial/novelai-api/actions/workflows/codeql-analysis.yml) [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) |\n| Stats            | [![GitHub top language](https://img.shields.io/github/languages/top/Aedial/novelai-api)](https://github.com/Aedial/novelai-api/search?l=python) ![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Aedial/novelai-api) ![GitHub repo size](https://img.shields.io/github/repo-size/Aedial/novelai-api) ![GitHub issues](https://img.shields.io/github/issues-raw/Aedial/novelai-api) ![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/Aedial/novelai-api)                                                                                                                                                                                                         |\n| Activity         | ![GitHub last commit](https://img.shields.io/github/last-commit/Aedial/novelai-api) ![GitHub commits since tagged version](https://img.shields.io/github/commits-since/Aedial/novelai-api/v0.10.1) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Aedial/novelai-api)                                                                                                                                                                                                                                                                                                                                                                                                                              |\n\n\n### Prerequisites\nBefore anything, ensure that nox is installed (pip install poetry).\nFor logging in, credentials are needed (NAI_USERNAME and NAI_PASSWORD). They should be passed via the environment variables.\n\n### Examples\nThe examples are in the example folder. Each example is standalone and can be used as a test.\nExamples should be ran with `nox -s run -- python example/<name>.py`.\n\nSome tests act as example. The full list is as follows :\n- decryption and re-encryption: tests/test_decrypt_encrypt_integrity_check.py\n- diverse generations: tests/test_generate.py\n- parallel generations: tests/test_generate_parallel.py\n\n### Usage\nThe source and all the required functions are located in the novelai-api folder.\nThe examples and tests showcase how this API should be used and can be regarded as the "right way" to use it. However, it doesn\'t mean one can\'t use the "low level" part, which is a thin implementation of the REST endpoints, while the "high level" part is an abstraction built on that low level.\n\n### Contributing\nYou can contribute features and enhancements through PR. Any PR should pass the tests and the pre-commits before submission.\n\nThe tests against the API can be ran with `nox -s test_api`. Note that having node.js installed is required for the test to run properly\n/!\\ WIP /!\\ The tests against the mocked backend can be ran with `nox -s test_mock`.\n\nTo install and run the pre-commit hook, run `nox -s pre-commit`. This hook should be installed before committing anything.\n',
    'author': 'Aedial',
    'author_email': 'aedial.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Aedial/novelai-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
