# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datatables']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'sqlalchemy>=2.0.0rc2,<3.0.0']

setup_kwargs = {
    'name': 'sqlalchemy2-datatables',
    'version': '0.1.0',
    'description': 'Python Sqlalchemy based serverside processing for jQuery datatables.',
    'long_description': '# sqlalchemy2-datatables\n\n[![versions](https://img.shields.io/pypi/pyversions/sqlalchemy2-datatables.svg)](https://github.com/hniedner/sqlalchemy2-datatables)\n[![license](https://img.shields.io/github/license/pydantic/pydantic.svg)](https://github.com/pydantic/pydantic/blob/main/LICENSE)\n\nsqlalchemy2-datatables is a framework agnostic library providing an SQLAlchemy integration of\njQuery DataTables >= 1.10, and helping you manage server side requests in your application.\n\nThis project was inspired by [sqlalchemyw-datatables](https://github.com/Pegase745/sqlalchemy-datatables)\ndeveloped by Michel Nemnom aka [Pegase745](https://github.com/Pegase745).\n\nKey motivation was compatibility with [SQLAlchemy2.0](https://docs.sqlalchemy.org/en/20/).\n',
    'author': 'R. Hannes Niedner',
    'author_email': 'hniedner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
