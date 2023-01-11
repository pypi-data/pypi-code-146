# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocl']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'diskcache>=5.4.0,<6.0.0',
 'flufl.lock>=7.1.1,<8.0.0',
 'iterfzf>=0.5.0,<0.6.0',
 'playwright>=1.28.0,<2.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'selenium>=4.3.0,<5.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ocl = ocl.__main__:app']}

setup_kwargs = {
    'name': 'openshift-cluster-login',
    'version': '0.11.0',
    'description': 'Openshift cluster login on command line',
    'long_description': '![logo](images/logo-white-bg.png)\n# OCL (OpenShift Login)\n\n[![PyPI](https://img.shields.io/pypi/v/openshift-cluster-login)][pypi-link]\n[![PyPI platforms][pypi-platforms]][pypi-link]\n![PyPI - License](https://img.shields.io/pypi/l/openshift-cluster-login)\n[![Release and Package Application](https://github.com/chassing/ocl/actions/workflows/release.yaml/badge.svg)](https://github.com/chassing/ocl/actions/workflows/release.yaml)\n\nOCL does an automatic login to an OpenShift cluster. It fetches cluster information from app-interface and performs a login via [Selenium](https://selenium-python.readthedocs.io).\n\n## Installation\n\nYou can install this library from [PyPI][pypi-link] with `pip`:\n\n\n```shell\n$ python3 -m pip install openshift-cluster-login\n```\n\nor install it with `pipx`:\n```shell\n$ pipx install openshift-cluster-login\n```\n\nYou can also use `pipx` to run the library without installing it:\n\n```shell\n$ pipx run openshift-cluster-login\n```\n\n## Usage\n\n```shell\n$ ocl\n```\n\n<img src="demo/quickstart.gif"/>\n\nThis spawns a new shell with the following environment variables are set:\n\n* `KUBECONFIG` - path to kubeconfig file\n* `OCL_CLUSTER_NAME` - cluster name\n* `OCL_CLUSTER_CONSOLE` - url to cluster console\n\n## Features\n\nOCL currently provides the following features (get help with `-h` or `--help`):\n\n- OpenShift console login (oc login) via GitHub authentication\n- Get cluster information from app-interface or user-defined (`OCL_USER_CLUSTERS``)\n- Open OpenShift console in browser (`--open-in-browser`)\n- Shell completion (`--install-completion`, `--show-completion`)\n- Credentials via environment variables or shell command (e.g. [1password CLI](https://developer.1password.com/docs/cli/))\n\n\n## Environment Variables\n\n| Variable Name                                       | Description                                                                                                                                 | Required           | Default |\n| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------- |\n| OCL_GITHUB_USERNAME OCL_GITHUB_USERNAME_COMMAND     | Your GitHub username                                                                                                                        | :heavy_check_mark: |         |\n| OCL_GITHUB_PASSWORD OCL_GITHUB_PASSWORD_COMMAND     | Your GitHub password (e.g. command `op read op://Private/Github/password`)                                                                  | :heavy_check_mark: |         |\n| OCL_GITHUB_TOTP OCL_GITHUB_TOTP_COMMAND             | Your GitHub two factor token (e.g. command `op item get Github --otp`)                                                                      | :heavy_check_mark: |         |\n| OCL_WAIT OCL_WAIT_COMMAND                           | Selenium webdriver wait timeout                                                                                                             |                    | 2       |\n| OCL_APP_INTERFACE_URL OCL_APP_INTERFACE_URL_COMMAND | App-Interface URL                                                                                                                           | :heavy_check_mark: |         |\n| OCL_APP_INT_TOKEN OCL_APP_INT_TOKEN_COMMAND         | App-Interface authentication token                                                                                                          | :heavy_check_mark: |         |\n| USER_CLUSTERS USER_CLUSTERS_COMMAND                 | User defined clusters as json format (e.g. `[{"name": "local-kind", "serverUrl": "https://localhost:6443", "consoleUrl": "not available}]`) |                    | "[]"    |\n\nYou can either set a variable, e.g. `export OCL_GITHUB_USERNAME="mail@example.com"` or retrieve it via a command, e.g. `export OCL_GITHUB_USERNAME_COMMAND="op read op://Private/Github/username"`\n\n\n## Limitations\n\n* MacOS only\n* Only Selenium `webdriver.Chrome` is supported and must be installed manually\n  ```shell\n  $ brew install --cask chromedriver\n  ```\n\n\n## Development\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n\nUse [Conventional Commit messages](https://www.conventionalcommits.org).\nThe most important prefixes you should have in mind are:\n\n* `fix:` which represents bug fixes, and correlates to a [SemVer](https://semver.org/)\n  patch.\n* `feat:` which represents a new feature, and correlates to a SemVer minor.\n* `feat!:`,  or `fix!:`, `refactor!:`, etc., which represent a breaking change\n  (indicated by the `!`) and will result in a SemVer major.\n* `chore: release` to create a new release\n\nConsider using an empty commit:\n\n```\ngit commit --allow-empty -m "chore: release"\n```\n\nWhen a commit to the main branch has `Release-As: x.x.x` (case insensitive) in the **commit body**, Release Please will open a new pull request for the specified version.\n```\ngit commit --allow-empty -m "chore: release 2.0.0" -m "Release-As: 2.0.0"\n```\n\n\n[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github\n[github-discussions-link]:  https://github.com/chassing/ocl/discussions\n[pypi-link]:                https://pypi.org/project/openshift-cluster-login/\n[pypi-platforms]:           https://img.shields.io/pypi/pyversions/openshift-cluster-login\n[pypi-version]:             https://badge.fury.io/py/openshift-cluster-login.svg\n',
    'author': 'Christian Assing',
    'author_email': 'cassing@redhat.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/chassing/ocl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
