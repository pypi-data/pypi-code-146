# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['terramare', 'terramare.classes']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'typing-extensions>=3.7,<5']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.9']}

setup_kwargs = {
    'name': 'terramare',
    'version': '0.5.5',
    'description': 'Automatically construct complex objects from simple Python types.',
    'long_description': '![dragon](docs/_static/emoji.png)\n\n# terramare\n\n[![python: 3.6 | 3.7 | 3.8 | 3.9 | 3.10](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/)\n[![license: MIT](https://img.shields.io/badge/license-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)\n[![PyPI](https://img.shields.io/pypi/v/terramare)](https://pypi.org/project/terramare/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/terramare)](https://pypistats.org/packages/terramare)\n[![docs: pages](https://img.shields.io/badge/docs-pages-blue)](https://tomwatson1024.gitlab.io/terramare/)\n\n[![ci status](https://gitlab.com/tomwatson1024/terramare/badges/master/pipeline.svg)](https://gitlab.com/tomwatson1024/terramare/commits/master)\n[![coverage](https://gitlab.com/tomwatson1024/terramare/badges/master/coverage.svg)](https://gitlab.com/tomwatson1024/terramare/commits/master)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n\nAutomatically construct complex objects from simple Python types.\n\nHighlights:\n\n- **No boilerplate:** `terramare` uses Python\'s standard type hints to determine how to construct instances of a class;\n- **Format-agnostic:** `terramare` takes simple Python types as input - pass it the output from `json.load`, `toml.load`, or `yaml.load`;\n- **Non-invasive:** `terramare` requires no modifications to your existing classes and functions beyond standard type hints;\n\nFull documentation available at <https://tomwatson1024.gitlab.io/terramare/>.\n\n## Example\n\n### Deserializing a Simple Class\n\nConsider the following simple class, defined using [`attrs`](https://github.com/python-attrs/attrs) for brevity:\n\n```python\n>>> from typing import List\n>>> import attr\n>>> import terramare\n\n>>> @attr.s(auto_attribs=True)\n... class Example:\n...     words: List[str]\n...\n...     def __str__(self):\n...         return " ".join(self.words)\n\n```\n\nDeserializing an instance of the class from a dictionary is as simple as:\n\n```python\n>>> print(terramare.structure({"words": ["hello", "world!"]}, into=Example))\nhello world!\n\n```\n\n### Deserializing a More Complex Class\n\nConsider the `Person` class defined below:\n\n```python\n>>> from typing import NamedTuple, NewType, Sequence\n>>> import attr\n>>> import terramare\n\n    # `terramare` handles NamedTuples\n>>> class Location(NamedTuple):\n...     longitude: float\n...     latitude: float\n\n\n    # `terramare` handles NewType aliases\n>>> JobTitle = NewType("JobTitle", str)\n\n\n    # `terramare` handles custom classes [experimental]\n>>> @terramare.auto\n... class Occupation:\n...     def __init__(self, title: JobTitle, field: str):\n...         self.title = title\n...         self.field = field\n...\n...     def __eq__(self, other):\n...         if isinstance(other, self.__class__):\n...             return vars(self) == vars(other)\n...         return False\n...\n...     def __repr__(self):\n...         return "Occupation(\'{0.title}\', \'{0.field}\')".format(self)\n\n\n>>> @attr.s(auto_attribs=True)\n... class Person:\n...     name: str\n...     age: int\n...     friends: Sequence[str]\n...\n...     # `terramare` handles complex member variable types\n...     location: Location\n...     occupation: Occupation\n\n```\n\nAgain, deserialization is a single function call:\n\n```python\n>>> terramare.structure(\n...     {\n...         "name": "Alice",\n...         "age": 20,\n...         "friends": ["Bob", "Charlie"],\n...         "location": [51.5074, 0.1278],\n...         "occupation": {"title": "programmer", "field": "technology"}\n...     },\n...     into=Person,\n... )\nPerson(name=\'Alice\', age=20, friends=[\'Bob\', \'Charlie\'], location=Location(longitude=51.5074, latitude=0.1278), occupation=Occupation(\'programmer\', \'technology\'))\n\n```\n\n## Installation\n\nInstall using [pip](https://pip.pypa.io/en/stable/):\n\n```bash\npip install terramare\n```\n\n## Alternatives\n\nCheck out:\n\n- [`pydantic`](https://pydantic-docs.helpmanual.io/) - _"Data validation and settings management using python type annotations"_. A much more mature library also using Python\'s standard type hints for deserialization that requires a little more integration with your code;\n- [`schematics`](https://schematics.readthedocs.io/en/latest/) - _"...combine types into structures, validate them, and transform the shapes of your data based on simple descriptions"_. Uses custom types instead of Python\'s standard type hints;\n- [`cerberus`](https://docs.python-cerberus.org/en/stable/) - _"...provides powerful yet simple and lightweight data validation functionality out of the box and is designed to be easily extensible, allowing for custom validation"_. Schema validation that doesn\'t change the type of the primitive value.\n',
    'author': 'Tom W',
    'author_email': '796618-tomwatson1024@users.noreply.gitlab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tomwatson1024/terramare',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
