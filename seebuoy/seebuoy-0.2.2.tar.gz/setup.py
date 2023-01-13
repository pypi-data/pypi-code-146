# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seebuoy', 'seebuoy.ndbc', 'seebuoy.ndbc.data', 'seebuoy.ww3']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.1.2,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'scikit-learn>=1.1.3,<2.0.0']

setup_kwargs = {
    'name': 'seebuoy',
    'version': '0.2.2',
    'description': 'Remote data access for oceanographic data.',
    'long_description': '# \n<p align="center">\n  <a href="#"><img src="https://raw.githubusercontent.com/nickc1/seebuoy/master/docs/img/seebuoy_logo_text.png" alt="seebuoy"></a>\n</p>\n<p align="center">\n<em>Easily access real time and historical data from the <a href="http://www.ndbc.noaa.gov">National Data Buoy Center</a>.</em>\n\n<p align="center">\n<em> <a href="https://www.seebuoy.com">DOCUMENTATION</a>.</em>\n\n</p>\n\n---\n\nseebuoy provides an easy to use python interface to the [National Data Buoy Center](http://www.ndbc.noaa.gov). Easily access realtime data, historical data, and metadata about buoys, gliders, and ADCPs.\n\n## Quick Start\n\n```python\nfrom seebuoy import NDBC\n\nndbc = NDBC()\n\n# Information on NDBC\'s ~1800 buoys and gliders\ndf_buoys = ndbc.stations()\n\n# list all available data for all buoys\ndf_data = ndbc.available_data()\n\n# get all data for a buoy\nstation_id = "41037"\ndf_buoy = ndbc.get_station(station_id)\n```\n\nSee the [documentation](https://seebuoy.com/ndbc) for more detailed description.\n\n\n## Examples\n\nIn addition to this documentation, we also provide standalone jupyter notebooks. You can see them rendered on github:\n\n- [North Carolina Stations](https://github.com/nickc1/seebuoy/blob/master/examples/north_carolina_stations.ipynb): Find all buoys near North Carolina, list all available data, and pull data for a specific buoy.\n- [Historical Data](https://github.com/nickc1/seebuoy/blob/master/examples/historical_data.ipynb): Get all historical data for the South Hatteras buoy going back to 1973.\n\n\n## Installation\n\n```\npip install seebuoy\n```\n\n\n## Other Resources\n\n- [The Distributed Oceanographic Data Systems](https://dods.ndbc.noaa.gov)\n- [Measurement Descriptions](https://www.ndbc.noaa.gov/measdes.shtml)\n- [NDBC File Directory](https://www.ndbc.noaa.gov/data/)\n\n\n',
    'author': 'nickc1',
    'author_email': 'nickcortale@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
