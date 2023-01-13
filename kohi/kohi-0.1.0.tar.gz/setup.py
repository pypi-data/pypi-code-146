# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kohi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kohi',
    'version': '0.1.0',
    'description': 'A powerfull schema validator',
    'long_description': '\n# kohi\n\n<p align="center">A powerfull schema validator</p>\n\n![GitHub Repo stars](https://img.shields.io/github/stars/natanfeitosa/kohi)\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/natanfeitosa/kohi/pytest.yml?label=Pytest&logo=github)\n![GitHub](https://img.shields.io/github/license/natanfeitosa/kohi)\n\n## Quickstart\n\nTo validate a type you can import your schema validator from `kohi` or `from kohi.<type> import <type>Schema`\n\ne.g.\n\nLet\'s check if a person\'s date of birth is a positive integer less than the current date — 2023 — and greater than or equal to 2005\n\n```python\nfrom kohi import NumberSchema\n# from kohi.number import NumberSchema\n\nn = NumberSchema().int().positive().lt(2023).gte(2005)\n\nprint(n.validate(2005)) # True\nprint(n.validate(2022)) # True\nprint(n.validate(2004)) # False\nprint(n.validate(2023)) # False\n\n# You can see the errors generated in the last `validate` call just by accessing the `errors` property\n# print(n.errors) # [\'number must be less than 2022\']\n```\n\n## Validators\n\n* [`kohi.base.BaseSchema`](#baseschema)\n> Only one base class for all schema validators\n* [`kohi.number.NumberSchema`](#numberschema)\n> or `kohi.NumberSchema`\n* [`kohi.string.StringSchema`](#stringschema)\n> or `kohi.StringSchema`\n\n## Methods\n\n### `BaseSchema`\n* `add_validator(name, func): Self`\n  > Add a custom data validator\n* `validate(data): bool`\n  > The method to be called when we validate the schema\n* `reset(): None`\n  > Reset error list\n* `throw(): Self`\n  > By default no errors are thrown, but when this method is chained a `ValidationError` will be thrown\n\n### `NumberSchema`\ninherits from [`BaseSchema`](#baseschema)\n> By default validates int and float \n\n* `float(): Self`\n  > Validate only `float`\n* `int(): Self`\n  > Validate only `int`\n* `lt(num): Self`\n  > Validates if the data is less than `num`\n* `gt(num): Self`\n  > Validates if the data is greater than `num`\n* `lte(num): Self`\n  > Validates if the data is less than or equal to `num`\n* `gte(num): Self`\n  > Validates if the data is greater than or equal to `num`\n* `min(num): Self`\n  > Just an alias for `gte(num)`\n* `max(num): Self`\n  > Just an alias for `lte(nun)`\n* `positive(): Self`\n  > Just an alias for `gt(0)`\n* `negative(): Self`\n  > Just an alias for `lt(0)`\n\n### StringSchema\ninherits from [`BaseSchema`](#baseschema)\n\n## Dev env\n\n* install development dependencies\n* check types using `mypy`\n* run all tests using `pytest`\n',
    'author': 'Natan Santos',
    'author_email': 'natansantosapps@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/natanfeitosa/kohi#readme',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
