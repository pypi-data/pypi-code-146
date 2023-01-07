# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskiq',
 'taskiq.abc',
 'taskiq.brokers',
 'taskiq.cli',
 'taskiq.cli.scheduler',
 'taskiq.cli.worker',
 'taskiq.formatters',
 'taskiq.middlewares',
 'taskiq.result_backends',
 'taskiq.schedule_sources',
 'taskiq.scheduler']

package_data = \
{'': ['*']}

install_requires = \
['gitignore-parser>=0.1.0,<0.2.0',
 'importlib-metadata<4.3',
 'pycron>=3.0.0,<4.0.0',
 'pydantic>=1.6.2,<2.0.0',
 'taskiq_dependencies>=1.0.0,<1.1.0',
 'typing-extensions>=3.10.0.0',
 'watchdog>=2.1.9,<3.0.0']

extras_require = \
{'uv': ['uvloop>=0.16.0,<1'], 'zmq': ['pyzmq>=23.2.0,<24.0.0']}

entry_points = \
{'console_scripts': ['taskiq = taskiq.__main__:main'],
 'taskiq_cli': ['scheduler = taskiq.cli.scheduler.cmd:SchedulerCMD',
                'worker = taskiq.cli.worker.cmd:WorkerCMD']}

setup_kwargs = {
    'name': 'taskiq',
    'version': '0.1.6',
    'description': 'Distributed task queue with full async support',
    'long_description': '[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/taskiq?style=for-the-badge)](https://pypi.org/project/taskiq/)\n[![PyPI](https://img.shields.io/pypi/v/taskiq?style=for-the-badge)](https://pypi.org/project/taskiq/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/taskiq?style=for-the-badge)](https://pypistats.org/packages/taskiq)\n\n<div align="center">\n<a href="https://taskiq-python.github.io/"><img src="https://raw.githubusercontent.com/taskiq-python/taskiq/master/imgs/logo.svg" width=600></a>\n<hr/>\n</div>\n\nTaskiq is an asynchronous distributed task queue for python.\nThis project takes inspiration from big projects such as [Celery](https://docs.celeryq.dev) and [Dramatiq](https://dramatiq.io/).\nBut taskiq can send and run both the sync and async functions.\nAlso, we use [PEP-612](https://peps.python.org/pep-0612/) to provide the best autosuggestions possible. But since it\'s a new PEP, I encourage you to use taskiq with VS code because Pylance understands all types correctly.\n\n# Installation\n\nThis project can be installed using pip:\n```bash\npip install taskiq\n```\n\nOr it can be installed directly from git:\n\n```bash\npip install git+https://github.com/taskiq-python/taskiq\n```\n\nYou can read more about how to use it in our docs: https://taskiq-python.github.io/.\n\n\n# Local development\n\n\n## Linting\n\nWe use pre-commit to do linting locally.\n\nAfter cloning this project, please install [pre-commit](https://pre-commit.com/#install). It helps fix files before committing changes.\n\n```bash\npre-commit install\n```\n\n\n## Testing\n\nPytest can run without any additional actions or options.\n\n```bash\npytest\n```\n\n## Docs\n\nTo run docs locally, you need to install [yarn](https://yarnpkg.com/getting-started/install).\n\nFirst, you need to install dependencies.\n```\nyarn install\n```\n\nAfter that you can set up a docs server by running:\n\n```\nyarn docs:dev\n```\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': 'Pavel Kirilin',
    'maintainer_email': 'win10@list.ru',
    'url': 'https://taskiq-python.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
