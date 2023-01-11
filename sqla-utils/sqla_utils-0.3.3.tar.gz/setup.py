# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqla_utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4,<2.0']

setup_kwargs = {
    'name': 'sqla-utils',
    'version': '0.3.3',
    'description': 'Opinionated utilities for working with SQLAlchemy',
    'long_description': '# sqla-utils\n\nOpinionated utilities for working with SQLAlchemy\n\n[![MIT License](https://img.shields.io/pypi/l/sqla-utils.svg)](https://pypi.python.org/pypi/sqla-utils/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sqla-utils)](https://pypi.python.org/pypi/sqla-utils/)\n[![GitHub](https://img.shields.io/github/release/srittau/sqla-utils/all.svg)](https://github.com/srittau/sqla-utils/releases/)\n[![pypi](https://img.shields.io/pypi/v/sqla-utils.svg)](https://pypi.python.org/pypi/sqla-utils/)\n[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/srittau/sqla-utils/test-and-lint.yml?branch=main)](https://github.com/srittau/sqla-utils/actions/workflows/test-and-lint.yml)\n\n## Contents\n\n### Transaction Wrapper\n\n**FIXME**\n\n### `DBObjectBase`\n\n`DBObjectBase` is a base class for mapped classes.\n\nExample:\n\n```python\nfrom datetime import datetime\nfrom sqlalchemy import Column, DateTime, Integer, String\nfrom sqla_utils import DBObjectBase, Transaction\n\nclass DBAppointment(DBObjectBase):\n    __tablename__ = "appointments"\n\n    id = Column(Integer, primary_key=True)\n    date = Column(DateTime, nullable=False)\n    description = Column(String(1000), nullable=False, default="")\n```\n\nAppointment items can then be queried like this:\n\n```python\nfrom sqla_utils import begin_transaction\n\nwith begin_transaction() as t:\n    app123 = DBAppointment.fetch_by_id(t, 123)\n    great_apps = DBAppointment.fetch_all(t, DBAppointment.description.like("%great%"))\n```\n\nIt is recommended to add custom query, creation, and update methods:\n\n```python\nclass DBAppointment(DBObjectBase):\n    ...\n\n    @classmethod\n    def create(cls, t: Transaction, date: datetime, description: str) -> DBAppointment:\n        o = cls()\n        o.date = date\n        o.description = description\n        t.add(o)\n        return o\n\n    @classmethod\n    def fetch_all_after(cls, t: Transaction, date: datetime) -> List[DBAppointment]:\n        return cls.fetch_all(t, cls.start >= dates.start)\n\n    def update_description(self, t: Transaction, new_description: str) -> None:\n        self.description = new_description\n        t.changed(self)\n```\n\n### Database Builder\n\n**FIXME**\n\n### pytest Utilities\n\nThe `sqla_utils.test` module contains a few utilities for working with pytest and SQLAlchemy.\n\n**FIXME**\n',
    'author': 'Sebastian Rittau',
    'author_email': 'srittau@rittau.biz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/srittau/sqla-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
