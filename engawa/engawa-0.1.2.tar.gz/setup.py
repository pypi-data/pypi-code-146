# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['engawa', 'engawa.misc']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'datasets>=2.8.0,<3.0.0',
 'nltk>=3.8,<4.0',
 'pytorch-lightning>=1.8.6,<2.0.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'sienna>=0.1.5,<0.2.0',
 'tokenizers>=0.13.2,<0.14.0',
 'transformers>=4.25.1,<5.0.0',
 'wandb>=0.13.7,<0.14.0']

entry_points = \
{'console_scripts': ['engawa = engawa.cli:main']}

setup_kwargs = {
    'name': 'engawa',
    'version': '0.1.2',
    'description': '',
    'long_description': '# engawa\n\n**NOT YET FULLY TESTED**\n\nA simple implementation to pre-train BART from scratch with your own corpus.\n\n\n# Usage\n\nSoon, I will make this pip-installable with CLI commands but at the moment, you need to run it as a repository.\n\n## Installation\n\n```bash\ngit clone git@github.com:sobamchan/engawa.git && cd engawa\npoetry install\n```\n\n## Build tokenizer\n\n```bash\npython engawa/tokenizer.py --data-path /path/to/train.txt --save-dir /path/to/save\n\n# Checkout other options by\npython engawa/tokenizer.py -h\n```\n\n## Pre-train BART\n\n```bash\npython engawa/train.py --tokenizer-file /path/to/tokenizer.json --train-file /path/to/train.txt --val-file /path/to/val.txt --default-root-dir /path/to/save/things\n\n# Checkout other options by\npython engawa/train.py -h\n```\n',
    'author': 'sobamchan',
    'author_email': 'oh.sore.sore.soutarou@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.8,<4.0.0',
}


setup(**setup_kwargs)
