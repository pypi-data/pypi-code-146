# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['odapdbxbundle', 'odapdbxbundle.common']

package_data = \
{'': ['*']}

install_requires = \
['databricks_api', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'odapdbxbundle',
    'version': '0.0.4',
    'description': 'ODAP Databricks Bundle',
    'long_description': "# ODAP Databricks Bundle\n\n## Overview\n\nODAP Databricks Bundle is a bundle containing connectors to various data sources to make importing and exporting of data easier.\n\nODAP Databricks Bundle supports metadata driven ingestion and exports of tables and files\n\nIt's build on top of the Databricks platform.\n\n## Documentation\nTODO \n\n### DBR & Python\nDBR 10.4+ with python 3.8+ are supported\n\n### Dependency management\nUse `poetry` as main dependency management tool\n\n### Linting & Formatting\n- pylint\n- pyre-check\n- black\n\n### Code style\n- functions-only python (no dependency injection)\n- try to avoid classes as much as possible\n- data classes are OK\n- no `__init__.py` files\n- keep the `src` directory in root\n- project config is raw YAML\n- use type hinting as much as possible\n",
    'author': 'Tomas Bouma',
    'author_email': 'tomas.bouma@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
