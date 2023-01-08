# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['invitation']

package_data = \
{'': ['*'], 'invitation': ['templates/*']}

install_requires = \
['Jinja2==3.1.2', 'MarkupSafe==2.1.1', 'PyYAML==6.0', 'phonenumbers==8.13.3']

entry_points = \
{'console_scripts': ['uk-invitation-letter = invitation.builder:main']}

setup_kwargs = {
    'name': 'uk-invitation-letter',
    'version': '0.2.1',
    'description': 'UK visa invitation letter generator.',
    'long_description': 'UK visa invitation letter generator. ![PyPI](https://img.shields.io/pypi/v/uk-invitation-letter?style=flat-square)\n===\n\nAuto-generates UK tourist visa invitation letter.\n\n\n---\n\n### Requirements\n\n* Python 3 with pip\n* LaTeX\n\n### Usage\n\n1. Install the package:\n\n```bash\npip3 install uk-invitation-letter\n```\n\n2. Create `data.yml` config file\n\nExample:\n\n```yaml\ninviter: !entity\n  name: Kayleigh H Welch\n  address: !address\n    lines:\n      - 75 Hertingfordbury Road\n      - NEWTON NG13 8QY\n      # UK auto-added\n  phone: "07758888305"\n  email: slwzgtew2wj@temporary-mail.net\n\nemployer: !entity\n  name: Jstory UK Ltd\n  address: !address\n    lines:\n      - 89 Well Lane\n      - PATTERDALE CA11 0LQ\n\nembassy: !entity\n  name: British Embassy Moscow\n  address: !address\n    lines:\n      - Smolenskaya Naberezhnaya 10\n      - Moscow 121099\n      - Russian Federation\n\ninvitee: !entity\n  name: # <first name> [<other names>]+ <last name>\n    - Joseph Brodsky\n    - Maria Sozzani\n  pronoun: null # they/them/their by default\n  relationship: friends\n\ntrip: !trip\n  arrival_date: 2020-01-01\n  departure_date: 2020-01-31\n  reason: a short trip\n  return_reason: null\n  return_country: Russia\n  financial_support: false\n```\n\n3. Run the generator\n\n```bash\nLATEX_BINARY=<path to latex binary> uk-invitation-letter\n```\n\nThe output will be saved to `build/invitation.pdf`.\n',
    'author': 'Timur Iskhakov',
    'author_email': 'me@timur.is',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iskhakovt/uk-invitation-letter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
