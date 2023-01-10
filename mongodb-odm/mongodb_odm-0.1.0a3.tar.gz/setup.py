# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongodb_odm', 'mongodb_odm.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.0,<2.0.0', 'pymongo>=4.3.3,<5.0.0']

setup_kwargs = {
    'name': 'mongodb-odm',
    'version': '0.1.0a3',
    'description': 'MongoDB-ODM, NOSQL databases in Python, designed for simplicity, compatibility, and robustness.',
    'long_description': '# ODM\n\n<p align="center">\n    <em>MongoDB-ODM, NOSQL databases in Python, designed for simplicity, compatibility, and robustness.</em>\n</p>\n\n<p align="center">\n\n<a href="https://github.com/nayan32biswas/mongodb-odm" target="_blank">\n    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/nayan32biswas/mongodb-odm/total?color=success">\n</a>\n<a href="https://pypi.org/project/mongodb-odm/">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/mongodb-odm?color=blue">\n</a>\n</p>\n\n---\n\n## Introduction\n\nThe purpose of this module is to do provide easy access to the database with the python object feature with MongoDB and pymongo. With pymongo that was very easy to make spelling mistakes of a collection name when you are doing database operation. This module provides you minimal ODM with a modeling feature so that you don’t have to look up the MongoDB dashboard(Mongo Compass) to know about field names or data types.\n\n**MongoDb-ODM** is based on Python type annotations, and powered by <a href="https://pymongo.readthedocs.io/en/stable/" class="external-link" target="_blank">PyMongo</a> and <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>.\n\nThe key features are:\n\n- **Intuitive to write**: Great editor support. Completion everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.\n- **Easy to use**: It has sensible defaults and does a lot of work underneath to simplify the code you write.\n- **Compatible**: It is designed to be compatible with **FastAPI**, **Pydantic**, and **PyMongo**.\n- **Extensible**: You have all the power of **PyMongo** and **Pydantic** underneath.\n- **Short**: Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in **PyMongo** and Pydantic.\n\n---\n\n## Requirement\n\n**MongoDb-ODM** will work on <a href="https://www.python.org/downloads/" class="external-link" target="_blank">Python 3.7 and above</a>\n\nThis **MongoDb-ODM** is build top of **PyMongo** and **Pydantic**. Those package are required and will auto install while **MongoDb-ODM** was installed.\n\n## Example\n\n#### Define model\n\n```py\nfrom datetime import datetime\nfrom pydantic import Field\nfrom pymongo import IndexModel, ASCENDING\nfrom typing import Optional\n\nfrom mongodb_odm import Document\n\n\nclass User(Document):\n    username: str = Field(...)\n    email: Optional[str] = Field(default=None)\n    full_name: str = Field(...)\n\n    is_active: bool = True\n    date_joined: datetime = Field(default_factory=datetime.utcnow)\n\n    last_login: datetime = Field(default_factory=datetime.utcnow)\n    password: Optional[str] = Field(default=None)\n    image: Optional[str] = Field(default=None)\n\n    created_at: datetime = Field(default_factory=datetime.utcnow)\n    updated_at: datetime = Field(default_factory=datetime.utcnow)\n\n    class Config:\n        collection_name = "user"\n        indexes = (\n            IndexModel([("username", ASCENDING)], unique=True),\n            IndexModel([("email", ASCENDING)]),\n        )\n```\n\n#### Create Document\n\n```py\nuser = User(\n    email="example@example.com",\n    full_name="Example Name",\n    password="hash-password",\n).create()\n```\n\n#### Retrive Document\n\n- Filter data from collection\n\n```py\nfor user in find({"is_active": True}):\n    print(user)\n```\n\n- Find first object with filter\n\n```py\nuser = User.find_first({"is_active": True})\n```\n\n#### Update Data\n\n\n```py\nuser = User.find_first({"is_active": True})\nuser.full_name = "New Name"\n```\n\n#### Delete Data\n\n```py\nuser = User.find_first({"is_active": True})\nif user:\n    user.delete()\n```\n\n### Apply Indexes\n\n```py\nfrom mongodb_odm import apply_indexes, ASCENDING, Document, IndexModel\n\n\nclass User(Document):\n    ...\n\n    class Config:\n        indexes = (\n            IndexModel([("username", ASCENDING)], unique=True),\n            IndexModel([("email", ASCENDING)]),\n        )\n```\n\n- To create indexes in database diclare [IndexModel](https://pymongo.readthedocs.io/en/stable/tutorial.html#indexing) and assign in indexes array in Config class. **IndexModel** module that are directly imported from **pymongo**.\n- Call `apply_indexes` function from your CLI. You can use [Typer](https://typer.tiangolo.com/) to implement CLI.\n',
    'author': 'Nayan Biswas',
    'author_email': 'nayan32biswas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nayan32biswas/mongodb-odm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
