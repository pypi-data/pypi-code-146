# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deep_collections']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deep-collections',
    'version': '0.3.0',
    'description': 'Easy access to items in deep collections.',
    'long_description': '## DeepCollection\n\n[![PyPI version](https://badge.fury.io/py/deep-collection.svg)](https://pypi.org/project/deep-collection/)\n<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\ndeep_collection is a Python library that provides tooling for easy access to deep collections (dicts, lists, deques, etc), while maintaining a great portion of the collection\'s original API. The class DeepCollection class will automatically subclass the original collection that is provided, and add several quality of life extensions to make using deep collections much more enjoyable.\n\nGot a bundle of JSON from an API? A large Python object from some data science problem? Some very lengthy set of instructions from some infrastructure as code like Ansible or SaltStack? Explore and modify it with ease.\n\nDeepCollection can take virtually any kind of object including all built-in iterables, everything in the collections module, and [dotty-dicts](https://github.com/pawelzny/dotty_dict), and all of these nested in any fashion.\n\n### Features\n\n- Path traversal by supplying an list of path components as a key. This works for getting, setting, and deleting.\n- Setting paths when parent parts do not exist.\n- Path traversal through dict-like collections by dot chaining for getting\n- Finding all paths to keys or subpaths\n- Finding all values for keys or subpaths, and deduping them.\n- Provide all of the above through a class that is:\n    - easily instantiable\n    - a native subclass of the type it was instantiated with\n    - easily subclassable\n\n\n### Path concept\n\nDeepCollections has a concept of a "path" for nested collections, where a path is a sequence of keys or indices that if followed in order, traverse the deep collection. As a quick example, `{\'a\': [\'b\', {\'c\': \'d\'}]}` could be traversed with the path `[\'a\', 1, \'c\']` to find the value `\'d\'`.\n\nDeepCollections natively use paths as well as simple keys and indices. For `dc = DeepCollection(foo)`, items can be retrieved through the familiar `dc[path]` as normal if `path` is a simple key or index, or if it is an non-stringlike iterable path (strings are assumed to be literal keys). This is done with a custom `__getitem__` method. Similarly, `__delitem__` and `__setitem__` also support using a path. The same flexibility exists for the familiar methods like `.get`, which behaves the same as `dict.get`, but can accept a path as well as a key.\n\n### DeepCollection object API\n\nDeepCollections are instantiated as a normal class, optionally with a given initial collection as an arguement.\n\n```python\nfrom deep_collections import DeepCollection\n\ndc = DeepCollection()\n# or\ndc = DeepCollection({"a": {"b": {"c": "d"}}})\n# or\ndc = DeepCollection(["a", ["b", ["c", "d"]]])\n```\n\nThese are the noteworthy methods available on all DCs:\n\n- `__getitem__`\n- `__delitem__`\n- `__setitem__`\n- `get`\n- `paths_to_value`\n- `paths_to_key`\n- `values_for_key`\n- `deduped_values_for_key`\n\nThere are also corresponding functions availble that can use any native object that could be deep, but is not a `DeepCollection`, like a normal nested `dict` or `list`. This may be a convenient alternative to ad hoc traverse an object you already have, but it is also faster to use because it doesn\'t come with the initialization cost of a DeepCollection object. So if speed matters, use a function.\n\n### deep_collections function API\n\nAll of the useful methods for DeepCollection objects are available as functions that can take a collection as an argument, as well as several other supporting functions, which are made plainly availble.\n\nThe core functions are focused on using the same path concept. The available functions and their related DC methods are:\n\n- `getitem_by_path` - `DeepCollection().__getitem__`\n- `get_by_path` - `DeepCollection().get`\n- `set_by_path` - `DeepCollection().set_by_path`\n- `del_by_path` - `DeepCollection().del_by_path`\n- `paths_to_value` - `DeepCollection().paths_to_value`\n- `paths_to_key` - `DeepCollection().paths_to_key`\n- `values_for_key` - `DeepCollection().values_for_key`\n- `deduped_values_for_key` - `DeepCollection().deduped_values_for_key`\n- `dedupe_items`\n- `resolve_path`\n- `matched_keys`\n',
    'author': 'Joseph Nix',
    'author_email': 'nixjdm@terminallabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/terminal-labs/deep_collections',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
