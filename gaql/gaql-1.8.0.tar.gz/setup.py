# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaql',
 'gaql.client',
 'gaql.lib',
 'gaql.lib.click_decorators',
 'gaql.lib.google_clients',
 'gaql.lib.google_clients.completion',
 'gaql.tooling',
 'gaql.tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'google-ads==19.0.0',
 'prompt_toolkit>=3.0.22,<4.0.0',
 'pygments>=2.10.0,<3.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['gaql = gaql.client.commands:cli',
                     'gaql-tools = gaql.tools.commands:tools']}

setup_kwargs = {
    'name': 'gaql',
    'version': '1.8.0',
    'description': 'A command line interface to the Google Ads Query Language (GAQL). Run with `gaql` or `gaql-tools`',
    'long_description': "# GAQL CLI\n\n[![PyPI version](https://badge.fury.io/py/gaql.svg)](https://badge.fury.io/py/gaql)\n![PyPI downloads](https://img.shields.io/pypi/dm/gaql)\n\nA CLI for running [GoogleAds queries](https://developers.google.com/google-ads/api/docs/query/overview).\n\n## Usage\n### Installing\n\n- `pip install gaql`\n- `pipx install gaql` (recommended)\n\n### Querying\nThe default mode. Runs either as a REPL, or as a one off command\n\n```bash\n- gaql [ACCOUNT_ID] - run in REPL mode\n- gaql [ACCOUNT_ID] [WORDS*] - run a single query. Note depending on your shell you may need to quote some queries if you run like this.\n\nflags:\n--help show the help message; basically the below\n-f|--format <csv|json|jsonl|proto> specify an output format\n-o|--output <file> specify an output file. Based on the extension, format is inferred. Non REPL usage only\n```\n\nExamples, using 1-000-000-000 as our demo account id:\n```bash\n# opens a REPL with json lines as the output format\ngaql -f jsonl 1-000-000-000\n\n# runs the query against the given account, outputting to the terminal the results as json lines\ngaql -f jsonl 1-000-000-000 'SELECT campaign.id FROM campaign'\n\n# runs the query against the given account, outputting to 'campaigns.jsonl' the result as json lines\ngaql -o campaigns.jsonl 1-000-000-000 'SELECT campaign.id FROM campaign'\n```\n\n**tip**: by default `LIMIT 100` will be added to your queries. To override this behavior, simply define your own `LIMIT X`.\n\n**tip**: the autocomplete will return only valid fields for the selected entity if you fill out the `FROM <entity>` part\nfirst.\n\n### Other tools\nUsed for useful common queries. Currently only supports getting all accounts under an MCC, to help when managing multiple accounts. The MCC is taken from the `login_customer_id` field.\n- `gaql-tools queries clients`\n\n## Notes\n- credentials come from the environment > the google .yaml file > a user provided credential file\n- credentials, settings, and history are stored in `./config/gaql/*`. The credential file will only be present if you create it through a prompt (i.e you aren't using the ENV, or the YAML file Google specifies)\n\n## Ideas / TODO\n- tables as an output format\n- autocomplete for account ids (with caching)\n\n## Development\nWe're using [poetry](https://github.com/python-poetry/poetry) for local development, package management, and publishing. `pyenv` is\nrecommended for Python version management, and `pipx` for installation.\n\nBuild commands:\n\n```\nmake develop - install a development version. run via `poetry run gaql <args>`\nmake publish - build and distribute to PyPi\nmake clean   - remove the existing build files\nmake format  - run black over the code\nmake lint    - lint and format the code\n```\n\n## Security\nFor sensitive security matters please contact security@getyourguide.com.\n\n## Legal\ngaql-cli is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full text.\n",
    'author': 'Ben Ryves',
    'author_email': 'bryves@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/getyourguide/gaql-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
