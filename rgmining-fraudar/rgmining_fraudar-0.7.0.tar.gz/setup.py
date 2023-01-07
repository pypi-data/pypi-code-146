# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fraudar', 'fraudar.export']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0', 'scikit-learn>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'rgmining-fraudar',
    'version': '0.7.0',
    'description': 'A wrapper of Fraudar algorithm for Review graph mining project',
    'long_description': 'A wrapper of FRAUDAR algorithm\n==============================\n\n|GPLv3| |Build Status| |Maintainability| |Test Coverage| |Release|\n\n|Logo|\n\nThis package implements a wrapper of\n`FRAUDAR <https://bhooi.github.io/projects/fraudar/index.html>`__\nalgorithm to provide APIs defined in `Review Graph Mining\nproject <https://rgmining.github.io/>`__.\n\nInstallation\n------------\n\nUse ``pip`` to install this package.\n\n.. code:: shell\n\n    $pip install --upgrade rgmining-fraudar\n\nLicense\n-------\n\nThis software is released under The GNU General Public License Version\n3, see\n`COPYING <https://github.com/rgmining/fraudar/blob/master/COPYING>`__\nfor more detail.\n\nThe original FRAUDAR source code is made by `Bryan\nHooi <https://bhooi.github.io/index.html>`__, `Hyun Ah\nSong <http://www.cs.cmu.edu/~hyunahs/>`__, `Alex\nBeutel <http://alexbeutel.com/>`__, `Neil\nShah <http://nshah.net/>`__, `Kijung\nShin <https://kijungs.github.io/>`__, and `Christos\nFaloutsos <http://www.cs.cmu.edu/~christos/>`__, and licensed under\n`Apache License, Version 2.0 <LICENSE-2.0>`__. It is available at\nhttps://bhooi.github.io/projects/fraudar/index.html.\n\n.. |GPLv3| image:: https://img.shields.io/badge/license-GPLv3-blue.svg\n   :target: https://www.gnu.org/copyleft/gpl.html\n.. |Build Status| image:: https://github.com/rgmining/fraudar/actions/workflows/python-lib.yaml/badge.svg\n   :target: https://github.com/rgmining/fraudar/actions/workflows/python-lib.yaml\n.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/4c4c3df79b33f65b77cd/maintainability\n   :target: https://codeclimate.com/github/rgmining/fraudar/maintainability\n.. |Test Coverage| image:: https://api.codeclimate.com/v1/badges/4c4c3df79b33f65b77cd/test_coverage\n   :target: https://codeclimate.com/github/rgmining/fraudar/test_coverage\n.. |Release| image:: https://img.shields.io/badge/release-0.7.0-brightgreen.svg\n   :target: https://pypi.org/project/rgmining-fraudar/\n.. |Logo| image:: https://rgmining.github.io/fraudar/_static/image.png\n   :target: https://rgmining.github.io/fraudar/\n',
    'author': 'Junpei Kawamoto',
    'author_email': 'kawamoto.junpei@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://rgmining.github.io/fraudar/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
