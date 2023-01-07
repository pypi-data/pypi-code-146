# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parachute']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9',
 'json5>=0.9.5,<0.10.0',
 'pymavlink>=2.4.14,<3.0.0',
 'pyserial>=3.5,<4.0']

entry_points = \
{'console_scripts': ['parachute = parachute.cli:cli']}

setup_kwargs = {
    'name': 'parachute',
    'version': '0.4.2',
    'description': 'A lifeline for ArduPilot craft.',
    'long_description': 'Parachute\n=========\n\nParachute is a swiss army knife for ArduPilot settings. It helps you quickly and\neasily back up all your parameters to a file (and restore them). It also lets\nyou get/set them, filter them, diff them, restore them or convert them to\nparameter files compatible with Mission Planner/QGroundControl.\n\n\nInstallation\n------------\n\nInstalling Parachute is simple. You can use `pipx` (recommended):\n\n```bash\n$ pipx install parachute\n```\n\nOr `pip` (less recommended):\n\n```bash\n$ pip install parachute\n```\n\nYou can also download pre-built binaries for Windows and Linux from the\n[artifacts page](https://gitlab.com/stavros/parachute/-/pipelines).\n\n\nUsage\n-----\n\nParachute is called like so:\n\n```bash\n$ parachute backup <craft name>\n```\n\nFor example:\n\n```bash\n$ parachute backup Mini-Drak\n```\n\nTo restore:\n\n```bash\n$ parachute restore backup.chute\n```\n\n\nConversion\n----------\n\nYou can also convert a Parachute file to a file compatible with Mission Planner or QGroundControl:\n\n```bash\n$ parachute convert qgc Mini-Drak_2021-03-02_02-29.chute Mini-Drak.params\n```\n\n\nFiltering\n---------\n\nYou can filter parameters based on a regular expression:\n\n```bash\n$ parachute filter "serial[123]_" Mini-Drak_2021-03-02_02-29.chute filtered.chute\n```\n\nSince all parameter names are uppercase, the regex is case-insensitive, for convenience.\n\nYou can also filter when converting:\n\n```bash\n$ parachute convert --filter=yaw mp Mini-Drak_2021-03-02_02-29.chute -\n```\n\n\nComparing\n---------\n\nYou can compare parameters in a backup with parameters on the craft:\n\n```bash\n$ parachute compare backup.chute\n```\n\n\nGetting/setting\n---------------\n\nYou can get and set parameters:\n\n```bash\n$ parachute get BATT_AMP_OFFSET BATT_AMP_PERVLT\n```\n\n```bash\n$ parachute set BATT_AMP_OFFSET=-0.0135 BATT_AMP_PERVLT=63.8826\n```\n\nYou can get and set a single bit like so:\n\n```bash\n$ parachute get --binary FLIGHT_OPTIONS\n```\n\n```bash\n$ parachute set FLIGHT_OPTIONS:5=1\n```\n\n\nShell completions\n------------------\n\nParachute includes shell completion for AP parameters for various shells.  After you\'ve\nenabled completions, you can get parameter completion for the `get` and `set` commands.\nFor example, try typing `parachute get acr<TAB>`.\n\nThe way to enable it depends on your shell:\n\n\n### fish\n\nSave the completion script to ~/.config/fish/completions/parachute.fish:\n\n```bash\n_PARACHUTE_COMPLETE=fish_source parachute > ~/.config/fish/completions/parachute.fish\n```\n\n\n### bash\n\nSave the completion script somewhere.\n\n```bash\n_PARACHUTE_COMPLETE=bash_source parachute > ~/.parachute-complete.bash\n```\n\nSource the file in ~/.bashrc.\n\n```bash\n. ~/.parachute-complete.bash\n```\n\n\n### zsh\n\nSave the completion script somewhere.\n\n```bash\n_PARACHUTE_COMPLETE=zsh_source parachute > ~/.parachute-complete.zsh\n```\n\nSource the file in ~/.zshrc.\n\n```bash\n. ~/.parachute-complete.zsh\n```\n\n# Changelog\n\n\n## v0.4.2 (2023-01-07)\n\n### Features\n\n* Add the `force-accept-calibration` command. [Stavros Korokithakis]\n\n### Fixes\n\n* Fix parameter display order. [Stavros Korokithakis]\n\n\n## v0.4.1 (2022-11-05)\n\n### Features\n\n* Don\'t exit on missing parameters when restoring. [Stavros Korokithakis]\n\n### Fixes\n\n* Fix bug where negative numbers were erroneously not accepted. [Stavros Korokithakis]\n\n\n## v0.4.0 (2022-07-02)\n\n### Features\n\n* Add getting and setting bits directly. [Stavros Korokithakis]\n\n* Add the "--binary" parameter to display bit indexes. [Stavros Korokithakis]\n\n### Fixes\n\n* Remove unused code. [Stavros Korokithakis]\n\n\n## v0.3.11 (2022-02-26)\n\n### Features\n\n* Add "--compare" flag to "restore" [Stavros Korokithakis]\n\n### Fixes\n\n* Name files a bit better. [Stavros Korokithakis]\n\n\n## v0.3.10 (2021-12-17)\n\n### Fixes\n\n* Improve autodetection even more again. [Stavros Korokithakis]\n\n* Improve autodetection even more. [Stavros Korokithakis]\n\n* Improve autodetection default. [Stavros Korokithakis]\n\n\n## v0.3.9 (2021-11-02)\n\n### Fixes\n\n* Show the correct parameter name when diffing. [Stavros Korokithakis]\n\n\n## v0.3.8 (2021-10-29)\n\n### Features\n\n* Colorize tables. [Stavros Korokithakis]\n\n* Make table Markdown-compatible. [Stavros Korokithakis]\n\n### Fixes\n\n* Fix inverted `compare` display. [Stavros Korokithakis]\n\n\n## v0.3.7 (2021-10-23)\n\n### Features\n\n* Include parameter completions. [Stavros Korokithakis]\n\n* Add `--baud-rate` cli option` [Stavros Korokithakis]\n\n### Fixes\n\n* Display accurate names when diffing. [Stavros Korokithakis]\n\n* Fix port detection on Windows. [Stavros Korokithakis]\n\n\n## v0.3.6 (2021-08-29)\n\n### Features\n\n* Attempt socket autodetection. [Stavros Korokithakis]\n\n### Fixes\n\n* Make messages more consistent. [Stavros Korokithakis]\n\n\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/stavros/parachute',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
