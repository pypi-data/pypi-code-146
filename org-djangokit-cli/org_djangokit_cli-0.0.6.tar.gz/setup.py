# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djangokit',
 'djangokit.cli',
 'djangokit.cli.routes',
 'djangokit.cli.scaffolding',
 'djangokit.cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0',
 'org-djangokit-core>=0.0.3.dev0',
 'typer[all]>=0.7.0',
 'watchdog>=2.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1']}

entry_points = \
{'console_scripts': ['djangokit = djangokit.cli.__main__:app',
                     'dk = djangokit.cli.__main__:app']}

setup_kwargs = {
    'name': 'org-djangokit-cli',
    'version': '0.0.6',
    'description': 'DjangoKit command line interface',
    'long_description': "# DjangoKit CLI\n\n> NOTE: DjangoKit is a full stack Django+React framework. See\n> https://djangokit.org/ for more information.\n\nThis package provides the DjangoKit command line interface. When it's\ninstalled, it will install the `djangokit` console script.\n\nTo see a list of commands, run `djangokit` without any arguments (or use\nthe `dk` alias as shown here):\n\n    dk\n\nTo run a Django management command:\n\n    dk manage <args>\n\n## Configuring the CLI\n\nThe DjangoKit CLI can be configured via options passed to the\n`djangokit` base command or settings added to your project's settings\nfile(s) in the `[djangokit.cli]` section. Using a settings file is\nuseful when you want to change a default permanently.\n\n- `--env` / `env`: Specify the default environment to run commands in.\n\n- `--settings-module` / `django_settings_module`: Specify the Django\n  settings module.\n\n- `--additional-settings-module` / `django_additional_settings_module`:\n  Specify an *additional* Django settings module that will be loaded\n  after (and override) the base settings module.\n\n- `--settings-file` / `django_settings_file`: Path to settings file.\n  This will be derived from `ENV` if not specified.\n\n- `--typescript` / `use_typescript`: Since using TypeScript is the\n  default, you can use this to disable TypeScript. This will affect how\n  files are generated, for example (e.g. when using `dk add-page`).\n\n- `--quiet` / `quiet`: Squelch stdout.\n",
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
