# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsmanager',
 'dsmanager.controller',
 'dsmanager.datamanager',
 'dsmanager.datamanager.datasources',
 'dsmanager.datamanager.utils',
 'dsmanager.model',
 'dsmanager.view']

package_data = \
{'': ['*']}

install_requires = \
['dash>=2.7.1,<3.0.0',
 'explainerdashboard>=0.4.0,<0.5.0',
 'llvmlite>=0.39.1,<0.40.0',
 'numba>=0.56.4,<0.57.0',
 'numexpr>=2.8.4,<3.0.0',
 'numpy>=1.23.3,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'optuna>=3.0.5,<4.0.0',
 'pandas>=1.5.0,<2.0.0',
 'paramiko>=2.12.0,<3.0.0',
 'pickle-mixin>=1.0.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'setuptools>=65.6.3,<66.0.0',
 'sqlalchemy>=1.4.45,<2.0.0',
 'sweetviz>=2.1.4,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{'kaggle': ['kaggle>=1.5.12,<2.0.0'],
 'mysql': ['mysqlclient>=2.1.1,<3.0.0'],
 'pgsql': ['psycopg2-binary>=2.9.5,<3.0.0'],
 'salesforce': ['simple-salesforce>=1.12.2,<2.0.0'],
 'sharepoint': ['azure-storage-common>=2.1.0,<3.0.0',
                'azure-storage-blob>=12.14.1,<13.0.0',
                'azure-common>=1.1.28,<2.0.0',
                'shareplum>=0.5.1,<0.6.0'],
 'snowflake': ['snowflake-sqlalchemy>=1.4.4,<2.0.0']}

setup_kwargs = {
    'name': 'dsmanager',
    'version': '1.1.5',
    'description': 'Data Science tools to ease access and use of data and models',
    'long_description': '<h1 align="center"\n>Data Science Manager 👨\u200d💻\n</h1>\n<p\n>\n  <a\n  href="#"\n  target="_blank"\n  >\n    <img\n    alt="Version"\n    src="https://img.shields.io/badge/version-1.1-blue.svg?cacheSeconds=2592000"\n    />\n  </a>\n  <a\n  href="http://dsmanager.rtfd.io/"\n  target="_blank"\n  >\n    <img\n    alt="Documentation"\n    src="https://img.shields.io/badge/documentation-pdoc-orange.svg"\n    />\n  </a>\n  <a\n  href="LICENSE"\n  target="_blank"\n  >\n    <img\n    alt="License: Adel Rayane Amrouche"\n    src="https://img.shields.io/badge/License-Adel Rayane Amrouche-yellow.svg"\n    />\n  </a>\n</p>\n\n> Data Science tools to ease access and use of data and models\n\n## Install\n\nThe easiest way to install scikit-learn is using `pip`:\n\n```sh\npip install dsmanager\n```\n\nor `poetry`\n\n```sh\npoetry add dsmanager\n```\n\nor `conda`\n\n```sh\nconda install dsmanager\n```\n\nMultiple sub dependencies are available depending on the needs:\n\n```sh\npip install dsmanager[sharepoint] # Add Sharepoint source handling\npip install dsmanager[salesforce] # Add SalesForce source handling\npip install dsmanager[kaggle] # Add Kaggle source handling\npip install dsmanager[snowflake] # Add Snowflkae source handling\npip install dsmanager[mysql] # Add MySQL source handling\npip install dsmanager[pgsql] # Add PostgreSQL source handling\n```\n\n## Usage\n\nThe DS Manager has 3 main components:\n\n- A **DataManager** component\n- A **Controller** component\n- A **Model** component\n\n### DataManager\n\nThe DataManager allows to manage different types of data sources among which one can mention:\n\n- File (File locally or online)\n- Http (Http requests)\n- Ftp (Ftp hosted files)\n- Sql (Sql database tables)\n- Sharepoint (Microsoft OneDrive files)\n- SalesForce (SalesForce classes)\n- Kaggle (Kaggle datasets)\n\nThe first step to use the DataManager is to instance it with a metadata path.\n\n```python\nfrom dsmanager import DataManager\ndm = DataManager("data/metadata.json")\n```\n\nThe metadata file is generated if it does not exist and it consist of a dict of sources following this schema:\n\n```json\n{\n  "SOURCE_NAME": {\n    "source_type": "name_of_the_source",\n    "args": {}\n  }\n}\n```\n\nEach source has a `source_type` corresponding to the name of the source. You can access this list with this command:\n\n```python\nDataManager().datasources\n```\n\nEach of these data sources has its own schema because of its own parameters requierements. You can also add additional arguments which are not required with the parameter `args`.\n\nYou can obtain the schema for a specific datasource with the following command:\n\n```python\nsource_name = "file"\nDataManager().datasources[source_name]\n```\n\nOutput:\n\n```json\n{\n    "source_type": "file",\n    "path": "local_path | online_uri",\n    "file_type": "csv | excel | text | json | ...",\n    "encoding": "utf-8",\n    "args": {\n        "pandas_read_file_argument_keyword": "value_for_this_argument"\n    }\n}\n```\n\n## Development\n\n### Source code\n\nYou can check the latest sources with the command:\n\n```python\ngit clone https://gitlab.com/bigrayou/dsmanager\n```\n\n### Testing\n\nAfter installation, you can launch the test suite from outside the dsmanager directory (you will need to have pytest >= 7.1.3 installed):\n\n```python\npytest -v\n```\n\n### Dependencies\n\nThe DSManager requires:\n\n- dash >=2.7.1,<3.0.0\n- explainerdashboard >=0.4.0,<0.5.0\n- llvmlite >=0.39.1,<0.40.0\n- numba >=0.56.4,<0.57.0\n- numexpr >=2.8.4,<3.0.0\n- numpy >=1.23.3,<2.0.0\n- openpyxl >=3.0.10,<4.0.0\n- pandas >=1.5.0,<2.0.0\n- pickle-mixin >=1.0.2,<2.0.0\n- python-dotenv >=0.21.0,<0.22.0\n- requests >=2.28.1,<3.0.0\n- scikit-learn >=1.2.0,<2.0.0\n- setuptools >=65.6.3,<66.0.0\n- sqlalchemy >=1.4.45,<2.0.0\n- sweetviz >=2.1.4,<3.0.0\n- tqdm >=4.64.1,<5.0.0\n\nOptionnaly, the DSManager could require:\n\n- azure-common >=1.1.28,<2.0.0\n- azure-storage-blob >=12.14.1,<13.0.0\n- azure-storage-common >=2.1.0,<3.0.0\n- kaggle >=1.5.12,<2.0.0\n- shareplum >=0.5.1,<0.6.0\n- simple-salesforce >=1.12.2,<2.0.0\n- snowflake-sqlalchemy >=1.4.4,<2.0.0\n- psycopg2-binary >=2.9.5,<3.0.0\n- mysqlclient >=2.1.1,<3.0.0\n\n## Author\n\n👤 **Rayane Amrouche**\n\n- Github: [@AARayane](https://github.com/AARayane)\n- Gitlab: [@Bigrayou](https://gitlab.com/bigrayou)\n',
    'author': 'Rayane AMROUCHE',
    'author_email': 'rayaneamrouche@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
