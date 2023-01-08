# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geometry_to_spatialite']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.6.4,<3.0.0', 'pyshp>=2.1.0,<3.0.0', 'sqlite-utils>=2.1,<4.0']

entry_points = \
{'console_scripts': ['geojson-to-spatialite = '
                     'geometry_to_spatialite.geojson:main',
                     'shapefile-to-spatialite = '
                     'geometry_to_spatialite.shapefile:main']}

setup_kwargs = {
    'name': 'geometry-to-spatialite',
    'version': '0.4.0',
    'description': 'Import geographic and spatial data from files into a SpatiaLite DB',
    'long_description': '# geometry-to-spatialite\n\n[![Run tests](https://github.com/chris48s/geometry-to-spatialite/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/chris48s/geometry-to-spatialite/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/chris48s/geometry-to-spatialite/branch/master/graph/badge.svg?token=Y15Y63PPM4)](https://codecov.io/gh/chris48s/geometry-to-spatialite)\n[![PyPI Version](https://img.shields.io/pypi/v/geometry-to-spatialite.svg)](https://pypi.org/project/geometry-to-spatialite/)\n![License](https://img.shields.io/pypi/l/geometry-to-spatialite.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fgeometry-to-spatialite%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nImport geographic and spatial data from files into a SpatiaLite DB.\n\n## 📚 [Documentation](https://chris48s.github.io/geometry-to-spatialite)\n* [Installation](https://chris48s.github.io/geometry-to-spatialite/installation.html)\n* [Usage](https://chris48s.github.io/geometry-to-spatialite/usage.html)\n* [Troubleshooting](https://chris48s.github.io/geometry-to-spatialite/troubleshooting.html)\n',
    'author': 'chris48s',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chris48s/geometry-to-spatialite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
