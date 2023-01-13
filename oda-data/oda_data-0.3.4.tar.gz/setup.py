# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oda_data',
 'oda_data.classes',
 'oda_data.clean_data',
 'oda_data.get_data',
 'oda_data.indicators',
 'oda_data.read_data',
 'oda_data.tools']

package_data = \
{'': ['*'], 'oda_data': ['.raw_data/*', 'settings/*']}

install_requires = \
['bblocks>=0.5.0,<0.6.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pydeflate>=1.2.10,<2.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'oda-data',
    'version': '0.3.4',
    'description': 'A python package to work with Official Development Assistance data from the OECD DAC.',
    'long_description': '[![pypi](https://img.shields.io/pypi/v/oda_data.svg)](https://pypi.org/project/oda_data/)\n[![python](https://img.shields.io/pypi/pyversions/oda_data.svg)](https://pypi.org/project/oda_data/)\n[![codecov](https://codecov.io/gh/ONEcampaign/oda_data_package/branch/main/graph/badge.svg?token=G8N8BWWPL8)](https://codecov.io/gh/ONEcampaign/oda_data_package)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# The ODA Data Package\nThis package contains key tools used by The ONE Campaign to analyse Official Development Assistance (ODA) data from\nthe OECD [DAC](https://www.oecd.org/dac/stats/) databases.\n\n**This package is currently in active development. Features and APIs may change.** Please submit questions, feedback\nor requests via the [issues page](https://github.com/ONEcampaign/oda_data_package/issues).\n\n## Getting started\n\nMost users can get the data they need by using the `ODAData` class.\n\nAn object of this class can handle:\n- getting data for specific indicators (one or more)\n- filtering the data for specific donors, recipients(if relevant), years.\n- returning the data in a variety of currency/prices combinations.\n\nFor example, to get Total ODA in net flows and grant equivalents, in constant 2021 Euros, for 2018-2021.\n\n```python\nfrom oda_data import ODAData\n\n# create object, specifying key details of the desired output\ndata = ODAData(years=range(2018,2022), currency="EUR", prices="constant", base_year=2021)\n\n# load the desired indicators\ndata.load_indicator(indicator="total_oda_flow_net")\ndata.load_indicator(indicator="total_oda_ge")\n\n# get the data\ndf = data.get_data(indicators=\'all\')\n\nprint(df.head(6))\n```\nThis would result in the following dataframe:\n\n|   donor_code | donor_name   |   year |   value | indicator          | currency   | prices   |\n|-------------:|:-------------|-------:|--------:|:-------------------|:-----------|:---------|\n|            1 | Austria      |   2021 | 1261.76 | total_oda_flow_net | EUR        | constant |\n|            1 | Austria      |   2021 | 1240.31 | total_oda_ge       | EUR        | constant |\n|            2 | Belgium      |   2021 | 2176.38 | total_oda_flow_net | EUR        | constant |\n|            2 | Belgium      |   2021 | 2174.38 | total_oda_ge       | EUR        | constant |\n|            3 | Denmark      |   2021 | 2424.51 | total_oda_flow_net | EUR        | constant |\n|            3 | Denmark      |   2021 | 2430.65 | total_oda_ge       | EUR        | constant |\n\n\nTo view the full list of available indicators, you can call `.get_available_indicators()`.\n\n```python\nfrom oda_data import ODAData\n\n# create object\ndata = ODAData()\n\n# get the list of available indicators\ndata.available_indicators()\n```\nThis logs the list of indicators to the console. For example, the first several:\n```markdown\nAvailable indicators:\ntotal_oda_flow_net\ntotal_oda_ge\ntotal_oda_bilateral_flow_net\ntotal_oda_bilateral_ge\ntotal_oda_multilateral_flow_net\ntotal_oda_multilateral_ge\ntotal_oda_flow_gross\ntotal_oda_flow_commitments\ntotal_oda_grants_flow\ntotal_oda_grants_ge\ntotal_oda_non_grants_flow\ntotal_oda_non_grants_ge\ngni\noda_gni_flow\nod_gni_ge\n.\n.\n.\n```\n',
    'author': 'Jorge Rivera',
    'author_email': 'jorge.rivera@one.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
