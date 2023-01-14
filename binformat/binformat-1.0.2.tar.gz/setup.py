# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['binformat']
setup_kwargs = {
    'name': 'binformat',
    'version': '1.0.2',
    'description': 'Implementation of the Permuatio wire format',
    'long_description': '# Binfmt is a binary exchange format\n\n[Permuatio](https://codeberg.org/Patpine/Permutatio) uses a binary format called binformat.\nThis is a python implementation of said format.\n\n## Usage\n\nThe module exports main 2 methods `write_msg` and `read_msg`, as well as their safe (non-exception throwing) counterparts `safe_write_msg` and `safe_read_msg`.\n\nDocumentation:\n\n### `write_msg`\n\nTakes 2 argumentss\n\n- `file`: a BufferedWriter that can have binary values write to\n- `obj`: one of the types that binformat can represent, that will be writen\n\n### `safe_write_msg`\n\nTakes 2 argument:\n\n- `filename`: a filename that the file should be written to, should there not be issues with writing the value\n- `obj`: as in above\n\nIt also returns 1 value: Either `None` or `str` which is an error string\n\n### `read_msg`\n\nTakes 1 argument:\n\n- `file`: a BufferedReader that can have binary values read from\n\nIt also returns 1 value: an object that has been read from the file.\n\n### `safe_read_msg`\n\nTakes 1 argument:\n\n- `filename`: a filename that the file should be read from\n\nIt also returns 1 value: an object that has been read from the file or an error.\n\n## Example\n\n```python\nimport binformat\n\nsafe_write_msg("hexxy", {\n    1: b"Hello world",\n    2: [1, 2, 3]\n})\n\nwith open("hexxy", "rb") as f:\n    print(read_msg(f))\n    # { 1: b"Hello world", 2: [1, 2, 3] }\n```\n\n## Testing\n\nRun `tests.py`\n',
    'author': 'Arcade Wise',
    'author_email': 'l3gacy.b3ta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/Patpine/binformat-py',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
