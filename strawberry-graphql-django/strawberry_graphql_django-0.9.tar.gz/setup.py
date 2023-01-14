# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawberry_django',
 'strawberry_django.auth',
 'strawberry_django.extensions',
 'strawberry_django.fields',
 'strawberry_django.mutations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0', 'strawberry-graphql>=0.139.0']

setup_kwargs = {
    'name': 'strawberry-graphql-django',
    'version': '0.9',
    'description': 'Strawberry GraphQL Django extension',
    'long_description': '# Strawberry GraphQL Django integration\n\n[![CI](https://github.com/la4de/strawberry-graphql-django/actions/workflows/main.yml/badge.svg)](https://github.com/la4de/strawberry-graphql-django/actions/workflows/main.yml)\n[![PyPI](https://img.shields.io/pypi/v/strawberry-graphql-django)](https://pypi.org/project/strawberry-graphql-django/)\n[![Downloads](https://pepy.tech/badge/strawberry-graphql-django)](https://pepy.tech/project/strawberry-graphql-django)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/strawberry-graphql-django)\n\nThis package provides powerful tools to generate GraphQL types, queries, mutations and resolvers from Django models.\n\nInstalling `strawberry-graphql-django` package from the python package repository.\n\n```shell\npip install strawberry-graphql-django\n```\n\nFull documentation is available under [docs](https://strawberry-graphql.github.io/strawberry-graphql-django/) github folder.\n\n* [x] GraphQL type generation from models\n* [x] Filtering, pagination and ordering\n* [x] Basic create, retrieve, update and delete (CRUD) types and mutations\n* [x] Basic Django auth support, current user query, login and logout mutations\n* [x] Django sync and async views\n* [x] Unit test integration\n\n## Basic Usage\n\n```python\n# models.py\nfrom django.db import models\n\nclass Fruit(models.Model):\n    """A tasty treat"""\n    name = models.CharField(max_length=20)\n    color = models.ForeignKey(\'Color\', blank=True, null=True,\n            related_name=\'fruits\', on_delete=models.CASCADE)\n\nclass Color(models.Model):\n    name = models.CharField(\n        max_length=20,\n        help_text="field description",\n    )\n```\n\n```python\n# types.py\nimport strawberry\nfrom strawberry import auto\nfrom typing import List\nfrom . import models\n\n@strawberry.django.type(models.Fruit)\nclass Fruit:\n    id: auto\n    name: auto\n    color: \'Color\'\n\n@strawberry.django.type(models.Color)\nclass Color:\n    id: auto\n    name: auto\n    fruits: List[Fruit]\n```\n\n```python\n# schema.py\nimport strawberry\nfrom typing import List\nfrom .types import Fruit\n\n@strawberry.type\nclass Query:\n    fruits: List[Fruit] = strawberry.django.field()\n\nschema = strawberry.Schema(query=Query)\n```\n\nCode above generates following schema.\n\n```schema\n"""\nA tasty treat\n"""\ntype Fruit {\n  id: ID!\n  name: String!\n  color: Color\n}\n\ntype Color {\n  id: ID!\n  """\n  field description\n  """\n  name: String!\n  fruits: [Fruit!]\n}\n\ntype Query {\n  fruits: [Fruit!]!\n}\n```\n\n```python\n# urls.py\nfrom django.urls import include, path\nfrom strawberry.django.views import AsyncGraphQLView\nfrom .schema import schema\n\nurlpatterns = [\n    path(\'graphql\', AsyncGraphQLView.as_view(schema=schema)),\n]\n```\n',
    'author': 'Lauri Hintsala',
    'author_email': 'lauri.hintsala@verkkopaja.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/strawberry-graphql/strawberry-graphql-django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
