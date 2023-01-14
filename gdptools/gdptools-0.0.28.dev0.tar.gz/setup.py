# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gdptools', 'gdptools.agg', 'gdptools.data', 'gdptools.weights', 'tests']

package_data = \
{'': ['*'],
 'tests': ['data/*',
           'data/DRB/*',
           'data/TM_WORLD_BORDERS_SIMPL-0.3/*',
           'data/rasters/TEXT_PRMS/*',
           'data/rasters/slope/*']}

install_requires = \
['Bottleneck>=1.3.3',
 'MetPy>=1.2.0',
 'Shapely<2.0.0',
 'attrs>=21.4.0',
 'dask>=2022.0.0',
 'geopandas>=0.11.0',
 'joblib>=1.1.0',
 'netCDF4<=1.6.1',
 'numpy<1.24.0',
 'pandas>=1.4.0',
 'pydantic>=1.9.0',
 'pygeos>=0.12.0',
 'pyproj>=3.3.0',
 'rasterio>=1.2.9',
 'rioxarray>=0.12.0',
 'scipy>=1.9.0',
 'xarray>=2022.6.0',
 'zarr>=2.12.0']

entry_points = \
{'console_scripts': ['gdptools = gdptools.__main__:main']}

setup_kwargs = {
    'name': 'gdptools',
    'version': '0.0.28.dev0',
    'description': 'Gdptools',
    'long_description': "# Readme\n\n[![PyPI](https://img.shields.io/pypi/v/gdptools.svg)](https://pypi.org/project/gdptools/)\n[![conda](https://anaconda.org/conda-forge/gdptools/badges/version.svg)](https://anaconda.org/conda-forge/gdptools)\n[![Latest Release](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/badges/release.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/releases)\n\n[![Status](https://img.shields.io/pypi/status/gdptools.svg)](https://pypi.org/project/gdptools/)\n[![Python Version](https://img.shields.io/pypi/pyversions/gdptools)](https://pypi.org/project/gdptools)\n\n[![License](https://img.shields.io/pypi/l/gdptools)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)\n\n[![Read the documentation at https://gdptools.readthedocs.io/](https://img.shields.io/readthedocs/gdptools/latest.svg?label=Read%20the%20Docs)](https://gdptools.readthedocs.io/)\n[![pipeline status](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/pipeline.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)\n[![coverage report](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/badges/main/coverage.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/-/commits/main)\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://code.usgs.gov/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://code.usgs.gov/psf/black)\n[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)\n[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)\n\n## Welcome\n\nWelcome to gdptools, a python package for grid- or polyon-to-polygon area-weighted interpolation statistics.\n\n![Welcome figure](./docs/assets/Welcom_fig.png)\n\n<figcaption>Example grid-to-polygon interpolation.  A) Huc12 basins for Delaware River Watershed. B) Gridded monthly water evaporation amount (mm) from TerraClimate dataset. C) Area-weighted-average interpolation of gridded TerraClimate data to Huc12 polygons.</figcaption>\n\n## Documentation\n\n[gdptools documentation](https://gdptools.readthedocs.io/en/latest/)\n\n## Features\n\n- Grid-to-polygon interpolation of area-weighted statistics.\n- Use [Mike Johnson's OPeNDAP catalog][1] to access over 1700 unique datasets.\n- Use any gridded dataset that can be read by xarray.\n- Uses spatial index methods for improving the efficiency of areal-wieght calculation detailed by [Geoff Boeing][2]\n\n[1]: https://mikejohnson51.github.io/opendap.catalog/articles/catalog.html\n[2]: https://geoffboeing.com/2016/10/r-tree-spatial-index-python/\n\n### Example catalog datasets\n\n| Dataset                                                                                    | Description                                                                                                                                                                                                                                                                                                    | Dates                      | Links |\n| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----- |\n| [BCCA](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#About)     | Bias Corrected Constructed Analogs V2 Daily Climate Projections (BACA) contains projections of daily BCCA CMIP3 and CMIP5 projections of precipitation, daily maximum, and daily minimum temperature over the contiguous United States                                                                         | 1950 - 2100                |       |\n| [BCSD](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#About)     | Bias Corrected Spatially Downscaled (BCSD) Monthly CMIP5 Climate Projections                                                                                                                                                                                                                                   | 1950 - 2100                |       |\n| [CHIRPS](https://www.chc.ucsb.edu/data/chirps)                                             | Rainfall Estimates from Rain Gauge and Satellite Observations                                                                                                                                                                                                                                                  | 1980 - Current Month       |       |\n| [Daymet](https://daymet.ornl.gov/)                                                         | Daymet provides long-term, continuous, gridded estimates of daily weather and climatology variables by interpolating and extrapolating ground-based observations through statistical modeling techniques.                                                                                                      | 1980 through previous year |       |\n| [LOCA](https://gdo-dcp.ucllnl.org/downscaled_cmip_projections/dcpInterface.html#**About**) | LOCA, which stands for Localized Constructed Analogs, is a technique for downscaling climate model projections of the future climate.                                                                                                                                                                          | 1950 - 2100                |       |\n| [MACA](https://www.climatologylab.org/maca.html)                                           | Multivariate Adaptive Constructed Analogs (MACA) is a statistical method for downscaling Global Climate Models (GCMs) from their native coarse resolution to a higher spatial resolution that captures reflects observed patterns of daily near-surface meteorology and simulated changes in GCMs experiments. | 1950-2005 and 2006-2100    |       |\n| [PRISM-Monthly](https://cida.usgs.gov/thredds/catalog.html?dataset=cida.usgs.gov/prism_v2) | Parameter-elevation Regressions on Independent Slopes                                                                                                                                                                                                                                                          | 1895-2020                  |       |\n| [TerraClimate](https://www.climatologylab.org/terraclimate.html)                           | TerraClimate is a dataset of monthly climate and climatic water balance for global terrestrial surfaces from 1958-2019. These data provide important inputs for ecological and hydrological studies at global scales that require high spatial resolution and time-varying data.                               | 1958-2020                  |       |\n| [gridMET](https://www.climatologylab.org/gridmet.html)                                     | daily high-spatial resolution (~4-km, 1/24th degree) surface meteorological data covering the contiguous US                                                                                                                                                                                                    | 1979-yesterday             |       |\n\n## Data Requirements\n\n### Data - xarray (gridded data) and Geopandas (Polygon data)\n\n- [Xarray](https://docs.xarray.dev/en/stable/)\n\n  - Any endpoint that can be read by xarray and contains projected coordinates.\n    - The endpoint can be supplied by the OPeNDAP catalog or from a user-supplied end-point.\n  - Projection: any projection that can be read by proj.CRS (similar to Geopandas)\n\n- [Geopandas](https://geopandas.org/en/stable/)\n  - Any file that can be read by Geopandas\n  - Projection: any projection that can be read by proj.CRS\n\n## Installation\n\nYou can install _Gdptools_ via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):\n\n        pip install gdptools\n\nor install via [conda](https://anaconda.org/) from [conda-forge](https://anaconda.org/conda-forge/gdptools):\n\n       conda install -c conda-forge gdptools\n\n## Usage\n\nPlease see the example notebooks for detailes.\n\n### Catalog Examples\n\n- [OPeNDAP Catalog Example](./docs/terraclime_et.ipynb)\n\n### Non-catalog Examples\n\n- [Non-catalog example - gridMET](./docs/Gridmet_non_catalog.ipynb)\n- [Non-catalog example - Merra-2](./docs/Merra-2-example.ipynb)\n\n## Contributing\n\nContributions are very welcome. To learn more, see the Contributor Guide\\_.\n\n## License\n\nDistributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode), _Gdptools_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems, please [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/issues) along with a detailed description.\n\n## Credits\n\nThis project was generated from [@hillc-usgs](https://code.usgs.gov/hillc-usgs)'s [Pygeoapi Plugin Cookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter) template.\n",
    'author': 'Richard McDonald',
    'author_email': 'rmcd@usgs.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://code.usgs.gov/wma/nhgf/toolsteam/gdptools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
