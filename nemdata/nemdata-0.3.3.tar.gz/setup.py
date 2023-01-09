# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nemdata']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pyarrow>=10.0.1,<11.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['nemdata = nemdata.cli:cli']}

setup_kwargs = {
    'name': 'nemdata',
    'version': '0.3.3',
    'description': "Simple CLI for downloading data for Australia's NEM from AEMO.",
    'long_description': '# nem-data\n\nA simple & opinionated Python command line tool to access Australian National Energy Market (NEM) data provided by the Australian Energy Market Operator (AEMO).  It features:\n\n- access to the NEMDE dataset as well as the predispatch, unit-scada, trading-price, demand and interconnectors tables from MMSDM,\n- a cache to not re-download data that already exists in `~/nem-data/data`,\n- adds `interval-start` and `interval-end` columns.\n\nIt is designed for use by researchers & data scientists - this tool supports my personal research work.  It is not designed for production use - see [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS) for a production grade package.\n\nSee [A Hackers Guide to AEMO & NEM Data](https://adgefficiency.com/hackers-aemo/) for more context on the data provided by AEMO.\n\n\n## Setup\n\n```bash\n$ pip install nemdata\n```\n\n\n## Use\n\n### CLI\n\n```shell-session\n$ nemdata --help\nUsage: nemdata [OPTIONS]\n\n  Downloads NEM data from AEMO.\n\nOptions:\n  -t, --table TEXT          Available tables: nemde, predispatch, unit-scada,\n                            trading-price, demand, interconnectors.\n  -s, --start TEXT          Start date (YYYY-MM or YYYY-MM-DD for NEMDE).\n  -e, --end TEXT            End date (incusive) (YYYY-MM or YYYY-MM-DD for\n                            NEMDE).\n  --dry-run / --no-dry-run  Whether to save downloaded data to disk.\n  --help                    Show this message and exit.\n```\n\nDownload NEMDE data for the first three days in January 2018:\n\n```shell-session\n$ nemdata -t nemde --start 2018-01-01 --end 2018-01-03\n```\n\nDownload trading price data from MMSDM for January to March 2018:\n\n```shell-session\n$ nemdata -t trading-price -s 2018-01 -e 2018-03\n```\n\n### Python\n\nDownload trading price data from MMSDM for January to Feburary 2020:\n\n```python\nimport nemdata\n\ndata = nemdata.download(start="2020-01", end="2020-02", table="trading-price")\n```\n\nLoad this data back into Python:\n\n```python\ndata = nemdata.load()[\'trading-price\']\n```\n\n\n## Data\n\nData is downloaded into into `$HOME/nem-data/data/`:\n\n```shell-session\n$ nemdata -t trading-price -s 2020-01 -e 2020-02\n$ tree ~/nem-data\n/Users/adam/nem-data\n└── data\n    └── trading-price\n        ├── 2020-01\n        │\xa0\xa0 ├── PUBLIC_DVD_TRADINGPRICE_202001010000.CSV\n        │\xa0\xa0 ├── clean.csv\n        │\xa0\xa0 ├── clean.parquet\n        │\xa0\xa0 └── raw.zip\n        └── 2020-02\n            ├── PUBLIC_DVD_TRADINGPRICE_202002010000.CSV\n            ├── clean.csv\n            ├── clean.parquet\n            └── raw.zip\n```\n\nA few things happen during data processing:\n\n- the top & bottom rows of the raw CSV are removed to create a rectangular CSV,\n- `interval-start` and `interval-end` columns are added with timezones,\n- when using `nemdata.loader.loader` for the `trading-price`, all data is resampled to a 5 minute frequency (both before and after the 30 to 5 minute settlement interval change).\n',
    'author': 'Adam Green',
    'author_email': 'adam.green@adgefficiency.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
