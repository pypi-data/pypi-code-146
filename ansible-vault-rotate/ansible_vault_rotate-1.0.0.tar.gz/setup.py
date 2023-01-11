# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansible_vault_rotate',
 'ansible_vault_rotate.cli',
 'ansible_vault_rotate.match',
 'ansible_vault_rotate.vault']

package_data = \
{'': ['*']}

install_requires = \
['ansible-core>=2.9.0,<3.0.0']

entry_points = \
{'console_scripts': ['ansible-vault-rotate = ansible_vault_rotate.cli.run:run']}

setup_kwargs = {
    'name': 'ansible-vault-rotate',
    'version': '1.0.0',
    'description': 'Advanced Python CLI to rotate the secret used for ansible vault inline secrets and files in a project',
    'long_description': 'python-ansible-vault-rotate\n===\n[![GitHub License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/trustedshops-public/spring-boot-starter-keycloak-path-based-resolver/blob/main/LICENSE)\n[![pre-commit](https://img.shields.io/badge/%E2%9A%93%20%20pre--commit-enabled-success)](https://pre-commit.com/)\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/trustedshops-public/python-ansible-vault-rotate/tree/main.svg?style=shield&circle-token=9c1ea1cc46c804b46f457772637c8481717b511a)](https://dl.circleci.com/status-badge/redirect/gh/trustedshops-public/python-ansible-vault-rotate/tree/main)\n[![codecov](https://codecov.io/gh/trustedshops-public/python-ansible-vault-rotate/branch/main/graph/badge.svg?token=6PJ1GJzIcB)](https://codecov.io/gh/trustedshops-public/python-ansible-vault-rotate)\n\nAdvanced Python CLI to rotate the secret used for ansible vault inline secrets and files in a project\n\n## Features\n\n- Reencrypt vault files\n- Reencrypt inline vaulted secrets\n\n## Installation\n\nIt is strongly recommended to use pipx instead of pip if possible:\n\n```sh\npipx install ansible-vault-rotate\n```\n\nOtherwise you can also use plain pip, but be warned that this might\ncollide with your ansible installation globally!\n\n```sh\npip install ansible-vault-rotate\n```\n\n## Usage\n\n### Rekey given vault secret with new secret specified on CLI\n\n```sh\nansible-vault-rotate --old-vault-secret-source file://my-vault-password --new-vault-secret-source my-new-secret\n```\n\n## Rekey only specific files (e.g. when using multiple keys per stage)\n\n```sh\nansible-vault-rotate --old-vault-secret-source file://my-vault-password-<stage> --new-vault-secret-source my-new-secret --file-glob-pattern group_vars/<stage>/*.yml\n```\n\n## Getting help about all args\n\n```sh\nansible-vault-rotate --help\n```\n\n## Development\n\nFor development, you will need:\n\n- Python 3.9 or greater\n- Poetry\n\n### Install\n\n```\npoetry install\n```\n\n### Run tests\n\n```\npoetry run pytest\n```\n',
    'author': 'Timo Reymann',
    'author_email': 'Timo.Reymann@trustedshops.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/trustedshops-public/python-ansible-vault-rotate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
