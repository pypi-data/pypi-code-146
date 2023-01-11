# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['json_file_split', 'json_file_split.split_libs']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.10.4,<0.11.0',
 'fsai-shared-funcs>=0.0.35,<0.0.36',
 'loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['json-file-split = json_file_split.main:app']}

setup_kwargs = {
    'name': 'json-file-split',
    'version': '0.0.104',
    'description': 'Split a json or jsonl file into equal chunks.',
    'long_description': '# json-file-split\nSplit a json or jsonl file into different chunks.\n\n## Installation \n```shell\npip install json-file-split\n```\n\n## Usage\n```shell\njson-file-split \\\n--input_file_path ./tests/data/test.jsonl \\\n--save_to_dir /tmp/output/ \\\n--output_file_name test.jsonl \\\n--split_by number_of_buckets \\\n--batch_size 10\n```',
    'author': 'Michael Mohamed',
    'author_email': 'michael@foundationstack.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fsai-dev/fsai-cli-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
