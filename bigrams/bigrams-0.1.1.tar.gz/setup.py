# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bigrams']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.12.1,<0.13.0', 'more-itertools>=9.0.0,<10.0.0']

setup_kwargs = {
    'name': 'bigrams',
    'version': '0.1.1',
    'description': 'Simply create (N)grams',
    'long_description': '# (N)Grams\n![bigrams](bigrams.png)\n> Simply create (N)grams: N ~ Bi | Tri ...\n\n[![PyPI](https://img.shields.io/pypi/v/bigrams?style=flat-square)](https://pypi.python.org/pypi/bigrams/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bigrams?style=flat-square)](https://pypi.python.org/pypi/bigrams/)\n[![PyPI - License](https://img.shields.io/pypi/l/bigrams?style=flat-square)](https://pypi.python.org/pypi/bigrams/)\n[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)\n\n\nWelcome to bigrams, a Python project that provides a non-intrusive way to connect tokenized sentences in (N)grams.\nThis tool is designed to work with tokenized sentences, and it is focused on a single task: providing an efficient way\nto merge tokens from a list of tokenized sentences.\n\nIt\'s non-intrusive as it leaves tokenisation, stopwords removal and other text preprocessing out of its flow.\n\n---\n\n**Source Code**: [https://github.com/proteusiq/bigrams](https://github.com/proteusiq/bigrams)\n\n**PyPI**: [https://pypi.org/project/bigrams/](https://pypi.org/project/bigrams/)\n\n---\n\n\n## Installation\n\n```sh\npip install -U bigrams\n```\n\n## Usage\n\nTo use bigrams, import it into your Python script, and use `scikit-learn`-ish API to transform your tokens.\n\n```python\nfrom bigrams import Grams\n\n# expects tokenised sentences\nin_sentences = [["this", "is", "new", "york", "baby", "again!"],\n              ["new", "york", "and", "baby", "again!"],\n            ]\ng = Grams(window_size=2, threshold=2)\n\nout_sentences = g.fit_transform(in_stences)\nprint(out_sentences)\n# [["this", "is", "new_york", "baby_again!"],\n#   ["new_york", "and", "baby_again!"],\n#  ]\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n\n# Contributing are welcome\n\n# ToDo:\n - [ ] ~~create a save & load function~~\n - [ ] compare it with gensim Phrases\n - [ ] write replacer in Rust - [PyO3](https://github.com/PyO3/pyo3)\n',
    'author': 'Prayson W. Daniel',
    'author_email': 'praysonpi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://proteusiq.github.io/bigrams',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
