# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mts']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn']

setup_kwargs = {
    'name': 'mt-system',
    'version': '0.1.4',
    'description': 'Python library of MT system.',
    'long_description': '# MT-system\n\nPython library of MT system.\n\n## Dependencies\n\nThis library requires:\n\n- Python (>=3.8)\n\n## Installation\n\nIt can be installed as follows using pip:\n\n```shell\npip install -U mt-system\n```\n\n## Usage\n\nDescribe how to use the library in this part.\n\n## Development\n\nDevelopment requires:\n\n- Python (>=3.8)\n- Poetry\n- Git (Option)\n- Make (Option)\n\n### Source code\n\nYou can check the latest sources with the command:\n\n```shell\ngit clone https://github.com/stfukuda/mt-system.git\n```\n\n### Enviroment\n\nAfter cloning the repository, you can install the development environment with the command:\n\n```shell\nmake install\n```\n\n### Testing\n\nAfter installation, you can run the test with the command:\n\n```shell\nmake test\n```\n\n### Submitting a Pull Request\n\nIf the test passes, send the pull request according to the format.\n\n## License\n\n[BSD-3-Clause License](LICENSE)\n',
    'author': 'Shota Fukuda',
    'author_email': 'st_fukuda@outlook.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/stfukuda/mt-system.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
