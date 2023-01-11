# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['log_config_watcher']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'log-config-watcher',
    'version': '0.1.3',
    'description': 'Watches your logging configuration file for change and applies them without requiring an application restart',
    'long_description': '# Log Config Watcher\n\nThis library makes it easy to load a JSON formatted Python Logging configuration file\nand monitor the file for changes. If the configuration has changed, and is valid, it will\nautomatically be applied and the changes will be reflect in your logging without restarting.\n\n## Getting Started\n\n```python\nfrom log_config_watcher import LogConfigWatcher\n\nlog_watcher = LogConfigWatcher("config.json")\nlog_Watcher.start()\n```\n\n## Options\n\nThe `LogConfigWatcher` class using the Python logging system to setup a `basicConfig` before\nattempting to load the config file. This way if there are any errors during the loading of the file\nthey will be reported somewhere. You can customize the defaults using the following settings passed\nto the constructor.\n\n* default_level: int - A Python logging logging level, such as, DEBUG, INFO, WARNIGN, or ERROR\n* default_format: str - A Python logging format string\n* default_handler: logging.Handler - A Python logging Handler type, such as, StreamHandler, FileHandler, etc, etc\n\n## Development\n\nThis project uses [Poetry](https://python-poetry.org/) as its project manager.\nThe goal of this library is to have no external runtime dependencies.\nHowever, for development, the following are used:\n\n* Black - For Formatting the code base\n* iSort - For sorting imports\n* autoflake - For removing unused imports and variables\n* poetry-bumpversion - For keeping the project and internal `__version__` value in sync\n\nIf you make a PR, you must run the `format.sh` script or your PR will be rejected.\n',
    'author': 'Robert DeRose',
    'author_email': 'rderose@checkpt.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RobertDeRose/log_config_watcher',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
