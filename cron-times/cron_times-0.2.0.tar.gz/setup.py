# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cron_times']

package_data = \
{'': ['*'], 'cron_times': ['static/*', 'templates/*']}

install_requires = \
['croniter>=1.3.8,<2.0.0',
 'flask>=2.2.2,<3.0.0',
 'markdown2>=2.4.6,<3.0.0',
 'pypugjs>=5.9.12,<6.0.0',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'cron-times',
    'version': '0.2.0',
    'description': 'Show schdueled jobs in a more readable way',
    'long_description': '# Timetable for cronjobs\n\nShow schdueled jobs in a more readable way.\n\n![screenshot](./screenshot.png)\n\n*features*\n\n* Easy configure - Setup job list in YAML format\n* Timezone supported - Able to configure server timezone and show the time in local time\n* Quick filtering - Allow customized label and quick lookup\n\n\n## Usage\n\n1. Install\n\n   ```bash\n   pip install git+https://github.com/tzing/cron-times.git\n   ```\n\n2. Create job definition files\n\n   Job definition are YAML files placed under `jobs/` folder in current working directory.\n\n   An example job:\n\n   ```yaml\n   - name: Job name\n     schedule: "0 10 * * *"\n     timezone: Asia/Taipei  # tzdata format; Would use UTC if not provided\n     description: In the description, you *can* use `markdown`\n     labels:\n       - sample-label\n       - another-label\n   ```\n\n   All `*.yaml` files would be loaded on initialization time.\n   We could build some code to pull the defines from other places before flask started.\n\n4. Run the app\n\n   ```bash\n   flask --app cron_times run\n   ```\n',
    'author': 'tzing',
    'author_email': 'tzingshih@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
