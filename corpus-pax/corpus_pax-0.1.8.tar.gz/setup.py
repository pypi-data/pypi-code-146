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
    'version': '0.1.8',
    'description': 'Using Github API (to pull individuals, orgs, and article content), setup a local sqlite database, syncing images to Cloudflare.',
    'long_description': '# corpus-pax\n\nInitial, foundational sqlite tables with generic users, organizations, and articles.\n\n```mermaid\nflowchart TB\nsubgraph dev env\n  pax[corpus-pax]\n  pax--run setup--->db[(sqlite.db)]\nend\nsubgraph /corpus-entities\n  1(members)--github api---pax\n  2(orgs)--github api---pax\nend\nsubgraph /lawsql-articles\n  3(articles)--github api---pax\nend\npax--cloudflare api-->cf(cloudflare images)\n```\n\n## Prerequisites\n\nRepository | Description\n--:|:--\n[corpus-entities](https://github.com/justmars/corpus-entities) | yaml-formatted member and org files\n[lawsql-articles](https://github.com/justmars/lawsql-articles) | markdown-styled articles with frontmatter\n\nSince data concerning members will be pulled from such repositories, make sure the individual / org fields in [resources.py](corpus_pax/resources.py) match the data pulled from `corpus-entities`.\n\nEach avatar image should be named `avatar.jpeg` so that these can be uploaded to Cloudflare.\n\n## Install\n\n```zsh\npoetry add corpus-pax\npoetry update\n```\n\n## Supply .env\n\nCreate an .env file to create/populate the database. See [sample .env](.env.example) highlighting the following variables:\n\n1. Cloudflare `CF_ACCT`\n2. Cloudflare `CF_TOKEN`\n3. Github `GH_TOKEN`\n4. `DB_FILE` (sqlite)\n\nNote the [workflow](.github/workflows/main.yml) where the secrets are included for Github actions. Ensure these are set in the repository\'s `<url-to-repo>/settings/secrets/actions`, making the proper replacements when the tokens for Cloudflare and Github expire.\n\n### Notes\n\n#### Why Github\n\nThe names and profiles of individuals and organizations are stored in Github. These are pulled into the application via an API call requiring the use of a personal access token.\n\n#### Why Cloudflare Images\n\nIndividuals and organizations have images stored in Github. To persist and optimize images for the web, I use [Cloudflare Images](https://www.cloudflare.com/products/cloudflare-images/) to take advantage of modern image formats and customizable variants.\n\n#### Why sqlite\n\nThe initial data is simple. This database however will be the foundation for a more complicated schema. Sqlite seems a better fit for experimentation and future app use (Android and iOS rely on sqlite).\n\n## Steps\n\nNeed to specify filename, e.g. ex.db, for this to created in the root directory of the project folder.\n\nWithout the filename, the `Connection` (sqlite-utils\' Database() under the hood) used is the path declared in $env.DB_FILE\n\n```python\nfrom sqlpyd import Connection  # this is sqlite-utils\' Database() under the hood\nfrom corpus_pax import setup\n\nc = Connection(DatabasePath="ex.db", WALMode=False)\nsetup_pax_db("x.db")\n```\n\n## Gotcha\n\nThe m2m tables are not corrected when an update is made via `add_individuals_from_api()`, `add_organizations_from_api()` and `add_articles_from_api()`. To alleviate, simply reset the tables and recreate the same from scratch.\n',
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
