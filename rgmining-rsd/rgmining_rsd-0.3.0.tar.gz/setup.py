# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rsd']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.0.0,<4.0.0', 'numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'rgmining-rsd',
    'version': '0.3.0',
    'description': 'An implementation of Review Spammer Detection algorithm',
    'long_description': 'An implementation of Review Spammer Detection\n=============================================\n\n|GPLv3| |Build Status| |Maintainability| |Test Coverage| |Release|\n\n|Logo|\n\nThis package provides an implementation of Review Spammer Detection\n(RSD) introduced in this paper:\n\n- `Guan Wang <https://www.linkedin.com/in/guanwang/>`__,\n  `Sihong Xie <https://engineering.lehigh.edu/faculty/sihong-xie>`__,\n  `Bing Liu <https://www.cs.uic.edu/~liub/>`__, and\n  `Philip S. Yu <https://www.cs.uic.edu/~psyu/>`__,\n  "`Review Graph Based Online Store Review Spammer Detection <https://ieeexplore.ieee.org/document/6137345?arnumber=6137345>`__,"\n  Proc. of `IEEE 11th International Conference on Data Mining <https://ieeexplore.ieee.org/xpl/conhome/6135855/proceeding>`__, 2011, pp. 1242-1247.\n\nSee `the documents <https://rgmining.github.io/rsd/>`__ for more\ninformation.\n\nInstallation\n------------\n\nUse ``pip`` to install this package.\n\n::\n\n    pip install --upgrade rgmining-rsd\n\nLicense\n-------\n\nThis software is released under The GNU General Public License Version\n3, see `COPYING <COPYING>`__ for more detail.\n\n.. |GPLv3| image:: https://img.shields.io/badge/license-GPLv3-blue.svg\n   :target: https://www.gnu.org/copyleft/gpl.html\n.. |Build Status| image:: https://github.com/rgmining/rsd/actions/workflows/python-lib.yaml/badge.svg\n   :target: https://github.com/rgmining/rsd/actions/workflows/python-lib.yaml\n.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/6461704a370307ee0d55/maintainability\n   :target: https://codeclimate.com/github/rgmining/rsd/maintainability\n.. |Test Coverage| image:: https://api.codeclimate.com/v1/badges/6461704a370307ee0d55/test_coverage\n   :target: https://codeclimate.com/github/rgmining/rsd/test_coverage\n.. |Release| image:: https://img.shields.io/badge/release-0.3.0-brightgreen.svg\n   :target: https://pypi.org/project/rgmining-rsd/\n.. |Logo| image:: https://rgmining.github.io/synthetic/_static/image.png\n   :target: https://rgmining.github.io/rsd/\n',
    'author': 'Junpei Kawamoto',
    'author_email': 'kawamoto.junpei@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://rgmining.github.io/rsd/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
