#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['rcdesign', 'rcdesign.is456']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'scipy', 'sympy']

extras_require = \
{'dev': ['flake8', 'black'],
 'doc': ['sphinx', 'myst-parser', 'sphinx-rtd-theme'],
 'test': ['pytest >=2.7.3', 'pytest-cov']}

setup(name='rcdesign',
      version='0.4.4',
      description='A Python package for reinforced concrete analysis and design as per IS 456:2000',
      author=None,
      author_email='Satish Annigeri <satish.annigeri@gmail.com>',
      url=None,
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      python_requires='>=3.7',
     )
