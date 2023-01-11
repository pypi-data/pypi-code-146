# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mines_data_engineering']

package_data = \
{'': ['*']}

install_requires = \
['docker>=6.0.1,<7.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'pymongo>=4.3.3,<5.0.0',
 'spython>=0.3.0,<0.4.0',
 'xattr>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'mines-data-engineering',
    'version': '0.1.6',
    'description': 'Helper package for the Data Engineering course at Colorado School of Mines',
    'long_description': '# Mines Data Engineering\n\nThis package simplifies the process of starting common database systems in the background on Singularity Hub.\n\n## Supported Databases\n\n- MongoDB\n- TimescaleDB (and Postgres)\n\n## Examples\n\n### MongoDB\n\n```python\nfrom mines_data_engineering import start_mongo\nimport pymongo\n\n# will need wait a couple minutes the first time this happens\n# while Singularity downloads and converts the Docker image\nconnection_string = start_mongo()\n\nclient = pymongo.MongoClient(connection_string)\nclient.my_db.my_col.insert_one({\'finally\': \'working\'})\n```\n\n### Postgres/TimescaleDB\n\n```python\nfrom mines_data_engineering import start_postgres\nimport psycopg2\n\n\n# will need wait a couple minutes the first time this happens\n# while Singularity downloads and converts the Docker image\nconnection_string = start_postgres()\n\nconn = psycopg2.connect(connection_string)\ncur = conn.cursor()\ncur.execute("SELECT 1")\nassert next(cur) == (1,)\n```\n',
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@mines.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
