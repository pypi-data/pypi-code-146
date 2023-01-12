# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dirgh']

package_data = \
{'': ['*'], 'dirgh': ['ci/*', 'ci/deployment/*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'trio>=0.20.0,<0.23.0']

entry_points = \
{'console_scripts': ['dirgh = dirgh.cli:run']}

setup_kwargs = {
    'name': 'dirgh',
    'version': '0.2.0',
    'description': 'With dirgh you can easily download a directory from GitHub programmatically from Python or using the CLI.',
    'long_description': "# dirgh\n\nWith `dirgh` you can easily download a directory from GitHub programmatically from Python or using the CLI.\n\n## CLI\n\n```shell\nusage: dirgh [-h] -r REPO [-o OWNER] [-d DIRECTORY] [-t TARGET] [--ref REF] [-R] [-O] [-a AUTH]\n\nDownload single directories from GitHub.\nGitHub rate limits are 60 requests/hour when unauthenticated and 5,000/hour\n when using a token. Each subfolder  requires extra requests.\n\nexamples:\ndirgh -r tiauth -o tiptenbrink -d deployment --ref cf51bff1a79b280388ba65f18998717b2fa5e1e3\ndirgh -r tiptenbrink/tiauth -d deployment -R -t 'C:\\Users\\dirgher'\\Cool projects/dürghé'\n(You can use both forward and backwardslashes, even interchangeably)\ndirgh -r tiptenbrink/tiauth -R -t './dürghé'\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -r REPO, --repo REPO  repository on GitHub using the format <owner>/<repository> or just <repository> if owner is also specified. If both are specified, owner is ignored.\n  -o OWNER, --owner OWNER\n                        repository owner on GitHub, can be an organization or user. Only necessary when not provided in the --repo option.\n  -d DIRECTORY, --directory DIRECTORY\n                        initial directory path in the format <subfolder1>/<subfolder2> etc. Defaults to root directory.\n  -t TARGET, --target TARGET\n                        output directory. If requesting a directory, this will overwrite the directory name. By default, the content will be placed in './dirgh/1673538759'.\n  --ref REF             commit reference, can be in any branch. (default: HEAD)\n  -R, --recursive       recursively enter all subfolders to get all files.\n  -O, --overwrite       Overwrite target directory.\n  -a AUTH, --auth AUTH  user authentication token, OAuth or personal access token. Not required but increases rate limits.\n```\n",
    'author': 'tiptenbrink',
    'author_email': '75669206+tiptenbrink@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
