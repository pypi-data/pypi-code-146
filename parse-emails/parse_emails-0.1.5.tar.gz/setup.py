# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parse_emails', 'parse_emails.tests']

package_data = \
{'': ['*'], 'parse_emails.tests': ['test_data/*']}

install_requires = \
['RTFDE',
 'chardet',
 'compressed_rtf',
 'datetime',
 'olefile',
 'pip',
 'pyopenssl',
 'pytest',
 'python-magic']

setup_kwargs = {
    'name': 'parse-emails',
    'version': '0.1.5',
    'description': 'Parses an email message file and extracts the data from it.',
    'long_description': "[![Coverage Status](https://coveralls.io/repos/github/demisto/email-parser/badge.svg?branch=master)](https://coveralls.io/github/demisto/email-parser?branch=master)\n[![CLA assistant](https://cla-assistant.io/readme/badge/demisto/parse-emails)](https://cla-assistant.io/demisto/parse-emails)\n[![CircleCI](https://circleci.com/gh/demisto/parse-emails/tree/master.svg?style=svg)](https://circleci.com/gh/demisto/parse-emails/tree/master)\n# parse-emails\nParses an email message file and extracts the data from it.\n\nThe key features are:\n* Supports `.eml` and `.msg` files.\n* Extracts nested attachments.\n\n## Requirements\n\nPython 3.8.5+\n\n## Installation\n\n```console\n$ pip install parse-emails\n```\n\n## Usage\n\nThe main class `EmailParser` contains all what you need to parse an email:\n\n```python\nimport parse_emails\n\nemail = parse_emails.EmailParser(file_path=<file_path>, max_depth=3, parse_only_headers=False)\nemail.parse()\nprint(email.parsed_email['Subject'])\n```\n\n## Inputs\n\n| **Argument Name** | **Description** |\n| --- | --- |\n| file_path* | the file_path of a in msg or eml format |\n| parse_only_headers | Will parse only the headers and return headers table, Default is False|\n| max_depth | How many levels deep we should parse the attached emails \\(e.g. email contains an emails contains an email\\). Default depth level is 3. Minimum level is 1, if set to 1 the script will parse only the first level email |\n| file_info | the file info |\n\n## Contributing\nContributions are welcome and appreciated. To contribute you can submit a PR.\n\nBefore merging any PRs, we need all contributors to sign a contributor license agreement. By signing a contributor license agreement, we ensure that the community is free to use your contributions.\n\nWhen you open a new pull request, a bot will evaluate whether you have signed the CLA. If required, the bot will comment on the pull request, including a link to accept the agreement. The CLA document is also available for review as a [PDF](https://github.com/demisto/content/blob/master/docs/cla.pdf).\n\nIf the `license/cla` status check remains on *Pending*, even though all contributors have accepted the CLA, you can recheck the CLA status by visiting the following link (replace **[PRID]** with the ID of your PR): https://cla-assistant.io/check/demisto/email-parser?pullRequest=[PRID] .\n",
    'author': 'Demisto',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
