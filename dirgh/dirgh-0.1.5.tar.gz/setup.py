# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dirgh']

package_data = \
{'': ['*'], 'dirgh': ['ci/*', 'ci/deployment/*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'trio>=0.20.0,<0.22.0']

entry_points = \
{'console_scripts': ['dirgh = dirgh.cli:run']}

setup_kwargs = {
    'name': 'dirgh',
    'version': '0.1.5',
    'description': 'With dirgh you can easily download a directory from GitHub programmatically from Python or using the CLI.',
    'long_description': 'None',
    'author': 'tiptenbrink',
    'author_email': '75669206+tiptenbrink@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
