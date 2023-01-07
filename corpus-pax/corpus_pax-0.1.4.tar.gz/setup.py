# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corpus_pax']

package_data = \
{'': ['*'], 'corpus_pax': ['templates/*']}

install_requires = \
['email-validator>=1.3.0,<2.0.0',
 'httpx>=0.23.0,<0.24.0',
 'jinja2>=3.1.2,<4.0.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'sqlpyd>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'corpus-pax',
    'version': '0.1.4',
    'description': 'Using Github API (to pull individuals, orgs, and article content), setup a local sqlite database, syncing images to Cloudflare.',
    'long_description': '# corpus-pax\n\nSetting up the initial, foundational tables with generic users, organizations, and articles.\n\n```mermaid\nflowchart LR\n\nsubgraph main\n  local(local machine)--run corpus-pax--->db[(sqlite.db)]\n  local--avatar.jpeg---cf(cloudflare)\nend\nsubgraph github/corpus\n  folder1(members)--data via api---local\n  folder2(orgs)--data via api---local\nend\nsubgraph github/lawsql-articles\n  folder3(github/lawsql-articles/content)--data via api---local\nend\n\n```\n\nImplies _updated_ Github repositories:\n\n1. `corpus` (for entities, i.e. members and orgs) and\n2. `lawsql-articles` (markdown style articles).\n\nWith respect to entities, data concerning members will be pulled from such repository. Each avatar image should be named `avatar.jpeg` so that these can be uploaded to Cloudflare.\n\n## Install\n\n```zsh\npoetry add corpus-pax\npoetry update\n```\n\n## Supply .env\n\nCreate an .env file to create/populate the database. See [sample .env](.env.example) highlighting the following variables:\n\n1. Cloudflare `CF_ACCT`\n2. Cloudflare `CF_TOKEN`\n3. Github `GH_TOKEN`\n4. `DB_FILE` (sqlite)\n\nNote the [workflow](.github/workflows/main.yml) where the secrets are included for Github actions. Ensure these are set in the repository\'s `<url-to-repo>/settings/secrets/actions`, making the proper replacements when the tokens for Cloudflare and Github expire.\n\n### Notes\n\n#### Why Github\n\nThe names and profiles of individuals and organizations are stored in Github. These are pulled into the application via an API call requiring the use of a personal access token.\n\n#### Why Cloudflare Images\n\nIndividuals and organizations have images stored in Github. To persist and optimize images for the web, I use Cloudflare images.\n\n#### Why sqlite\n\nThe initial data is simple. This database however will be the foundation for a more complicated schema. Sqlite seems a better fit for experimentation and future embeddability of the same for app use.\n\n## Steps\n\n### Review database connection\n\nNeed to specify filename, e.g. ex.db, for this to created in the root directory of the project folder.\nWithout the filename, the `Connection` (sqlite-utils\' Database() under the hood) used is the path declared in $env.DB_FILE\n\n```python\nfrom sqlpyd import Connection  # this is sqlite-utils\' Database() under the hood\n\nc = Connection(DatabasePath="ex.db", WALMode=False)\n```\n\n### Add persons\n\nCreate and populate the _persons_-related tables:\n\n```python\nfrom corpus_pax import init_persons\n\ninit_persons(c)\n```\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lawdata.xyz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.0',
}


setup(**setup_kwargs)
