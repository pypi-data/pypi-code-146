# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_commit_copyright']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML']

entry_points = \
{'console_scripts': ['pre-commit-copyright = pre_commit_copyright:main']}

setup_kwargs = {
    'name': 'pre-commit-copyright',
    'version': '0.1.2',
    'description': 'Pre commit hooh to update the copyright',
    'long_description': '# Pre commit to update the copyright header\n\n[pre-commit](https://pre-commit.com/) hook used to check if the copyright is up to date.\n\n### Adding to your `.pre-commit-config.yaml`\n\n```yaml\nrepos:\n  - repo: https://github.com/sbrunner/pre-commit-copyright\n    rev: <version> # Use the ref you want to point at\n    hooks:\n      - id: copyright\n```\n',
    'author': 'Stéphane Brunner',
    'author_email': 'stephane.brunner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hub.docker.com/r/sbrunner/pre-commit-copyright/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
