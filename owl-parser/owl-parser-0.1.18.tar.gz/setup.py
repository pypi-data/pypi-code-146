# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owl_parser',
 'owl_parser.bp',
 'owl_parser.dmo',
 'owl_parser.dmo.core',
 'owl_parser.dmo.exact',
 'owl_parser.dmo.spans',
 'owl_parser.dto',
 'owl_parser.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'owl-finder', 'rdflib>=6.2.0,<7.0.0', 'regression-framework']

setup_kwargs = {
    'name': 'owl-parser',
    'version': '0.1.18',
    'description': 'Parse Input Text using One-or-More Ontology (OWL) files',
    'long_description': '# Ontology Parser (owl-parser)\nUse an Ontology model to parse unstructured text\n\n## Under the hood\nThis is the root level method.\n\nThe input parameters and return values have well-described data types.\n```python\ndef owl_parser(tokens: list,\n               ontology_name: str,\n               absolute_path: str) -> list:\n\n    Enforcer.is_list_of_dicts(tokens)\n    Enforcer.is_str(ontology_name)\n    FileIO.exists_or_error(absolute_path)\n\n    from owl_finder.multiquery.bp import FindOntologyData\n    from owl_parser.bp import MutatoAPI\n\n    finder = FindOntologyData(ontologies=[ontology_name],\n                              absolute_path=absolute_path)\n\n    results = MutatoAPI(finder).swap(tokens)\n    Enforcer.is_list_of_dicts(results)\n\n    return results\n```\n\n## Import\n```python\nfrom owl_parser import owl_parser\n```\n\n## Usage\n```python\nresults = owl_parser(\n    tokens,\n    ontology_name="<ontology-name>",\n    absolute_path="<absolute-path>")\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/owl-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
