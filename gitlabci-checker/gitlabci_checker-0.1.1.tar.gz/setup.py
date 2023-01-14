# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlabci_checker']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['cicheck = gitlabci_checker.cli:cli']}

setup_kwargs = {
    'name': 'gitlabci-checker',
    'version': '0.1.1',
    'description': 'Checks if your gitlab-ci pipeline compiles correctly.',
    'long_description': '# Gitlabci checker\n\n![release](https://img.shields.io/github/v/release/lorenzophys/gitlabci-checker)\n[![codecov](https://codecov.io/gh/lorenzophys/gitlabci-checker/branch/main/graph/badge.svg?token=WEZ1UH621Y)](https://codecov.io/gh/lorenzophys/gitlabci-checker)\n[![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/lorenzophys/gitlabci-checker/test-workflow.yml?branch=main&label=tests)](https://img.shields.io/github/actions/workflow/status/lorenzophys/gitlabci-checker/test-workflow.yml)\n![pver](https://img.shields.io/pypi/pyversions/gitlabci-checker)\n![MIT](https://img.shields.io/github/license/lorenzophys/gitlabci-checker)\n\n## Installation\n\nYou can install `gitlabci-checker` via `pip`:\n\n```console\nuser@laptop:~$ pip install gitlabci-checker\n```\n\nYou can interact with the CLI via the `cicheck` comand:\n\n```console\nuser@laptop:~$ cicheck\nUsage: cicheck [OPTIONS] FILENAME\n\n  Check if your gitlab-ci pipeline compiles correctly.\n\nOptions:\n  -h, --help                 Show this message and exit.\n  -v, --version              Show the version and exit.\n  -t, --token TEXT           Your Gitlab access token: by default the content\n                             of the GITLAB_TOKEN variable is used.  [required]\n  -s, --gitlab-server TEXT   The Gitlab server hostname.  [required]\n  -k, --insecure             Use insecure connection (http).\n  -w, --warnings-are-errors  Force the failure if warnings are found.\n```\n\n## How it works?\n\n`cicheck` just calls the [Gitlab CI lint API](https://docs.gitlab.com/15.7/ee/api/lint.html) with the file you pass to it.\n\nBy default it will send the request to `gitlab.com`. If you want to use your own Gitlab instance you must pass the server address:\n\n```console\nuser@laptop:~$ cicheck .gitlab-ci.yaml --gitlab-server code.company.com\nEverything\'s fine.\n```\n\nYou must pass a valid token to the CLI: either as the environment variable `GITLAB_TOKEN` or via the `--token` flag.\n\n## Usage example\n\nIf your pipeline is valid it returns a "Everything\'s fine." message\n\n```console\nuser@laptop:~$ cicheck .gitlab-ci.yaml\nEverything\'s fine.\n```\n\nIf your configuration is invalid it returns an error message together with the response from Gitlab:\n\n```console\nuser@laptop:~$ cicheck .gitlab-ci.yaml\nCheck failed with error(s).\n{\n  "status": "invalid",\n  "errors": [\n    "variables config should be a hash of key value pairs"\n  ],\n  "warnings": []\n}\n```\n\nYou can also force a failure whenever the linter returns a warning by appending `--warnings-are-errors` or `-w`:\n\n```console\nuser@laptop:~$ cicheck .gitlab-ci.yaml\nCheck failed with warning(s).\n{\n  "status": "valid",\n  "errors": [],\n  "warnings": ["jobs:job may allow multiple pipelines to run for a single action due to\n  `rules:when` clause with no `workflow:rules` - read more:\n  https://docs.gitlab.com/ee/ci/troubleshooting.html#pipeline-warnings"]\n}\n```\n\n## `pre-commit` hook\n\n`gitlabci-checker` can be also used as a [pre-commit](https://pre-commit.com) hook. For example:\n\n```yaml\nrepos:\n  - repo: https://github.com/lorenzophys/gitlabci-checker\n    rev: v0.1.1\n    hooks:\n      - id: gitlabci-checker\n        args:\n          - --gitlab-server code.company.com\n          - --warnings-are-errors\n```\n\n## License\n\nThis project is licensed under the **MIT License** - see the *LICENSE* file for details.\n',
    'author': 'Lorenzo Maffioli',
    'author_email': 'lorenzo.maffioli@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lorenzophys/gitlabci-checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
