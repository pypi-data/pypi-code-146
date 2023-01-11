# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swidget']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1',
 'anyio',
 'asyncclick>=8',
 'importlib-metadata',
 'pydantic>=1,<2',
 'ssdp==1.1.1']

extras_require = \
{'docs': ['sphinx>=4,<5',
          'm2r>=0,<1',
          'mistune<2.0.0',
          'sphinx_rtd_theme>=0,<1',
          'sphinxcontrib-programoutput>=0,<1']}

entry_points = \
{'console_scripts': ['swidget = swidget.cli:cli']}

setup_kwargs = {
    'name': 'python-swidget',
    'version': '0.0.11',
    'description': 'Python API for Swidget smart devices',
    'long_description': '# python-swidget\nA library to manage Swidget smart devices\n',
    'author': 'Swidget',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/swidget/python-swidget',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
