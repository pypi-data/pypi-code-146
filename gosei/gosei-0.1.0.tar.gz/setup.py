# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gosei']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pillow>=9.4.0,<10.0.0']

entry_points = \
{'console_scripts': ['gosei = gosei.main:main']}

setup_kwargs = {
    'name': 'gosei',
    'version': '0.1.0',
    'description': '',
    'long_description': '# gosei\n\nMake a collage from two photos.\n\n# Installation\n\n```bash\npip install gosei\n```\n\n# Run\n\n```\ngosei -a /path/to/first/image -b /path/to/second/image -o /save/path\n```\n\n# Limitations\n\n- Only works with vertical photos in same size now\n',
    'author': 'sobamchan',
    'author_email': 'oh.sore.sore.soutarou@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
