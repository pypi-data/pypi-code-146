# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memoframe']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'memoframe',
    'version': '0.1.4',
    'description': 'Python project that creates a package that optimize pandas dataframe',
    'long_description': '# 1. What is it ?\n\nmemoframe is a Python package that enables to easily optimize memory consumption of pandas dataframe. If you encounter OOM (Out of Memory) errors or slow downs during data analysis or model training.\n\n# 2. Where to get the package ?\n\nBinary installers for the latest released version are available at the Python Package Index (PyPI).\n\n    # PyPI \n    pip install memoframe\n\n# 3. Features \n\n- Optimize integer memory usage\n- Optimize float memory usage\n- Optimize object memory usage\n- Get an estimation of the memory usage saved\n\n# 4. How to use the library\n\n    from memoframe import memoframe as mf\n    \n    # dataframe is a pandas DataFram\n    optimized_dataframe = mf.downsize_memory(dataframe)\n\n    # Estimates memory usage gains\n    mf.get_opti_info(dataframe)\n',
    'author': 'Ilyes Braham',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
