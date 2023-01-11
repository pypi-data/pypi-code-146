# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guardian', 'guardian.probes']

package_data = \
{'': ['*'], 'guardian': ['config/*', 'templates/*']}

install_requires = \
['PyYAML>=6.0.0,<7.0.0', 'jinja2>=3.1.2,<4.0.0']

entry_points = \
{'console_scripts': ['guardian = guardian.main:run']}

setup_kwargs = {
    'name': 'guardian',
    'version': '0.2.2',
    'description': 'Monitor the status of a set of services.',
    'long_description': '# Guardian\n\n[![PyPi version](https://img.shields.io/pypi/v/guardian.svg?style=flat-square)](https://pypi.org/project/guardian)\n\nMonitor the status of a set of services. Characteristics:\n\n- definition of the services to monitor with a YAML file;\n- tests performed by custom scripts (Shell scripts, Python scripts, etc.);\n- no database and serverless;\n- generation of HTML status page;\n- email notifications;\n- IRC notifications.\n\n\n## Installation\n\n```bash\n$ pipx install guardian\n  installed package guardian 0.2.1, Python 3.9.2\n  These apps are now globally available\n    - guardian\ndone! ✨ 🌟 ✨\n```\n\nYou can now use Guardian from anywhere on your system.\n\n\n## Usage\n\n```bash\n$ guardian --help\nusage: guardian [-h] -c CONFIG_FILE [--email] [--irc] [--html]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG_FILE, --config CONFIG_FILE\n                        Configuration file (YAML).\n  --email               Send notification of failed test(s) via email.\n  --irc                 Send notification of failed test(s) via IRC.\n  --html                Generate a HTML status page.\n```\n\n\nIn order to use notification via IRC you need to install\n[irker](http://www.catb.org/~esr/irker/). irker is very easy to install and\nto run, no configuration is needed. Once executed, irker will wait for JSON\nformatted messages on the port 6659. irker will automatically join the channel\nyou have specified in the\n[Guardian configuration file](guardian/config/conf.cfg.sample#L2).\nirker will maintain connection state for multiple channels, avoiding obnoxious\njoin/leave spam.\n\nConfigurations related to the sending of emails are in the\n[same file](guardian/config/conf.cfg.sample#L5).\n\n\n## Examples\n\nThe goal of the INI configuration file is to set global variables (IRC channel, SMTP\nserver, etc.). If you do not create your own configuration file, the default one will\nbe used automatically.\n\nThe services to monitor must be described in one (or several) YAML file(s).\n\n\n```bash\n$ cp guardian/config/config.cfg.sample guardian/config/config.cfg\n$ cp guardian/config/services.yaml.example guardian/config/services.yaml\n\n\n$ guardian -c guardian/config/services.yaml\n+ Service Newspipe\n - Test about page\n     ✅\n+ Service MOSP\n - Test main page\n     ✅\n - Test search with API v2\n     ✅\n - Test API v1\n     ✅\n+ Freshermeat\n - Test main page\n     ✅\nExecution time: 0.47015 seconds.\n✨ 🌟 ✨ All 5 tests are successful.\n```\n\n\nWith email notification:\n\n```bash\n$ guardian -c guardian/config/google-services.yaml --email\n+ Google services\n - Test GMail\n     ✅\n - Test Web search\n     ❌\n - Test Google Drive\n     ✅\n1 error occurred.\nExecution time: 0:00:00.793011\nSending email notification...\n```\n\nYou can combine email notifications, IRC notifications and HTML reporting.\n\n\n## Contributing\n\nPatches and questions? Send to my [public\ninbox](https://lists.sr.ht/~cedric/public-inbox):\n[`~cedric/public-inbox@lists.sr.ht`](mailto:~cedric/public-inbox@lists.sr.ht).\nThanks!\n\n\n## License\n\n[Guardian](https://sr.ht/~cedric/guardian) is licensed under\n[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).\n\nCopyright (C) 2021-2023 [Cédric Bonhomme](https://www.cedricbonhomme.org)\n',
    'author': 'Cédric Bonhomme',
    'author_email': 'cedric@cedricbonhomme.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sr.ht/~cedric/guardian',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
