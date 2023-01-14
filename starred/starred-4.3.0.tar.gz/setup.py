# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starred']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'github3.py>=3.2.0,<4.0.0',
 'gql>=3.4.0,<4.0.0',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['starred = starred.starred:starred']}

setup_kwargs = {
    'name': 'starred',
    'version': '4.3.0',
    'description': 'creating your own Awesome List used GitHub stars!',
    'long_description': '# Starred\n\n[![ci](https://github.com/maguowei/starred/actions/workflows/ci.yml/badge.svg)](https://github.com/maguowei/starred/actions/workflows/ci.yml)\n[![Upload Python Package](https://github.com/maguowei/starred/actions/workflows/deploy.yml/badge.svg)](https://github.com/maguowei/starred/actions/workflows/deploy.yml)\n\n## Install\n\n```bash\n\n$ pip install starred\n$ starred --username maguowei --token=xxxxxxxx --sort > README.md\n```\n\n## Usage\n\n```bash\n$ starred --help\n\nUsage: starred [OPTIONS]\n\n  GitHub starred\n\n  creating your own Awesome List by GitHub stars!\n\n  example:     starred --username maguowei --token=xxxxxxxx --sort > README.md\n\nOptions:\n  --username TEXT        GitHub username  [required]\n  --token TEXT           GitHub token  [required]\n  --sort                 sort by category[language/topic] name alphabetically\n                         [default: False]\n\n  --topic                category by topic, default is category by language\n                         [default: False]\n\n  --topic_limit INTEGER  topic stargazer_count gt number, set bigger to reduce\n                         topics number  [default: 500]\n\n  --repository TEXT      repository name  [default: ]\n  --filename TEXT        file name  [default: README.md]\n  --message TEXT         commit message  [default: update stars]\n  --private              include private repos  [default: False]\n  --version              Show the version and exit.\n  --help                 Show this message and exit.\n```\n\n## Demo\n\n```bash\n# automatically create the repository\n$ export GITHUB_TOKEN=yourtoken\n$ starred --username yourname --repository awesome-stars --sort\n```\n\n- [`maguowei/awesome-stars`](https://github.com/maguowei/awesome-stars)\n- [update awesome-stars every day by GitHub Action](https://github.com/maguowei/awesome-stars/blob/master/.github/workflows/schedules.yml) the example with GitHub Action\n\n### Who uses starred?\n\n- by search: https://github.com/search?p=1&q=%22Generated+by+starred%22&type=Code\n- by topics:\n  - https://github.com/topics/starred\n  - https://github.com/topics/awesome-stars\n\n## Use [awesome-stars](https://github.com/maguowei/awesome-stars) as template\n\nThe simple way to create an awesome-stars repository is to use [maguowei/awesome-stars](https://github.com/maguowei/awesome-stars/generate) as template.\nIt will auto update your awesome-stars repository every day by GitHub Action.\n\n1. Click [Create a new repository from awesome-stars](https://github.com/maguowei/awesome-stars/generate)\n\n![use-awesome-stars-as-template](https://raw.githubusercontent.com/maguowei/starred/master/imgs/use-awesome-stars-as-template.png)\n\n2. [Setting the permissions of the GITHUB_TOKEN for your repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#setting-the-permissions-of-the-github_token-for-your-repository)\n\nset permissions to `Read and write permissions` and click `Save` button\n\n![workflow-permissions](https://raw.githubusercontent.com/maguowei/starred/master/imgs/workflow-permissions.png)\n\n3. Run the workflow first time\n\nclick `Run workflow` button\n\n![run-workflow](https://raw.githubusercontent.com/maguowei/starred/master/imgs/run-workflow.png)\n\n4. Customize the workflow schedule\n\n- [.github/workflows/schedules.yml#L5](https://github.com/maguowei/awesome-stars/blob/master/.github/workflows/schedules.yml#L5)\n\n![schedule](https://raw.githubusercontent.com/maguowei/starred/master/imgs/schedule.png)\n\n## FAQ\n\n1. Generate new token\n\n   link: [Github Personal access tokens](https://github.com/settings/tokens)\n\n2. Install the master branch version\n\n    ```bash\n    $ poetry build \n    $ pip install dist/starred-${x.x.x}.tar.gz\n    ```\n3. Dev & Run\n   ```bash\n   poetry run starred --help\n   ```',
    'author': 'maguowei',
    'author_email': 'imaguowei@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/maguowei/starred',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
