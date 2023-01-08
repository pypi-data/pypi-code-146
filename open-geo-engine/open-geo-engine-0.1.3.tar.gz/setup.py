# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_geo_engine',
 'open_geo_engine.config',
 'open_geo_engine.src',
 'open_geo_engine.utils']

package_data = \
{'': ['*']}

install_requires = \
['click-config-file>=0.6.0,<0.7.0',
 'click-option-group>=0.5.3,<0.6.0',
 'earthengine-api>=0.1.323,<0.2.0',
 'esda>=2.4.3,<3.0.0',
 'gcloud>=0.18.3,<0.19.0',
 'geemap>=0.16.9,<0.17.0',
 'geopandas>=0.11.1,<0.12.0',
 'google-streetview>=1.2.9,<2.0.0',
 'google>=3.0.0,<4.0.0',
 'ipykernel>=6.15.2,<7.0.0',
 'ipyleaflet>=0.17.1,<0.18.0',
 'joblib>=1.1.0,<2.0.0',
 'libpysal>=4.6.2,<5.0.0',
 'osmnx>=1.2.2,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy==1.9.1',
 'setuptools>=65.3.0,<66.0.0']

setup_kwargs = {
    'name': 'open-geo-engine',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'ChristinaLast',
    'author_email': 'christina.last@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
