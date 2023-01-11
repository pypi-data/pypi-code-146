# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kardiasclean']

package_data = \
{'': ['*']}

install_requires = \
['nltk==3.7', 'numpy==1.21.6', 'pandas==1.3.5', 'phonetics==1.0.5']

setup_kwargs = {
    'name': 'kardiasclean',
    'version': '0.3.0',
    'description': 'Medical Records Normalizer',
    'long_description': '# Kardiasclean\n\nClean, Normalize, and Tokenize medical records data.\n\n## Install\n\n```shell\npip install kardiasclean\n```\n\n## Usage\n\n```python\nimport kardiasclean\n\ndata[\'procedure\'] = kardiasclean.split_string(data[\'procedure\'], delimiter="+")\ndata_map = kardiasclean.spread_column(data[\'procedure\'])\n\ndata_map[\'procedure\'] = kardiasclean.clean_accents(data_map[\'procedure\'])\ndata_map[\'procedure\'] = kardiasclean.clean_symbols(data_map[\'procedure\'])\ndata_map[\'keywords\'] = kardiasclean.clean_stopwords(data_map[\'procedure\'])\ndata_map[\'token\'] = kardiasclean.clean_tokenize(data_map[\'keywords\'])\n\nlist_df = kardiasclean.create_unique_list(spread_df, spread_df[\'token\'])\nlist_df = list_df.drop(["patient_id", "index"], axis=1)\n\nspread_df[\'procedure\'] = kardiasclean.normalize_from_tokens(spread_df[\'token\'], list_df[\'token\'], list_df[\'procedure\'])\n\n>>>    patient_id                 procedure               keywords      token\n>>> 0           0  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN\n>>> 1           1  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN\n>>> 2           2  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN\n>>> 3           3  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN\n>>> 4           4  Reparacion de CIA parche  cia parche reparacion  SPRXRPRSN\n```\n\n## How does it work?\n\nThis package contains ETL functions for extracting all the unique natural language medical terms from a pandas DataFrame. The steps are much like any other ETL process for creating a bag of words/terms but this includes methods for normalizing the original column via "fuzzy string matching", as well as preparing new DataFrames for loading to an SQL database, and ML pre-processing like binning of low frequency records and categorical data encoding.\n\n\n## Development\n\n```shell\npoetry run pytest\n```\n\n## Changelog\n\n- 0.3.0: Removed SQLAlchemy dependency\n\n- 0.2.1: Replaced psycopg2 dependency with psycopg2-binary.\n- 0.2.0: Fixed perform_binning implementations, new api for all functions.\n\n- 0.1.7: Added support for not appending column name to matrix encoding.\n- 0.1.6: Small fixes to stopwords, updated readme.\n- 0.1.5: Fix stopwords implementation, added lowercase conversion.\n- 0.1.3: Added Documentation.\n- 0.1.2: Added SQL support and improved pre-processing functions.\n- 0.1.1: Small readme fixes.\n- 0.1.0: Initial Release.\n',
    'author': 'AlbertoV5',
    'author_email': '58243333+AlbertoV5@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AlbertoV5/kardiasclean',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.6,<3.11',
}


setup(**setup_kwargs)
