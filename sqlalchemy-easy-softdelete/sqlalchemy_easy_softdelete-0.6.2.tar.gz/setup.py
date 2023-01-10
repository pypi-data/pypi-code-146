# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_easy_softdelete',
 'sqlalchemy_easy_softdelete.handler',
 'sqlalchemy_easy_softdelete.handler.rewriter',
 'tests',
 'tests.seed_data',
 'tests.snapshots']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4,<2.0', 'certifi>=2022.12.07', 'cryptography>=38.0.3']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'sqlalchemy-easy-softdelete',
    'version': '0.6.2',
    'description': 'Easily add soft-deletion to your SQLAlchemy Models.',
    'long_description': '# SQLAlchemy Easy Soft-Delete\n\n[![pypi](https://img.shields.io/pypi/v/sqlalchemy-easy-softdelete.svg)](https://pypi.org/project/sqlalchemy-easy-softdelete/)\n[![python](https://img.shields.io/pypi/pyversions/sqlalchemy-easy-softdelete.svg)](https://pypi.org/project/sqlalchemy-easy-softdelete/)\n[![Build Status](https://github.com/flipbit03/sqlalchemy-easy-softdelete/actions/workflows/build.yml/badge.svg)](https://github.com/flipbit03/sqlalchemy-easy-softdelete/actions/workflows/build.yml)\n\n[//]: # ([![codecov]&#40;https://codecov.io/gh/flipbit03/sqlalchemy-easy-softdelete/branch/main/graphs/badge.svg&#41;]&#40;https://codecov.io/github/flipbit03/sqlalchemy-easy-softdelete&#41;)\n\nEasily add soft-deletion to your SQLAlchemy Models and automatically filter out soft-deleted objects from your queries and relationships.\n\nThis package can generate a tailor-made SQLAlchemy Mixin that can be added to your SQLAlchemy Models, making them contain a field that, when set, will mark the entity as being soft-deleted.\n\nThe library also installs a hook which dynamically rewrites all selects which are sent to the database for all tables that implement the soft-delete mixin, providing a seamless experience in both manual queries and model relationship accesses.\n\nMixin generation is fully customizable and you can choose the field name, its type, and the presence of (soft-)delete/undelete methods.\n\nThe default implementation will generate a `deleted_at` field in your models, of type `DateTime(timezone=True)`, and will also provide a `.delete(v: Optional = datetime.utcnow())` and `.undelete()` methods.\n\n### Installation:\n\n```\npip install sqlalchemy-easy-softdelete\n```\n\n### How to use:\n\n```py\nfrom sqlalchemy_easy_softdelete.mixin import generate_soft_delete_mixin_class\nfrom sqlalchemy.orm import declarative_base\nfrom sqlalchemy import Column, Integer\nfrom datetime import datetime\n\n# Create a Class that inherits from our class builder\nclass SoftDeleteMixin(generate_soft_delete_mixin_class()):\n    # type hint for autocomplete IDE support\n    deleted_at: datetime\n\n# Apply the mixin to your Models\nBase = declarative_base()\n\nclass Fruit(Base, SoftDeleteMixin):\n    __tablename__ = "fruit"\n    id = Column(Integer)\n```\n\n### Example Usage:\n\n```py\nall_active_fruits = session.query(Fruit).all()\n```\nThis will generate a query with an automatic `WHERE fruit.deleted_at IS NULL` condition added to it.\n\n```py\nall_fruits = session.query(Fruit).execution_options(include_deleted=True).all()\n```\nSetting `include_deleted=True` (attribute name can be customized) in the query disables soft delete for that query.\n\n#### License\n\n* BSD-3-Clause\n\n[//]: # (* Documentation: <https://flipbit03.github.io/sqlalchemy-easy-softdelete>)\n[//]: # (* GitHub: <https://github.com/flipbit03/sqlalchemy-easy-softdelete>)\n[//]: # (* PyPI: <https://pypi.org/project/sqlalchemy-easy-softdelete/>)\n',
    'author': 'Cadu',
    'author_email': 'cadu.coelho@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/flipbit03/sqlalchemy-easy-softdelete',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
