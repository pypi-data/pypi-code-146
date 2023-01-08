# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_singer_jsonl']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.17.3,<5.0.0', 'smart-open[s3]>=6.3.0,<7.0.0']

entry_points = \
{'console_scripts': ['target-singer-jsonl = target_singer_jsonl:main']}

setup_kwargs = {
    'name': 'target-singer-jsonl',
    'version': '0.0.3',
    'description': 'A Singer.io target for writing singer-formatted JSONL files to various destinations (e.g. local or s3).',
    'long_description': '# target-singer-jsonl\n\nThis is a [Singer](https://singer.io) target that reads JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md) and writes it to JSONL formatted files.\nFile writing is done via the `smart_open` python package, supporting local disk as well as many other destinations (e.g. S3).\n',
    'author': 'Ken Payne',
    'author_email': 'ken@meltano.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
