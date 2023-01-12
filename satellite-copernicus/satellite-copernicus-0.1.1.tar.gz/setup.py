# -*- coding: utf-8 -*-
from setuptools import setup

package_data = {'': ['*'], 'satellite': ['dist/*']}

packages = [
    'downloader',
    'downloader.utils',
    'weather',
    'weather.utils',
]

install_requires = [
    'MetPy>=1.4.0,<2.0.0',
    'SQLAlchemy>=1.4.46,<2.0.0',
    'cdsapi>=0.5.1,<0.6.0',
    'loguru>=0.6.0,<0.7.0',
    'netCDF4>=1.6.2,<2.0.0',
    'numpy>=1.24.1,<2.0.0',
    'psycopg2-binary>=2.9.5,<3.0.0',
    'python-dotenv>=0.21.0,<0.22.0',
    'xarray>=2022.12.0,<2023.0.0',
]

setup_kwargs = {
    'name': 'satellite-copernicus',
    'version': '0.1.1',
    'license':'MIT',
    'description': 'satellite-weather-downloader PYPI package',
    'long_description': None,
    'author': 'Luã Bida Vacaro',
    'author_email': 'luabidaa@gmail.com',
    'maintainer': 'Luã Bida Vacaro',
    'maintainer_email': 'luabidaa@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}

setup(**setup_kwargs)
