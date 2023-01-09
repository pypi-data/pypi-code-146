# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['qtbplot']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'qtb-plot',
    'version': '0.3.1',
    'description': 'Standard plotting styles of our institute',
    'long_description': '# QTB Plot\n\n[![pipeline status](https://gitlab.com/marvin.vanaalst/qtb-plot/badges/main/pipeline.svg)](https://gitlab.com/marvin.vanaalst/qtb-plot/-/commits/main)\n[![coverage report](https://gitlab.com/marvin.vanaalst/qtb-plot/badges/main/coverage.svg)](https://gitlab.com/marvin.vanaalst/qtb-plot/-/commits/main)\n[![PyPi](https://img.shields.io/pypi/v/qtb-plot)](https://pypi.org/project/qtb-plot/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Downloads](https://pepy.tech/badge/qtb-plot)](https://pepy.tech/project/qtb-plot)\n\nThis package is basically just a convenience matplotlib option setter.\nYou have two ways of using it.\nWith `set_style` you set the style for the entire notebook or whatever session\nyou are working in and with `plotting_context` you create a context manager\nthat will only set the style locally for the current plot.\n\nTake a look at the supplied tutorial notebok to see how this is done.\n\n\nThe easiest way of installing the package is to cd into the package folder and to install it locally with\n`pip install -e .`\n',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/marvin.vanaalst/qtb-plot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
