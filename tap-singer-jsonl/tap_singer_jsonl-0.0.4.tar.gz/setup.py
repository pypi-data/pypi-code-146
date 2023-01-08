# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_singer_jsonl']

package_data = \
{'': ['*']}

install_requires = \
['singer-sdk>=0.16.0,<0.17.0', 'smart-open[s3]>=6.3.0,<7.0.0']

entry_points = \
{'console_scripts': ['tap-singer-jsonl = tap_singer_jsonl:main']}

setup_kwargs = {
    'name': 'tap-singer-jsonl',
    'version': '0.0.4',
    'description': 'A Singer.io tap fro reading raw singer-formatted JSONL files from local and remote sources (e.g. s3).',
    'long_description': '# tap-singer-jsonl\n\nThis is a [Singer](https://singer.io) tap that reads JSON-formatted data\nfollowing the [Singer\nspec](https://github.com/singer-io/getting-started/blob/master/SPEC.md) from JSONL files.\n',
    'author': 'Ken Payne',
    'author_email': 'ken@meltano.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
