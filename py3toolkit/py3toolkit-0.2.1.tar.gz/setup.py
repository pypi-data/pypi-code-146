# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py3toolkit']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['gen_supervisor_conf = '
                     'py3toolkit.gen_supervisor_conf:main']}

setup_kwargs = {
    'name': 'py3toolkit',
    'version': '0.2.1',
    'description': 'my python3 toolkit for daily use',
    'long_description': 'None',
    'author': 'codeskyblue',
    'author_email': 'codeskyblue@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
