# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modelbase_pde', 'modelbase_pde.utils']

package_data = \
{'': ['*']}

install_requires = \
['modelbase>=1.18.9,<2.0.0',
 'pybind11>=2.10.0,<3.0.0',
 'setuptools>=65.4.0,<66.0.0']

setup_kwargs = {
    'name': 'modelbase-pde',
    'version': '0.2.12',
    'description': 'A subpackage of modelbase that enables investigation of PDE models',
    'long_description': '# modelbase pde\n\n[![pipeline status](https://gitlab.com/marvin.vanaalst/modelbase-pde/badges/main/pipeline.svg)](https://gitlab.com/marvin.vanaalst/modelbase-pde/-/commits/main)\n[![coverage report](https://gitlab.com/marvin.vanaalst/modelbase-pde/badges/main/coverage.svg)](https://gitlab.com/marvin.vanaalst/modelbase-pde/-/commits/main)\n[![PyPi](https://img.shields.io/pypi/v/modelbase-pde)](https://pypi.org/project/modelbase-pde/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Downloads](https://pepy.tech/badge/modelbase-pde)](https://pepy.tech/project/modelbase-pde)\n\nSubpackage of the [modelbase](https://gitlab.com/ebenhoeh/modelbase) package.\n',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
