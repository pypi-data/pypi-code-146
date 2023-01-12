# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autocontext',
 'iolanta',
 'iolanta.cli',
 'iolanta.facets',
 'iolanta.graph_providers',
 'iolanta.loaders',
 'iolanta.parsers',
 'ldflex',
 'mkdocs_iolanta',
 'mkdocs_iolanta.cli',
 'mkdocs_iolanta.cli.formatters',
 'mkdocs_iolanta.facets',
 'mkdocs_iolanta.octiron',
 'mkdocs_iolanta_tables',
 'mkdocs_iolanta_tables.facets',
 'octadocs_adr',
 'octadocs_adr.facets',
 'octadocs_github',
 'octadocs_github.facets',
 'octadocs_ibis',
 'octadocs_ibis.facets',
 'octadocs_prov',
 'octadocs_prov.facets',
 'octadocs_telegram',
 'octadocs_telegram.facets']

package_data = \
{'': ['*'],
 'iolanta.facets': ['sparql/*'],
 'mkdocs_iolanta': ['data/foaf/*',
                    'data/iolanta/*',
                    'data/octa/*',
                    'data/owl/*',
                    'data/rdf/*',
                    'data/rdfs/*',
                    'data/skos/*',
                    'yaml/*'],
 'mkdocs_iolanta.facets': ['sparql/*'],
 'mkdocs_iolanta_tables': ['templates/octadocs-table/*', 'yaml/*'],
 'mkdocs_iolanta_tables.facets': ['sparql/*'],
 'octadocs_adr': ['templates/octadocs-decisions/*', 'yaml/*'],
 'octadocs_adr.facets': ['sparql/*'],
 'octadocs_github': ['data/*'],
 'octadocs_ibis': ['data/*', 'templates/octadocs-ibis/*'],
 'octadocs_prov': ['data/*'],
 'octadocs_telegram': ['data/*']}

install_requires = \
['PyGithub>=1.55,<2.0',
 'PyLD>=2.0.3,<3.0.0',
 'backoff>=1.11.1,<2.0.0',
 'backports.cached-property>=1.0.0,<2.0.0',
 'boltons>=21.0.0,<22.0.0',
 'classes>=0.4.0,<0.5.0',
 'deepmerge>=0.1.1,<0.2.0',
 'documented>=0.1.1,<0.2.0',
 'dominate>=2.6.0,<3.0.0',
 'funcy>=1.17,<2.0',
 'mkdocs-macros-plugin>=0.7.0,<0.8.0',
 'mkdocs>=1.3.0,<2.0.0',
 'more-itertools>=9.0.0,<10.0.0',
 'owlrl>=6.0.2,<7.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pydotplus>=2.0.2,<3.0.0',
 'python-frontmatter>=0.5.0,<0.6.0',
 'rdflib>=6.2.0,<7.0.0',
 'requests>=2.25.1,<3.0.0',
 'singledispatchmethod>=1.0,<2.0',
 'typer>=0.7.0,<0.8.0',
 'urlpath>=1.1.7,<2.0.0']

entry_points = \
{'console_scripts': ['iolanta = iolanta.cli:app'],
 'iolanta.graph': ['mkdocs_iolanta = '
                   'mkdocs_iolanta:MkDocsIolantaGraphProvider'],
 'mkdocs.plugins': ['mkdocs-iolanta-tables = '
                    'mkdocs_iolanta_tables.plugin:TablesPlugin',
                    'octadocs-github = octadocs_github.plugin:GithubPlugin',
                    'octadocs-ibis = octadocs_ibis.plugin:IbisPlugin',
                    'octadocs-prov = octadocs_prov.plugin:ProvenancePlugin',
                    'octadocs-telegram = '
                    'octadocs_telegram.plugin:TelegramPlugin',
                    'octadocs_adr = octadocs_adr.plugin:ADRPlugin']}

setup_kwargs = {
    'name': 'mkdocs-iolanta-tables',
    'version': '1.1.14',
    'description': 'Structured tables for MkDocs',
    'long_description': '# octadocs\n\n[![Build Status](https://travis-ci.com/anatoly-scherbakov/octadocs.svg?branch=master)](https://travis-ci.com/anatoly-scherbakov/octadocs)\n[![Coverage](https://coveralls.io/repos/github/anatoly-scherbakov/octadocs/badge.svg?branch=master)](https://coveralls.io/github/anatoly-scherbakov/octadocs?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/octadocs.svg)](https://pypi.org/project/octadocs/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install octadocs\n```\n\n## License\n\n[MIT](https://github.com/anatoly-scherbakov/octadocs/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [868260c2d659e455bafc2ed4fe242413ef39e4dc](https://github.com/wemake-services/wemake-python-package/tree/868260c2d659e455bafc2ed4fe242413ef39e4dc). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/868260c2d659e455bafc2ed4fe242413ef39e4dc...master) since then.\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iolanta-tech/mkdocs-iolanta-tables',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
